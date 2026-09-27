# TP5 — Unidad 5

Trabajo práctico integrador: **Gestor de Productos**. Dos proyectos independientes en este repositorio.

| Parte | Carpeta         | Contenido                                                          | README                            |
| ----- | --------------- | ------------------------------------------------------------------- | ---------------------------------- |
| A     | `backend/`       | API REST (FastAPI + SQLModel + PostgreSQL) — Categorías, Productos, Proveedores | [backend/README.md](backend/README.md) |
| B     | `tp-productos/`  | Pantalla de Productos maquetada (React + TypeScript + Tailwind CSS), sin conexión a la API | [tp-productos/README.md](tp-productos/README.md) |

## Orden para levantar ambos

Los dos proyectos son independientes entre sí — la Parte B no consume la Parte A en esta entrega — pero si se quieren tener corriendo a la vez:

```bash
# Terminal 1 — backend
cd backend
pip install -r requirements.txt
alembic upgrade head
fastapi dev app/main.py          # http://localhost:8000 (docs en /docs)

# Terminal 2 — frontend
cd tp-productos
pnpm install
pnpm dev                          # http://localhost:5173
```

Cada carpeta tiene su propio README con el detalle de stack, arquitectura, decisiones de diseño y checklist de entrega.

## Estructura del repositorio

```
TP5_Franco_Ghilardi/
├── backend/            # Parte A — API REST
├── tp-productos/        # Parte B — Frontend React
├── CLAUDE.md            # Guía para Claude Code (convenciones de ambos proyectos)
└── TP Integrador Unidad 5.pdf
```
