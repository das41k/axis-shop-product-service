from loguru import logger
from fastapi import APIRouter
from ...dependencies import ProductServiceDep
from ...schemas.product import ProductResponse, ProductUpdate, ProductCreate

router = APIRouter()

@router.get("/", response_model= list[ProductResponse])
async def get_all(service: ProductServiceDep):
    logger.info("GET /products - пришел запрос на получение всех продуктов")
    return await service.get_all()

@router.get("/{id}", response_model= ProductResponse)
async def get_by_id(id: int, service: ProductServiceDep):
    logger.info(f"GET /products/{id} - пришел запрос на получение продукта")
    return await service.get_by_id(id)

@router.post("/", response_model= ProductResponse, status_code=201)
async def create(product_create: ProductCreate, service: ProductServiceDep):
    logger.info("POST /products - пришел запрос на создание продукта")
    return await service.create(product_create)

@router.patch("/{id}", response_model= ProductResponse)
async def update(id: int, product_update: ProductUpdate, service: ProductServiceDep):
    logger.info(f"PATCH /products/{id} - пришел запрос на обновление продукта")
    return await service.update(id, product_update)

@router.delete("/{id}", status_code=204)
async def delete(id: int, service: ProductServiceDep):
    logger.info(f"DELETE /products/{id} - пришел запрос на удаление продукта")
    return await service.delete(id)