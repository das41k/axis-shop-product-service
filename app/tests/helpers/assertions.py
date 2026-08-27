from app.schemas.product import ProductResponse
from app.models.product import Product

class ProductAssertions:
    
    @classmethod
    def assert_product_equal(cls, product_schema: ProductResponse, product_model: Product):
        """Сравнивает Pydantic и SQLAlchemy модели продукта"""
        assert product_schema == ProductResponse.model_validate(product_model)