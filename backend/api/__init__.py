from typing import Optional, Any, Dict, List, Union
from math import floor
from time import time
from gino import Gino
from .models import (
    InsertRequest,
    DomainReponse,
    AggregatedDomainResponse,
    RuegenUpdateRequest,
)
from .db import db
from .db.schema import Domain, Link, Ruege
from fastapi import FastAPI, Query, HTTPException, Response, Body
from fastapi.encoders import jsonable_encoder

api = FastAPI()
db.init_app(api)


@api.get(
    "/spec/",
    response_description="OpenAPI 3.0 Spec as JSON. Use a viewer like https://editor.swagger.io/ for easier inspection",
    response_model=Dict[str, Any],
)
async def openapi_spec() -> Dict[str, Any]:
    return api.openapi()


@api.post(
    "/ruege/update/",
    status_code=201,
    summary="Interface for ruegen scraper",
    description="Interface used by ruegen scraper on instance startup to feed updates and/ or new ruegen to the database",
)
async def update_ruege(ruege: RuegenUpdateRequest):
    data = jsonable_encoder(ruege)

    try:
        db_ruege = await Ruege.query.where(
            Ruege.identifier == data["aktenzeichen"]
        ).gino.first()
        domain_id = db_ruege.domain
    except:
        try:
            domain_id = (
                await db.select([Domain.id])
                .where(Domain.fqdn == data["medium"])
                .gino.first()
            )[0]
        except:
            domain_id = (
                await Domain.create(
                    fqdn=data["medium"],
                    fqdn_hash=Domain.hash_name(data["medium"].encode()),
                    last_updated=floor(time()),
                )
            ).id

        db_ruege = await Ruege.create(
            identifier=data["aktenzeichen"],
            year=data["year"],
            title=data["title"],
            ziffer=data["ziffer"],
            domain=domain_id,
        )

    await db_ruege.update(
        title=data["title"], ziffer=data["ziffer"], year=data["year"], domain=domain_id
    ).apply()

    return Response(status_code=201)


@api.get(
    "/domain/",
    summary="Interface for clients",
    description="Route for requesting domains with scores by a hash prefix",
    status_code=200,
)
async def fetch_domains(
    domains: Optional[str] = Query(
        None,
        min_length=4,
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
    print(domains)
    if domains is None:
        return HTTPException(status_code=400, detail="Missing domains parameter")

    if page is None:
        page = 0
    else:
        page -= 1

    # Not efficient but okay
    return {
        "domains": [
            {
                "fqdn": domain[1],
                "score": (1, 1),  # domain.score(),
                "last_updated": domain[0],
            }
            for domain in await db.select([Domain.last_updated, Domain.fqdn])
            .where(Domain.fqdn_hash.startswith(domains))
            .limit(100)
            .offset(page * 100)
            .gino.all()
        ]
    }


@api.get("/db-dump/", include_in_schema=False)
async def db_dump():

    return {
        "domains": [
            {"fqdn": domain[0], "hash": domain[1]}
            for domain in await db.select([Domain.fqdn, Domain.fqdn_hash]).gino.all()
        ]
    }


@api.post(
    "/update/",
    description="Interface for updating the graph database by scrapers. All linked new domains will automatically be inserted into the database",
    status_code=201,
    response_description="Empty Respose if not errors have arisen.",
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

    return Response(status_code=201)
