from testcontainers.postgres import PostgresContainer
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.tests.test_config import setting

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer(
        image="postgres:17-alpine",
        username=setting.DB_USER,
        password=setting.DB_PASSWORD,
        dbname=setting.DB_NAME
    ) as postgres:
        yield postgres
        
@pytest.fixture(scope="session")
def test_engine(postgres_container):
    return create_engine(
        url= setting.DATABASE_URL_psycopg,
        echo=True,
        pool_size=7,
        max_overflow=10)

@pytest.fixture(scope="session")
def test_async_engine(postgres_container):
    return create_async_engine(
        url= setting.DATABASE_URL_asyncpg,
        echo= True,
        pool_size= 7,
        max_overflow=10)

@pytest.fixture
def test_session(test_engine):
    """Фикстура создает внешнюю транзакцию и откатывает её после теста."""
    with test_engine.connect() as connection:
        transaction = connection.begin()
        SessionLocal = sessionmaker(bind=connection, expire_on_commit=False, 
                            join_transaction_mode="create_savepoint")
        with SessionLocal() as session:
            try:
                yield session
            finally:
                transaction.rollback()

@pytest.fixture
async def test_async_session(test_async_engine):
    """Фикстура создает внешнюю транзакцию и откатывает её после теста."""
    async with test_async_engine.connect() as connection:
        transaction = await connection.begin()
        AsyncSessionLocal = async_sessionmaker(bind=connection, expire_on_commit=False, 
                                join_transaction_mode="create_savepoint")
        async with AsyncSessionLocal() as session:
            try:
                yield session
            finally:
                await transaction.rollback()