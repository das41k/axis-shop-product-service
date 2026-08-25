from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional
from ..models.category import Category

T = TypeVar('T')

class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    async def get_all(self) -> list[T]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[T]:
        raise NotImplementedError
    
    @abstractmethod
    async def create(self, data: dict) -> T:
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, id: int, data: dict) -> Optional[T]:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(self, id: int) -> bool:
        raise NotImplementedError


class AbstractCategoryRepository(AbstractRepository[Category], ABC):
    @abstractmethod
    async def exists_by_title(self, title: str) -> bool:
        raise NotImplementedError