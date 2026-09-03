class CategoryCacheKeys:
    PREFIX = "categories"
    ALL = f"{PREFIX}:all"
    
    @classmethod
    def category_by_id(cls, category_id: int) -> str:
        return f"{CategoryCacheKeys.PREFIX}:id:{category_id}"