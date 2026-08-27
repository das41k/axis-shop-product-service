import pytest
from pydantic import ValidationError
from app.schemas.product import ProductCreate, ProductUpdate

valid_data = [
    {"title": "Вилка", "description": "Очень удобная", "price": 100 ,"quantity": 3, "category_id": 1},
    {"title": "Вилка", "price": 100 ,"quantity": 3, "category_id": 1},
]

# ============ НЕВАЛИДНЫЕ ДАННЫЕ С ТИПАМИ ОШИБОК ============

not_valid_title = [
    ({"title": None, "price": 100 ,"quantity": 3, "category_id": 1}, "string_type"),
    ({"title": "    ", "price": 100 ,"quantity": 3, "category_id": 1}, "string_too_short"),
    ({"title": "a" * 31, "price": 100 ,"quantity": 3, "category_id": 1}, "string_too_long")
]

not_valid_desc = [
    ({"title": "Вилка", "description": "   ", "price": 100 ,"quantity": 3, "category_id": 1}, "string_too_short"),
    ({"title": "Вилка", "description": "a" * 101, "price": 100 ,"quantity": 3, "category_id": 1}, "string_too_long")
]

not_valid_price = [
    ({"title": "Вилка", "price": None ,"quantity": 3, "category_id": 1}, "float_type"),
    ({"title": "Вилка", "price": "string" ,"quantity": 3, "category_id": 1}, "float_parsing"),
    ({"title": "Вилка", "price": 0, "quantity": 3, "category_id": 1}, "greater_than"),
    ({"title": "Вилка", "price": -5, "quantity": 3, "category_id": 1}, "greater_than")
]

not_valid_quantity = [
    ({"title": "Вилка", "price": 100, "quantity": None, "category_id": 1}, "int_type"),
    ({"title": "Вилка", "price": 100, "quantity": "string", "category_id": 1}, "int_parsing"),
    ({"title": "Вилка", "price": 100, "quantity": -5, "category_id": 1}, "greater_than_equal"),
]

not_valid_category_id = [
    ({"title": "Вилка", "price": 100, "quantity": 3, "category_id": None}, "int_type"),
    ({"title": "Вилка", "price": 100, "quantity": 3, "category_id": "string"}, "int_parsing"),
    ({"title": "Вилка", "price": 100, "quantity": 3, "category_id": 0}, "greater_than"),
    ({"title": "Вилка", "price": 100, "quantity": 3, "category_id": -5}, "greater_than"),
    ({"title": "Вилка", "price": 100, "quantity": 3, "category_id": 5.7}, "int_from_float")
]

# ============ ТЕСТЫ ДЛЯ ProductCreate ============

@pytest.mark.parametrize("data", valid_data)
def test_valid_creation(data: dict):
    product = ProductCreate(**data)
    
    assert product.title == data["title"]
    assert product.price == data["price"]
    assert product.quantity == data["quantity"]
    assert product.category_id == data["category_id"]
    
    if "description" in data:
        assert product.description == data["description"]
    else:
        assert product.description is None


@pytest.mark.parametrize("data, expected_type", not_valid_title)
def test_not_valid_title_creation(data: dict, expected_type: str):
    with pytest.raises(ValidationError) as ex:
        ProductCreate(**data)
    
    errors = ex.value.errors()
    assert len(errors) >= 1
    assert errors[0]["loc"][0] == "title"
    assert errors[0]["type"] == expected_type


@pytest.mark.parametrize("data, expected_type", not_valid_desc)
def test_not_valid_desc_creation(data: dict, expected_type: str):
    with pytest.raises(ValidationError) as ex:
        ProductCreate(**data)
        
    errors = ex.value.errors()
    assert len(errors) >= 1
    assert errors[0]["loc"][0] == "description"
    assert errors[0]["type"] == expected_type
    

@pytest.mark.parametrize("data, expected_type", not_valid_price)
def test_not_valid_price_creation(data: dict, expected_type: str):
    with pytest.raises(ValidationError) as ex:
        ProductCreate(**data)
    
    errors = ex.value.errors()
    assert len(errors) >= 1
    assert errors[0]["loc"][0] == "price"
    assert errors[0]["type"] == expected_type
    

@pytest.mark.parametrize("data, expected_type", not_valid_quantity)
def test_not_valid_quantity_creation(data: dict, expected_type: str):
    with pytest.raises(ValidationError) as ex:
        ProductCreate(**data)
        
    errors = ex.value.errors()
    assert len(errors) >= 1
    assert errors[0]["loc"][0] == "quantity"
    assert errors[0]["type"] == expected_type


@pytest.mark.parametrize("data, expected_type", not_valid_category_id)
def test_not_valid_category_id_creation(data: dict, expected_type: str):
    with pytest.raises(ValidationError) as ex:
        ProductCreate(**data)
        
    errors = ex.value.errors()
    assert len(errors) >= 1
    assert errors[0]["loc"][0] == "category_id"
    assert errors[0]["type"] == expected_type

# ============ ТЕСТЫ ДЛЯ ProductUpdate ============

@pytest.mark.parametrize("data", valid_data + [
    {"title": "Новая вилка"},
    {"price": 200.50},
    {"quantity": 10},
    {"category_id": 5},
    {"description": "Новое описание"},
    {},
    {"title": "Вилка", "price": 150.75},
    {"quantity": 7, "category_id": 3},
])
def test_valid_updation(data: dict):
    product = ProductUpdate(**data)
    
    for field_name in ProductUpdate.model_fields.keys():
            if field_name in data:
                assert getattr(product, field_name) == data[field_name]
            else:
                assert getattr(product, field_name) is None


@pytest.mark.parametrize("data, expected_type", not_valid_title[1:])
def test_not_valid_title_updation(data: dict, expected_type: str):
    with pytest.raises(ValidationError) as ex:
        ProductUpdate(**data)
    
    errors = ex.value.errors()
    assert len(errors) >= 1
    assert errors[0]["loc"][0] == "title"
    assert errors[0]["type"] == expected_type
 

@pytest.mark.parametrize("data, expected_type", not_valid_desc[1:])
def test_not_valid_desc_updation(data: dict, expected_type: str):
    with pytest.raises(ValidationError) as ex:
        ProductUpdate(**data)
        
    errors = ex.value.errors()
    assert len(errors) >= 1
    assert errors[0]["loc"][0] == "description"
    assert errors[0]["type"] == expected_type
 

@pytest.mark.parametrize("data, expected_type", not_valid_price[1:])
def test_not_valid_price_updation(data: dict, expected_type: str):
    with pytest.raises(ValidationError) as ex:
        ProductUpdate(**data)
    
    errors = ex.value.errors()
    assert len(errors) >= 1
    assert errors[0]["loc"][0] == "price"
    assert errors[0]["type"] == expected_type
    

@pytest.mark.parametrize("data, expected_type", not_valid_quantity[1:])
def test_not_valid_quantity_updation(data: dict, expected_type: str):
    with pytest.raises(ValidationError) as ex:
        ProductUpdate(**data)
        
    errors = ex.value.errors()
    assert len(errors) >= 1
    assert errors[0]["loc"][0] == "quantity"
    assert errors[0]["type"] == expected_type


@pytest.mark.parametrize("data, expected_type", not_valid_category_id[1:])
def test_not_valid_category_id_updation(data: dict, expected_type: str):
    with pytest.raises(ValidationError) as ex:
        ProductUpdate(**data)
        
    errors = ex.value.errors()
    assert len(errors) >= 1
    assert errors[0]["loc"][0] == "category_id"
    assert errors[0]["type"] == expected_type