from typing import Optional

from ..repository.base import AbstractRepository
from ..models.product import Product
from ..models.category import Category
from ..schemas.product import ProductCreate, ProductResponse, ProductUpdate
from ..exceptions.product import ProductNotFoundException
from ..exceptions.category import CategoryNotFoundExceptionNotFoundException

class ProductService:
    def __init__(self, product_repository: AbstractRepository[Product],
                 category_repository: AbstractRepository[Category]):
        self.product_repository = product_repository
        self.category_repository = category_repository
    
    async def get_all(self) -> list[ProductResponse]:
        products = await self.product_repository.get_all()
        return [ProductResponse.model_validate(p) for p in products]
    
    async def get_by_id(self, product_id: int) -> Optional[ProductResponse]:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(f"Product with ID: {product_id} not found")
        
        return ProductResponse.model_validate(product)
    
    async def create(self, product_create: ProductCreate) -> ProductResponse:
        category_id = product_create.category_id
        self.validate_category_id(category_id)
        
        data = product_create.model_dump()
        product = await self.product_repository.create(data)
        return ProductResponse.model_validate(product)
    
    async def update(self, product_id: int, product_update: ProductUpdate) -> Optional[ProductResponse]:
        category_id = product_update.category_id
        self.validate_category_id(category_id)
        
        data = product_update.model_dump()
        product = await self.product_repository.update(product_id, data)
        if not product:
            raise ProductNotFoundException(f"Product with ID: {product_id} not found")
        return ProductResponse.model_validate(product)
        
    async def delete(self, product_id: int) -> None:
        deleted = await self.product_repository.delete_by_id(product_id)
        if not deleted:
            raise ProductNotFoundException(f"Product with ID: {product_id} not found")
        
    async def validate_category_id(self, category_id: int) -> None:
        category = await self.category_repository.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundExceptionNotFoundException(f"Category with ID: {category_id} not found")