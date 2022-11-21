from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn

load_dotenv()


class Settings(BaseSettings):
    ACCESS_TOKEN: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    DATABASE_URL: PostgresDsn

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


settings = Settings()
# settings.DATABASE_URL = PostgresDsn.build(
#     scheme='postgresql+asyncpg',
#     user=settings.POSTGRES_USER,
#     password=settings.POSTGRES_PASSWORD,
#     host=settings.POSTGRES_HOST,
#     port=settings.POSTGRES_PORT,
#     path=f"/{settings.POSTGRES_DB or ''}"
# )
