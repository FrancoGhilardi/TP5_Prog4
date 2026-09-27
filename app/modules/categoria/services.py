from typing import List, Optional

from sqlmodel import Session, select

from .models import Categoria
from .schemas import CategoriaCreate


def crear(session: Session, data: CategoriaCreate) -> Categoria:
    nueva = Categoria.model_validate(data)
    session.add(nueva)
    session.commit()
    session.refresh(nueva)
    return nueva


def obtener_todas(session: Session, skip: int = 0, limit: int = 10) -> List[Categoria]:
    return session.exec(select(Categoria).offset(skip).limit(limit)).all()


def obtener_por_id(session: Session, id: int) -> Optional[Categoria]:
    return session.get(Categoria, id)


def actualizar_total(session: Session, id: int, data: CategoriaCreate) -> Optional[Categoria]:
    categoria = session.get(Categoria, id)
    if categoria is None:
        return None
    for campo, valor in data.model_dump().items():
        setattr(categoria, campo, valor)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


def desactivar(session: Session, id: int) -> Optional[Categoria]:
    categoria = session.get(Categoria, id)
    if categoria is None:
        return None
    categoria.activo = False
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria
