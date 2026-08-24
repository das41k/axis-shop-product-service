from fastapi import APIRouter

from .category import router as category_router

router = APIRouter()
router.include_router(category_router, prefix="/categories", tags=["Categories V1"])