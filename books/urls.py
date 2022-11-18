from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from books.schemas import BookCreate, BookUpdate
from books.services import BookService
from main_app.db import get_session

router = APIRouter(
    prefix='/books',
    tags=[''],
    responses={404: {'detail': 'Not Found'}}
)


def get_service(db: AsyncSession = Depends(get_session)):
    return BookService(db)


@router.post('/create/')
async def create_book(
        db: AsyncSession = Depends(get_session),
        book: BookCreate = None):
    return await get_service(db).create_book(book)


@router.get('/')
async def get_books(
        db: AsyncSession = Depends(get_session), offset: int = 0, limit: int = 50):
    return await get_service(db).get_books(offset, limit)


@router.get('/{book_id}/')
async def get_book(
        db: AsyncSession = Depends(get_session),
        book_id: int = None):
    return await get_service(db).get_book(book_id)


@router.patch('/{book_id}/')
async def patch_book(
        db: AsyncSession = Depends(get_session),
        changes: BookUpdate = None,
        book_id: int = None):
    return await get_service(db).update_book(changes, book_id)


@router.delete('/{author_id}/')
async def delete_book(
        db: AsyncSession = Depends(get_session),
        book_id: int = None):
    return await get_service(db).delete_book(book_id)
