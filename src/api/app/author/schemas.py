
from pydantic import BaseModel
from typing import List


class BaseSchema(BaseModel):
    name: str


class createSchema(BaseSchema):
    pass


class responseSchema(BaseSchema):
    id: int
    # books: List[int] = []

    class Config:
        orm_mode = True


class updateSchema(BaseSchema):
    id: int
