from pydantic import BaseModel
from typing import List, Tuple


class InsertRequest(BaseModel):
    """Request for inserting and/ or updating content on graph"""

    domain: str
    network: bool
    links: List[str]
    last_updated: int


class DomainDuplet(BaseModel):
    """Duplet of fqdn and sha1-hexdigest"""

    fqdn: str
    hash: str


class DomainDumpResponse(BaseModel):
    """Response listing all domain duplets (fqdn and sha1-hexdigest) from the database sorted by id in ascending order"""

    domains: List[DomainDuplet]


class RuegenUpdateRequest(BaseModel):
    """Request for updating or creating a new ruege"""

    medium: str
    aktenzeichen: str
    title: str
    ziffer: str
    year: int


class DomainReponse(BaseModel):
    """Information about domain including evaluated scores"""

    fqdn: str
    score: Tuple[int, int]
    last_updated: int


class AggregatedDomainResponse(BaseModel):
    """Aggregated model of `DomainReponse`"""

    domains: List[DomainReponse] = []
