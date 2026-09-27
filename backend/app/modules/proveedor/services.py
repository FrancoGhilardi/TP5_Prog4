from typing import List, Optional

from sqlmodel import Session, select

from .models import Proveedor
from .schemas import ProveedorCreate


def existe_codigo(session: Session, codigo: str, excluir_id: Optional[int] = None) -> bool:
    sentencia = select(Proveedor).where(Proveedor.codigo == codigo)
    if excluir_id is not None:
        sentencia = sentencia.where(Proveedor.id != excluir_id)
    return session.exec(sentencia).first() is not None


def crear(session: Session, data: ProveedorCreate) -> Optional[Proveedor]:
    if existe_codigo(session, data.codigo):
        return None
    nuevo = Proveedor.model_validate(data)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo


def obtener_todos(
    session: Session, skip: int, limit: int, activo: Optional[bool] = None
) -> List[Proveedor]:
    sentencia = select(Proveedor)
    if activo is not None:
        sentencia = sentencia.where(Proveedor.activo == activo)
    return session.exec(sentencia.offset(skip).limit(limit)).all()


def obtener_por_id(session: Session, id: int) -> Optional[Proveedor]:
    return session.get(Proveedor, id)


def actualizar_total(
    session: Session, id: int, data: ProveedorCreate
) -> tuple[Optional[Proveedor], Optional[str]]:
    proveedor = session.get(Proveedor, id)
    if proveedor is None:
        return None, "not_found"
    if existe_codigo(session, data.codigo, excluir_id=id):
        return None, "conflict"
    for campo, valor in data.model_dump().items():
        setattr(proveedor, campo, valor)
    session.add(proveedor)
    session.commit()
    session.refresh(proveedor)
    return proveedor, None


def desactivar(session: Session, id: int) -> tuple[Optional[Proveedor], Optional[str]]:
    proveedor = session.get(Proveedor, id)
    if proveedor is None:
        return None, "not_found"
    if proveedor.activo is False:
        return None, "conflict"
    proveedor.activo = False
    session.add(proveedor)
    session.commit()
    session.refresh(proveedor)
    return proveedor, None
