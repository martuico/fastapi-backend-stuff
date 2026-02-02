"""Add a new column is_active queues table

Revision ID: dea8aca0ef6b
Revises: bba8a824d3d3
Create Date: 2026-02-02 14:03:20.328198

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dea8aca0ef6b"
down_revision: Union[str, Sequence[str], None] = "bba8a824d3d3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("queues", sa.Column("is_active", sa.Boolean, default=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("queues", "is_active")
    pass
