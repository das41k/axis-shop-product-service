import pytest
from app.models.product import Product
from app.models.category import Category

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