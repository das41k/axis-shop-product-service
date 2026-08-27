# tests/data/category_data.py
"""Тестовые данные для Category"""

# ============ ВАЛИДНЫЕ ДАННЫЕ ============
VALID_CATEGORY_DATA = [
    {"title": "Спальня", "description": "Очень удобные спальные товары"},
    {"title": "Спальня"}
]

# ============ НЕВАЛИДНЫЕ ДАННЫЕ ============
CATEGORY_INVALID_TITLE = [
    ({"title": None}, "string_type"),
    ({"title": "    "}, "string_too_short"),
    ({"title": "a" * 31}, "string_too_long")
]

CATEGORY_INVALID_DESC = [
    ({"title": "Ванная", "description": "     "}, "string_too_short"),
    ({"title": "Ванная", "description": "a" * 101}, "string_too_long")
]

# ============ ДАННЫЕ ДЛЯ UPDATE ============
VALID_CATEGORY_UPDATE_DATA = VALID_CATEGORY_DATA + [
    {"description": "Очень удобные спальные товары"},
    {"title": "Гостиная"},
    {"title": "Кухня", "description": "Все для кухни"},
    {},
]