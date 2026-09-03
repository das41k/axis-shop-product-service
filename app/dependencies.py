from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, AsyncGenerator
from redis.asyncio import Redis

from .core.database import get_async_session
from .repository.base import AbstractRepository, AbstractCategoryRepository
from .repository.category import CategoryRepository
from .repository.product import ProductRepository
from .services.category import CategoryService
from .services.product import ProductService
from .models.category import Category
from .models.product import Product
from .core.redis_manager import redis_manager

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

async def get_category_repository(db: SessionDep) -> AbstractCategoryRepository:
    return CategoryRepository(db)

async def get_product_repository(db: SessionDep) -> AbstractRepository[Product]:
    return ProductRepository(db)

async def get_redis() -> AsyncGenerator[Redis, None]:
    if redis_manager.redis is None:
        raise RuntimeError("Redis не инициализирован!")
    return redis_manager.redis

RedisDep = Annotated[Redis, Depends(get_redis)]

CategoryRepoDep = Annotated[AbstractCategoryRepository, Depends(get_category_repository)]
ProductRepoDep = Annotated[AbstractRepository[Product], Depends(get_product_repository)]

async def get_category_service(category_repository: CategoryRepoDep, redis: RedisDep) -> CategoryService:
    return CategoryService(category_repository, redis)

async def get_product_service(product_repository: ProductRepoDep,
                              category_repository: CategoryRepoDep) -> ProductService:
    return ProductService(product_repository, category_repository)

CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]
ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]