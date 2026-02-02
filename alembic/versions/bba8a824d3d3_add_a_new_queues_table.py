"""Add a new queues table

Revision ID: bba8a824d3d3
Revises: f2035dcfee68
Create Date: 2026-02-02 13:49:13.898219

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bba8a824d3d3"
down_revision: Union[str, Sequence[str], None] = "f2035dcfee68"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "queues",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("queues")
    pass
