from typing import List

from pydantic import BaseModel


class baseSchema(BaseModel):
    title: str
    num_pages: int


class createSchema(baseSchema):
    pass


class updateSchema(baseSchema):
    id: int

    class Config:
        orm_mode = True


class responseSchema(baseSchema):
    id: int

    class Config:
        orm_mode = True


# createSchema.update_forward_refs()
# updateSchema.update_forward_refs()
# responseSchema.update_forward_refs()
