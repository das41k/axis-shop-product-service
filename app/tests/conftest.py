from testcontainers.postgres import PostgresContainer
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from httpx import AsyncClient, ASGITransport
from app.main import create_app
from app.core.database import get_async_session, Base

from app.tests.test_config import TestSettings

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer(image="postgres:17-alpine",) as postgres:
        yield postgres

@pytest.fixture(scope="session")
def test_settings(postgres_container):
    return TestSettings(
        DB_PORT=postgres_container.get_exposed_port(5432),
        DB_HOST=postgres_container.get_container_host_ip(),
        DB_NAME=postgres_container.dbname,
        DB_USER=postgres_container.username,
        DB_PASSWORD=postgres_container.password
    )
 
@pytest.fixture(scope="session")
def test_engine(test_settings):
     return create_engine(
        url= test_settings.DATABASE_URL_psycopg,
        echo=True,
        pool_size=7,
        max_overflow=10)

@pytest.fixture(scope="session")
def test_async_engine(test_settings):
    return create_async_engine(
        url= test_settings.DATABASE_URL_asyncpg,
        echo= True,
        pool_size= 7,
        max_overflow=10)

@pytest.fixture
def definition_tables(test_engine):
    with test_engine.begin() as conn:
        Base.metadata.create_all(bind=conn)
    yield
    with test_engine.begin() as conn:
        Base.metadata.drop_all(bind=conn)

@pytest.fixture
async def async_definition_tables(test_async_engine):
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def test_session(test_engine, definition_tables):
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
async def test_async_session(test_async_engine, async_definition_tables):
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

@pytest.fixture
def override_dependencies(app, test_async_session):
    def override_get_async_session():
        return test_async_session
    app.dependency_overrides[get_async_session] = override_get_async_session
    yield
    app.dependency_overrides.clear()

@pytest.fixture
async def client(app, override_dependencies):
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as client:
        yield client
        

@pytest.fixture(scope="session")
def app():
    return create_app(enable_lifespan=False)