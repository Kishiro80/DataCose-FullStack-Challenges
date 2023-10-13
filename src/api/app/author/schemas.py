from typing import lists

from pydantic import BaseModel


class BaseSchema(BaseModel):
    name: str


class createSchema(BaseSchema):
    pass


class responseSchema(BaseSchema):
    id: int
    books: lists[int] = []

    class Config:
        orm_mode = True


class updateSchema(BaseSchema):
    id: int
