from pydantic import BaseModel, Field

from app.book.schemas import responseSchema as BookresponseSchema
from app.book.schemas import baseSchema as BookbaseSchema


class BaseSchema(BaseModel):
    name: str


class createSchema(BaseSchema):
    pass


class responseSchema(BaseSchema):
    id: int
    book: list["BookresponseSchema"] = Field(default_factory=list)

    class Config:
        orm_mode = True


class cleanResponseSchema(BaseSchema):
    id: int

    class Config:
        orm_mode = True


class updateSchema(BaseSchema):
    id: int
    book: list["BookbaseSchema"] = Field(default_factory=list)


responseSchema.update_forward_refs()
