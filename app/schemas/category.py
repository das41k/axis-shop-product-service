from pydantic import BaseModel, Field
from datetime import datetime

class CategoryNested(BaseModel):
    id: int
    title: str