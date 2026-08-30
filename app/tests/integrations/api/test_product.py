import pytest
from httpx import AsyncClient
from sqlalchemy import select
from app.models.product import Product
from app.schemas.product import ProductResponse
from app.tests.helpers.assertions import assert_product_equal

@pytest.mark.asyncio
async def test_get_all_returns_created_products(client: AsyncClient, create_products):
    response = await client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    validated_products = [ProductResponse(**item) for item in data]
    assert len(validated_products) == len(create_products)
    
    sorted_response = sorted(validated_products, key=lambda product: product.id)
    sorted_fixture = sorted(create_products, key = lambda product: product.id)
    
    for schema, model in zip(sorted_response, sorted_fixture):
        assert_product_equal(schema, model)
        
@pytest.mark.asyncio
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