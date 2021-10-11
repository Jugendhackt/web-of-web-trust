from pydantic import BaseModel
from typing import List, Tuple
from fastapi import Query


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
    ruegen_amount: int


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


DomainHash = Query(
    ...,
    min_length=4,
    max_length=40,
    title="Domain Hash Prefix",
    description="To ensure a privacy-first design domains are not retrieved by their fqdn but instead by the first 4-40 chars of their sha-1 hexdigest. Using this design makes it hard for a malicious server operator, of an MITM attack, to precisely track the user. This will yield more results as the graph grows and you may increse the hash precision in such cases to ensure you won't always have to refetch for new pages. (Credits to @",
)
