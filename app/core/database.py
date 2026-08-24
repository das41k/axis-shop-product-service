from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
from .config import settings

engine = create_engine(
    url = settings.DATABASE_URL_psycopg,
    echo=True, # Вывод запросов
    pool_size= 7, # Количество соединений
    max_overflow=10 # Дополнительные соединения
)

async_engine = create_async_engine(
    url= settings.DATABASE_URL_asyncpg,
    echo=True, # Вывод запросов
    pool_size= 7, # Количество соединений
    max_overflow=10 # Дополнительные соединения
)

class Base(DeclarativeBase):
    pass

AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)
# По умолчанию (expire_on_commit=True) после вызова session.commit() все объекты, связанные с этой сессией, истекают
# Это означает, что их загруженные атрибуты помечаются как устаревшие. 
# При следующем обращении к любому атрибуту такого объекта SQLAlchemy автоматически выполнит дополнительный запрос к базе данных, 
# чтобы загрузить его актуальное состояние


SessionLocal = sessionmaker(engine)

async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session

def get_session():
    with SessionLocal() as session:
        yield session