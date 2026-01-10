"""Task service layer for business logic and database operations.

This module implements CRUD operations for tasks with strict user isolation.
All methods require user_id and filter database queries accordingly.
"""

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from typing import List, Optional
import logging

# Set up logging
logger = logging.getLogger(__name__)

from src.models.task import Task
from src.models.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
)


class TaskService:
    """Service class for task CRUD operations with user isolation."""

    @staticmethod
    async def create_task(
        session: AsyncSession, user_id: int, task_data: TaskCreate
    ) -> TaskResponse:
        """
        Create a new task for the authenticated user.

        Args:
            session: Database session
            user_id: Authenticated user ID from JWT token
            task_data: Task creation data (title, description)

        Returns:
            TaskResponse: Created task with ID and timestamps

        Example:
            task = await TaskService.create_task(session, 42, TaskCreate(title="Todo"))
        """
        logger.info(f"Creating task for user_id: {user_id}")

        # Create Task model instance
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            is_complete=False,
        )

        # Add to session and commit
        session.add(task)
        await session.commit()
        await session.refresh(task)

        logger.info(f"Created task with id: {task.id} for user_id: {user_id}")
        return TaskResponse.model_validate(task)

    @staticmethod
    async def get_user_tasks(
        session: AsyncSession,
        user_id: int,
        status_filter: Optional[str] = None,
    ) -> TaskListResponse:
        """
        Get all tasks for the authenticated user with optional status filtering.

        Args:
            session: Database session
            user_id: Authenticated user ID from JWT token
            status_filter: Optional filter ('complete', 'incomplete', or None for all)

        Returns:
            TaskListResponse: List of tasks with counts

        Example:
            response = await TaskService.get_user_tasks(session, 42, "incomplete")
        """
        logger.info(f"Getting tasks for user_id: {user_id}, filter: {status_filter}")

        # Build query with user_id filter
        query = select(Task).where(Task.user_id == user_id)

        # Apply status filter if provided
        if status_filter == "complete":
            query = query.where(Task.is_complete == True)
        elif status_filter == "incomplete":
            query = query.where(Task.is_complete == False)

        # Order by created_at DESC (newest first)
        query = query.order_by(Task.created_at.desc())

        # Execute query
        result = await session.execute(query)
        tasks = result.scalars().all()

        logger.info(f"Found {len(tasks)} tasks for user_id: {user_id}")

        # Get total count (all user's tasks without filter)
        total_query = select(Task).where(Task.user_id == user_id)
        total_result = await session.execute(total_query)
        total_count = len(total_result.scalars().all())

        # Convert to response models
        task_responses = [TaskResponse.model_validate(task) for task in tasks]

        return TaskListResponse(
            tasks=task_responses,
            total_count=total_count,
            filtered_count=len(task_responses),
        )

    @staticmethod
    async def get_task_by_id(
        session: AsyncSession, user_id: int, task_id: int
    ) -> TaskResponse:
        """
        Get a single task by ID with ownership verification.

        Args:
            session: Database session
            user_id: Authenticated user ID from JWT token
            task_id: Task ID to retrieve

        Returns:
            TaskResponse: Task data

        Raises:
            HTTPException: 404 if task not found or 403 if not owned by user

        Example:
            task = await TaskService.get_task_by_id(session, 42, 1)
        """
        logger.info(f"Getting task {task_id} for user_id: {user_id}")

        # Query with user_id AND task_id to enforce ownership
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            logger.warning(f"Task {task_id} not found for user_id: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or access denied",
            )

        logger.info(f"Found task {task.id} for user_id: {user_id}")
        return TaskResponse.model_validate(task)

    @staticmethod
    async def update_task(
        session: AsyncSession, user_id: int, task_id: int, task_data: TaskUpdate
    ) -> TaskResponse:
        """
        Update an existing task with ownership verification.

        Args:
            session: Database session
            user_id: Authenticated user ID from JWT token
            task_id: Task ID to update
            task_data: Task update data (title, description)

        Returns:
            TaskResponse: Updated task

        Raises:
            HTTPException: 404 if task not found or 403 if not owned by user

        Example:
            task = await TaskService.update_task(session, 42, 1, TaskUpdate(title="New"))
        """
        logger.info(f"Updating task {task_id} for user_id: {user_id}")

        # Get task with ownership verification
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            logger.warning(f"Task {task_id} not found for user_id: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or access denied",
            )

        # Update only provided fields
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description

        # Commit changes (updated_at will be updated by DB trigger)
        await session.commit()
        await session.refresh(task)

        logger.info(f"Updated task {task.id} for user_id: {user_id}")
        return TaskResponse.model_validate(task)

    @staticmethod
    async def delete_task(session: AsyncSession, user_id: int, task_id: int) -> None:
        """
        Delete a task with ownership verification.

        Args:
            session: Database session
            user_id: Authenticated user ID from JWT token
            task_id: Task ID to delete

        Raises:
            HTTPException: 404 if task not found or 403 if not owned by user

        Example:
            await TaskService.delete_task(session, 42, 1)
        """
        logger.info(f"Deleting task {task_id} for user_id: {user_id}")

        # Get task with ownership verification
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            logger.warning(f"Task {task_id} not found for user_id: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or access denied",
            )

        # Delete task
        await session.delete(task)
        await session.commit()

        logger.info(f"Deleted task {task.id} for user_id: {user_id}")

    @staticmethod
    async def toggle_completion(
        session: AsyncSession, user_id: int, task_id: int
    ) -> TaskResponse:
        """
        Toggle task completion status with ownership verification.

        Args:
            session: Database session
            user_id: Authenticated user ID from JWT token
            task_id: Task ID to toggle

        Returns:
            TaskResponse: Updated task

        Raises:
            HTTPException: 404 if task not found or 403 if not owned by user

        Example:
            task = await TaskService.toggle_completion(session, 42, 1)
        """
        logger.info(f"Toggling completion for task {task_id} for user_id: {user_id}")

        # Get task with ownership verification
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            logger.warning(f"Task {task_id} not found for user_id: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or access denied",
            )

        # Toggle is_complete
        task.is_complete = not task.is_complete

        # Commit changes
        await session.commit()
        await session.refresh(task)

        logger.info(f"Toggled completion for task {task.id} for user_id: {user_id}")
        return TaskResponse.model_validate(task)
