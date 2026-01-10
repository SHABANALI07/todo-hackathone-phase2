"""Task model representing a todo item with user ownership.

This module defines the SQLModel entity for tasks stored in PostgreSQL.
"""

from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional


class Task(SQLModel, table=True):
    """
    Task entity representing a todo item.

    Attributes:
        id: Unique task identifier (auto-generated)
        user_id: Owner user ID (required, foreign key to users table)
        title: Task title, 1-200 characters (required)
        description: Optional task details, max 1000 characters
        is_complete: Completion status (default: False)
        created_at: Creation timestamp (auto-generated)
        updated_at: Last update timestamp (auto-updated via DB trigger)
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(nullable=False, index=True)  # FK constraint created in SQL migration
    title: str = Field(min_length=1, max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_complete: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 42,
                "title": "Complete project proposal",
                "description": "Draft and submit the Q1 project proposal",
                "is_complete": False,
                "created_at": "2026-01-08T10:30:00Z",
                "updated_at": "2026-01-08T10:30:00Z",
            }
        }
