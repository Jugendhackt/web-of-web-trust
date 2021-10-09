from .. import db
from gino import Column, Integer, String, Boolean


class Domain(db.Model):
    __tablename__ = "domains"

    id = Column(Integer(), primary_key=True)
    fqdn = Column(
        String(),
        unique=True,
        index=True,
    )


class Edge(db.Model):
    __tablename__ = "edges"

    t = Column(Boolean())

class 