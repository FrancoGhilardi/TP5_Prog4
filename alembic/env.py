from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlmodel import SQLModel

from alembic import context

from app.core.config import settings
from app.modules.categoria.models import Categoria  # noqa: F401
from app.modules.producto.models import Producto  # noqa: F401
from app.modules.proveedor.models import Proveedor  # noqa: F401

# objeto de configuración de Alembic, da acceso a los valores
# del archivo .ini en uso
config = context.config

# interpreta el archivo de configuración para el logging de Python
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.database_url)

# metadata de los modelos, usada por autogenerate para comparar
# el esquema de la base contra las clases SQLModel
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Corre las migraciones en modo 'offline'.

    Configura el contexto solo con una URL, sin crear un Engine.
    Las llamadas a context.execute() emiten el SQL directamente
    a la salida del script.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Corre las migraciones en modo 'online', usando un Engine real."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
