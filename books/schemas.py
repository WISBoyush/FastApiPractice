from typing import Optional

from pydantic import BaseModel, PositiveInt

from authors.schemas import Author


class BooksAuthor(BaseModel):
    id: Optional[int]


class BookBase(BaseModel):
    author_id: Optional[int]
    title: str
    price: int
    quantity: int
    description: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    author_id: PositiveInt
    title: Optional[str]
    price: Optional[int]
    quantity: Optional[int]
    description: Optional[str]
