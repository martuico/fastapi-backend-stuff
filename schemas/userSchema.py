from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, computed_field


class User(BaseModel):
    username: str
    email: Annotated[str, EmailStr] | None = None
    full_name: str | None = None
    created_at: datetime | None = None
    deleted_at: datetime | None = None
    updated_at: datetime | None = None
    password: str | None = None

    @computed_field
    def is_active(self) -> bool:
        return self.deleted_at is None
