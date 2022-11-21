from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship

from main_app.db import Base


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=False)
    description = Column(String, index=False)
    price = Column(Integer, index=False)
    quantity = Column(Integer, index=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=True)

    author = relationship("Author", back_populates="books")
