from fastapi import HTTPException, status

class ProductNotFoundException(HTTPException):
    def __init__(self, detail: str = "Product not found", headers: dict | None = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            headers=headers
        )