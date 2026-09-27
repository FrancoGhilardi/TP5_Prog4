from sqlmodel import Session, select

from app.modules.categoria.models import Categoria

_CATEGORIAS_INICIALES = [
    {"codigo": "MUE-01", "descripcion": "Muebles de Oficina"},
    {"codigo": "ELE-02", "descripcion": "Electrónica"},
]


def seed_categorias(session: Session) -> None:
    existe_alguna = session.exec(select(Categoria)).first()
    if existe_alguna is not None:
        return
    for datos in _CATEGORIAS_INICIALES:
        session.add(Categoria(**datos, activo=True))
    session.commit()
