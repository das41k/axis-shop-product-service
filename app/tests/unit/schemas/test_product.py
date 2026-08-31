# tests/unit/schemas/test_product_schema.py
import pytest
from pydantic import ValidationError
from app.schemas.product import ProductCreate, ProductUpdate

# Импорты из новых файлов
from app.tests.data.product_data import (
    VALID_PRODUCT_DATA,
    VALID_PRODUCT_UPDATE_DATA,
    PRODUCT_INVALID_TITLE,
    PRODUCT_INVALID_DESC,
    PRODUCT_INVALID_PRICE,
    PRODUCT_INVALID_QUANTITY,
    PRODUCT_INVALID_CATEGORY_ID
)
from app.tests.helpers.validation_helpers import (
    assert_validation_error,
    assert_valid_model_creation
)

pytestmark = [pytest.mark.unit, pytest.mark.unit_schemas]

# ============ ТЕСТЫ ДЛЯ ProductCreate ============

class TestProductCreate:
    
    @pytest.mark.parametrize("data", VALID_PRODUCT_DATA)
    def test_valid_creation(self, data: dict):
        """Тест создания с валидными данными"""
        assert_valid_model_creation(ProductCreate, data)
    
    @pytest.mark.parametrize("data, expected_type", PRODUCT_INVALID_TITLE)
    def test_invalid_title(self, data: dict, expected_type: str):
        """Тест невалидного title"""
        with pytest.raises(ValidationError) as exc:
            ProductCreate(**data)
        assert_validation_error(exc, "title", expected_type)
    
    @pytest.mark.parametrize("data, expected_type", PRODUCT_INVALID_DESC)
    def test_invalid_description(self, data: dict, expected_type: str):
        """Тест невалидного description"""
        with pytest.raises(ValidationError) as exc:
            ProductCreate(**data)
        assert_validation_error(exc, "description", expected_type)
    
    @pytest.mark.parametrize("data, expected_type", PRODUCT_INVALID_PRICE)
    def test_invalid_price(self, data: dict, expected_type: str):
        """Тест невалидного price"""
        with pytest.raises(ValidationError) as exc:
            ProductCreate(**data)
        assert_validation_error(exc, "price", expected_type)
    
    @pytest.mark.parametrize("data, expected_type", PRODUCT_INVALID_QUANTITY)
    def test_invalid_quantity(self, data: dict, expected_type: str):
        """Тест невалидного quantity"""
        with pytest.raises(ValidationError) as exc:
            ProductCreate(**data)
        assert_validation_error(exc, "quantity", expected_type)
    
    @pytest.mark.parametrize("data, expected_type", PRODUCT_INVALID_CATEGORY_ID)
    def test_invalid_category_id(self, data: dict, expected_type: str):
        """Тест невалидного category_id"""
        with pytest.raises(ValidationError) as exc:
            ProductCreate(**data)
        assert_validation_error(exc, "category_id", expected_type)


# ============ ТЕСТЫ ДЛЯ ProductUpdate ============

class TestProductUpdate:
    
    @pytest.mark.parametrize("data", VALID_PRODUCT_UPDATE_DATA)
    def test_valid_update(self, data: dict):
        """Тест обновления с валидными данными"""
        assert_valid_model_creation(ProductUpdate, data)
    
    @pytest.mark.parametrize("data, expected_type", PRODUCT_INVALID_TITLE[1:])
    def test_invalid_title(self, data: dict, expected_type: str):
        """Тест невалидного title при обновлении"""
        with pytest.raises(ValidationError) as exc:
            ProductUpdate(**data)
        assert_validation_error(exc, "title", expected_type)
    
    @pytest.mark.parametrize("data, expected_type", PRODUCT_INVALID_DESC[1:])
    def test_invalid_description(self, data: dict, expected_type: str):
        """Тест невалидного description при обновлении"""
        with pytest.raises(ValidationError) as exc:
            ProductUpdate(**data)
        assert_validation_error(exc, "description", expected_type)
    
    @pytest.mark.parametrize("data, expected_type", PRODUCT_INVALID_PRICE[1:])
    def test_invalid_price(self, data: dict, expected_type: str):
        """Тест невалидного price при обновлении"""
        with pytest.raises(ValidationError) as exc:
            ProductUpdate(**data)
        assert_validation_error(exc, "price", expected_type)
    
    @pytest.mark.parametrize("data, expected_type", PRODUCT_INVALID_QUANTITY[1:])
    def test_invalid_quantity(self, data: dict, expected_type: str):
        """Тест невалидного quantity при обновлении"""
        with pytest.raises(ValidationError) as exc:
            ProductUpdate(**data)
        assert_validation_error(exc, "quantity", expected_type)
    
    @pytest.mark.parametrize("data, expected_type", PRODUCT_INVALID_CATEGORY_ID[1:])
    def test_invalid_category_id(self, data: dict, expected_type: str):
        """Тест невалидного category_id при обновлении"""
        with pytest.raises(ValidationError) as exc:
            ProductUpdate(**data)
        assert_validation_error(exc, "category_id", expected_type)