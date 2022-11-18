import hashlib

from fastapi import Depends
from fastapi.exceptions import HTTPException
from pydantic import Required
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from authors.models import Author
from authors.schemas import AuthorCreate, AuthorUpdate, Authentication
from main_app.config import settings
from main_app.db import get_session


class AuthorService:
    def __init__(self, db: AsyncSession = Depends(get_session)):
        self.db = db
        self.salt = settings.ACCESS_TOKEN

    async def get_instance(self, item_id: int) -> Author:
        instance = (await self.db.execute(select(Author).where(Author.id == item_id))).scalars().first()
        if not instance:
            raise HTTPException(404, "There is not Author Instance")
        return instance

    async def create_author(self, author: AuthorCreate) -> Author:
        author = author.dict()
        author["is_active"] = True
        author["is_superuser"] = False
        author["password"] = hashlib.md5((author["password"] + self.salt).encode()).hexdigest()

        new_author = Author(**author)
        self.db.add(new_author)
        await self.db.commit()
        await self.db.refresh(new_author)
        return new_author

    async def get_authors(self, offset: int = 0, limit: int = 50) -> list[Author]:
        return (
            await self.db.execute(
                select(Author).order_by(Author.id).offset(offset).limit(limit)
            )
        ).scalars().all()

    async def authorize(self, data: Authentication = None):
        data = data.dict()
        author = (
            await self.db.execute(select(Author).where(Author.email == data["email"]))
        ).scalars().first()

        db_password = author.password
        entered_password = hashlib.md5((data["password"] + self.salt).encode()).hexdigest()

        # Bruteforce security.
        # Time to validate two string will be equal.
        if not all([db_password[i] is entered_password[i] for i in range(len(db_password))]):
            raise HTTPException(403, "Permission Denied")

        return {"Success": f"Hello, {author.first_name} {author.last_name}"}

    async def get_author(self, author_id: int = Required) -> Author:
        return await self.get_instance(author_id)

    async def update_author(self, changes: AuthorUpdate = None, author_id: int = Required) -> Author:
        author = await self.get_instance(author_id)

        for field, value in changes.dict(exclude_unset=True).items():
            setattr(author, field, value)

        await self.db.commit()
        await self.db.refresh(author)
        return author

    async def delete_author(self, author_id: int = None):
        await self.db.execute(delete(Author).where(Author.id == author_id))
        await self.db.commit()
        return {"Object": "Was successfully deleted"}
