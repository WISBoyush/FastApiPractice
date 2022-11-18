from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from main_app.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# sqlalchemy_database_uri = PostgresDsn.build(
#     scheme="postgresql+asyncpg",
#     user=os.environ.get("POSTGRES_USER"),
#     password=os.environ.get("POSTGRES_PASSWORD"),
#     host=os.environ.get("POSTGRES_HOST"),
#     port=os.environ.get("POSTGRES_PORT"),
#     path=f"/{os.environ.get('POSTGRES_DB') or ''}",
# )
# sqlalchemy_database_uri, pool_pre_ping=True

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True, future=True
)

async_session = sessionmaker(
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
        await session.close()
