from typing import Optional
from loguru import logger

from ..repository.base import AbstractRepository
from ..models.product import Product
from ..models.category import Category
from ..schemas.product import ProductCreate, ProductResponse, ProductUpdate
from ..exceptions.product import ProductNotFoundException
from ..exceptions.category import CategoryNotFoundException

class ProductService:
    def __init__(self, product_repository: AbstractRepository[Product],
                 category_repository: AbstractRepository[Category]):
        self.product_repository = product_repository
        self.category_repository = category_repository
    
    async def get_all(self) -> list[ProductResponse]:
        logger.info("Запрос на получение всех продуктов")
        products = await self.product_repository.get_all()
        logger.info(f"Получено {len(products)} продуктов")
        return [ProductResponse.model_validate(p) for p in products]
    
    async def get_by_id(self, product_id: int) -> Optional[ProductResponse]:
        logger.info(f"Поиск продукта с ID: {product_id}")
        product = await self.product_repository.get_by_id(product_id)
        if product is None:
            logger.warning(f"Продукт с ID: {product_id} не найден")
            raise ProductNotFoundException(f"Продукт с ID: {product_id} не найден")
        logger.info(f"Найден продукт: '{product.title}' (ID: {product_id})")
        return ProductResponse.model_validate(product)
    
    async def create(self, product_create: ProductCreate) -> ProductResponse:
        logger.info(f"Создание продукта: '{product_create.title}'")
        category_id = product_create.category_id
        await self.validate_category_id(category_id)
        
        data = product_create.model_dump()
        product = await self.product_repository.create(data)
        logger.info(f"Продукт создан: '{product.title}' (ID: {product.id})")
        return ProductResponse.model_validate(product)
    
    async def update(self, product_id: int, product_update: ProductUpdate) -> Optional[ProductResponse]:
        logger.info(f"Обновление продукта с ID: {product_id}")
        category_id = product_update.category_id
        await self.validate_category_id(category_id)
        
        data = product_update.model_dump()
        product = await self.product_repository.update(product_id, data)
        if product is None:
            logger.warning(f"Продукт с ID: {product_id} не найден для обновления")
            raise ProductNotFoundException(f"Продукт с ID: {product_id} не найден")
        logger.info(f"Продукт обновлен: '{product.title}' (ID: {product_id})")
        return ProductResponse.model_validate(product)
        
    async def delete(self, product_id: int) -> None:
        logger.info(f"Удаление продукта с ID: {product_id}")
        deleted = await self.product_repository.delete_by_id(product_id)
        if not deleted:
            logger.warning(f"Продукт с ID: {product_id} не найден для удаления")
            raise ProductNotFoundException(f"Продукт с ID: {product_id} не найден")
        logger.info(f"Продукт с ID: {product_id} успешно удален")
        
    async def validate_category_id(self, category_id: int) -> None:
        logger.debug(f"Проверка существования категории с ID: {category_id}")
        category = await self.category_repository.get_by_id(category_id)
        if not category and category_id is not None:
            logger.warning(f"Категория с ID: {category_id} не найдена")
            raise CategoryNotFoundException(f"Категория с ID: {category_id} не найдена")
        logger.debug(f"Категория с ID: {category_id} существует")