import pytest
from unittest.mock import AsyncMock
from httpx import AsyncClient
from sqlalchemy import select
from fastapi import FastAPI
from redis.asyncio import Redis
from pydantic import TypeAdapter, Field
from typing import Annotated
from app.dependencies import get_category_repository
from app.tests.helpers.assertions import assert_category_equal
from app.models.category import Category
from app.schemas.category import CategoryResponse
from app.core.cache.category_keys import CategoryCacheKeys

pytestmark = [pytest.mark.integration, pytest.mark.api]

async def test_get_all_returns_created_categories(client: AsyncClient, create_categories, test_redis: Redis):
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
    
    cached_data = await test_redis.get(CategoryCacheKeys.ALL)
    assert cached_data is not None
    adapter = TypeAdapter(list[CategoryResponse])
    response_data_with_cache = adapter.validate_json(cached_data)
    sorted_response_data_with_cache = sorted(response_data_with_cache, key=lambda category : category.id)
    for schema, model in zip(sorted_response_data_with_cache, sorted_fixture):
        assert_category_equal(schema, model)

async def test_get_all_returns_empty_list(client: AsyncClient, test_async_session, test_redis: Redis):
    response = await client.get("/api/v1/categories")
    assert response.status_code == 200
    data = response.json()
    assert data == []
    
    query_from_db = await test_async_session.execute(
            select(Category)
        )
    result = query_from_db.scalars().all()
    assert result == []
    
    cached_data = await test_redis.get(CategoryCacheKeys.ALL)
    assert cached_data is not None
    adapter = TypeAdapter(Annotated[list, Field(max_length=0)])
    assert adapter.validate_json(cached_data) == []

async def test_get_all_cache_hit_skip_db(
    client: AsyncClient,
    app: FastAPI,
    create_categories,
    test_redis: Redis,
    category_repo: AsyncMock
):
    def override_get_category_repository():
        return category_repo
    app.dependency_overrides[get_category_repository] = override_get_category_repository
    
    category_repo.get_all.return_value = create_categories
    responseForDb = await client.get("/api/v1/categories")
    print("RESPONSE BODY:", responseForDb.json()) 
    assert responseForDb.status_code == 200
    category_repo.get_all.assert_called_once()
    category_repo.reset_mock()
    
    cached_data = test_redis.get(CategoryCacheKeys.ALL)
    assert cached_data is not None
    
    responseForRedis = await client.get("/api/v1/categories")
    assert responseForRedis.status_code == 200
    category_repo.get_all.assert_not_called()
    
    assert responseForDb.json() == responseForRedis.json()
    

async def test_get_by_id_returns_success(client: AsyncClient, create_category, test_redis: Redis):
    category_id = create_category.id
    response = await client.get(f"/api/v1/categories/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    validated_category = CategoryResponse.model_validate(data)
    assert_category_equal(validated_category, create_category)
    
    cached_data = await test_redis.get(CategoryCacheKeys.category_by_id(category_id))
    assert cached_data is not None
    adapter = TypeAdapter(CategoryResponse)
    response_data_with_cache = adapter.validate_json(cached_data)
    assert_category_equal(response_data_with_cache, create_category)


async def test_get_by_id_returns_not_found(client: AsyncClient):
    category_id = 4
    response = await client.get(f"/api/v1/categories/{category_id}")
    assert response.status_code == 404
    data = response.json()
    assert f"Категория с ID: {category_id} не найдена" in data["detail"]
    

async def test_create_returns_success(client: AsyncClient, schema_category_create_valid, test_async_session, test_redis):
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
    
    cached_data = await test_redis.get(CategoryCacheKeys.ALL)
    assert cached_data is None
    

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
                                      schema_category_update_valid, test_async_session, test_redis: Redis):
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
    
    cached_data_all = await test_redis.get(CategoryCacheKeys.ALL)
    cached_data_category = await test_redis.get(CategoryCacheKeys.category_by_id(category_id))
    assert cached_data_all is None and cached_data_category is None


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
    

async def test_delete_returns_success(client: AsyncClient, create_category, test_async_session, test_redis: Redis):
    category_id = create_category.id
    response = await client.delete(f"/api/v1/categories/{category_id}")
    assert response.status_code == 204
    db_category = await test_async_session.get(Category, category_id)
    assert db_category is None
    
    cached_data_all = await test_redis.get(CategoryCacheKeys.ALL)
    cached_data_category = await test_redis.get(CategoryCacheKeys.category_by_id(category_id))
    assert cached_data_all is None and cached_data_category is None


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