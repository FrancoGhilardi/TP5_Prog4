from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import List

from app.core.database import SessionDep
from app.core.schemas import MensajeError

from . import schemas, services

router = APIRouter(prefix="/productos", tags=["Productos"])

# Respuestas de error declaradas para que Swagger UI las muestre junto al 422
RESPUESTA_404 = {
    404: {"model": MensajeError, "description": "El producto no existe"}
}
RESPUESTA_409 = {
    409: {"model": MensajeError, "description": "Ya existe un producto con ese nombre"}
}


# ---------------------------------------------------------
# ALTA DE PRODUCTO
# Método: POST | Endpoint: /productos | Estado: 201 Created
# ---------------------------------------------------------
@router.post(
    "/",
    response_model=schemas.ProductoRead,
    status_code=status.HTTP_201_CREATED,
    responses={**RESPUESTA_409},
)
def alta_producto(producto: schemas.ProductoCreate, session: SessionDep):
    nuevo, error = services.crear(session, producto)
    if error == "conflict":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un producto con el nombre '{producto.nombre}'",
        )
    return nuevo


# (Extra) LISTAR PRODUCTOS
@router.get(
    "/", response_model=List[schemas.ProductoRead], status_code=status.HTTP_200_OK
)
def listar_productos(
    session: SessionDep, skip: int = Query(0, ge=0), limit: int = Query(10, le=50)
):
    return services.obtener_todos(session, skip, limit)


# ---------------------------------------------------------
# DETALLE DE PRODUCTO
# Método: GET | Endpoint: /productos/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.get(
    "/{id}",
    response_model=schemas.ProductoRead,
    status_code=status.HTTP_200_OK,
    responses={**RESPUESTA_404},
)
def detalle_producto(session: SessionDep, id: int = Path(..., gt=0)):
    producto = services.obtener_por_id(session, id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return producto


# ---------------------------------------------------------
# ACTUALIZACIÓN (Reemplazo Total)
# Método: PUT | Endpoint: /productos/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.put(
    "/{id}",
    response_model=schemas.ProductoRead,
    status_code=status.HTTP_200_OK,
    responses={**RESPUESTA_404, **RESPUESTA_409},
)
def actualizar_producto(
    producto: schemas.ProductoCreate, session: SessionDep, id: int = Path(..., gt=0)
):
    # Usamos ProductoCreate porque es un reemplazo total (exige todos los campos)
    actualizado, error = services.actualizar_total(session, id, producto)
    if error == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    if error == "conflict":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un producto con el nombre '{producto.nombre}'",
        )
    return actualizado


# ---------------------------------------------------------
# BORRADO LÓGICO
# Método: PUT | Endpoint: /productos/{id}/desactivar | Estado: 200 OK
# ---------------------------------------------------------
@router.put(
    "/{id}/desactivar",
    response_model=schemas.ProductoRead,
    status_code=status.HTTP_200_OK,
    responses={**RESPUESTA_404},
)
def borrado_logico(session: SessionDep, id: int = Path(..., gt=0)):
    desactivado = services.desactivar(session, id)
    if not desactivado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return desactivado


# ---------------------------------------------------------
# CONSULTAR STOCK (Lógica de Negocio)
# Método: GET | Endpoint: /productos/{id}/stock | Estado: 200 OK
# ---------------------------------------------------------
@router.get(
    "/{id}/stock",
    response_model=schemas.ProductoStockResponse,
    status_code=status.HTTP_200_OK,
    responses={**RESPUESTA_404},
)
def consultar_stock(session: SessionDep, id: int = Path(..., gt=0)):
    resultado = services.obtener_estado_stock(session, id)  # Llamada al servicio
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return resultado  # El router solo devuelve el resultado
