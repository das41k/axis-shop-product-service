from fastapi import APIRouter

from ...schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate
from ...dependencies import CategoryServiceDep

router = APIRouter()

@router.get("/", response_model=list[CategoryResponse])
async def get_all(service: CategoryServiceDep):
    return await service.get_all()

@router.get("/{id}", response_model = CategoryResponse)
async def get_by_id(id: int, service: CategoryServiceDep):
    return await service.get_by_id(id)

@router.post("/", response_model = CategoryResponse, status_code=201)
async def create(category_create: CategoryCreate, service: CategoryServiceDep):
    return await service.create(category_create)

@router.patch("/{id}", response_model = CategoryResponse)
async def update(id: int, category_update: CategoryUpdate, service: CategoryServiceDep):
    return await service.update(id, category_update)

@router.delete("/{id}", status_code=204)
async def delete(id: int, service: CategoryServiceDep):
    return await service.delete_by_id(id)