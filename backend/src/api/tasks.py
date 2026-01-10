"""Task API endpoints with JWT authentication.

This module defines all RESTful API routes for task CRUD operations.
All endpoints require JWT authentication and enforce user isolation.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.database import get_session
from src.middleware.auth import get_current_user_id
from src.services.task_service import TaskService
from src.models.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
)

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task for the authenticated user with title and optional description.",
)
async def create_task(
    task_data: TaskCreate,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Create a new task.

    - **title**: Task title (required, 1-200 characters)
    - **description**: Optional task description (max 1000 characters)

    Returns the created task with ID and timestamps.
    """
    return await TaskService.create_task(session, user_id, task_data)


@router.get(
    "",
    response_model=TaskListResponse,
    summary="Get task list",
    description="Get all tasks for the authenticated user with optional status filtering.",
)
async def get_tasks(
    status_filter: Optional[str] = None,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TaskListResponse:
    """
    Get task list for authenticated user.

    - **status**: Optional filter ('complete', 'incomplete', or omit for all)

    Returns list of tasks with counts.
    """
    return await TaskService.get_user_tasks(session, user_id, status_filter)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get single task",
    description="Get a specific task by ID with ownership verification.",
)
async def get_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Get a single task by ID.

    - **task_id**: Task ID to retrieve

    Returns the task if owned by authenticated user, otherwise 404.
    """
    return await TaskService.get_task_by_id(session, user_id, task_id)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update task",
    description="Update an existing task's title and/or description.",
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Update an existing task.

    - **task_id**: Task ID to update
    - **title**: New title (optional)
    - **description**: New description (optional)

    Returns the updated task.
    """
    return await TaskService.update_task(session, user_id, task_id, task_data)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    description="Permanently delete a task.",
)
async def delete_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> None:
    """
    Delete a task.

    - **task_id**: Task ID to delete

    Returns 204 No Content on success.
    """
    await TaskService.delete_task(session, user_id, task_id)


@router.patch(
    "/{task_id}/toggle",
    response_model=TaskResponse,
    summary="Toggle task completion",
    description="Toggle the completion status of a task.",
)
async def toggle_task_completion(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Toggle task completion status.

    - **task_id**: Task ID to toggle

    Returns the updated task with toggled is_complete field.
    """
    return await TaskService.toggle_completion(session, user_id, task_id)
