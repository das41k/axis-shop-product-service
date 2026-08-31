from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Integer, Numeric, DateTime
from sqlalchemy import ForeignKey, func
from datetime import datetime
import uuid
from typing import Optional
from ..core.database import Base

def generate_sku() -> str:
    return f"SKU-{uuid.uuid4().hex[:8].upper()}"

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(100))
    
    sku: Mapped[str] = mapped_column(String(30), nullable=False, unique=True, default=generate_sku)
    
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False,)
    quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)
    category: Mapped["Category"] = relationship("Category", back_populates="products", lazy="selectin")
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),   # <-- Берем время из БД
        nullable=False
    )
    
    # Обновление: БД сама обновляет время при каждом изменении строки
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),   # <-- На случай, если не указали при вставке
        onupdate=func.now(),         # <-- БД сама обновляет при UPDATE
        nullable=False
    )