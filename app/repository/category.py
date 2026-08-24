from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from typing import Optional
from .base import AbstractRepository
from ..models.category import Category

class CategoryRepository(AbstractRepository[Category]):
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_all(self) -> list[Category]:
        result = await self.session.scalars(select(Category).order_by(Category.title))
        return result.all()
    
    async def get_by_id(self, category_id: int) -> Optional[Category]:
        return await self.session.get(Category, category_id)
    
    async def create(self, data: dict) -> Category:
        category = Category(**data)
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category
    
    async def update(self, category_id: int, data: dict) -> Optional[Category]:
        category = await self.get_by_id(category_id)
        if not category:
            return None
        
        for key, value in data.items():
            if value is not None:
                setattr(category, key, value)
        
        await self.session.commit()
        await self.session.refresh(category)
        return category
        
    async def delete_by_id(self, category_id: int) -> bool:
        stmt = delete(Category).where(Category.id == category_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0