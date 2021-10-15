from api.db import db
from api.utility.dependencies import PaginationParameter
from api.ruegen.models import RuegeModel
from cache import AsyncTTL
from gino.loader import ColumnLoader
from blake3 import blake3
from typing import Tuple, List, Dict


class Domain(db.Model):
    """Domain node representation with hashed (SHA-1) domain name and uid"""

    __tablename__ = "domains"

    # unique, incremental identifier
    id = db.Column(db.BigInteger(), primary_key=True)
    # Fully Qualified Domain Name
    fqdn = db.Column(db.String(), unique=True, index=True, nullable=False)
    # Hash
    fqdn_hash = db.Column(db.String(32), unique=True, nullable=False)
    # Last updated field
    last_updated = db.Column(db.Integer(), nullable=False)

    @staticmethod
    @AsyncTTL(time_to_live=30, maxsize=1024)
    def hash_name(name: str) -> str:
        return blake3(name.encode(encoding="utf-8")).hexdigest(length=32)

    @staticmethod
    @AsyncTTL(time_to_live=60, maxsize=1024)
    async def score(id: int) -> tuple[int, int]:
        """Calculate score"""
        positive = await count_children_query(
            network=True, id=id
        ) - await count_children_query.scalar(network=True, id=id)

        negative = await count_parents_query(
            network=False, id=id
        ) - await count_children_query.scalar(network=False, id=id)

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
    domain_hash = db.Column(
        db.String(120), db.ForeignKey("domains.fqdn_hash"), nullable=False, index=True
    )
    # Ziffer
    ziffer = db.Column(db.String(), nullable=False)

    @staticmethod
    #  @AsyncTTL(time_to_live=60, maxsize=1024)
    async def by_hash(
        fqdn_hash: str, pagination: PaginationParameter
    ) -> List[RuegeModel]:
        print(
            await paginated_ruege_query.gino.all(
                fqdn_hash=fqdn_hash,
                per_page=pagination.per_page,
                offset=pagination.offset,
            )
        )
        return [
            RuegeModel(
                identifier=ruege[0], title=ruege[1], year=ruege[2], ziffer=ruege[3]
            )
            for ruege in await paginated_ruege_query.gino.all(
                fqdn_hash=fqdn_hash,
                per_page=pagination.per_page,
                offset=pagination.offset,
            )
        ]


# Pre-baked Queries
# Baking queries not only helps with performance on repeated queries
# but also will avoid high-level error since sqlalchemy will attempt to build them at least once
count_parents_query = db.bake(
    db.select([db.func.count()]).where(
        Link.parent_id == db.bindparam("id") and Link.network == db.bindparam("network")
    )
)

count_children_query = db.bake(
    db.select([db.func.count()]).where(
        Link.child_id == db.bindparam("id") and Link.network == db.bindparam("network")
    )
)

count_ruegen_query = db.bake(
    db.select([db.func.count()]).where(Ruege.domain_hash == db.bindparam("id"))
)

paginated_ruege_query = db.bake(
    db.select([Ruege.identifier, Ruege.title, Ruege.year, Ruege.ziffer])
    .where(Ruege.domain_hash.startswith(db.bindparam("fqdn_hash")))
    .limit(db.bindparam("per_page"))
    .offset(db.bindparam("offset"))
    .order_by(Ruege.domain_hash)
)

paginated_domain_dump_query = db.bake(
    db.select([Domain.fqdn, Domain.fqdn_hash])
    .limit(db.bindparam("per_page"))
    .offset(db.bindparam("offset"))
)

paginated_domain_fetch_query = db.bake(
    db.select([Domain.last_updated, Domain.fqdn, Domain.id])
    .where(Domain.fqdn_hash.startswith(db.bindparam("fqdn_hash")))
    .limit(db.bindparam("per_page"))
    .offset(db.bindparam("offset"))
)

get_domain_id_query = db.bake(
    db.select([Domain.id]).where(Domain.fqdn == db.bindparam("fqdn"))
)

link_exists_query = db.bake(
    db.exists()
    .where(
        Link.parent_id == db.bindparam("parent")
        and Link.child_id == db.bindparam("child")
    )
    .select()
)
