import pytest
from app.schemas.product import ProductCreate, ProductUpdate
from app.schemas.category import CategoryCreate, CategoryUpdate

# ============ CATEGORY SCHEMAS ============
@pytest.fixture
def schema_category_create_valid():
    return CategoryCreate(
        title="Туалет", 
        description="Товары для туалета"
    )

@pytest.fixture
def schema_category_create_not_valid():
    return {
        "title": "   ",
        "description": "a" * 101
    }

@pytest.fixture
def schema_category_update_valid():
    return CategoryUpdate(
        title="Туалет", 
        description="Товары для туалета"
    )

@pytest.fixture
def schema_category_update_not_valid():
    return {
        "title": "   ",
        "description": "a" * 101
    }

# ============ PRODUCT SCHEMAS ============
@pytest.fixture
def schema_product_create_valid(create_category):
    """Создает валидную схему для продукта"""
    category = create_category
    category_id = category.id
    return ProductCreate(
        title="Вилка", 
        description="Удобная вилка", 
        price=100, 
        quantity=3, 
        category_id=category_id
    )

@pytest.fixture
def schema_product_create_not_valid():
    return {
        "title": "   ", 
        "description": "a" * 101, 
        "price": 0, 
        "quantity": -56, 
        "category_id": -5
    }

@pytest.fixture
def schema_product_create_not_found_category():
    return ProductCreate(
        title="Вилка", 
        description="Удобная вилка", 
        price=100, 
        quantity=3, 
        category_id=101
    )

@pytest.fixture
def schema_product_update_valid():
    return ProductUpdate(
        title="Ложка", 
        description="Удобная ложка", 
        price=200, 
        quantity=1
    )

@pytest.fixture
def schema_product_update_not_valid():
    return {
        "title": "   ", 
        "description": "a" * 101, 
        "price": 0, 
        "quantity": -56, 
        "category_id": -5
    }

@pytest.fixture
def schema_product_update_not_found_category():
    return ProductUpdate(
        title="Вилка", 
        description="Удобная вилка", 
        price=100, 
        quantity=3, 
        category_id=101
    )