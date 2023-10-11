
from pydantic import BaseModel, root_validator


class nopassSchema(BaseModel):
    username: str
    email: str


class baseSchema(nopassSchema):
    password: str


class createSchema(baseSchema):
    pass


class responseSchema(nopassSchema):
    id: int


class authResponseSchema(BaseModel):
    user: responseSchema


class updateSchema(nopassSchema):
    id: int


class changePassSchema(baseSchema):
    id: int
    old_password: str
