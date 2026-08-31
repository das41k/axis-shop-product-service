import pytest
from httpx import AsyncClient
from sqlalchemy import select
from app.tests.helpers.assertions import assert_category_equal
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate


async def test_get_all_returns_created_categories(client: AsyncClient, create_categories):
    response = await client.get("/api/v1/categories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    validated_categories = [CategoryResponse.model_validate(item) for item in data]
    sorted_response = sorted(validated_categories, key=lambda category: category.id)
    sorted_fixture = sorted(create_categories, key=lambda category: category.id)
    
    for schema, model in zip(sorted_response, sorted_fixture):
        assert_category_equal(schema, model)


async def test_get_all_returns_empty_list(client: AsyncClient, test_async_session):
    response = await client.get("/api/v1/categories")
    assert response.status_code == 200
    data = response.json()
    assert data == []
    
    query_from_db = await test_async_session.execute(
            select(Category)
        )
    result = query_from_db.scalars().all()
    assert result == []


async def test_get_by_id_returns_success(client: AsyncClient, create_category):
    category_id = create_category.id
    response = await client.get(f"/api/v1/categories/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    validated_category = CategoryResponse.model_validate(data)
    assert_category_equal(validated_category, create_category)


async def test_get_by_id_returns_not_found(client: AsyncClient):
    category_id = 4
    response = await client.get(f"/api/v1/categories/{category_id}")
    assert response.status_code == 404
    data = response.json()
    assert f"Категория с ID: {category_id} не найдена" in data["detail"]
    

async def test_create_returns_success(client: AsyncClient, schema_category_create_valid, test_async_session):
    response = await client.post("/api/v1/categories", json=schema_category_create_valid.model_dump())
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data, dict)
    validated_category = CategoryResponse.model_validate(data)
    db_category = await test_async_session.get(Category, validated_category.id)
    assert db_category is not None
    assert_category_equal(validated_category, db_category)
    assert db_category.title == schema_category_create_valid.title
    assert db_category.description == schema_category_create_valid.description
    

async def test_create_returns_exists_by_title(client: AsyncClient, schema_category_create_valid, create_category):
    category_title = create_category.title
    schema_category_create_valid.title = category_title
    response = await client.post("/api/v1/categories", json=schema_category_create_valid.model_dump())
    assert response.status_code == 400
    data = response.json()
    assert f"Категория с названием {category_title} уже есть в системе" in data["detail"]


async def test_create_returns_not_valid_schema(client: AsyncClient, schema_category_create_not_valid):
    response = await client.post("/api/v1/categories", json=schema_category_create_not_valid)
    assert response.status_code == 422


async def test_update_returns_success(client: AsyncClient, create_category, 
                                      schema_category_update_valid, test_async_session):
    category_id = create_category.id
    response = await client.patch(f"/api/v1/categories/{category_id}", json=schema_category_update_valid.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    validated_category = CategoryResponse.model_validate(data)
    db_product = await test_async_session.get(Category, category_id)
    assert_category_equal(validated_category, db_product)
    for field, value in schema_category_update_valid.model_dump().items():
        if value is not None:
            assert getattr(db_product, field) == value


async def test_update_returns_not_valid(client: AsyncClient, schema_category_update_not_valid):
    response = await client.patch("/api/v1/categories/1", json=schema_category_update_not_valid)
    assert response.status_code == 422


async def test_update_returns_not_found(client: AsyncClient, schema_category_update_valid):
    category_id = 99
    response = await client.patch(f"/api/v1/categories/{category_id}", json=schema_category_update_valid.model_dump())
    assert response.status_code == 404
    data = response.json()
    assert f"Категория с ID: {category_id} не найдена" in data["detail"]


async def test_update_returns_exists_by_title(client: AsyncClient, schema_category_update_valid, create_category):
    category_title = create_category.title
    schema_category_update_valid.title = category_title
    category_id = create_category.id
    response = await client.patch(f"/api/v1/categories/{category_id}", json=schema_category_update_valid.model_dump())
    assert response.status_code == 400
    data = response.json()
    assert f"Категория с названием {category_title} уже есть в системе" in data["detail"]
    

async def test_delete_returns_success(client: AsyncClient, create_category, test_async_session):
    category_id = create_category.id
    response = await client.delete(f"/api/v1/categories/{category_id}")
    assert response.status_code == 204
    db_category = await test_async_session.get(Category, category_id)
    assert db_category is None


async def test_delete_returns_not_found(client: AsyncClient):
    category_id = 99
    response = await client.delete(f"/api/v1/categories/{category_id}")
    assert response.status_code == 404
    data = response.json()
    assert f"Категория с ID: {category_id} не найдена" in data["detail"]
    

async def test_delete_returns_has_products(client: AsyncClient, create_category_with_products):
    category_id = create_category_with_products.id
    response = await client.delete(f"/api/v1/categories/{category_id}")
    assert response.status_code == 400
    data = response.json()
    assert f"Нельзя удалить категорию с ID: {category_id}, т.к у нее есть товары" in data["detail"]