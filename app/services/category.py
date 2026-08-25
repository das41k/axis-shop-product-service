from typing import Optional
from loguru import logger

from ..repository.base import AbstractRepository
from ..models.category import Category
from ..schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from ..exceptions.category import CategoryNotFoundException

class CategoryService:
    def __init__(self, category_repository: AbstractRepository[Category]):
        self.category_repository = category_repository
        
    async def get_all(self) -> list[CategoryResponse]:
        logger.info("Запрос на получение всех категорий")
        categories = await self.category_repository.get_all()
        logger.info(f"Получено {len(categories)} категорий")
        return [CategoryResponse.model_validate(c) for c in categories]
    
    async def get_by_id(self, category_id: int) -> Optional[CategoryResponse]:
        logger.info(f"Поиск категории с ID: {category_id}")
        category = await self.category_repository.get_by_id(category_id)
        if category is None:
            logger.warning(f"Категория с ID: {category_id} не найдена")
            raise CategoryNotFoundException(f"Категория с IDD: {category_id} не найдена")
        logger.info(f"Найдена категория: '{category.title}' (ID: {category_id})")
        return CategoryResponse.model_validate(category)
        
    async def create(self, category_create: CategoryCreate) -> CategoryResponse:
        logger.info(f"Создание категории: '{category_create.title}'")
        logger.debug(f"Проверяем есть ли уже категориями с названием: {category_create.title}")
        data = category_create.model_dump()
        category = await self.category_repository.create(data)
        logger.info(f"Категория создана: '{category.title}' (ID: {category.id})")
        return CategoryResponse.model_validate(category)
    
    async def update(self, category_id: int, category_update: CategoryUpdate) -> Optional[CategoryResponse]:
        logger.info(f"Обновление категории с ID: {category_id}")
        data = category_update.model_dump()
        category = await self.category_repository.update(category_id, data)
        if category is None:
            logger.warning(f"Категория с ID: {category_id} не найдена для обновления")
            raise CategoryNotFoundException(f"Категория с ID: {category_id} не найдена")
        logger.info(f"Категория обновлена: '{category.title}' (ID: {category_id})")
        return CategoryResponse.model_validate(category)
    
    async def delete_by_id(self, category_id: int) -> None:
        logger.info(f"Удаление категории с ID: {category_id}")
        deleted = await self.category_repository.delete_by_id(category_id)
        if not deleted:
            logger.warning(f"Категория с ID: {category_id} не найдена для удаления")
            raise CategoryNotFoundException(f"Категория с ID: {category_id} не найдена")
        logger.info(f"Категория с ID: {category_id} успешно удалена")