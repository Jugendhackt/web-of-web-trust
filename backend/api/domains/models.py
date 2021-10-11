from pydantic import BaseModel
from typing import List, Tuple


class InsertRequest(BaseModel):
    """Request for inserting and/ or updating content on graph"""

    domain: str = "example.de"
    network: bool = True
    links: List[str] = []
    last_updated: int = -1


class DomainResponse(BaseModel):
    """Information about domain including evaluated scores"""

    fqdn: str = "example.de"
    score: tuple[int, ...] = (1, -2)
    last_updated: int = -1


class AggregatedDomainResponse(BaseModel):
    """Aggregated model of `DomainResponse`"""

    domains: List[DomainResponse]


class DomainDuplet(BaseModel):
    """Duplet of fqdn and sha1-hexdigest"""

    fqdn: str
    hash: str


class DomainDumpResponse(BaseModel):
    """Response listing all domain duplets (fqdn and sha1-hexdigest) from the database sorted by id in ascending order"""

    domains: List[DomainDuplet]
