from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class CategoryNested(BaseModel):
    id: int
    title: str
    model_config = {"from_attributes": True}


class CategoryResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}  

class CategoryCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str = Field(..., min_length=3, max_length=30, description= "Название категории обязательно и занимает от 3 до 30 символов")
    description: Optional[str] = Field(min_length=5, max_length=100, description= "Описание категории занимает от 5 до 100 символов")
    

class CategoryUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: Optional[str] = Field(None, min_length=3, max_length=30, description= "Название категории обязательно и занимает от 3 до 30 символов")
    description: Optional[str] = Field(None, min_length=5, max_length=100, description= "Описание категории занимает от 5 до 100 символов")
    