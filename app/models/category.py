from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from sqlalchemy.types import Integer, String, DateTime
from datetime import datetime, timezone
from typing import Optional
from ..core.database import Base


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    title: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(100))
    
    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")
    
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