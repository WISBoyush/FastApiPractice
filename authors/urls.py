from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from authors.schemas import AuthorCreate, AuthorUpdate, Authentification
from authors.services import AuthorService
from main_app.db import get_session

router = APIRouter(
    prefix='/authors',
    tags=[''],
    responses={404: {'detail': 'Not Found'}}
)


def get_service():
    return AuthorService()


@router.post('/create/')
async def create_author(
        db: AsyncSession = Depends(get_session),
        author: AuthorCreate = None):
    service = AuthorService()
    return await service.create_author(db, author)


@router.get('/')
async def get_authors(
        db: AsyncSession = Depends(get_session), offset: int = 0, limit: int = 50):
    return await get_service().get_authors(db, offset, limit)


@router.get('/{author_id}/')
async def get_author(
        db: AsyncSession = Depends(get_session),
        author_id: int = None):
    service = AuthorService()
    return await service.get_author(db, author_id)


@router.patch('/{author_id}/')
async def patch_author(
        db: AsyncSession = Depends(get_session),
        changes: AuthorUpdate = None,
        author_id: int = None):
    service = AuthorService()
    return await service.update_author(db, changes, author_id)


@router.delete('/{author_id}/')
async def patch_author(
        db: AsyncSession = Depends(get_session),
        author_id: int = None):
    service = AuthorService()
    return await service.delete_author(db, author_id)


@router.post('/auth/')
async def patch_author(
        db: AsyncSession = Depends(get_session),
        data: Authentification = None):
    service = AuthorService()
    return await service.authorization(db, data)
