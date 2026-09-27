"""${message}

ID de revisión: ${up_revision}
Revisa a: ${down_revision | comma,n}
Fecha de creación: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, Sequence[str], None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """Aplica el esquema."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Revierte el esquema."""
    ${downgrades if downgrades else "pass"}
