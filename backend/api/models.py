from pydantic import BaseModel
from typing import List, Tuple


class InsertRequest(BaseModel):
    """Request for inserting and/ or updating content on graph"""

    domain: str
    links: List[str]
    last_updated: int


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
    score: Tuple[int]
    last_updated: int


class AggregatedDomainResponse(BaseModel):
    """Aggregated model of `DomainReponse`"""

    domains: List[DomainReponse] = []
