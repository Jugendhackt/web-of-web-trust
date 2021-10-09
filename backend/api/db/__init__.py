from api.db.init import db
from hashlib import sha1
from gino.loader import ColumnLoader


class Domain(db.Model):
    """Domain node representation with hashed (SHA-1) domain name and uid"""

    __tablename__ = "domains"

    # unique, incremental identifier
    id = db.Column(db.BigInteger(), primary_key=True)
    # Fully Qualified Domain Name
    fqdn = db.Column(db.String(), unique=True, index=True, nullable=False)
    # Hash
    hash = db.Column(db.String(40))
    # Last updated field
    last_updated = db.Column(db.Integer(), nullable=False)
    # network
    network = db.Column(db.Boolean())

    @staticmethod
    def hash_name(name: str) -> str:
        return sha1(name)

    def score(self) -> (int, int):
        links = db.func.count(Link.parent_id)
        db.scalar(db.exists().where(User.email == email).select())
        db.scalar(db.exists().where(User.email == email).select())
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

    id = db.Column(db.BigInteger(), primary_key=True)

    aktenzeichen = db.Column(db.String(), unique=True, nullable=False)
    titel = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
