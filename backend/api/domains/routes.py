from api.db import db
from api.db.schema import Domain, Link
from api.domains.models import (
    AggregatedDomainResponse,
    DomainDumpResponse,
    DomainResponse,
    InsertRequest,
)
from api.utility.dependencies import pagination
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
    domains: str = Query(
        ...,
        min_length=4,
        max_length=40,
        title="Domain Hash Prefix",
        description="Prefix for domain hashes that should be retrieved",
    ),
    pagination: dict = Depends(pagination),
):
    # Assemble List of domains
    return {
        "domains": [
            {
                "fqdn": domain[1],
                "score": domain.score(),
                "last_updated": domain[0],
            }
            for domain in await db.select([Domain.last_updated, Domain.fqdn])
            .where(Domain.fqdn_hash.startswith(domains))
            .limit(pagination["per_page"])
            .offset(pagination["offset"])
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
    try:
        parent = (
            await db.select([Domain.id])
            .where(Domain.fqdn == data["domain"])
            .gino.first()
        ).id
    except Exception:
        parent = (
            await Domain.create(
                fqdn=data["domain"],
                fqdn_hash=Domain.hash_name(data["domain"].encode()),
                last_updated=floor(time()),
            )
        ).id

    for link in domain.links:
        try:
            id = (await db.select([Domain.id]).where(Domain.fqdn == link).gino.first())[
                0
            ]
        except Exception as e:
            id = (
                await Domain.create(
                    fqdn=link,
                    fqdn_hash=Domain.hash_name(link.encode()),
                    last_updated=floor(time()),
                )
            ).id

        if not await db.scalar(
            db.exists().where(Link.parent_id == parent and Link.child_id == id).select()
        ):
            await Link.create(network=data["network"], parent_id=parent, child_id=id)

    return Response(status_code=202)


@domain_router.get(
    "/list/",
    summary="List Domains in DB",
    description="List all (domain, hash) triplets from the database sorted by id",
    response_model=DomainDumpResponse,
)
async def db_dump(pagination: dict = Depends(pagination)):
    return {
        "domains": [
            {"fqdn": domain[0], "hash": domain[1]}
            for domain in await db.select([Domain.fqdn, Domain.fqdn_hash])
            .limit(pagination["per_page"])
            .offset(pagination["offset"])
            .gino.all()
        ]
    }
