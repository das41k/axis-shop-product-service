import pytest
from unittest.mock import AsyncMock
import uuid
from datetime import timezone, datetime
from app.services.product import ProductService
from app.repository.base import AbstractRepository
from app.models.product import Product
from app.exceptions.product import ProductNotFoundException
from app.exceptions.category import CategoryNotFoundException
from app.models.category import Category
from app.models.category import Category
from app.schemas.product import ProductResponse, ProductCreate, ProductUpdate
from app.tests.helpers.assertions import assert_product_equal

@pytest.fixture
def product_repo(mocker):
    return mocker.AsyncMock(autospec=AbstractRepository[Product])
    
@pytest.fixture
def category_repo(mocker):
    return mocker.AsyncMock(autospec=AbstractRepository[Category])
    
@pytest.fixture
def product_service(product_repo: AsyncMock, category_repo: AsyncMock):
    return ProductService(product_repo, category_repo)

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
    category = Category(id = 1, title = "Кухня")
    fixed_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    return Product(
        id = 1,
        **product_base_data,
        sku = "TEST1234",
        category = category,
        created_at=fixed_time,
        updated_at=fixed_time 
    )

@pytest.fixture
def product_create_data(product_base_data):
    return ProductCreate(**product_base_data)

@pytest.fixture
def product_update_data(product_base_data):
    return ProductUpdate(**product_base_data)

@pytest.fixture
def get_list_product():
    category = Category(id = 1, title="Кухня")
            
    products = [
            Product(id = 1, title = "Вилка", description = "Очень удобная", 
                        sku = uuid.uuid4().hex[:8].upper(), price = 100, quantity = 3, category_id = 1, category = category,
                        created_at = datetime.now(timezone.utc), updated_at = datetime.now(timezone.utc)),
            Product(id = 2, title = "Ложка", description = "Очень красивая", 
                                    sku = uuid.uuid4().hex[:8].upper(), price = 200, quantity = 3, category_id = 1, category = category,
                                    created_at = datetime.now(timezone.utc), updated_at = datetime.now(timezone.utc)),
            Product(id = 3, title = "Тарелка", description = "Очень красивая",  category = category,
                                                sku = uuid.uuid4().hex[:8].upper(), price = 300, quantity = 4, category_id = 1,
                                                created_at = datetime.now(timezone.utc), updated_at = datetime.now(timezone.utc))
        ]
    return products


@pytest.mark.asyncio
async def test_get_all(product_service, product_repo, get_list_product):
    products = get_list_product
        
    product_repo.get_all.return_value = products
        
    result: list[ProductResponse] = await product_service.get_all()
        
    assert len(result) > 0
        
    for schema, model in zip(result, products):
        assert_product_equal(schema, model)
            
    product_repo.get_all.assert_called_once()
        
    
@pytest.mark.asyncio
async def test_valid_get_by_id(product_service, product_repo, get_product):
    
    product_repo.get_by_id.return_value = get_product
        
    result = await product_service.get_by_id(get_product.id)
        
    assert result is not None
    assert_product_equal(result, get_product)
        
    product_repo.get_by_id.assert_called_once_with(get_product.id)

       
@pytest.mark.asyncio
async def test_not_found_get_by_id(product_service, product_repo):
    product_id = 33
    product_repo.get_by_id.return_value = None
    
    with pytest.raises(ProductNotFoundException) as ex:
        await product_service.get_by_id(product_id)
    
    assert f"Продукт с ID: {product_id} не найден" in str(ex.value)
    
    product_repo.get_by_id.assert_called_once_with(product_id)


@pytest.mark.asyncio
async def test_valid_create(product_service, product_repo, category_repo, get_product, product_create_data):
    category_repo.get_by_id.return_value = Category(id=1, title="Кухня")
    product_repo.create.return_value = get_product
    
    result = await product_service.create(product_create_data)
    
    assert result is not None
    assert_product_equal(result, get_product)
    
    
    category_repo.get_by_id.assert_called_once_with(product_create_data.category_id)
    product_repo.create.assert_called_once_with(product_create_data.model_dump())
    
@pytest.mark.asyncio
async def test_not_found_category_create(product_service, product_repo, category_repo, product_create_data):
    category_repo.get_by_id.return_value = None
    
    category_id = product_create_data.category_id
    
    with pytest.raises(CategoryNotFoundException) as ex:
        await product_service.create(product_create_data)
    
    assert f"Категория с ID: {category_id} не найдена" in str(ex.value)
    
    category_repo.get_by_id.assert_called_once_with(category_id)
    product_repo.create.assert_not_called()
    

@pytest.mark.asyncio
async def test_valid_update(product_service, product_repo, category_repo, get_product, product_update_data):
    category_repo.get_by_id.return_value = Category(id=1, title="Кухня")
    product_repo.update.return_value = get_product
    
    result = await product_service.update(get_product.id, product_update_data)
    
    assert result is not None     
    assert_product_equal(result, get_product)
    
    category_repo.get_by_id.assert_called_once_with(product_update_data.category_id)
    product_repo.update.assert_called_once_with(get_product.id, product_update_data.model_dump())

@pytest.mark.asyncio
async def test_not_found_category_update(product_service, product_repo, category_repo, product_update_data):
    category_repo.get_by_id.return_value = None
    
    category_id = product_update_data.category_id
    
    with pytest.raises(CategoryNotFoundException) as ex:
        await product_service.update(1, product_update_data)
    
    assert f"Категория с ID: {category_id} не найдена" in str(ex.value)
    category_repo.get_by_id.assert_called_once_with(category_id)
    product_repo.assert_not_called()
       
 
@pytest.mark.asyncio
async def test_not_found_product_update(product_service, product_repo, category_repo, product_update_data):
    category_repo.get_by_id.return_value = Category(id=1, title="Кухня")
    product_repo.update.return_value = None
    
    product_id = 1
    
    with pytest.raises(ProductNotFoundException) as ex:
        await product_service.update(product_id, product_update_data)
    
    assert f"Продукт с ID: {product_id} не найден" in str(ex.value)
    category_repo.get_by_id.assert_called_once_with(product_update_data.category_id)
    product_repo.update.assert_called_once_with(product_id, product_update_data.model_dump())
        
    
@pytest.mark.asyncio
async def test_valid_delete(product_service, product_repo, get_product):
    product_repo.delete_by_id.return_value = True
    
    await product_service.delete(get_product.id)
    
    product_repo.delete_by_id.assert_called_once_with(get_product.id)
    

@pytest.mark.asyncio
async def test_not_found_product_delete(product_service, product_repo):
    product_repo.delete_by_id.return_value = False
    product_id = 99
    
    with pytest.raises(ProductNotFoundException) as ex:
        await product_service.delete(product_id)
    
    assert f"Продукт с ID: {product_id} не найден" in str(ex.value)
    product_repo.delete_by_id.assert_called_once_with(product_id)