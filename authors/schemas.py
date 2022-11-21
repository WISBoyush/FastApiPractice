from typing import Optional

from pydantic import BaseModel, PositiveInt, Required


class AuthorBase(BaseModel):
    email: str = Required
    password: str
    first_name: Optional[str]
    last_name: Optional[str]
    bio: Optional[str]
    books: Optional[list[PositiveInt]] = []


class Authentication(BaseModel):
    email: str
    password: str


class AuthorCreate(AuthorBase):
    pass


class Author(BaseModel):
    id: int

    class Config:
        orm_mode = True


class AuthorDelete(Author):
    pass


class AuthorUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    bio: Optional[str]
