import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.tests.helpers.assertions import assert_category_equal
from app.repository.base import AbstractCategoryRepository
from app.services.category import CategoryService
from app.schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate
from app.models.category import Category
from app.exceptions.category import CategoryNotFoundException, CategoryIsExistsException, CategoryContainsProductsException

@pytest.fixture
def category_repo(mocker):
    return mocker.AsyncMock(autospec = AbstractCategoryRepository)

@pytest.fixture
def category_service(category_repo: AsyncMock) -> CategoryService:
    return CategoryService(category_repo)

@pytest.fixture
def category_base_data():
    return {
        "title": "Кухня",
        "description": "Товары для кухни, выбирай что хочешь"
    }

@pytest.fixture
def category_data(category_base_data):
    
    fixed_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    return Category(
        id = 1,
        **category_base_data,
        created_at = fixed_time,
        updated_at = fixed_time
    )

@pytest.fixture
def category_data_list():
    fixed_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    return [
        Category(id = 1, title = "Кухня", description = "Товары для кухни, выбирай что хочешь",
                 created_at = fixed_time, updated_at = fixed_time),
        Category(id = 2, title = "Ванная", description = "Товары для ванны",
                 created_at = fixed_time, updated_at = fixed_time),
        Category(id = 3, title = "Спальня", description = "Товары для спальни",
                 created_at = fixed_time, updated_at = fixed_time)
    ]

@pytest.fixture
def category_for_create_data(category_base_data):
    return CategoryCreate(**category_base_data)

@pytest.fixture
def category_for_update_data(category_base_data):
    return CategoryUpdate(**category_base_data)

@pytest.fixture
def category_updated_data(category_data) -> Category:
    category_data.title = "Спальня"
    category_data.description = None
    return category_data

@pytest.mark.asyncio
async def test_get_all_valid(category_service, category_repo, category_data_list):
    category_repo.get_all.return_value = category_data_list
    
    result: list[CategoryResponse] = await category_service.get_all()
    
    assert len(result) > 0
    
    for schema, model in zip(result, category_data_list):
        assert_category_equal(schema, model)
        
    category_repo.get_all.assert_called_once()
    
@pytest.mark.asyncio
async def test_get_by_id_valid(category_service, category_repo, category_data):
    category_repo.get_by_id.return_value = category_data
    
    result = await category_service.get_by_id(category_data.id)
    
    assert result is not None
    assert_category_equal(result, category_data)
    
    category_repo.get_by_id.assert_called_once_with(category_data.id)
    
@pytest.mark.asyncio
async def test_not_found_get_by_id(category_service, category_repo):
    category_repo.get_by_id.return_value = None
    category_id = 99
    
    with pytest.raises(CategoryNotFoundException) as ex:
        await category_service.get_by_id(category_id)
    
    assert f"Категория с ID: {category_id} не найдена" in str(ex.value)
    category_repo.get_by_id.assert_called_once_with(category_id)
    
@pytest.mark.asyncio
async def test_valid_create(category_service, category_repo, category_data, category_for_create_data):
    category_repo.exists_by_title.return_value = False
    category_repo.create.return_value = category_data

    result = await category_service.create(category_for_create_data)
    
    assert result is not None
    assert_category_equal(result, category_data)
    
    category_repo.exists_by_title.assert_called_once_with(category_for_create_data.title)
    category_repo.create.assert_called_once_with(category_for_create_data.model_dump())

@pytest.mark.asyncio
async def test_title_exists_create(category_service, category_repo, category_for_create_data):
    category_repo.exists_by_title.return_value = True
    category_title = category_for_create_data.title
    
    with pytest.raises(CategoryIsExistsException) as ex:
        await category_service.create(category_for_create_data)
        
    assert f"Категория с названием {category_title} уже есть в системе" in str(ex.value)
    category_repo.exists_by_title.assert_called_once_with(category_title)
    category_repo.update.assert_not_called()
    
@pytest.mark.asyncio
async def test_valid_update(category_service, category_repo, category_data, category_for_update_data, category_updated_data):
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
    
@pytest.mark.asyncio
async def test_not_found_update(category_service, category_repo, category_for_update_data):
    category_repo.get_by_id.return_value = None
    category_id = 99
    
    with pytest.raises(CategoryNotFoundException) as ex:
        await category_service.update(category_id, category_for_update_data)
    
    assert f"Категория с ID: {category_id} не найдена" in str(ex.value)
    
    category_repo.get_by_id.assert_called_once_with(category_id)
    category_repo.exists_by_title.assert_not_called()
    category_repo.update.assert_not_called()
    
@pytest.mark.asyncio
async def test_title_exists_update(category_service, category_repo, category_for_update_data, category_data):
    category_repo.get_by_id.return_value = category_data
    category_repo.exists_by_title.return_value = True
    category_title = category_for_update_data.title
    
    with pytest.raises(CategoryIsExistsException) as ex:
        await category_service.update(category_data.id, category_for_update_data)
        
    assert f"Категория с названием {category_title} уже есть в системе" in str(ex.value)
    
    category_repo.get_by_id.assert_called_once_with(category_data.id)
    category_repo.exists_by_title.assert_called_once_with(category_title)
    category_repo.update.assert_not_called()
    
@pytest.mark.asyncio
async def test_valid_delete(category_service, category_repo, category_data):
    category_repo.has_products.return_value = False
    category_repo.delete_by_id.return_value = True
    
    await category_service.delete_by_id(category_data.id)
    
    category_repo.has_products.assert_called_once_with(category_data.id)
    category_repo.delete_by_id.assert_called_once_with(category_data.id)
    
@pytest.mark.asyncio
async def test_has_products_delete(category_service, category_repo):
    category_repo.has_products.return_value = True
    category_id = 99
    
    with pytest.raises(CategoryContainsProductsException) as ex:
        await category_service.delete_by_id(category_id)
    
    assert f"Нельзя удалить категорию с ID: {category_id}, т.к у нее есть товары" in str(ex.value)
    
    category_repo.has_products.assert_called_once_with(category_id)
    category_repo.delete_by_id.assert_not_called()
    
@pytest.mark.asyncio
async def test_not_found_delete(category_service, category_repo):
    category_repo.has_products.return_value = False
    category_id = 99
    category_repo.delete_by_id.return_value = False
    
    with pytest.raises(CategoryNotFoundException) as ex:
        await category_service.delete_by_id(category_id)
        
    assert f"Категория с ID: {category_id} не найдена" in str(ex.value)
    
    category_repo.delete_by_id.assert_called_once_with(category_id)