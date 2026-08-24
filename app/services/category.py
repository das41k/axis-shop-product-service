from typing import Optional

from ..repository.base import AbstractRepository
from ..models.category import Category
from ..schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from ..exceptions.category import CategoryNotFoundException

class CategoryService:
    def __init__(self, category_repository: AbstractRepository[Category]):
        self.category_repository = category_repository
        
    async def get_all(self) -> list[CategoryResponse]:
        categories = await self.category_repository.get_all()
        return [CategoryResponse.model_validate(c) for c in categories]
    
    async def get_by_id(self, category_id: int) -> Optional[CategoryResponse]:
        category = await self.category_repository.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundException(f"Category with ID: {category_id} not found")
        return CategoryResponse.model_validate(category)
        
    async def create(self, category_create: CategoryCreate) -> CategoryResponse:
        data = category_create.model_dump()
        category = await self.category_repository.create(data)
        return CategoryResponse.model_validate(category)
    
    async def update(self, category_id: int, category_update: CategoryUpdate) -> Optional[CategoryResponse]:
        data = category_update.model_dump()
        category = await self.category_repository.update(category_id, data)
        if category is None:
             raise CategoryNotFoundException(f"Category with ID: {category_id} not found")
        return CategoryResponse.model_validate(category)
    
    async def delete_by_id(self, category_id: int) -> None:
        deleted = await self.category_repository.delete_by_id(category_id)
        if not deleted:
            raise CategoryNotFoundException(f"Category with ID: {category_id} not found")