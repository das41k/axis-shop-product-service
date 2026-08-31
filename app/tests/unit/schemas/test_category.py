# tests/unit/schemas/test_category_schema.py
import pytest
from pydantic import ValidationError
from app.schemas.category import CategoryCreate, CategoryUpdate

from app.tests.data.category_data import (
    VALID_CATEGORY_DATA,
    VALID_CATEGORY_UPDATE_DATA,
    CATEGORY_INVALID_TITLE,
    CATEGORY_INVALID_DESC
)
from app.tests.helpers.validation_helpers import (
    assert_validation_error,
    assert_valid_model_creation
)

pytestmark = [pytest.mark.unit, pytest.mark.unit_schemas]

class TestCategoryCreate:
    
    @pytest.mark.parametrize("data", VALID_CATEGORY_DATA)
    def test_valid_creation(self, data: dict):
        """Тест создания с валидными данными"""
        assert_valid_model_creation(CategoryCreate, data)
    
    @pytest.mark.parametrize("data, expected_type", CATEGORY_INVALID_TITLE)
    def test_invalid_title(self, data: dict, expected_type: str):
        """Тест невалидного title"""
        with pytest.raises(ValidationError) as exc:
            CategoryCreate(**data)
        assert_validation_error(exc, "title", expected_type)
    
    @pytest.mark.parametrize("data, expected_type", CATEGORY_INVALID_DESC)
    def test_invalid_description(self, data: dict, expected_type: str):
        """Тест невалидного description"""
        with pytest.raises(ValidationError) as exc:
            CategoryCreate(**data)
        assert_validation_error(exc, "description", expected_type)


class TestCategoryUpdate:
    
    @pytest.mark.parametrize("data", VALID_CATEGORY_UPDATE_DATA)
    def test_valid_update(self, data: dict):
        """Тест обновления с валидными данными"""
        assert_valid_model_creation(CategoryUpdate, data)
    
    @pytest.mark.parametrize("data, expected_type", CATEGORY_INVALID_TITLE[1:])
    def test_invalid_title(self, data: dict, expected_type: str):
        """Тест невалидного title при обновлении"""
        with pytest.raises(ValidationError) as exc:
            CategoryUpdate(**data)
        assert_validation_error(exc, "title", expected_type)
    
    @pytest.mark.parametrize("data, expected_type", CATEGORY_INVALID_DESC)
    def test_invalid_description(self, data: dict, expected_type: str):
        """Тест невалидного description при обновлении"""
        with pytest.raises(ValidationError) as exc:
            CategoryUpdate(**data)
        assert_validation_error(exc, "description", expected_type)