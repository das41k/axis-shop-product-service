from fastapi import FastAPI
from loguru import logger
from .core.database import async_engine, Base
from .routes.v1.router import router as v1_router
from .core.config import settings

async def lifespan(app: FastAPI):
    logger.info(f"Приложение: {settings.APP_NAME} запущено по адресу: http://{settings.APP_HOST}:{settings.APP_PORT}")
    logger.info("Устанавливаем соединение с базой данных")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Подключение к БД установлено")
    yield
    logger.info(f"Приложение: {settings.APP_NAME} завершает выполнение")
    await async_engine.dispose()
    logger.info("Успешно закрыли соединение с базой данных")    

app = FastAPI(
    title=settings.APP_NAME,
    version="1.2",
    description="Product Service API",
    lifespan=lifespan
)

app.include_router(v1_router, prefix="/api/v1")