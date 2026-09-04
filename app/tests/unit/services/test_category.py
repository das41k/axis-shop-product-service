import pytest
from pydantic import TypeAdapter
from unittest.mock import call

from app.tests.helpers.assertions import assert_category_equal
from app.schemas.category import CategoryResponse
from app.core.cache.category_keys import CategoryCacheKeys
from app.exceptions.category import CategoryNotFoundException, CategoryIsExistsException, CategoryContainsProductsException

pytestmark = [pytest.mark.unit, pytest.mark.unit_services]

async def test_get_all_valid_from_db(category_service, category_repo, category_redis, category_data_list):
    category_redis.get.return_value = None
    category_repo.get_all.return_value = category_data_list
    
    result: list[CategoryResponse] = await category_service.get_all()
    
    assert len(result) == len(category_data_list)
    
    for schema, model in zip(result, category_data_list):
        assert_category_equal(schema, model)
    
    category_redis.get.assert_called_once_with(CategoryCacheKeys.ALL)
    category_repo.get_all.assert_called_once()
    category_redis.set.assert_called_once()
    
    call_args = category_redis.set.call_args
    assert call_args.args[0] == CategoryCacheKeys.ALL
    saved_cache = call_args.args[1]
    adapter = TypeAdapter(list[CategoryResponse])
    resposed_data = adapter.validate_json(saved_cache)
    for schema, model in zip(resposed_data, category_data_list):
        assert_category_equal(schema, model)

async def test_get_all_valid_from_redis(category_service, category_repo, category_redis, category_data_list):
    adapter = TypeAdapter(list[CategoryResponse])
    response_data = [CategoryResponse.model_validate(c) for c in category_data_list]
    cached_data = adapter.dump_json(response_data)
    category_redis.get.return_value = cached_data
    
    result = await category_service.get_all()
    assert len(result) == len(category_data_list)
    for schema, model in zip(result, category_data_list):
        assert_category_equal(schema, model)

    category_redis.get.assert_called_once_with(CategoryCacheKeys.ALL)
    category_repo.get_all.assert_not_called()
    
async def test_get_by_id_valid_from_db(category_service, category_repo, category_redis, category_data):
    category_redis.get.return_value = None
    category_repo.get_by_id.return_value = category_data
    
    result = await category_service.get_by_id(category_data.id)
    
    assert result is not None
    assert_category_equal(result, category_data)
    
    category_id = category_data.id
    category_redis.get.assert_called_once_with(CategoryCacheKeys.category_by_id(category_id))
    category_repo.get_by_id.assert_called_once_with(category_data.id)
    category_redis.set.assert_called_once()
    
    call_args = category_redis.set.call_args
    assert call_args.args[0] == CategoryCacheKeys.category_by_id(category_id)
    saved_cache = call_args.args[1]
    adapter = TypeAdapter(CategoryResponse)
    responsed_data = adapter.validate_json(saved_cache)
    assert_category_equal(responsed_data, category_data)
    
async def test_get_by_id_valid_from_redis(category_service, category_redis, category_repo, category_data):
    adapter = TypeAdapter(CategoryResponse)
    response_data = CategoryResponse.model_validate(category_data)
    cached_data = adapter.dump_json(response_data)
    category_redis.get.return_value = cached_data
    
    category_id = category_data.id
    result = await category_service.get_by_id(category_id)
    
    assert result is not None
    assert_category_equal(result, category_data)
    
    category_redis.get.assert_called_once_with(CategoryCacheKeys.category_by_id(category_id))
    category_repo.get_by_id.assert_not_called()
    category_redis.set.assert_not_called()

async def test_not_found_get_by_id(category_service, category_repo, category_redis):
    category_redis.get.return_value = None
    category_repo.get_by_id.return_value = None
    category_id = 99
    
    with pytest.raises(CategoryNotFoundException) as ex:
        await category_service.get_by_id(category_id)
    
    assert f"Категория с ID: {category_id} не найдена" in str(ex.value)
    category_redis.get.assert_called_once_with(CategoryCacheKeys.category_by_id(category_id))
    category_repo.get_by_id.assert_called_once_with(category_id)
    category_redis.set.assert_not_called()

async def test_valid_create(category_service, category_repo, category_redis, category_data, category_for_create_data):
    category_repo.exists_by_title.return_value = False
    category_repo.create.return_value = category_data

    result = await category_service.create(category_for_create_data)
    
    assert result is not None
    assert_category_equal(result, category_data)
    
    category_repo.exists_by_title.assert_called_once_with(category_for_create_data.title)
    category_repo.create.assert_called_once_with(category_for_create_data.model_dump())
    category_redis.delete.assert_called_once_with(CategoryCacheKeys.ALL)

async def test_title_exists_create(category_service, category_repo, category_redis, category_for_create_data):
    category_repo.exists_by_title.return_value = True
    category_title = category_for_create_data.title
    
    with pytest.raises(CategoryIsExistsException) as ex:
        await category_service.create(category_for_create_data)
        
    assert f"Категория с названием {category_title} уже есть в системе" in str(ex.value)
    category_repo.exists_by_title.assert_called_once_with(category_title)
    category_repo.update.assert_not_called()
    category_redis.delete.assert_not_called()

async def test_valid_update(category_service, category_repo, category_redis, category_data, category_for_update_data, category_updated_data):
    category_repo.get_by_id.return_value = category_data
    category_repo.exists_by_title.return_value = False
    category_repo.update.return_value = category_updated_data
    
    result = await category_service.update(category_data.id, category_for_update_data)
    
    assert result is not None
    assert category_data.id == category_updated_data.id
    assert_category_equal(result, category_updated_data)
    
    category_repo.get_by_id.assert_called_once_with(category_data.id)
    category_repo.exists_by_title.assert_called_once_with(category_for_update_data.title)
    category_repo.update.assert_called_once_with(category_data, category_for_update_data.model_dump())
    expected_calls = [
            call(CategoryCacheKeys.category_by_id(category_data.id)),
            call(CategoryCacheKeys.ALL)
        ]
    category_redis.delete.assert_has_calls(expected_calls, any_order=True)

async def test_not_found_update(category_service, category_repo, category_redis, category_for_update_data):
    category_repo.get_by_id.return_value = None
    category_id = 99
    
    with pytest.raises(CategoryNotFoundException) as ex:
        await category_service.update(category_id, category_for_update_data)
    
    assert f"Категория с ID: {category_id} не найдена" in str(ex.value)
    
    category_repo.get_by_id.assert_called_once_with(category_id)
    category_repo.exists_by_title.assert_not_called()
    category_repo.update.assert_not_called()
    category_redis.delete.assert_not_called()
    

async def test_title_exists_update(category_service, category_repo, category_redis, category_for_update_data, category_data):
    category_repo.get_by_id.return_value = category_data
    category_repo.exists_by_title.return_value = True
    category_title = category_for_update_data.title
    
    with pytest.raises(CategoryIsExistsException) as ex:
        await category_service.update(category_data.id, category_for_update_data)
        
    assert f"Категория с названием {category_title} уже есть в системе" in str(ex.value)
    
    category_repo.get_by_id.assert_called_once_with(category_data.id)
    category_repo.exists_by_title.assert_called_once_with(category_title)
    category_repo.update.assert_not_called()
    category_redis.delete.assert_not_called()
    

async def test_valid_delete(category_service, category_repo, category_redis, category_data):
    category_repo.has_products.return_value = False
    category_repo.delete_by_id.return_value = True
    
    await category_service.delete_by_id(category_data.id)
    
    category_repo.has_products.assert_called_once_with(category_data.id)
    category_repo.delete_by_id.assert_called_once_with(category_data.id)
    expected_calls = [
            call(CategoryCacheKeys.category_by_id(category_data.id)),
            call(CategoryCacheKeys.ALL)
        ]
    category_redis.delete.assert_has_calls(expected_calls, any_order=True)
    

async def test_has_products_delete(category_service, category_repo, category_redis):
    category_repo.has_products.return_value = True
    category_id = 99
    
    with pytest.raises(CategoryContainsProductsException) as ex:
        await category_service.delete_by_id(category_id)
    
    assert f"Нельзя удалить категорию с ID: {category_id}, т.к у нее есть товары" in str(ex.value)
    
    category_repo.has_products.assert_called_once_with(category_id)
    category_repo.delete_by_id.assert_not_called()
    category_redis.delete.assert_not_called()
    

async def test_not_found_delete(category_service, category_repo, category_redis):
    category_repo.has_products.return_value = False
    category_id = 99
    category_repo.delete_by_id.return_value = False
    
    with pytest.raises(CategoryNotFoundException) as ex:
        await category_service.delete_by_id(category_id)
        
    assert f"Категория с ID: {category_id} не найдена" in str(ex.value)
    
    category_repo.delete_by_id.assert_called_once_with(category_id)
    category_redis.delete.assert_not_called()