from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text
from sqlmodel import Session

from app.core.database import engine
from app.core.seed import seed_categorias
from app.modules.producto.routers import router as producto_router
from app.modules.categoria.routers import router as categoria_router
from app.modules.proveedor.routers import router as proveedor_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with engine.connect() as conexion:
            conexion.execute(text("SELECT 1"))
    except Exception as exc:
        raise RuntimeError(
            "No se pudo conectar a PostgreSQL. Verificá que el servicio esté "
            "corriendo y que DATABASE_URL en .env sea correcta."
        ) from exc

    with Session(engine) as session:
        seed_categorias(session)

    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Gestor de Productos - Unidad 5",
        description="API REST para la gestión de Categorías, Productos y Proveedores, persistida en PostgreSQL con SQLModel.",
        version="2.0.0",
        lifespan=lifespan,
    )

    app.include_router(producto_router)
    app.include_router(categoria_router)
    app.include_router(proveedor_router)

    return app

app = create_app()
