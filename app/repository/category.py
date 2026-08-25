from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from loguru import logger

from typing import Optional
from .base import AbstractRepository
from ..models.category import Category


class CategoryRepository(AbstractRepository[Category]):
    
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

    async def update(self, category_id: int, data: dict) -> Optional[Category]:
        """Обновление категории"""
        try:
            category = await self.get_by_id(category_id)
            if not category:
                return None
            
            for key, value in data.items():
                if value is not None:
                    setattr(category, key, value)
            
            await self.session.commit()
            await self.session.refresh(category)
            return category

        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Ошибка БД при обновлении категории {category_id}: {e}")
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