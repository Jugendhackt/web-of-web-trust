from api.db import db
from api.utility.dependencies import PaginationParameter
from api.ruegen.models import RuegeModel
from cache import AsyncTTL
from gino.loader import ColumnLoader
from hashlib import sha1
from random import randint
from typing import Tuple, List, Dict


class Domain(db.Model):
    """Domain node representation with hashed (SHA-1) domain name and uid"""

    __tablename__ = "domains"

    # unique, incremental identifier
    id = db.Column(db.BigInteger(), primary_key=True)
    # Fully Qualified Domain Name
    fqdn = db.Column(db.String(), unique=True, index=True, nullable=False)
    # Hash
    fqdn_hash = db.Column(db.String(120), unique=True, nullable=False)
    # Last updated field
    last_updated = db.Column(db.Integer(), nullable=False)

    @staticmethod
    @AsyncTTL(time_to_live=30, maxsize=1024)
    def hash_name(name: str) -> str:
        return sha1(name.encode(encoding="utf-8")).hexdigest().__str__()

    @staticmethod
    @AsyncTTL(time_to_live=300, maxsize=1024)
    async def count_ruegen(id: int) -> int:
        return (
            await db.select([db.func.count()]).where(Ruege.domain == id).gino.scalar()
        )

    @staticmethod
    @AsyncTTL(time_to_live=60, maxsize=1024)
    async def score(id: int) -> tuple[int, int]:
        """Calculate score"""
        # This is not efficient
        positive = (
            await db.select([db.func.count()])
            .where(Link.parent_id == id and Link.network == True)
            .gino.scalar()
            - await db.select([db.func.count()])
            .where(Link.child_id == id and Link.network == True)
            .gino.scalar()
        )

        negative = (
            await db.select([db.func.count()])
            .where(Link.parent_id == id and Link.network == False)
            .gino.scalar()
            - await db.select([db.func.count()])
            .where(Link.child_id == id and Link.network == False)
            .gino.scalar()
        )

        return (positive, negative)


class Link(db.Model):
    """Link is a directed connection between two domains"""

    __tablename__ = "links"

    # True = Network for most-likely correct information, False = Most likely misinformation
    network = db.Column("network", db.Boolean(), nullable=False)
    # Id of origin domain
    parent_id = db.Column(
        "parent_id", db.BigInteger(), db.ForeignKey("domains.id"), primary_key=True
    )
    # Id of target domain
    child_id = db.Column(
        "child_id", db.BigInteger(), db.ForeignKey("domains.id"), primary_key=True
    )


class Ruege(db.Model):
    __tablename__ = "ruegen"

    # Aktenzeichen – Might be used for indexing instead of having a hashed value
    identifier = db.Column(db.String(), unique=True, nullable=False, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    # Year of ruege
    year = db.Column(db.Integer(), nullable=False)
    # Associated domain
    domain_id = db.Column(
        db.String(120), db.ForeignKey("domains.fqdn_hash"), nullable=False
    )
    # Ziffer
    ziffer = db.Column(db.String(), nullable=False)

    @staticmethod
    @AsyncTTL(time_to_live=60, maxsize=1024)
    async def by_hash(
        fqdn_hash: str, pagination: PaginationParameter
    ): #-> List[Dict[str, RuegeModel]]:
        print(
            await db.select([Ruege.identifier, Ruege.title, Ruege.year, Ruege.ziffer])
            .where(Ruege.domain.startswith(fqdn_hash))
            .group_by(Ruege.domain)
            .limit(pagination.per_page)
            .offset(pagination.offset)
            .gino.all()
        )
        return [
            RuegeModel(
                identifier=ruege[0], title=ruege[1], year=ruege[2], ziffer=ruege[3]
            )
            for ruege in await db.select(
                [Ruege.identifier, Ruege.title, Ruege.year, Ruege.ziffer]
            )
            .where(Ruege.domain.startswith(fqdn_hash))
            .limit(pagination.per_page)
            .group_by(Ruege.domain)
            .offset(pagination.offset)
            .gino.all()
        ]
