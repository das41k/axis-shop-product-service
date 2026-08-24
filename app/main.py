from fastapi import FastAPI
from .core.database import async_engine, Base
from .routes.v1.router import router as v1_router

async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()
    

app = FastAPI(
    title="Axis Oline Shop: Product Service",
    version="1.2",
    description="Product Service API",
    lifespan=lifespan
)

app.include_router(v1_router, prefix="/api/v1")