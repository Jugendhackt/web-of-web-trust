from typing import Optional, Any, Dict, List, Union
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
            for domain in await Domain.select(Domain.id, Domain.name)
            .filter(Domain.name.startswith(domains))
            .limit(100)
            .offset(page * 100)
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
    print(domain)
    data = jsonable_encoder(domain)

        
    d = await Domain.create(
        fqdn=data["domain"],
        hash=Domain.hash_name(data["domain"]),
        last_updated=data["last_updated"],
    )

    print(d)

    return Response(status_code=201)
