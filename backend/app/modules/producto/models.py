from sqlmodel import Field, SQLModel


class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True, max_length=200)
    descripcion: str = Field(default="", max_length=300)
    categoria: str = Field(max_length=6)
    precio: float
    stock: int
    stock_minimo: int
    activo: bool = Field(default=True)
