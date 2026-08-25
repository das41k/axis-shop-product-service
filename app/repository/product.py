from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from loguru import logger

from typing import Optional
from .base import AbstractRepository
from ..models.product import Product


class ProductRepository(AbstractRepository[Product]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Product]:
        """Получение всех продуктов"""
        try:
            result = await self.session.scalars(
                select(Product).order_by(Product.title)
            )
            return result.all()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка БД при получении всех продуктов: {e}")
            raise

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        """Получение продукта по ID"""
        try:
            return await self.session.get(Product, product_id)
        except SQLAlchemyError as e:
            logger.error(f"Ошибка БД при получении продукта {product_id}: {e}")
            raise

    async def create(self, data: dict) -> Product:
        """Создание продукта"""
        try:
            product = Product(**data)
            self.session.add(product)
            await self.session.commit()
            await self.session.refresh(product)
            return product
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Ошибка БД при создании продукта: {e}")
            raise

    async def update(self, product_id: int, data: dict) -> Optional[Product]:
        """Обновление продукта"""
        try:
            product = await self.get_by_id(product_id)
            if not product:
                return None
            
            for key, value in data.items():
                if value is not None:
                    setattr(product, key, value)
            
            await self.session.commit()
            await self.session.refresh(product)
            return product
        
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Ошибка БД при обновлении {product_id}: {e}")
            raise

    async def delete_by_id(self, product_id: int) -> bool:
        """Удаление продукта"""
        try:
            stmt = delete(Product).where(Product.id == product_id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount > 0
        
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Ошибка БД при удалении {product_id}: {e}")
            raise