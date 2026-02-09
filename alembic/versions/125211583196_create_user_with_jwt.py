"""create user with jwt

Revision ID: 125211583196
Revises: dea8aca0ef6b
Create Date: 2026-02-09 14:45:28.021166

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op
from lib.auth import get_password_hash
from models.user import generate_user_id

# revision identifiers, used by Alembic.
revision: str = "125211583196"
down_revision: Union[str, Sequence[str], None] = "dea8aca0ef6b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    table = op.create_table(
        "users",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("username", sa.String, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("full_name", sa.String, nullable=False),
        sa.Column("password", sa.String, nullable=True),
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
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.bulk_insert(
        table,
        [
            {
                "id": generate_user_id(),
                "full_name": "Mar Tuico",
                "username": "mar@mail.com",
                "email": "mar@mail.com",
                "password": get_password_hash("hello"),
            }
        ],
    )

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    pass
