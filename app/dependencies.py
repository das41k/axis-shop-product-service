from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from .core.database import get_async_session
from .repository.category import CategoryRepository
from .repository.product import ProductRepository

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

async def get_category_repository(db: SessionDep):
    return CategoryRepository(db)

async def get_product_repository(db: SessionDep):
    return ProductRepository(db)