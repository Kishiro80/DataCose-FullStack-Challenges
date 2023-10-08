
from pydantic import BaseModel


class baseSchema(BaseModel):
    username: str
    email: str
    password: str


class createSchema(baseSchema):
    pass


class responseSchema(baseSchema):
    id: int


class updateSchema(baseSchema):
    id: int


class changePassSchema(baseSchema):
    id: int
    old_password: str
