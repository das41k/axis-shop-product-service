from app.schemas.product import ProductResponse
from app.schemas.category import CategoryResponse
from app.models.product import Product
from app.models.category import Category

def assert_product_equal(product_schema: ProductResponse, product_model: Product):
    """Сравнивает Pydantic и SQLAlchemy модели продукта"""
    assert product_schema == ProductResponse.model_validate(product_model)
        
def assert_category_equal(category_schema: CategoryResponse, category_model: Category):
    """Сравнивает Pydantic и SQLAlchemy модели категории"""
    assert category_schema ==  CategoryResponse.model_validate(category_model)