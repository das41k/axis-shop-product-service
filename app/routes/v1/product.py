from fastapi import APIRouter
from ...dependencies import ProductServiceDep
from ...schemas.product import ProductResponse, ProductUpdate, ProductCreate

router = APIRouter()

@router.get("/", response_model= list[ProductResponse])
async def get_all(service: ProductServiceDep):
    return await service.get_all()

@router.get("/{id}", response_model= ProductResponse)
async def get_by_id(id: int, service: ProductServiceDep):
    return await service.get_by_id(id)

@router.post("/", response_model= ProductResponse, status_code=201)
async def create(product_create: ProductCreate, service: ProductServiceDep):
    return await service.create(product_create)

@router.patch("/{id}", response_model= ProductResponse)
async def update(id: int, product_update: ProductUpdate, service: ProductServiceDep):
    return await service.update(id, product_update)

@router.delete("/{id}", status_code=204)
async def delete(id: int, service: ProductServiceDep):
    return await service.delete(id)