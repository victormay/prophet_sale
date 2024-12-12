from pydantic import BaseModel,Field


class Page(BaseModel):
    page:int=Field(1, ge=1)
    limit:int=Field(20, ge=10, le=100)


class PSDFResponse:
    code: int
    msg: str