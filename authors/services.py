import hashlib

from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload

from authors.models import Author
from authors.schemas import AuthorCreate, AuthorUpdate, Authentification
from main_app.config import settings
from main_app.db import get_session

app = FastAPI()


class AuthorService:
    def __init__(self, db: AsyncSession = Depends(get_session)):
        self.db = db
        self.salt = settings.ACCESS_TOKEN

    async def create_author(self,
                            db: AsyncSession = Depends(get_session),
                            author: AuthorCreate = None):
        author = author.dict()
        author["is_active"] = True
        author["is_superuser"] = False
        author["password"] = hashlib.md5((author["password"] + self.salt).encode()).hexdigest()

        new_author = Author(**author)
        db.add(new_author)
        await db.commit()
        await db.refresh(new_author)
        return new_author

    async def get_authors(
            self,
            db: AsyncSession = Depends(get_session),
            offset: int = 0, limit: int = 50):
        result = (
            await db.execute(
                select(Author).options(subqueryload(Author.id)).order_by(Author.id).offset(offset).limit(limit)
            )
        ).scalars().all()
        return result

    async def authorization(self, db: AsyncSession = Depends(get_session), data: Authentification = None):
        data = data.dict()
        author = (
            await db.execute(select(Author).where(Author.email == data["email"]))
        ).scalars().first()

        db_password = author.password

        entered_password = hashlib.md5((data["password"] + self.salt).encode()).hexdigest()

        if not all([db_password[i] is entered_password[i] for i in range(len(db_password))]):
            raise HTTPException(403, "Permission Denied")

        return {"Success": f"Hello, {author.first_name} {author.last_name}"}

    async def get_author(
            self,
            db: AsyncSession = Depends(get_session),
            author_id: int = None):
        if author_id:
            result = await db.execute(select(Author).where(Author.id == author_id))
            return result.scalars().first()

    async def update_author(
            self,
            db: AsyncSession = Depends(get_session),
            changes: AuthorUpdate = None,
            author_id: int = None):
        author = (await db.execute(select(Author).where(Author.id == author_id))).scalars().first()
        if author:
            for field, value in changes.dict(exclude_unset=True).items():
                setattr(author, field, value)
            await db.commit()
            await db.refresh(author)
            return author

    async def delete_author(
            self,
            db: AsyncSession = Depends(get_session),
            author_id: int = None):

        await db.execute(delete(Author).where(Author.id == author_id))
        await db.commit()
        return {"Object": "Was successfully deleted"}

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'
