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

async def test_get_all(product_service, product_repo, get_list_product):
    products = get_list_product
        
    product_repo.get_all.return_value = products
        
    result: list[ProductResponse] = await product_service.get_all()
        
    assert len(result) > 0
        
    for schema, model in zip(result, products):
        assert_product_equal(schema, model)
            
    product_repo.get_all.assert_called_once()
        
    
async def test_valid_get_by_id(product_service, product_repo, get_product):
    
    product_repo.get_by_id.return_value = get_product
        
    result = await product_service.get_by_id(get_product.id)
        
    assert result is not None
    assert_product_equal(result, get_product)
        
    product_repo.get_by_id.assert_called_once_with(get_product.id)

       
async def test_not_found_get_by_id(product_service, product_repo):
    product_id = 33
    product_repo.get_by_id.return_value = None
    
    with pytest.raises(ProductNotFoundException) as ex:
        await product_service.get_by_id(product_id)
    
    assert f"Продукт с ID: {product_id} не найден" in str(ex.value)
    
    product_repo.get_by_id.assert_called_once_with(product_id)


async def test_valid_create(product_service, product_repo, category_repo, get_product, product_for_create_data):
    category_repo.get_by_id.return_value = Category(id=1, title="Кухня")
    product_repo.create.return_value = get_product
    
    result = await product_service.create(product_for_create_data)
    
    assert result is not None
    assert_product_equal(result, get_product)
    
    
    category_repo.get_by_id.assert_called_once_with(product_for_create_data.category_id)
    product_repo.create.assert_called_once_with(product_for_create_data.model_dump())
    

async def test_not_found_category_create(product_service, product_repo, category_repo, product_for_create_data):
    category_repo.get_by_id.return_value = None
    
    category_id = product_for_create_data.category_id
    
    with pytest.raises(CategoryNotFoundException) as ex:
        await product_service.create(product_for_create_data)
    
    assert f"Категория с ID: {category_id} не найдена" in str(ex.value)
    
    category_repo.get_by_id.assert_called_once_with(category_id)
    product_repo.create.assert_not_called()
    

async def test_valid_update(product_service, product_repo, category_repo, get_product, product_for_update_data, product_updated_data):
    product_repo.get_by_id.return_value = get_product
    category_repo.get_by_id.return_value = get_product.category
    product_repo.update.return_value = product_updated_data
    
    result = await product_service.update(get_product.id, product_for_update_data)
    
    assert result is not None
    assert get_product.id == product_updated_data.id     
    assert_product_equal(result, product_updated_data)
    
    product_repo.get_by_id.assert_called_once_with(get_product.id)
    category_repo.get_by_id.assert_called_once_with(product_for_update_data.category_id)
    product_repo.update.assert_called_once_with(get_product, product_for_update_data.model_dump())

async def test_not_found_category_update(product_service, product_repo, category_repo, product_for_update_data, get_product):
    product_repo.get_by_id.return_value = get_product
    category_repo.get_by_id.return_value = None
    
    category_id = product_for_update_data.category_id
    
    with pytest.raises(CategoryNotFoundException) as ex:
        await product_service.update(get_product.id, product_for_update_data)
    
    assert f"Категория с ID: {category_id} не найдена" in str(ex.value)
    
    product_repo.get_by_id.assert_called_once_with(get_product.id)
    category_repo.get_by_id.assert_called_once_with(category_id)
    product_repo.update.assert_not_called()
       
 
async def test_not_found_product_update(product_service, product_repo, category_repo, product_for_update_data):
    product_repo.get_by_id.return_value = None
    product_id = 1
    
    with pytest.raises(ProductNotFoundException) as ex:
        await product_service.update(product_id, product_for_update_data)
    
    assert f"Продукт с ID: {product_id} не найден" in str(ex.value)
    
    product_repo.get_by_id.assert_called_once_with(product_id)
    category_repo.get_by_id.assert_not_called()
    product_repo.update.assert_not_called()
        
    
async def test_valid_delete(product_service, product_repo, get_product):
    product_repo.delete_by_id.return_value = True
    
    await product_service.delete(get_product.id)
    
    product_repo.delete_by_id.assert_called_once_with(get_product.id)
    

async def test_not_found_product_delete(product_service, product_repo):
    product_repo.delete_by_id.return_value = False
    product_id = 99
    
    with pytest.raises(ProductNotFoundException) as ex:
        await product_service.delete(product_id)
    
    assert f"Продукт с ID: {product_id} не найден" in str(ex.value)
    product_repo.delete_by_id.assert_called_once_with(product_id)