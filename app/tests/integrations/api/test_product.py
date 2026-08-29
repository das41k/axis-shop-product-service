import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_all_valid(client: AsyncClient):
    response = await client.get("/api/v1/products")
    print(response.status_code)
    print(response.json())
    print(response.request.url)