from typing import Optional, Any, Dict, List, Union
from math import floor
from time import time
from gino import Gino
from .models import InsertRequest, DomainReponse, AggregatedDomainResponse
from .db.init import db
from .db import Domain, Link
from fastapi import FastAPI, Query, HTTPException, Response, Body
from fastapi.encoders import jsonable_encoder

api = FastAPI()
db.init_app(api)


@api.get(
    "/spec",
    response_description="OpenAPI 3.0 Spec as JSON",
    response_model=Dict[str, Any],
)
async def openapi_spec() -> Dict[str, Any]:
    return api.openapi()


@api.post(
    "/domain/", response_model=AggregatedDomainResponse, include_in_schema=DomainReponse
)
async def fetch_domains(
    domains: str = Query(
        "",
        min_length=5,
        max_length=40,
        title="Domain Hash Prefix",
        description="Prefix for doman hashes that should be retrieved",
    ),
    page: Optional[int] = Query(
        1,
        alias="p",
        title="Page for pagination",
        description="When over a hundred domans are found for a request you need to specify a page to get more results.",
    ),
):
    if domains == "":
        return HTTPException(status_code=400, detail="Missing domain parameter")

    # Not efficient but okay
    return {
        "domains": [
            {
                "fqdn": domain.fqdn,
                "score": (1, 1),  # domain.score(),
                "last_updated": domain.last_updated,
            }
            for domain in await Domain.select('id', 'fqdn', 'last_updated')
            .where(Domain.fqdn.startswith(domains))
            #.limit(100)
            #.offset(page * 100)
            #.all()
            .gino
            .all()
        ]
    }


@api.get("/test/")
async def test():

    return {"domains": []}


@api.post(
    "/update",
    description="Interface for updating the graph database by scrapers. All linked new domains will automatically be inserted into the database",
    status_code=201,
    response_description="Empty Respose if not errors have arisen.",
    name="Scraper Interface",
)
async def insert_domain(domain: InsertRequest):
    data = jsonable_encoder(domain)
    try:
        parent = (
            await db.select([Domain.id])
            .where(Domain.fqdn == data["domain"])
            .limit(1)
            .gino.all()
        )[0][0]
    except Exception as e:
        parent = (
            await Domain.create(
                fqdn=data["domain"],
                fqdn_hash=Domain.hash_name(data["domain"].encode()).__str__(),
                last_updated=floor(time()),
            )
        ).id

    for link in domain.links:
        try:
            id = (
                await db.select([Domain.id])
                .where(Domain.fqdn == link)
                .limit(1)
                .gino.all()
            )[0][0]
        except Exception as e:
            id = (
                await Domain.create(
                    fqdn=link,
                    fqdn_hash=Domain.hash_name(link.encode()).__str__(),
                    last_updated=floor(time()),
                )
            ).id

        if not await db.scalar(
            db.exists().where(Link.parent_id == parent and Link.child_id == id).select()
        ):
            await Link.create(network=data["network"], parent_id=parent, child_id=id)

    return Response(status_code=201)
