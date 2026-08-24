from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from typing import Optional
from .base import AbstractRepository
from ..models.product import Product

class ProductRepository(AbstractRepository[Product]):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_all(self) -> list[Product]:
        result = await self.session.scalars(select(Product).order_by(Product.title))
        return result.all()
    
    async def get_by_id(self, product_id: int) -> Optional[Product]:
        return await self.session.get(Product, product_id)
    
    async def create(self, data: dict) -> Product:
        product = Product(**data)
        self.session.add(product)
        
        await self.session.commit()
        await self.session.refresh(product)
        return product
    
    async def update(self, product_id: int, data: dict) -> Optional[Product]:
        product = await self.get_by_id(product_id)
        if not product:
            return None
        
        for key, value in data.items():
             if value is not None:
                setattr(product, key, value)
            
        await self.session.commit()
        await self.session.refresh(product)
        return product
    
    async def delete_by_id(self, product_id: int) -> bool:
        stmt = delete(Product).where(Product.id == product_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0