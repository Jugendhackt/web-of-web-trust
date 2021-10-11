from fastapi import Query
from pydantic import BaseModel
from typing import Optional


page_description = """
All routes that return a list of entries may be paginated when over fifty matching entries exist.
Pages are zero indexed, e.g., you need: page = 0, per_page = 100 to get the first 100 entries.
If you repeatably hit this limit consider sending more accurate requests.
"""

per_page_description = """
How many items should be returned per page

> `page x per_page = number of items`
"""


class PaginationParameter(BaseModel):
    """Container for data in pagination query parameters"""

    page: int
    per_page: int
    offset: int


async def pagination(
    page: Optional[int] = Query(
        default=0,
        description=page_description,
        example=1,
        ge=0,
        title="Page for pagination",
    ),
    per_page: Optional[int] = Query(
        default=50,
        description=per_page_description,
        example=10,
        ge=1,
        le=100,
        title="Items per page",
    ),
) -> PaginationParameter:
    return PaginationParameter(page=page, per_page=per_page, offset=page * per_page)
