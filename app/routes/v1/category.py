from loguru import logger
from fastapi import APIRouter

from ...schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate
from ...dependencies import CategoryServiceDep

router = APIRouter()

@router.get("/", response_model=list[CategoryResponse])
async def get_all(service: CategoryServiceDep):
    logger.info("GET /categories - пришел запрос на получение всех категорий")
    return await service.get_all()

@router.get("/{id}", response_model = CategoryResponse)
async def get_by_id(id: int, service: CategoryServiceDep):
    logger.info(f"GET /categories/{id} - пришел запрос на получение категории")
    return await service.get_by_id(id)

@router.post("/", response_model = CategoryResponse, status_code=201)
async def create(category_create: CategoryCreate, service: CategoryServiceDep):
    logger.info("POST /categories - пришел запрос на создание категории")
    return await service.create(category_create)

@router.patch("/{id}", response_model = CategoryResponse)
async def update(id: int, category_update: CategoryUpdate, service: CategoryServiceDep):
    logger.info(f"PATCH /categories/{id} - пришел запрос на обновление категории")
    return await service.update(id, category_update)

@router.delete("/{id}", status_code=204)
async def delete(id: int, service: CategoryServiceDep):
    logger.info(f"DELETE /categories/{id} - пришел запрос на удаление категории")
    return await service.delete_by_id(id)