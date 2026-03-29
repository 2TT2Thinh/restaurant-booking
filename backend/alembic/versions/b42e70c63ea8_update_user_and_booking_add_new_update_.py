"""update user and booking add new update and forengkey for booking.py

Revision ID: b42e70c63ea8
Revises: 56a95498e586
Create Date: 2026-03-29 18:51:02.027402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b42e70c63ea8'
down_revision: Union[str, None] = '56a95498e586'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
