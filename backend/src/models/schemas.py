"""Pydantic schemas for API request and response validation.

This module defines the data transfer objects (DTOs) for Task CRUD operations.
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import List, Optional


class TaskCreate(BaseModel):
    """Request model for creating a new task."""

    title: str = Field(min_length=1, max_length=200, description="Task title (required)")
    description: Optional[str] = Field(None, max_length=1000, description="Task description (optional)")

    @field_validator("title")
    @classmethod
    def title_not_whitespace(cls, v: str) -> str:
        """Ensure title is not only whitespace."""
        if not v.strip():
            raise ValueError("Title cannot be only whitespace")
        return v.strip()

    @field_validator("description")
    @classmethod
    def clean_description(cls, v: Optional[str]) -> Optional[str]:
        """Trim description whitespace."""
        if v:
            stripped = v.strip()
            return stripped if stripped else None
        return None

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "title": "Complete project proposal",
                "description": "Draft and submit the Q1 project proposal",
            }
        }


class TaskUpdate(BaseModel):
    """Request model for updating an existing task."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

    @field_validator("title")
    @classmethod
    def title_not_whitespace(cls, v: Optional[str]) -> Optional[str]:
        """Ensure title is not only whitespace if provided."""
        if v is not None:
            if not v.strip():
                raise ValueError("Title cannot be only whitespace")
            return v.strip()
        return None

    @field_validator("description")
    @classmethod
    def clean_description(cls, v: Optional[str]) -> Optional[str]:
        """Trim description whitespace."""
        if v:
            stripped = v.strip()
            return stripped if stripped else None
        return None

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "title": "Complete project proposal by Friday",
                "description": "Draft, review, and submit by EOD Friday",
            }
        }


class TaskResponse(BaseModel):
    """Response model for a single task."""

    id: int
    title: str
    description: Optional[str]
    is_complete: bool
    created_at: datetime
    updated_at: datetime
    user_id: int  # Included for reference, but never editable via API

    class Config:
        """Pydantic configuration."""

        from_attributes = True  # Enable ORM mode for SQLModel conversion
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Complete project proposal",
                "description": "Draft and submit the Q1 project proposal",
                "is_complete": False,
                "created_at": "2026-01-08T10:30:00Z",
                "updated_at": "2026-01-08T10:30:00Z",
                "user_id": 42,
            }
        }


class TaskListResponse(BaseModel):
    """Response model for task list."""

    tasks: List[TaskResponse]
    total_count: int
    filtered_count: int  # Count after applying status filter

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": 1,
                        "title": "Complete project proposal",
                        "description": "Draft and submit the Q1 project proposal",
                        "is_complete": False,
                        "created_at": "2026-01-08T10:30:00Z",
                        "updated_at": "2026-01-08T10:30:00Z",
                        "user_id": 42,
                    }
                ],
                "total_count": 10,
                "filtered_count": 1,
            }
        }
