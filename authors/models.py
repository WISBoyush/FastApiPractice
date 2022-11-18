from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from books.models import Book  # noqa

from main_app.db import Base


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    bio = Column(String)
    is_active = Column(Boolean)
    is_superuser = Column(Boolean)

    books = relationship("Book", back_populates="author", lazy="subquery")
