from pydantic import BaseModel


class RuegenUpdateRequest(BaseModel):
    """Request for updating or creating a new ruege"""

    medium: str
    aktenzeichen: str
    title: str
    ziffer: str
    year: int
