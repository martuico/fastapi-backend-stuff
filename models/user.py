from datetime import datetime
from typing import cast

from nanoid import generate
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


def generate_user_id() -> str:
    return cast(str, generate(size=18))


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(21),
        primary_key=True,
        default=generate_user_id,
    )

    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    full_name: Mapped[str] = mapped_column(String, nullable=False)

    password: Mapped[str] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    @property
    def is_active(self) -> bool:
        return self.deleted_at is None
