"""Authentication middleware for JWT token verification.

This module provides middleware and dependency functions to verify JWT tokens
and inject user_id into request processing.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.services.auth import verify_token

# HTTP Bearer token extractor
security = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    """
    Dependency function that extracts and verifies JWT token from Authorization header.

    This function should be used as a FastAPI dependency in route handlers that
    require authentication.

    Usage:
        @app.get("/api/tasks")
        async def get_tasks(user_id: int = Depends(get_current_user_id)):
            # user_id is now available and verified
            ...

    Args:
        credentials: HTTP Bearer token credentials from Authorization header

    Returns:
        int: Verified user ID from JWT token

    Raises:
        HTTPException: 401 Unauthorized if token is missing or invalid
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract token and verify it
    token = credentials.credentials
    user_id = verify_token(token)

    return user_id
