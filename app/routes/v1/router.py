from fastapi import APIRouter

from .category import router as category_router
from .product import router as product_router

router = APIRouter()
router.include_router(category_router, prefix="/categories", tags=["Categories V1"])
router.include_router(product_router, prefix="/products", tags=["Products V1"])