from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import List

from app.core.database import SessionDep

from . import schemas, services

router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.post(
    "/", response_model=schemas.CategoriaRead, status_code=status.HTTP_201_CREATED
)
def alta_categoria(categoria: schemas.CategoriaCreate, session: SessionDep):
    return services.crear(session, categoria)


@router.get(
    "/", response_model=List[schemas.CategoriaRead], status_code=status.HTTP_200_OK
)
def listar_categorias(
    session: SessionDep, skip: int = Query(0, ge=0), limit: int = Query(10, le=50)
):
    return services.obtener_todas(session, skip, limit)


@router.get(
    "/{id}", response_model=schemas.CategoriaRead, status_code=status.HTTP_200_OK
)
def detalle_categoria(session: SessionDep, id: int = Path(..., gt=0)):
    categoria = services.obtener_por_id(session, id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
        )
    return categoria


@router.put(
    "/{id}", response_model=schemas.CategoriaRead, status_code=status.HTTP_200_OK
)
def actualizar_categoria(
    categoria: schemas.CategoriaCreate, session: SessionDep, id: int = Path(..., gt=0)
):
    actualizada = services.actualizar_total(session, id, categoria)
    if not actualizada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
        )
    return actualizada


@router.put(
    "/{id}/desactivar",
    response_model=schemas.CategoriaRead,
    status_code=status.HTTP_200_OK,
)
def borrado_logico(session: SessionDep, id: int = Path(..., gt=0)):
    desactivada = services.desactivar(session, id)
    if not desactivada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
        )
    return desactivada
