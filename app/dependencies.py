from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from .core.database import get_async_session
from .repository.base import AbstractRepository
from .repository.category import CategoryRepository
from .repository.product import ProductRepository
from .services.category import CategoryService
from .services.product import ProductService
from .models.category import Category
from .models.product import Product

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

async def get_category_repository(db: SessionDep) -> AbstractRepository:
    return CategoryRepository(db)

async def get_product_repository(db: SessionDep) -> AbstractRepository:
    return ProductRepository(db)

CategoryRepoDep = Annotated[AbstractRepository[Category], Depends(get_category_repository)]
ProductRepoDep = Annotated[AbstractRepository[Product], Depends(get_product_repository)]

async def get_category_service(category_repository: CategoryRepoDep) -> CategoryService:
    return CategoryService(category_repository)

async def get_product_service(product_repository: ProductRepoDep,
                              category_repository: CategoryRepoDep) -> ProductService:
    return ProductService(product_repository, category_repository)

CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]
ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]