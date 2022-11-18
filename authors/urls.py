from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from authors.schemas import AuthorCreate, AuthorUpdate, Authentication
from authors.services import AuthorService
from main_app.db import get_session

router = APIRouter(
    prefix='/authors',
    tags=[''],
    responses={404: {'detail': 'Not Found'}}
)


@router.post('/create/')
async def create_author(db: AsyncSession = Depends(get_session), author: AuthorCreate = None):
    return await AuthorService(db).create_author(author)


@router.get('/')
async def get_authors(db: AsyncSession = Depends(get_session), offset: int = 0, limit: int = 50):
    return await AuthorService(db).get_authors(offset, limit)


@router.get('/{author_id}/')
async def get_author(db: AsyncSession = Depends(get_session), author_id: int = None):
    return await AuthorService(db).get_author(author_id)


@router.patch('/{author_id}/')
async def patch_author(
        db: AsyncSession = Depends(get_session),
        changes: AuthorUpdate = None,
        author_id: int = None):
    return await AuthorService(db).update_author(changes, author_id)


@router.delete('/{author_id}/')
async def patch_author(db: AsyncSession = Depends(get_session), author_id: int = None):
    return await AuthorService(db).delete_author(author_id)


@router.post('/auth/')
async def patch_author(db: AsyncSession = Depends(get_session), data: Authentication = None):
    return await AuthorService(db).authorize(data)
