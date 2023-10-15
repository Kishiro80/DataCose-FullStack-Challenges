from typing import Optional

from pydantic import BaseModel


class baseSchema(BaseModel):
    title: str
    num_pages: int


class createSchema(baseSchema):
    author_id: int


class updateSchema(baseSchema):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class responseSchema(baseSchema):
    id: int
    author: Optional["AuthorresponseSchema"]

    class Config:
        orm_mode = True


class AuthorresponseSchema(BaseModel):
    id: int
    name: str


createSchema.update_forward_refs()
updateSchema.update_forward_refs()
responseSchema.update_forward_refs()
