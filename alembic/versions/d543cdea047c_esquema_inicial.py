"""esquema inicial

ID de revisión: d543cdea047c
Revisa a:
Fecha de creación: 2026-09-27 17:51:42.366199

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'd543cdea047c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Aplica el esquema."""
    op.create_table('categorias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('codigo', sqlmodel.sql.sqltypes.AutoString(length=6), nullable=False),
    sa.Column('descripcion', sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categorias_codigo'), 'categorias', ['codigo'], unique=True)
    op.create_table('productos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
    sa.Column('descripcion', sqlmodel.sql.sqltypes.AutoString(length=300), nullable=False),
    sa.Column('categoria', sqlmodel.sql.sqltypes.AutoString(length=6), nullable=False),
    sa.Column('precio', sa.Float(), nullable=False),
    sa.Column('stock', sa.Integer(), nullable=False),
    sa.Column('stock_minimo', sa.Integer(), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_productos_nombre'), 'productos', ['nombre'], unique=True)
    op.create_table('proveedores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('codigo', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
    sa.Column('razon_social', sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
    sa.Column('cuit', sqlmodel.sql.sqltypes.AutoString(length=15), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
    sa.Column('telefono', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_proveedores_codigo'), 'proveedores', ['codigo'], unique=True)


def downgrade() -> None:
    """Revierte el esquema."""
    op.drop_index(op.f('ix_proveedores_codigo'), table_name='proveedores')
    op.drop_table('proveedores')
    op.drop_index(op.f('ix_productos_nombre'), table_name='productos')
    op.drop_table('productos')
    op.drop_index(op.f('ix_categorias_codigo'), table_name='categorias')
    op.drop_table('categorias')
