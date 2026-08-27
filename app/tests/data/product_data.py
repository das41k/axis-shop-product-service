# tests/data/product_data.py
"""Тестовые данные для Product"""

# ============ ВАЛИДНЫЕ ДАННЫЕ ============
VALID_PRODUCT_DATA = [
    {"title": "Вилка", "description": "Очень удобная", "price": 100, "quantity": 3, "category_id": 1},
    {"title": "Вилка", "price": 100, "quantity": 3, "category_id": 1},
]

# ============ НЕВАЛИДНЫЕ ДАННЫЕ ============
PRODUCT_INVALID_TITLE = [
    ({"title": None, "price": 100, "quantity": 3, "category_id": 1}, "string_type"),
    ({"title": "    ", "price": 100, "quantity": 3, "category_id": 1}, "string_too_short"),
    ({"title": "a" * 31, "price": 100, "quantity": 3, "category_id": 1}, "string_too_long")
]

PRODUCT_INVALID_DESC = [
    ({"title": "Вилка", "description": "   ", "price": 100, "quantity": 3, "category_id": 1}, "string_too_short"),
    ({"title": "Вилка", "description": "a" * 101, "price": 100, "quantity": 3, "category_id": 1}, "string_too_long")
]

PRODUCT_INVALID_PRICE = [
    ({"title": "Вилка", "price": None, "quantity": 3, "category_id": 1}, "float_type"),
    ({"title": "Вилка", "price": "string", "quantity": 3, "category_id": 1}, "float_parsing"),
    ({"title": "Вилка", "price": 0, "quantity": 3, "category_id": 1}, "greater_than"),
    ({"title": "Вилка", "price": -5, "quantity": 3, "category_id": 1}, "greater_than")
]

PRODUCT_INVALID_QUANTITY = [
    ({"title": "Вилка", "price": 100, "quantity": None, "category_id": 1}, "int_type"),
    ({"title": "Вилка", "price": 100, "quantity": "string", "category_id": 1}, "int_parsing"),
    ({"title": "Вилка", "price": 100, "quantity": -5, "category_id": 1}, "greater_than_equal"),
    ({"title": "Вилка", "price": 100, "quantity": 5.5, "category_id": 1}, "int_from_float")
]

PRODUCT_INVALID_CATEGORY_ID = [
    ({"title": "Вилка", "price": 100, "quantity": 3, "category_id": None}, "int_type"),
    ({"title": "Вилка", "price": 100, "quantity": 3, "category_id": "string"}, "int_parsing"),
    ({"title": "Вилка", "price": 100, "quantity": 3, "category_id": 0}, "greater_than"),
    ({"title": "Вилка", "price": 100, "quantity": 3, "category_id": -5}, "greater_than"),
    ({"title": "Вилка", "price": 100, "quantity": 3, "category_id": 5.7}, "int_from_float")
]

# ============ ДАННЫЕ ДЛЯ UPDATE ============
VALID_PRODUCT_UPDATE_DATA = VALID_PRODUCT_DATA + [
    {"title": "Новая вилка"},
    {"price": 200.50},
    {"quantity": 10},
    {"category_id": 5},
    {"description": "Новое описание"},
    {},
    {"title": "Вилка", "price": 150.75},
    {"quantity": 7, "category_id": 3},
]