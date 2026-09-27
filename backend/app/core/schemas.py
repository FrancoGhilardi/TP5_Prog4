from pydantic import BaseModel, Field


class MensajeError(BaseModel):
    """Cuerpo de las respuestas de error de la API.

    Es la forma que FastAPI le da al `detail` de una `HTTPException`. Se declara
    como modelo para que Swagger UI muestre el schema de los 404 y 409 de cada
    endpoint, y no solo el 422 que documenta automáticamente Pydantic.
    """

    detail: str = Field(..., examples=["Producto no encontrado"])
