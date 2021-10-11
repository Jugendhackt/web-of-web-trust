from api.db import db
from api.db.schema import Ruege, Domain
from api.utility.dependencies import PaginationParameter, pagination
from api.ruegen.models import RuegenUpdateRequest, RuegeModel
from api.domains.models import DomainHash
from fastapi import APIRouter, Response, Depends, Query
from fastapi.encoders import jsonable_encoder
from math import floor
from time import time

ruegen_router = APIRouter(prefix="/ruegen", tags=["Rügen"])


@ruegen_router.get(
    "/fetch/",
    status_code=200,
    summary="Interface for clients",
    description="Interface for getting ruegen from the database",
)
async def test(
    domain: str = DomainHash,
    pagination: PaginationParameter = Depends(pagination),
):
    return [
        RuegeModel(identifier=ruege[0], title=ruege[1], year=ruege[2], ziffer=ruege[3])
        for ruege in await db.select(
            [Ruege.identifier, Ruege.title, Ruege.year, Ruege.ziffer]
        )
        .where(Ruege.domain_id.startswith(domain))
        .limit(pagination.per_page)
        # .group_by(Ruege.domain)
        .offset(pagination.offset).gino.all()
    ]


@ruegen_router.post(
    "/update/",
    status_code=202,
    summary="Interface for scraper",
    description="Interface used by ruegen scraper to update and/ or add new ruegen to the database",
    response_description="Empty when successfully otherwise see `Validation Error`",
)
async def update_ruege(ruege: RuegenUpdateRequest):
    data = jsonable_encoder(ruege)

    db_ruege = await Ruege.query.where(
        Ruege.identifier == data["identifier"]
    ).gino.first()

    if db_ruege is None:
        medium = (
            await db.select([Domain.id])
            .where(Domain.fqdn == data["medium"])
            .gino.first()
        )

        if medium is None:
            domain_id = (
                await Domain.create(
                    fqdn=data["medium"],
                    fqdn_hash=Domain.hash_name(data["medium"]),
                    last_updated=floor(time()),
                )
            ).id
        else:
            domain_id = medium[0]

        db_ruege = await Ruege.create(
            identifier=data["identifier"],
            year=data["year"],
            title=data["title"],
            ziffer=data["ziffer"],
            domain_id=domain_id,
        )
    else:
        domain_id = db_ruege.domain

    await db_ruege.update(
        title=data["title"],
        ziffer=data["ziffer"],
        year=data["year"],
        domain_id=domain_id,
    ).apply()

    return Response(status_code=201)
