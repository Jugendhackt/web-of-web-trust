from api.db import db
from api.db.schema import (
    count_ruegen_query,
    Domain,
    get_domain_id_query,
    link_exists_query,
    Link,
    paginated_domain_dump_query,
    paginated_domain_fetch_query,
)
from api.domains.models import (
    AggregatedDomainResponse,
    DomainDumpResponse,
    DomainHash,
    DomainResponse,
    InsertRequest,
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
    fqdn_hash: str = DomainHash,
    pagination: PaginationParameter = Depends(pagination),
):
    # Assemble List of domains
    return {
        "domains": [
            DomainResponse(
                fqdn=domain[1],
                score=await Domain.score(domain[2]),
                last_updated=domain[0],
                ruegen_amount=await count_ruegen_query.scalar(id=domain[2]),
            )
            for domain in await paginated_domain_fetch_query.all(
                offset=pagination.offset,
                per_page=pagination.per_page,
                fqdn_hash=fqdn_hash,
            )
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
    parent = await get_domain_id_query.first(fqdn=data["domain"])

    if parent is None:
        parent = await Domain.create(
            fqdn=data["domain"],
            fqdn_hash=Domain.hash_name(data["domain"]),
            last_updated=floor(time()),
        )
        parent_id = parent.id
    else:
        parent_id = parent[0]

    for link in domain.links:
        link_entry = await get_domain_id_query.first(fqdn=link)

        if link_entry is None:
            link_entry = await Domain.create(
                fqdn=link,
                fqdn_hash=Domain.hash_name(link),
                last_updated=floor(time()),
            )
            link_id = link_entry.id
        else:
            link_id = link_entry[0]

        if not await link_exists_query.scalar(parent=parent_id, child=link_id):
            await Link.create(
                network=data["network"], parent_id=parent_id, child_id=link_id
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
            for domain in await paginated_domain_dump_query.all(
                per_page=pagination.per_page, offset=pagination.offset
            )
        ]
    }
