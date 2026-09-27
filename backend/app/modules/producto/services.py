from typing import List, Optional

from sqlmodel import Session, select

from .models import Producto
from .schemas import ProductoCreate


def existe_nombre(session: Session, nombre: str, excluir_id: Optional[int] = None) -> bool:
    sentencia = select(Producto).where(Producto.nombre == nombre)
    if excluir_id is not None:
        sentencia = sentencia.where(Producto.id != excluir_id)
    return session.exec(sentencia).first() is not None


def crear(session: Session, data: ProductoCreate) -> tuple[Optional[Producto], Optional[str]]:
    if existe_nombre(session, data.nombre):
        return None, "conflict"
    nuevo = Producto.model_validate(data)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo, None


def obtener_todos(session: Session, skip: int, limit: int) -> List[Producto]:
    return session.exec(select(Producto).offset(skip).limit(limit)).all()


def obtener_por_id(session: Session, id: int) -> Optional[Producto]:
    return session.get(Producto, id)


def actualizar_total(
    session: Session, id: int, data: ProductoCreate
) -> tuple[Optional[Producto], Optional[str]]:
    # Reemplazo total: requiere todos los campos validables (ProductoCreate)
    producto = session.get(Producto, id)
    if producto is None:
        return None, "not_found"
    if existe_nombre(session, data.nombre, excluir_id=id):
        return None, "conflict"
    for campo, valor in data.model_dump().items():
        setattr(producto, campo, valor)
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto, None


def desactivar(session: Session, id: int) -> Optional[Producto]:
    # Borrado lógico: solo altera el estado 'activo'
    producto = session.get(Producto, id)
    if producto is None:
        return None
    producto.activo = False
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


def obtener_estado_stock(session: Session, id: int) -> Optional[dict]:
    producto = session.get(Producto, id)
    if producto is None:
        return None

    # La lógica de negocio vive aquí
    alerta_stock = producto.stock < producto.stock_minimo

    return {
        "stock": producto.stock,
        "bajo_stock_minimo": alerta_stock,
        "activo": producto.activo,
    }
