import pytest
from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductUpdate

@pytest.fixture
async def create_category(test_async_session):
    category = Category(title = "Кухня", description = "Товары для кухни")
    test_async_session.add(category)
    await test_async_session.commit()
    await test_async_session.refresh(category)
    return category

@pytest.fixture
async def create_product(test_async_session, create_category):
    product = Product(title = "Вилка", description = "Удобная вилка", price = 100, 
                      quantity = 3, category = create_category, 
                      category_id = create_category.id)
    test_async_session.add(product)
    await test_async_session.commit()
    await test_async_session.refresh(product)
    return product

@pytest.fixture
async def create_products(test_async_session, create_category):
    products = [
        Product(title = "Вилка", description = "Удобная вилка", price = 100, 
                      quantity = 3, category = create_category, 
                      category_id = create_category.id),
        Product(title = "Ложка", description = "Удобная ложка", price = 200, 
                              quantity = 4, category = create_category, 
                              category_id = create_category.id)
        ]
    test_async_session.add_all(products)
    await test_async_session.commit()
    for product in products:
        await test_async_session.refresh(product)
    print("ТЕСТОВЫЕ ДАННЫЕ====================")
    print(products)
    return products

@pytest.fixture
def schema_product_create_valid(create_category):
    return ProductCreate(
        title = "Вилка", description = "Удобная вилка", 
        price = 100, quantity = 3, category_id = create_category.id)

@pytest.fixture
def schema_product_create_not_valid():
    return {
            "title":  "   ", 
            "description": "a"*101, 
            "price": 0, 
            "quantity": -56, 
            "category_id": -5
        }
    
@pytest.fixture
def schema_product_create_not_found_category():
    return ProductCreate(
            title = "Вилка", description = "Удобная вилка", 
            price = 100, quantity = 3, category_id = 101)

@pytest.fixture
def schema_product_update_valid():
    return ProductUpdate(
        title = "Ложка", description = "Удобная ложка", 
        price = 200, quantity = 1)

@pytest.fixture
def schema_product_update_not_valid():
    return {
        "title":  "   ", 
        "description": "a"*101, 
        "price": 0, 
        "quantity": -56, 
        "category_id": -5
    }

@pytest.fixture
def schema_product_update_not_found_category():
    return ProductUpdate(
            title = "Вилка", description = "Удобная вилка", 
            price = 100, quantity = 3, category_id = 101)