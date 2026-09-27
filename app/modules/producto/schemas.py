from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional


class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, examples=["Silla de Oficina"])
    descripcion: str = Field("", max_length=300, examples=["Silla ergonómica con apoyabrazos"])
    categoria: str = Field(..., pattern=r"^[A-Z]{3}-\d{2}$", examples=["MUE-01"])
    precio: float = Field(gt=0, examples=[150.50])
    stock: int = Field(ge=0, examples=[20])
    stock_minimo: int = Field(ge=0, examples=[5])
    activo: bool = True

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío ni contener solo espacios")
        return v.strip()


class ProductoCreate(ProductoBase):
    pass  # Exige todos los campos obligatorios de Base


class ProductoUpdate(BaseModel):
    # Opcional: Se usa si en el futuro se implementa PATCH (actualización parcial)
    nombre: Optional[str] = None
    descripcion: Optional[str] = Field(None, max_length=300)
    categoria: Optional[str] = Field(None, pattern=r"^[A-Z]{3}-\d{2}$")
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    stock_minimo: Optional[int] = Field(None, ge=0)
    activo: Optional[bool] = None


class ProductoRead(ProductoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int  # Contrato de salida: siempre incluye el ID generado


class ProductoStockResponse(BaseModel):
    stock: int
    bajo_stock_minimo: bool
    activo: bool
