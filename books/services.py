from fastapi import Depends
from fastapi.exceptions import HTTPException
from pydantic import Required
from sqlalchemy import select, delete
from sqlalchemy.sql import exists
from sqlalchemy.ext.asyncio import AsyncSession

from authors.models import Author
from books.models import Book
from books.schemas import BookCreate, BookUpdate
from main_app.db import get_session


class BookService:
    def __init__(self, db: AsyncSession = Depends(get_session)):
        self.db = db

    async def get_instance(self, item_id: int = None) -> Book:
        instance = (await self.db.execute(select(Book).where(Book.id == item_id))).scalars().first()
        if not instance:
            raise HTTPException(404, "There is not Book Instance")
        return instance

    async def author_exists(self, author_id: int = None) -> bool:
        if not author_id:
            raise HTTPException(404, "Param is None", {"Error": "author_id is required"})

        return (await self.db.execute(exists(select(Author).where(Author.id == author_id)).select())).scalar()

    async def create_book(self, book: BookCreate = None) -> Book:
        book = book.dict()
        if book["author_id"] and not await self.author_exists(author_id=book["author_id"]):
            raise HTTPException(400, "There is not Author with this ID")
        new_book = Book(**book)
        self.db.add(new_book)
        await self.db.commit()
        await self.db.refresh(new_book)
        return new_book

    async def get_books(self, offset: int = 0, limit: int = 50) -> list[Book]:
        return (
            await self.db.execute(select(Book).order_by(Book.id).offset(offset).limit(limit))
        ).scalars().all()

    async def get_book(self, book_id: int = None) -> Book:
        return await self.get_instance(book_id)

    async def update_book(self, changes: BookUpdate = None, book_id: int = Required) -> Book:
        book = await self.get_instance(book_id)
        author_id = changes.author_id
        is_author: bool = False

        if changes.author_id:
            is_author = await self.author_exists(author_id)
        if not is_author:
            raise HTTPException(400, "There is not Author")
        for field, value in changes.dict(exclude_unset=True).items():
            setattr(book, field, value)

        await self.db.commit()
        await self.db.refresh(book)
        return book

    async def delete_book(self, book_id: int = None):
        instance = await self.get_instance(book_id)
        await self.db.execute(delete(Book).where(Book.id == instance.id))
        await self.db.commit()
        return instance
