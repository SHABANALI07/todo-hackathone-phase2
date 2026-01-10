"""User model representing authenticated users.

This module defines the SQLModel entity for users stored in PostgreSQL.
"""

from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional


class User(SQLModel, table=True):
    """
    User entity representing an authenticated user account.

    Attributes:
        id: Unique user identifier (auto-generated)
        email: User's email address (unique, used for login)
        password_hash: Bcrypt hashed password
        full_name: Optional user's full name
        is_active: Account status (default: True)
        created_at: Account creation timestamp (auto-generated)
        updated_at: Last update timestamp
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255, nullable=False)
    password_hash: str = Field(nullable=False, max_length=255)
    full_name: Optional[str] = Field(default=None, max_length=200)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "full_name": "John Doe",
                "is_active": True,
                "created_at": "2026-01-09T00:00:00Z",
                "updated_at": "2026-01-09T00:00:00Z",
            }
        }
