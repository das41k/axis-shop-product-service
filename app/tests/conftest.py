pytest_plugins = [
    "app.tests.fixtures.category_fixtures",
    "app.tests.fixtures.product_fixtures",
    "app.tests.fixtures.schema_fixtures"
]

import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from httpx import AsyncClient, ASGITransport
from app.main import create_app
from app.core.database import get_async_session, Base
from app.tests.test_config import TestSettings
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:17-alpine") as postgres:
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
async def test_async_engine(test_settings):
    async_engine = create_async_engine(
        url=test_settings.DATABASE_URL_asyncpg,
        echo=True,  # ← включи echo, чтобы видеть SQL
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield async_engine
    await async_engine.dispose()

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

@pytest.fixture
def app():
    _app = create_app(enable_lifespan=False)
    return _app


@pytest.fixture
async def client(app, test_async_session: AsyncSession):
    """
    Клиент для тестирования API.
    Зависимость get_async_session заменяется на транзакционную сессию.
    """
    async def override_get_db():
        yield test_async_session

    app.dependency_overrides[get_async_session] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver"
    ) as client:
        yield client

    app.dependency_overrides.clear()