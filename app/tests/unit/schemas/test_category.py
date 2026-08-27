from pydantic import ValidationError
import pytest
from app.schemas.category import CategoryCreate, CategoryUpdate

valid_data = [
    { "title": "Спальня", "description": "Очень удобные спальные товары" },
    { "title": "Спальня"}
]

not_valid_desc_data = [
    ({"title": "Ванная", "description": "     "}, "String should have at least 5 characters"),
    ({"title": "Ванная", "description": "a" * 101}, "String should have at most 100 character")
]

@pytest.mark.parametrize("data", valid_data)
def test_valid_creation(data: dict):
    category = CategoryCreate(**data)
    
    assert category.title == data["title"]
    
    if "description" in data:
        assert category.description == data["description"]
    else:
        assert category.description is None


@pytest.mark.parametrize("data, expected_msg", [
    ({"title": None}, "Input should be a valid string"),
    ({"title": "    "}, "String should have at least 3 characters"),
    ({"title": "a" * 31}, "String should have at most 30 characters")
])     
def test_not_valid_title_creation(data: dict, expected_msg: str):
    with pytest.raises(ValidationError) as ex:
        CategoryCreate(**data)
    errors = ex.value.errors()
    
    assert len(errors) >= 1
    assert errors
    assert errors[0]["loc"][0] == "title"
    assert expected_msg in errors[0]["msg"]

@pytest.mark.parametrize("data, expected_msg", not_valid_desc_data)
def test_not_valid_desc_creation(data: dict, expected_msg: str):
    with pytest.raises(ValidationError) as ex:
        CategoryCreate(**data)
    
    errors = ex.value.errors()
    assert len(errors) >= 1
    assert errors[0]["loc"][0] == "description"
    assert expected_msg in errors[0]["msg"]
    
@pytest.mark.parametrize("data", valid_data + [
    {"description": "Очень удобные спальные товары" }
])
def test_valid_updation(data):
    category = CategoryUpdate(**data)
    
    if "description" in data:
        assert category.description == data["description"]
    else:
        assert category.description is None

@pytest.mark.parametrize("data, expected_msg", [
    ({"title": "    "}, "String should have at least 3 characters"),
    ({"title": "a" * 31}, "String should have at most 30 characters")
])
def test_not_valid_title_updation(data: dict, expected_msg: str):
    with pytest.raises(ValidationError) as ex:
        CategoryUpdate(**data)
        
    errors = ex.value.errors()
    assert len(errors) >= 1
    assert errors[0]["loc"][0] == "title"
    assert expected_msg in errors[0]["msg"]
    
@pytest.mark.parametrize("data, expected_msg", not_valid_desc_data)
def test_not_valid_desc_updation(data: dict, expected_msg: str):
    with pytest.raises(ValidationError) as ex:
        CategoryUpdate(**data)
    
    errors = ex.value.errors()
    assert len(errors) >= 1
    assert errors[0]["loc"][0] == "description"
    assert expected_msg in errors[0]["msg"]