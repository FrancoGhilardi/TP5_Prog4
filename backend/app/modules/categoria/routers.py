from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import List

from app.core.database import SessionDep
from app.core.schemas import MensajeError

from . import schemas, services

router = APIRouter(prefix="/categorias", tags=["Categorías"])

# Respuestas de error declaradas para que Swagger UI las muestre junto al 422
RESPUESTA_404 = {
    404: {"model": MensajeError, "description": "La categoría no existe"}
}
RESPUESTA_409 = {
    409: {"model": MensajeError, "description": "Ya existe una categoría con ese código"}
}


@router.post(
    "/",
    response_model=schemas.CategoriaRead,
    status_code=status.HTTP_201_CREATED,
    responses={**RESPUESTA_409},
)
def alta_categoria(categoria: schemas.CategoriaCreate, session: SessionDep):
    nueva, error = services.crear(session, categoria)
    if error == "conflict":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una categoría con el código '{categoria.codigo}'",
        )
    return nueva


@router.get(
    "/", response_model=List[schemas.CategoriaRead], status_code=status.HTTP_200_OK
)
def listar_categorias(
    session: SessionDep, skip: int = Query(0, ge=0), limit: int = Query(10, le=50)
):
    return services.obtener_todas(session, skip, limit)


@router.get(
    "/{id}",
    response_model=schemas.CategoriaRead,
    status_code=status.HTTP_200_OK,
    responses={**RESPUESTA_404},
)
def detalle_categoria(session: SessionDep, id: int = Path(..., gt=0)):
    categoria = services.obtener_por_id(session, id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
        )
    return categoria


@router.put(
    "/{id}",
    response_model=schemas.CategoriaRead,
    status_code=status.HTTP_200_OK,
    responses={**RESPUESTA_404, **RESPUESTA_409},
)
def actualizar_categoria(
    categoria: schemas.CategoriaCreate, session: SessionDep, id: int = Path(..., gt=0)
):
    actualizada, error = services.actualizar_total(session, id, categoria)
    if error == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
        )
    if error == "conflict":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una categoría con el código '{categoria.codigo}'",
        )
    return actualizada


@router.put(
    "/{id}/desactivar",
    response_model=schemas.CategoriaRead,
    status_code=status.HTTP_200_OK,
    responses={**RESPUESTA_404},
)
def borrado_logico(session: SessionDep, id: int = Path(..., gt=0)):
    desactivada = services.desactivar(session, id)
    if not desactivada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
        )
    return desactivada
