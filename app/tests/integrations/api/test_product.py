import pytest
from httpx import AsyncClient
from sqlalchemy import select
from datetime import datetime, timezone
from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductResponse, ProductCreate, ProductUpdate
from app.tests.helpers.assertions import assert_product_equal


async def test_get_all_returns_created_products(client: AsyncClient, create_products):
    response = await client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    validated_products = [ProductResponse.model_validate(item) for item in data]
    assert len(validated_products) == len(create_products)
    
    sorted_response = sorted(validated_products, key=lambda product: product.id)
    sorted_fixture = sorted(create_products, key = lambda product: product.id)
    
    for schema, model in zip(sorted_response, sorted_fixture):
        assert_product_equal(schema, model)
        

async def test_get_all_returns_empty_list(client: AsyncClient, test_async_session):
    response = await client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert data == []
    query_from_db = await test_async_session.execute(
        select(Product)
    )
    products = query_from_db.scalars().all()
    assert products == []


async def test_get_by_id_returns_existing_record(client: AsyncClient, create_product):
    product_id = create_product.id
    response = await client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    validate_product = ProductResponse.model_validate(data)
    assert_product_equal(validate_product, create_product)
    

async def test_get_by_id_returns_not_found_product(client: AsyncClient):
    product_id = 99
    response = await client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 404
    data = response.json()
    assert f"Продукт с ID: {product_id} не найден" in data["detail"]


async def test_create_returns_success(client: AsyncClient, schema_product_create_valid, test_async_session):
    response = await client.post("/api/v1/products", json=schema_product_create_valid.model_dump())
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data, dict)
    validate_product = ProductResponse.model_validate(data)
    product_id = data["id"]
    db_product = await test_async_session.get(Product, product_id)
    assert db_product is not None
    assert_product_equal(validate_product, db_product)
    assert db_product.title == schema_product_create_valid.title
    assert db_product.description == schema_product_create_valid.description
    assert db_product.price == schema_product_create_valid.price
    assert db_product.quantity == schema_product_create_valid.quantity
    assert db_product.category_id == schema_product_create_valid.category_id


async def test_create_returns_not_valid_schema(client: AsyncClient, schema_product_create_not_valid):
    """
    Тест проверяет, что API возвращает 422 при невалидных данных.
    Детальные тесты валидации полей уже есть в тестах Pydantic моделей.
    """
    response = await client.post("/api/v1/products", json=schema_product_create_not_valid)
    assert response.status_code == 422


async def test_create_returns_not_found_category(client: AsyncClient, schema_product_create_not_found_category):
    response = await client.post("/api/v1/products", 
                                 json=schema_product_create_not_found_category.model_dump())
    category_id = schema_product_create_not_found_category.category_id
    assert response.status_code == 404
    data = response.json()
    assert f"Категория с ID: {category_id} не найдена" in data["detail"]


async def test_update_returns_success(client: AsyncClient, create_product, schema_product_update_valid, test_async_session):
    product_id = create_product.id
    response = await client.patch(f"/api/v1/products/{product_id}", json=schema_product_update_valid.model_dump())
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert isinstance(data, dict)
    validate_product = ProductResponse.model_validate(data)
    assert product_id == validate_product.id
    db_product = await test_async_session.get(Product, product_id)
    assert db_product is not None
    assert_product_equal(validate_product, db_product)
    for field, expected_value in schema_product_update_valid.model_dump().items():
        if expected_value is not None:
            assert getattr(db_product, field) == expected_value


async def test_update_returns_not_valid_schema(client: AsyncClient, schema_product_update_not_valid):
    """
    Тест проверяет, что API возвращает 422 при невалидных данных.
    Детальные тесты валидации полей уже есть в тестах Pydantic моделей.
    """
    response = await client.patch("/api/v1/products/1", json=schema_product_update_not_valid)
    assert response.status_code == 422
    

async def test_update_returns_not_found_category(client: AsyncClient, create_product, schema_product_update_not_found_category):
    category_id = schema_product_update_not_found_category.category_id
    product_id = create_product.id
    response = await client.patch(f"/api/v1/products/{product_id}", 
                                  json=schema_product_update_not_found_category.model_dump())
    assert response.status_code == 404
    data = response.json()
    assert f"Категория с ID: {category_id} не найдена" in data["detail"]


async def test_update_returns_not_found_product(client: AsyncClient, schema_product_update_valid):
    product_id = 99
    response = await client.patch(f"/api/v1/products/{product_id}", 
                                      json=schema_product_update_valid.model_dump())
    assert response.status_code == 404
    data = response.json()
    assert f"Продукт с ID: {product_id} не найден" in data["detail"]


async def test_delete_returns_success(client: AsyncClient, create_product, test_async_session):
    product_id = create_product.id
    response = await client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == 204
    product_db = await test_async_session.get(Product, product_id)
    assert product_db is None


async def test_delete_returns_not_found_product(client: AsyncClient):
    product_id = 99
    response = await client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == 404
    data = response.json()
    assert f"Продукт с ID: {product_id} не найден" in data["detail"]