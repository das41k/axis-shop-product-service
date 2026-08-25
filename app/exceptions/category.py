from fastapi import HTTPException, status

class CategoryNotFoundException(HTTPException):
    def __init__(
        self,
        detail: str = "Category not found",
        headers: dict | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            headers=headers,
        )
        
class CategoryIsExistsException(HTTPException):
    def __init__(
        self, 
        detail: str = "Category is exists in system",
        headers: dict | None = None
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            headers=headers
        )