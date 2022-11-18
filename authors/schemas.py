from typing import Optional

from pydantic import BaseModel, PositiveInt


class AuthorsBooks(BaseModel):
    id: Optional[int]
    title: Optional[str]


class AuthorBase(BaseModel):
    email: str
    password: str
    first_name: Optional[str]
    last_name: Optional[str]
    bio: Optional[str] = None
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
