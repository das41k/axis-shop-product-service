from pydantic import ValidationError
import pytest
from app.schemas.category import CategoryCreate, CategoryUpdate

# ============ ВАЛИДНЫЕ ДАННЫЕ ============

valid_data = [
    {"title": "Спальня", "description": "Очень удобные спальные товары"},
    {"title": "Спальня"}
]

# ============ НЕВАЛИДНЫЕ ДАННЫЕ С ТИПАМИ ОШИБОК ============

not_valid_title = [
    ({"title": None}, "string_type"),
    ({"title": "    "}, "string_too_short"),
    ({"title": "a" * 31}, "string_too_long")
]

not_valid_desc = [
    ({"title": "Ванная", "description": "     "}, "string_too_short"),
    ({"title": "Ванная", "description": "a" * 101}, "string_too_long")
]

# ============ ТЕСТЫ ДЛЯ CategoryCreate ============

@pytest.mark.parametrize("data", valid_data)
def test_valid_creation(data: dict):
    category = CategoryCreate(**data)
    
    assert category.title == data["title"]
    
    if "description" in data:
        assert category.description == data["description"]
    else:
        assert category.description is None


@pytest.mark.parametrize("data, expected_type", not_valid_title)
def test_not_valid_title_creation(data: dict, expected_type: str):
    with pytest.raises(ValidationError) as ex:
        CategoryCreate(**data)
    
    errors = ex.value.errors()
    assert len(errors) >= 1
    assert errors[0]["loc"][0] == "title"
    assert errors[0]["type"] == expected_type


@pytest.mark.parametrize("data, expected_type", not_valid_desc)
def test_not_valid_desc_creation(data: dict, expected_type: str):
    with pytest.raises(ValidationError) as ex:
        CategoryCreate(**data)
    
    errors = ex.value.errors()
    assert len(errors) >= 1
    assert errors[0]["loc"][0] == "description"
    assert errors[0]["type"] == expected_type

# ============ ТЕСТЫ ДЛЯ CategoryUpdate ============

@pytest.mark.parametrize("data", valid_data + [
    {"description": "Очень удобные спальные товары"},
    {"title": "Гостиная"},
    {"title": "Кухня", "description": "Все для кухни"},
    {},
])
def test_valid_updation(data: dict):
    category = CategoryUpdate(**data)
    
    for field_name in CategoryUpdate.model_fields.keys():
        if field_name in data:
            assert getattr(category, field_name) == data[field_name]
        else:
            assert getattr(category, field_name) is None


@pytest.mark.parametrize("data, expected_type", not_valid_title[1:])
def test_not_valid_title_updation(data: dict, expected_type: str):
    with pytest.raises(ValidationError) as ex:
        CategoryUpdate(**data)
    
    errors = ex.value.errors()
    assert len(errors) >= 1
    assert errors[0]["loc"][0] == "title"
    assert errors[0]["type"] == expected_type


@pytest.mark.parametrize("data, expected_type", not_valid_desc)
def test_not_valid_desc_updation(data: dict, expected_type: str):
    with pytest.raises(ValidationError) as ex:
        CategoryUpdate(**data)
    
    errors = ex.value.errors()
    assert len(errors) >= 1
    assert errors[0]["loc"][0] == "description"
    assert errors[0]["type"] == expected_type