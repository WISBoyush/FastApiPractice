from typing import Optional

from pydantic import BaseModel, Required, PositiveInt


class AuthorsBooks(BaseModel):
    id: Optional[int]
    title: Optional[str]


class AuthorBase(BaseModel):
    email: str = Required
    password: str = Required
    first_name: str
    last_name: str
    bio: Optional[str] = None
    books: Optional[list[PositiveInt]] = []


class Authentification(BaseModel):
    email: str = Required
    password: str = Required


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
