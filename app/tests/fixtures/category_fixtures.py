import pytest
from datetime import datetime, timezone
from redis.asyncio import Redis
from app.models.category import Category
from app.models.product import Product
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services.category import CategoryService
from app.repository.base import AbstractCategoryRepository

# ============ ДАННЫЕ ============
@pytest.fixture
def category_base_data():
    return {
        "title": "Кухня",
        "description": "Товары для кухни, выбирай что хочешь"
    }

@pytest.fixture
def category_data(category_base_data):
    fixed_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    return Category(
        id=1,
        **category_base_data,
        created_at=fixed_time,
        updated_at=fixed_time
    )

@pytest.fixture
def category_data_list():
    fixed_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    return [
        Category(id=1, title="Кухня", description="Товары для кухни", 
                 created_at=fixed_time, updated_at=fixed_time),
        Category(id=2, title="Ванная", description="Товары для ванны",
                 created_at=fixed_time, updated_at=fixed_time),
        Category(id=3, title="Спальня", description="Товары для спальни",
                 created_at=fixed_time, updated_at=fixed_time)
    ]

# ============ SCHEMA ============
@pytest.fixture
def category_for_create_data(category_base_data):
    return CategoryCreate(**category_base_data)

@pytest.fixture
def category_for_update_data(category_base_data):
    return CategoryUpdate(**category_base_data)

@pytest.fixture
def category_updated_data(category_data):
    category_data.title = "Спальня"
    category_data.description = None
    return category_data

# ============ SERVICE & REPO ============
@pytest.fixture
def category_repo(mocker):
    return mocker.AsyncMock(autospec=AbstractCategoryRepository)

@pytest.fixture
def category_redis(mocker):
    return mocker.AsyncMock(autospec = Redis)

@pytest.fixture
def category_service(category_repo, category_redis):
    return CategoryService(category_repo, category_redis)

# ============ DB FIXTURES (для интеграционных тестов) ============
@pytest.fixture
async def create_category(test_async_session):
    """Создает категорию в БД"""
    category = Category(title="Кухня", description="Товары для кухни")
    test_async_session.add(category)
    await test_async_session.commit()
    await test_async_session.refresh(category)
    return category

@pytest.fixture
async def create_categories(test_async_session):
    """Создает несколько категорий в БД"""
    categories = [
        Category(title="Кухня", description="Товары для кухни"),
        Category(title="Ванная", description="Товары для ванны"),
        Category(title="Спальня", description="Товары для спальни")
    ]
    test_async_session.add_all(categories)
    await test_async_session.commit()
    for category in categories:
        await test_async_session.refresh(category)
    return categories

@pytest.fixture
async def create_category_with_products(test_async_session, create_category):
    """Создает категорию с продуктами"""
    category = create_category
    
    products = [
        Product(title="Вилка", price=100, quantity=3, category_id=category.id),
        Product(title="Ложка", price=200, quantity=4, category_id=category.id),
    ]
    test_async_session.add_all(products)
    await test_async_session.commit()
    await test_async_session.refresh(category, attribute_names=["products"])
    return category