# tests/helpers/validation_helpers.py
"""Хелперы для тестирования валидации Pydantic"""

import pytest
from pydantic import ValidationError
from pydantic import BaseModel


def assert_validation_error(
    exc_info: pytest.ExceptionInfo[ValidationError],
    field_name: str,
    expected_error_type: str
):
    """Проверка ошибки валидации Pydantic"""
    errors = exc_info.value.errors()
    assert len(errors) >= 1
    assert errors[0]["loc"][0] == field_name
    assert errors[0]["type"] == expected_error_type


def assert_valid_model_creation(
    model_class: BaseModel,
    data: dict[str, any]
) -> BaseModel:
    """Создание и проверка валидной модели"""
    instance = model_class(**data)
    
    for field_name, field_value in data.items():
        assert getattr(instance, field_name) == field_value
    
    for field_name in model_class.model_fields.keys():
        if field_name not in data:
            assert getattr(instance, field_name) is None
    
    return instance