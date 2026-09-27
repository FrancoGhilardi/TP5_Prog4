from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import List, Optional

from app.core.database import SessionDep

from . import schemas, services

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


# POST /proveedores/ -> 201
@router.post(
    "/", response_model=schemas.ProveedorRead, status_code=status.HTTP_201_CREATED
)
def alta_proveedor(proveedor: schemas.ProveedorCreate, session: SessionDep):
    nuevo = services.crear(session, proveedor)
    if nuevo is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un proveedor con ese código",
        )
    return nuevo


# GET /proveedores/ -> 200
@router.get(
    "/", response_model=List[schemas.ProveedorRead], status_code=status.HTTP_200_OK
)
def listar_proveedores(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    activo: Optional[bool] = Query(None),
):
    return services.obtener_todos(session, skip, limit, activo)


# GET /proveedores/{id} -> 200
@router.get(
    "/{id}", response_model=schemas.ProveedorRead, status_code=status.HTTP_200_OK
)
def detalle_proveedor(session: SessionDep, id: int = Path(..., gt=0)):
    proveedor = services.obtener_por_id(session, id)
    if not proveedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado"
        )
    return proveedor


# PUT /proveedores/{id} -> 200
@router.put(
    "/{id}", response_model=schemas.ProveedorRead, status_code=status.HTTP_200_OK
)
def actualizar_proveedor(
    proveedor: schemas.ProveedorCreate, session: SessionDep, id: int = Path(..., gt=0)
):
    actualizado, error = services.actualizar_total(session, id, proveedor)
    if error == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado"
        )
    if error == "conflict":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un proveedor con ese código",
        )
    return actualizado


# PUT /proveedores/{id}/desactivar -> 200
@router.put(
    "/{id}/desactivar",
    response_model=schemas.ProveedorRead,
    status_code=status.HTTP_200_OK,
)
def borrado_logico(session: SessionDep, id: int = Path(..., gt=0)):
    desactivado, error = services.desactivar(session, id)
    if error == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado"
        )
    if error == "conflict":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El proveedor ya está desactivado",
        )
    return desactivado
