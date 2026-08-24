from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from .core.database import get_async_session
from .repository.base import AbstractRepository
from .repository.category import CategoryRepository
from .repository.product import ProductRepository
from .services.category import CategoryService
from .models.category import Category

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

async def get_category_repository(db: SessionDep) -> AbstractRepository:
    return CategoryRepository(db)

async def get_product_repository(db: SessionDep) -> AbstractRepository:
    return ProductRepository(db)

CategoryRepoDep = Annotated[AbstractRepository[Category], Depends(get_category_repository)]

async def get_category_service(category_repository: CategoryRepoDep) -> CategoryService:
    return CategoryService(category_repository)

CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]