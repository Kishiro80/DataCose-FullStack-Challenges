from pydantic import BaseModel, Field

from app.book.schemas import responseSchema as BookresponseSchema


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


responseSchema.update_forward_refs()
