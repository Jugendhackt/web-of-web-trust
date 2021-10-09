from pydantic import BaseModel
from typing import List, Tuple


class InsertRequest(BaseModel):
    """Request for inserting and/ or updating content on graph"""

    domain: str
    links: List[str]
    # True = 
    network: bool
    last_updated: int


class DomainReponse(BaseModel):
    """Information about domain including evaluated scores"""

    fqdn: str
    score: Tuple[int]
    last_updated: int


class AggregatedDomainResponse(BaseModel):
    """Aggregated model of `DomainReponse`"""

    domains: List[DomainReponse] = []
