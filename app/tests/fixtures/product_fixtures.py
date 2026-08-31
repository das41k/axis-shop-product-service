import pytest
import uuid
from datetime import datetime, timezone
from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.product import ProductService
from app.repository.base import AbstractRepository

# ============ ДАННЫЕ ============
@pytest.fixture
def product_base_data():
    return {
        "title": "Вилка",
        "description": "Очень удобная",
        "price": 100.0,
        "quantity": 3,
        "category_id": 1
    }

@pytest.fixture
def get_product(product_base_data):
    category = Category(id=1, title="Кухня")
    fixed_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    return Product(
        id=1,
        **product_base_data,
        sku="TEST1234",
        category=category,
        created_at=fixed_time,
        updated_at=fixed_time
    )

@pytest.fixture
def get_list_product():
    category = Category(id=1, title="Кухня")
    products = [
        Product(id=1, title="Вилка", description="Очень удобная", 
                sku=uuid.uuid4().hex[:8].upper(), price=100, quantity=3, 
                category_id=1, category=category,
                created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
        Product(id=2, title="Ложка", description="Очень красивая", 
                sku=uuid.uuid4().hex[:8].upper(), price=200, quantity=3, 
                category_id=1, category=category,
                created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
        Product(id=3, title="Тарелка", description="Очень красивая", 
                sku=uuid.uuid4().hex[:8].upper(), price=300, quantity=4, 
                category_id=1, category=category,
                created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc))
    ]
    return products

# ============ SCHEMA ============
@pytest.fixture
def product_for_create_data(product_base_data):
    return ProductCreate(**product_base_data)

@pytest.fixture
def product_for_update_data(product_base_data):
    return ProductUpdate(**product_base_data)

@pytest.fixture
def product_updated_data(get_product):
    get_product.title = "Ложка"
    get_product.description = None
    get_product.price = 250
    return get_product

# ============ SERVICE & REPO ============
@pytest.fixture
def product_repo(mocker):
    return mocker.AsyncMock(autospec=AbstractRepository[Product])

@pytest.fixture
def category_repo(mocker):
    return mocker.AsyncMock(autospec=AbstractRepository[Category])

@pytest.fixture
def product_service(product_repo, category_repo):
    return ProductService(product_repo, category_repo)

# ============ DB FIXTURES (для интеграционных тестов) ============
@pytest.fixture
async def create_product(test_async_session, create_category):
    """Создает продукт в БД"""
    category = create_category
    product = Product(
        title="Вилка", 
        description="Удобная вилка", 
        price=100, 
        quantity=3,
        category_id=category.id
    )
    test_async_session.add(product)
    await test_async_session.commit()
    await test_async_session.refresh(product)
    return product

@pytest.fixture
async def create_products(create_category_with_products):
    """Возвращает продукты из категории"""
    category = create_category_with_products
    return category.products