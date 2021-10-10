from hashlib import sha1
from gino.loader import ColumnLoader
from typing import Tuple
from gino.ext.starlette import Gino
from api.db.config import *

db = Gino(
    dsn=DB_DSN,
    pool_min_size=DB_POOL_MIN_SIZE,
    pool_max_size=DB_POOL_MAX_SIZE,
    echo=DB_ECHO,
    ssl=DB_SSL,
    use_connection_for_request=DB_USE_CONNECTION_FOR_REQUEST,
    retry_limit=DB_RETRY_LIMIT,
    retry_interval=DB_RETRY_INTERVAL,
)


class Domain(db.Model):
    """Domain node representation with hashed (SHA-1) domain name and uid"""

    __tablename__ = "domains"

    # unique, incremental identifier
    id = db.Column(db.BigInteger(), primary_key=True)
    # Fully Qualified Domain Name
    fqdn = db.Column(db.String(), unique=True, index=True, nullable=False)
    # Hash
    fqdn_hash = db.Column(db.String(120))
    # Last updated field
    last_updated = db.Column(db.Integer(), nullable=False)

    @staticmethod
    def hash_name(name: bytes) -> str:
        return sha1(name).hexdigest()

    def score(self) -> Tuple[int, int]:
        links = db.func.count(Link.parent_id)
        print(db.scalar(db.exists().where(Link.parent_id == self.id).select()))
        print(db.scalar(db.exists().where(Link.child_id == self.id).select()))
        print(
            db.select(
                [
                    Domain.name,
                    links,
                ]
            )
            .select_from(Domain.outerjoin(Link.child_id))
            .group_by(
                *Domain,
            )
            .gino.load((Domain, ColumnLoader(links)))
        )

        return (0, 0)


class Link(db.Model):
    """Link is a directed connection between two domains"""

    __tablename__ = "links"

    # True = Network for most-likely correct information, False = Most likely misinformation
    network = db.Column(db.Boolean(), nullable=False)
    # Id of origin domain
    parent_id = db.Column(
        db.BigInteger(), db.ForeignKey("domains.id"), primary_key=True
    )
    # Id of target domain
    child_id = db.Column(db.BigInteger(), db.ForeignKey("domains.id"), primary_key=True)


class Ruege(db.Model):
    __tablename__ = "ruegen"

    # Aktenzeichen – Might be used for indexing instead of having a hashed value
    identifier = db.Column(db.String(), unique=True, nullable=False, primary_key=True)
    titel = db.Column(db.String(), nullable=False)
    # Description for ruege that might be requested by extension
    description = db.Column(db.String(), nullable=False)
    # Year of ruege
    year = db.Column(db.Integer(), nullable=False)
    # Associated domain
    domain = db.Column(db.BigInteger(), db.ForeignKey("domains.id"), nullable=False)
