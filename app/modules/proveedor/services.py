from typing import List, Optional
from .schemas import ProveedorCreate, ProveedorRead

db_proveedores: List[ProveedorRead] = []
id_counter = 1


def existe_codigo(codigo: str, excluir_id: Optional[int] = None) -> bool:
    return any(
        p.codigo == codigo for p in db_proveedores if p.id != excluir_id
    )


def crear(data: ProveedorCreate) -> Optional[ProveedorRead]:
    global id_counter
    if existe_codigo(data.codigo):
        return None
    nuevo = ProveedorRead(id=id_counter, **data.model_dump())
    db_proveedores.append(nuevo)
    id_counter += 1
    return nuevo


def obtener_todos(
    skip: int, limit: int, activo: Optional[bool] = None
) -> List[ProveedorRead]:
    resultado = db_proveedores
    if activo is not None:
        resultado = [p for p in resultado if p.activo == activo]
    return resultado[skip : skip + limit]


def obtener_por_id(id: int) -> Optional[ProveedorRead]:
    for p in db_proveedores:
        if p.id == id:
            return p
    return None


def actualizar_total(id: int, data: ProveedorCreate) -> tuple[Optional[ProveedorRead], Optional[str]]:
    proveedor = obtener_por_id(id)
    if proveedor is None:
        return None, "not_found"
    if existe_codigo(data.codigo, excluir_id=id):
        return None, "conflict"
    for index, p in enumerate(db_proveedores):
        if p.id == id:
            actualizado = ProveedorRead(id=id, **data.model_dump())
            db_proveedores[index] = actualizado
            return actualizado, None
    return None, "not_found"


def desactivar(id: int) -> tuple[Optional[ProveedorRead], Optional[str]]:
    proveedor = obtener_por_id(id)
    if proveedor is None:
        return None, "not_found"
    if proveedor.activo is False:
        return None, "conflict"
    for index, p in enumerate(db_proveedores):
        if p.id == id:
            p_dict = p.model_dump()
            p_dict["activo"] = False
            actualizado = ProveedorRead(**p_dict)
            db_proveedores[index] = actualizado
            return actualizado, None
    return None, "not_found"
