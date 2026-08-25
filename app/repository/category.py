from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, exists
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from loguru import logger

from typing import Optional
from .base import AbstractCategoryRepository
from ..models.category import Category
from ..models.product import Product


class CategoryRepository(AbstractCategoryRepository):
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Category]:
        """Получение всех категорий"""
        try:
            result = await self.session.scalars(
                select(Category).order_by(Category.title)
            )
            return result.all()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка БД при получении всех категорий: {e}")
            raise

    async def get_by_id(self, category_id: int) -> Optional[Category]:
        """Получение категории по ID"""
        try:
            return await self.session.get(Category, category_id)
        except SQLAlchemyError as e:
            logger.error(f"Ошибка БД при получении категории {category_id}: {e}")
            raise
        
    async def exists_by_title(self, category_title: str) -> bool:
        """Проверка на существование по Title"""
        try:
            stmt = select(exists().where(Category.title == category_title))
            result = await self.session.execute(stmt)
            return result.scalar()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка БД при получении категории {category_title}: {e}")
            raise

    async def create(self, data: dict) -> Category:
        """Создание категории"""
        try:
            category = Category(**data)
            self.session.add(category)
            await self.session.commit()
            await self.session.refresh(category)
            return category

        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Ошибка БД при создании категории: {e}")
            raise

    async def update(self, category: Category, data: dict) -> Category:
        """Обновление категории"""
        try:
            for key, value in data.items():
                if value is not None:
                    setattr(category, key, value)
            
            await self.session.commit()
            await self.session.refresh(category)
            return category

        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Ошибка БД при обновлении категории {category.id}: {e}")
            raise

    async def delete_by_id(self, category_id: int) -> bool:
        """Удаление категории"""
        try:
            stmt = delete(Category).where(Category.id == category_id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount > 0
        
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Ошибка БД при удалении категории {category_id}: {e}")
            raise
        
    async def has_products(self, category_id: int) -> bool:
        """Проверка существования товаров у категории"""
        try:
            stmt = select(exists().where(Product.category_id == category_id))
            result = await self.session.execute(stmt)
            return result.scalar()
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Ошибка БД при проверке существования товаров у категории {category_id}: {e}")
            raise