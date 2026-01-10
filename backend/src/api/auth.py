"""Authentication API endpoints.

This module provides REST API endpoints for user registration, login, and profile management.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.middleware.auth import get_current_user_id
from src.services.user_service import UserService
from src.models.auth_schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse,
    MessageResponse,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegisterRequest,
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    """
    Register a new user account.

    Creates a new user with the provided email and password, then returns
    a JWT access token for immediate authentication.

    Args:
        user_data: User registration information (email, password, optional full_name)
        session: Database session (injected)

    Returns:
        TokenResponse: JWT access token and user information

    Raises:
        HTTPException: 400 if email already exists
    """
    return await UserService.register_user(session, user_data)


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLoginRequest,
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    """
    Login with email and password.

    Authenticates a user with their credentials and returns a JWT access token.

    Args:
        login_data: User login credentials (email, password)
        session: Database session (injected)

    Returns:
        TokenResponse: JWT access token and user information

    Raises:
        HTTPException: 401 if credentials are invalid
        HTTPException: 403 if account is inactive
    """
    return await UserService.login_user(session, login_data)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    user_id: int = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Logout current user.

    Note: Since we use stateless JWT tokens, logout is handled client-side
    by removing the token. This endpoint exists for consistency and future
    token revocation features.

    Args:
        user_id: Current user ID from JWT token (injected)

    Returns:
        MessageResponse: Success message
    """
    return MessageResponse(message="Logged out successfully")


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """
    Get current authenticated user information.

    Retrieves the profile information of the currently authenticated user.

    Args:
        user_id: Current user ID from JWT token (injected)
        session: Database session (injected)

    Returns:
        UserResponse: Current user information

    Raises:
        HTTPException: 404 if user not found
        HTTPException: 401 if token is invalid
    """
    return await UserService.get_current_user(session, user_id)
