"""create tickets table

Revision ID: f2035dcfee68
Revises:
Create Date: 2026-02-02 13:10:47.736094

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f2035dcfee68"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ticket_status = postgresql.ENUM("waiting", "called", "served", name="ticket_status", create_type=False)


def upgrade() -> None:
    """Upgrade schema."""
    ticket_status.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "tickets",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("queue_id", sa.Integer, nullable=False, index=True),
        sa.Column("ticket_number", sa.String(10), nullable=False, unique=True),
        sa.Column("status", ticket_status, nullable=False, server_default="waiting"),
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
    op.drop_table("tickets")

    ticket_status.drop(op.get_bind(), checkfirst=True)
    pass
