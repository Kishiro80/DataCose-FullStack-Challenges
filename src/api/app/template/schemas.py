from pydantic import BaseModel


class createSchema(BaseModel):
    username: str
    email: str


class responseSchema(BaseModel):
    id: int
    username: str
    email: str


class updateSchema(BaseModel):
    id: int
    username: str
    email: str
