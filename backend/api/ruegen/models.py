from pydantic import BaseModel


class RuegenUpdateRequest(BaseModel):
    """Request for updating or creating a new Ruege"""

    medium: str
    identifier: str
    title: str
    ziffer: str
    year: int


class RuegeModel(BaseModel):
    """All information about a ruege for a given domain"""

    identifier: str = "AK34J"
    title: str = "Falsche Angabe von …"
    year: int = 2004
    ziffer: str = "23135"
