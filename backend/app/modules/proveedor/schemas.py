from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class ProveedorBase(BaseModel):
    codigo: str = Field(..., min_length=1, examples=["PRO-01"])
    razon_social: str = Field(..., min_length=3, examples=["ACME SRL"])
    cuit: str = Field(..., min_length=11, max_length=15, examples=["20304050607"])
    email: str = Field("", examples=["contacto@acme.com"])
    telefono: str = Field("", examples=["011-4444-5555"])
    activo: bool = True


class ProveedorCreate(ProveedorBase):
    pass


class ProveedorUpdate(BaseModel):
    codigo: Optional[str] = Field(None, min_length=1)
    razon_social: Optional[str] = Field(None, min_length=3)
    cuit: Optional[str] = Field(None, min_length=11, max_length=15)
    email: Optional[str] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None


class ProveedorRead(ProveedorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
