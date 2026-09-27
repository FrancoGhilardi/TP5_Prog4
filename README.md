# API Integradora — Unidad 1 (TP4)

API REST construida con **FastAPI** y **Pydantic v2**, con persistencia en memoria (listas). Implementa los módulos **Categoría**, **Producto** y **Proveedor**, cada uno con arquitectura separada en `routers.py` / `schemas.py` / `services.py`.

## Instalación

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
```

## Ejecución

```bash
fastapi dev app/main.py
```

Servidor disponible en `http://localhost:8000`.

## Documentación interactiva (Swagger)

`http://localhost:8000/docs`

## Módulos

- **Categoría** — `app/modules/categoria/`
- **Producto** — `app/modules/producto/`
- **Proveedor** — `app/modules/proveedor/`

## Tests

Archivos `.http` de prueba (REST Client) en `tests/`.
