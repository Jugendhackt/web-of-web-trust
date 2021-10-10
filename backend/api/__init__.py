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
from .db.init import db
from .db import Domain, Link, Ruege
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
    # TODO:
    # - Define a mapping method for medium -> domain
    # -

    data = jsonable_encoder(ruege)

    try:
        db_ruege = Ruege.get(data["aktenzeichen"])
    except Exception as e:
        db_ruege = await Ruege.create(
            Indentifier=data["aktenzeichen"],
            year=data["year"],
            title=data["title"],
            ziffer=data["ziffer"],
        )

    changes = {}
    for key in data.keys():
        if db_ruege.__getattribute__(key) != data[key]:
            changes[key] = data[key]

    # TODO: Finish with changes
    db_ruege.update().values()

    return Response(status_code=201)


@api.post(
    "/domain/",
    response_model=AggregatedDomainResponse,
    summary="Interface for clients",
    description="Route for requesting domains with scores by a hash prefix",
    status_code=200,
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

    if page is None:
        page = 1

    # Not efficient but okay
    return {
        "domains": [
            {
                "fqdn": domain.fqdn,
                "score": (1, 1),  # domain.score(),
                "last_updated": domain.last_updated,
            }
            for domain in await Domain.select(Domain.id, Domain.fqdn)
            .where(Domain.fqdn.startswith(domains))
            .limit(100)
            .offset(page * 100)
            .all()
        ]
    }


@api.get("/test/")
async def test():

    return {"domains": []}


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
