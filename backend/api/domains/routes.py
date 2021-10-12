from api.db import db
from api.db.schema import Domain, Link
from api.domains.models import (
    AggregatedDomainResponse,
    DomainDumpResponse,
    DomainResponse,
    InsertRequest,
    DomainHash,
)
from api.utility.dependencies import pagination, PaginationParameter
from fastapi import Query, HTTPException, Response, APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from math import floor
from time import time
from typing import Optional, List


domain_router = APIRouter(prefix="/domain", tags=["Domains"])


@domain_router.get(
    "/fetch/",
    summary="Interface for clients",
    description="Route for requesting domains with scores by a hash prefix",
    response_model=AggregatedDomainResponse,
    status_code=200,
)
async def fetch_domains(
    domains: str = DomainHash,
    pagination: PaginationParameter = Depends(pagination),
):
    # Assemble List of domains
    return {
        "domains": [
            DomainResponse(
                fqdn=domain[1],
                score=await Domain.score(domain[2]),
                last_updated=domain[0],
                ruegen_amount=await Domain.count_ruegen(domain[2]),
            )
            for domain in await db.select([Domain.last_updated, Domain.fqdn, Domain.id])
            .where(Domain.fqdn_hash.startswith(domains))
            .limit(pagination.per_page)
            .offset(pagination.offset)
            .gino.all()
        ]
    }


@domain_router.post(
    "/update/",
    description="Interface for updating the graph database by scrapers. All linked new domains will automatically be inserted into the database",
    status_code=202,
    response_description="Empty when successfully otherwise see `Validation Error`",
    name="Interface for Scraper",
)
async def insert_domain(domain: InsertRequest):
    data = jsonable_encoder(domain)
    parent = (
        await db.select([Domain.id]).where(Domain.fqdn == data["domain"]).gino.first()
    )

    if parent is None:
        parent = await Domain.create(
            fqdn=data["domain"],
            fqdn_hash=Domain.hash_name(data["domain"]),
            last_updated=floor(time()),
        )

    for link in domain.links:
        link_entry = (
            await db.select([Domain.id]).where(Domain.fqdn == link).gino.first()
        )

        if link_entry is None:
            link_entry = await Domain.create(
                fqdn=link,
                fqdn_hash=Domain.hash_name(link),
                last_updated=floor(time()),
            )
            link_id = link_entry.id
        else:
            link_id = link_entry[0]

        if not await db.scalar(
            db.exists()
            .where(Link.parent_id == parent.id and Link.child_id == link_id)
            .select()
        ):
            await Link.create(
                network=data["network"], parent_id=parent.id, child_id=link_id
            )

    return Response(status_code=202)


@domain_router.get(
    "/list/",
    summary="List Domains in DB",
    description="List all (domain, hash) duplets from the database sorted by id",
    response_model=DomainDumpResponse,
)
async def db_dump(pagination: PaginationParameter = Depends(pagination)):
    return {
        "domains": [
            {"fqdn": domain[0], "hash": domain[1]}
            for domain in await db.select([Domain.fqdn, Domain.fqdn_hash])
            .limit(pagination.per_page)
            .offset(pagination.offset)
            .gino.all()
        ]
    }
