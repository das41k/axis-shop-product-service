from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from category import CategoryNested
from typing import Optional

class ProductResponse(BaseModel):
    id: int
    title: str
    description: str
    sku: str
    
    price: float
    quantity: int
    
    category: CategoryNested
    
    created_at: datetime
    updated_at: datetime


class ProductCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    title: str = Field(..., min_length=3, max_length=30, description= "Название продукта обязательно и занимает от 3 до 30 символов")
    description: Optional[str] = Field(min_length=5, max_length=100, description= "Описание продукта от 5 до 100 символов")
    
    price: float = Field(..., qt = 0, description = "Цена обязательна и должна быть больше 0")
    quantity: int = Field(..., qe = 0, description="Количество обьязательно и не может быть отрицательным")
    
    category_id: int =  Field(..., gt= 0, description="ID категории обязателен и больше 0")

    
class ProductUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
        
    title: Optional[str] = Field(..., min_length=3, max_length=30, description= "Название продукта обязательно и занимает от 3 до 30 символов")
    description: Optional[str] = Field(min_length=5, max_length=100, description= "Описание продукта от 5 до 100 символов")
        
    price: Optional[float] = Field(..., qt = 0, description = "Цена обязательна и должна быть больше 0")
    quantity: Optional[int] = Field(..., qe = 0, description="Количество обьязательно и не может быть отрицательным")
        
    category_id: Optional[int] =  Field(..., gt= 0, description="ID категории обязателен и больше 0")