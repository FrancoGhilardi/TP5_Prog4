from sqlmodel import Field, SQLModel


class Proveedor(SQLModel, table=True):
    __tablename__ = "proveedores"

    id: int | None = Field(default=None, primary_key=True)
    codigo: str = Field(index=True, unique=True, max_length=20)
    razon_social: str = Field(max_length=200)
    cuit: str = Field(max_length=15)
    email: str = Field(default="", max_length=200)
    telefono: str = Field(default="", max_length=50)
    activo: bool = Field(default=True)
