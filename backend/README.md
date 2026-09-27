# Gestor de Productos — Unidad 5

API REST construida con **FastAPI**, **Pydantic v2** y **SQLModel**, con persistencia real en **PostgreSQL** gestionada por **Alembic**. Implementa los módulos **Categoría**, **Producto** y **Proveedor**, cada uno con arquitectura en capas: `routers.py` (HTTP) → `services.py` (reglas de negocio) → `models.py` (tabla SQLModel), con `schemas.py` definiendo el contrato Pydantic de entrada/salida.

## Stack

- FastAPI + Uvicorn
- Pydantic v2 / pydantic-settings
- SQLModel (SQLAlchemy + Pydantic)
- PostgreSQL 16
- Alembic (migraciones versionadas)
- psycopg (driver v3)

## Requisitos previos

- Python 3.11+
- PostgreSQL 16 corriendo localmente (o accesible por red)

## Puesta en marcha

### 1. Base de datos

Instalar PostgreSQL localmente (por ejemplo con `winget install PostgreSQL.PostgreSQL.16` en Windows, o el instalador oficial de [postgresql.org](https://www.postgresql.org/download/)) y crear la base:

```sql
CREATE DATABASE gestor_productos;
```

### 2. Entorno Python

Todos los comandos siguientes se ejecutan desde la carpeta `backend/`:

```bash
cd backend

python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Variables de entorno

Copiar `backend/.env.example` a `backend/.env` y ajustar según corresponda:

```
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/gestor_productos
```

### 4. Migraciones

```bash
alembic upgrade head
```

Crea las tablas `categorias`, `productos` y `proveedores`.

### 5. Levantar el servidor

```bash
fastapi dev app/main.py
```

Servidor disponible en `http://localhost:8000`. Al arrancar, verifica la conexión a la base y siembra dos categorías iniciales (`MUE-01`, `ELE-02`) si la tabla está vacía.

## Documentación interactiva

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Cada endpoint puede probarse desde "Try it out" sin herramientas externas; los schemas Pydantic (`ProductoCreate`, `ProductoRead`, `CategoriaCreate/Read`, `ProveedorCreate/Read`, etc.) se reflejan con sus constraints (`minLength`, `pattern`, `gt`, `ge`).

## Arquitectura

```
backend/
├── app/
│   ├── main.py                 # create_app(), lifespan (verifica DB + seed), routers
│   ├── core/
│   │   ├── config.py           # Settings (pydantic-settings), lee .env
│   │   ├── database.py         # engine, get_session(), SessionDep
│   │   └── seed.py             # seed idempotente de categorías iniciales
│   └── modules/
│       ├── categoria/  (models.py, schemas.py, services.py, routers.py)
│       ├── producto/   (idem)
│       └── proveedor/  (idem)
├── alembic/
│   ├── env.py
│   └── versions/
├── alembic.ini
├── requirements.txt
└── tests/
    ├── test_api.http
    └── test_proveedores.http
```

**Flujo por request:** `Router` recibe la petición HTTP e inyecta una `Session` (`SessionDep`), delega la validación de negocio en `Service`, que opera sobre el modelo `SQLModel` (`table=True`) contra PostgreSQL. Los schemas Pydantic son el contrato de entrada/salida — el modelo de base nunca se expone directamente.

## Endpoints

| Módulo      | Método | Ruta                           | Descripción                       | Código éxito |
| ----------- | ------ | ------------------------------ | --------------------------------- | ------------ |
| Categorías  | POST   | `/categorias/`                 | Alta                              | 201          |
| Categorías  | GET    | `/categorias/`                 | Listado paginado                  | 200          |
| Categorías  | GET    | `/categorias/{id}`             | Detalle                           | 200          |
| Categorías  | PUT    | `/categorias/{id}`             | Reemplazo total                   | 200          |
| Categorías  | PUT    | `/categorias/{id}/desactivar`  | Borrado lógico                    | 200          |
| Productos   | POST   | `/productos/`                  | Alta                              | 201          |
| Productos   | GET    | `/productos/`                  | Listado paginado                  | 200          |
| Productos   | GET    | `/productos/{id}`              | Detalle                           | 200          |
| Productos   | PUT    | `/productos/{id}`              | Reemplazo total                   | 200          |
| Productos   | PUT    | `/productos/{id}/desactivar`   | Borrado lógico                    | 200          |
| Productos   | GET    | `/productos/{id}/stock`        | Estado de stock                   | 200          |
| Proveedores | POST   | `/proveedores/`                | Alta                              | 201          |
| Proveedores | GET    | `/proveedores/`                | Listado paginado, filtro `activo` | 200          |
| Proveedores | GET    | `/proveedores/{id}`            | Detalle                           | 200          |
| Proveedores | PUT    | `/proveedores/{id}`            | Reemplazo total                   | 200          |
| Proveedores | PUT    | `/proveedores/{id}/desactivar` | Borrado lógico                    | 200          |

Todos los listados soportan paginación `skip`/`limit`. Recurso inexistente → 404. Body inválido → 422 (automático de Pydantic).

## Reglas de negocio implementadas

| Regla                                                       | Validación                            | Código |
| ----------------------------------------------------------- | -------------------------------------- | ------ |
| `nombre` de producto obligatorio, no vacío ni solo espacios | Pydantic (`min_length=1` + validador) | 422    |
| `precio` de producto mayor a 0                              | Pydantic (`gt=0`)                      | 422    |
| `nombre` de producto único                                  | Service + `UNIQUE` en tabla            | 409    |
| `codigo` de proveedor único                                 | Service + `UNIQUE` en tabla            | 409    |
| Proveedor ya desactivado no puede desactivarse de nuevo     | Service                                | 409    |
| Consultar/actualizar/desactivar un id inexistente           | Service (`None` → router traduce)      | 404    |
| Toda escritura persiste vía sesión SQLModel (`commit`)      | Service                                | —      |

## Decisiones de diseño

**`precio` usa `gt=0` en vez de `ge=0`.** Un producto de catálogo con precio 0 no representa un alta válida — sería un artículo regalado o un registro cargado a medias, y la API no tiene forma de distinguir ese caso de un error de carga. La validación con `gt=0` es estrictamente más restrictiva: todo lo que se esperaría rechazar (precio negativo) sigue devolviendo 422, y el único caso adicional que bloquea es `precio == 0`.

**`descripcion` se agregó a `Producto`** como campo opcional (`default=""`), para dejar el modelo alineado con lo que necesita consumir el frontend.

**Migraciones con Alembic** en vez de `create_all()` directo, para tener un esquema versionado y reversible. `init_db()` queda disponible en `backend/app/core/database.py` solo como utilidad de desarrollo, sin usarse en el arranque normal.

**Unicidad de `nombre` en Producto** (409 ante duplicado): no existía en la versión original y se agregó porque un catálogo con nombres repetidos no tiene forma clara de identificar productos distintos. Se implementa con `UNIQUE` en la columna más un chequeo previo en el service, que es el que decide el mensaje de error.

## Tests

`backend/tests/test_api.http` y `backend/tests/test_proveedores.http` — casos de REST Client (VS Code) que cubren alta, listado paginado, detalle, actualización, borrado lógico y los casos de error (404, 409, 422) de los tres módulos.

## Checklist de entrega

- [ ] `backend/venv/` y `__pycache__/` eliminados antes de comprimir
- [ ] `backend/.env` **no** incluido en el zip; `backend/.env.example` sí
- [ ] `backend/requirements.txt` incluye fastapi, uvicorn, sqlmodel y sqlalchemy
- [ ] Proyecto probado en limpio: clonar, seguir este README paso a paso, confirmar que levanta
