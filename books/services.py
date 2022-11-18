from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from authors.models import Author
from books.models import Book
from books.schemas import BookCreate, BookUpdate
from main_app.db import get_session

app = FastAPI()


class BookService:
    def __init__(self, db: AsyncSession = Depends(get_session)):
        self.db = db

    async def get_instance(self, model, item_id: int = None):
        instance = (await self.db.execute(select(model).where(model.id == item_id))).scalars().first()
        if not instance:
            raise HTTPException(404, "There is not Instance")
        return instance

    async def author_exists(self, author_id: int = None) -> bool | Exception:
        if not author_id:
            raise HTTPException(404, "Param is None", {"Error": "author_id is required"})
        return bool((await self.db.execute(select(Author.email).where(Author.id == author_id))).scalars().first())

    async def create_book(self, book: BookCreate = None):
        book = book.dict()
        if book["author_id"] and not await self.author_exists(author_id=book["author_id"]):
            raise HTTPException(400, "There is not Author with this ID")
        new_book = Book(**book)
        self.db.add(new_book)
        await self.db.commit()
        await self.db.refresh(new_book)
        return new_book

    async def get_books(self, offset: int = 0, limit: int = 50):
        result = await self.db.execute(select(Book).order_by(Book.id).offset(offset).limit(limit))
        res = result.scalars().all()
        return res

    async def get_book(self, book_id: int = None):
        if book_id:
            result = await self.db.execute(select(Book).where(Book.id == book_id))
            return result.scalars().first()

    async def update_book(self, changes: BookUpdate = None, book_id: int = None):
        book = (await self.db.execute(select(Book).where(Book.id == book_id))).scalars().first()
        if not book:
            raise HTTPException(404, "NoItemFound")
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
        instance = await self.get_instance(Book, book_id)
        await self.db.execute(delete(Book).where(Book.id == instance.id))
        await self.db.commit()
        return {"Object": "Was successfully deleted"}
