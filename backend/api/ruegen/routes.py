from api.db import db
from api.db.schema import Ruege, Domain
from api.ruegen.models import RuegenUpdateRequest
from fastapi import APIRouter, Response
from fastapi.encoders import jsonable_encoder
from math import floor
from time import time

ruegen_router = APIRouter(prefix="/ruegen", tags=["Rügen"])


@ruegen_router.post(
    "/update/",
    status_code=202,
    summary="Interface for ruegen scraper",
    description="Interface used by ruegen scraper on instance startup to feed updates and/ or new ruegen to the database",
    response_description="Empty when successfully otherwise see `Validation Error`",
)
async def update_ruege(ruege: RuegenUpdateRequest):
    data = jsonable_encoder(ruege)

    db_ruege = await Ruege.query.where(
        Ruege.identifier == data["aktenzeichen"]
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
                    fqdn_hash=Domain.hash_name(data["medium"].encode()),
                    last_updated=floor(time()),
                )
            ).id
        else:
            domain_id = medium[0]

        db_ruege = await Ruege.create(
            identifier=data["aktenzeichen"],
            year=data["year"],
            title=data["title"],
            ziffer=data["ziffer"],
            domain=domain_id,
        )
    else:
        domain_id = db_ruege.domain

    await db_ruege.update(
        title=data["title"], ziffer=data["ziffer"], year=data["year"], domain=domain_id
    ).apply()

    return Response(status_code=201)
