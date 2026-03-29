"""add updated_at to user

Revision ID: fc8ff015b4fa
Revises: b42e70c63ea8
Create Date: 2026-03-29 18:57:12.509111

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc8ff015b4fa'
down_revision: Union[str, None] = 'b42e70c63ea8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
