"""JWT token verification utilities.

This module provides functions to verify JWT tokens and extract user information.
"""

from jose import JWTError, jwt
from fastapi import HTTPException, status
import os
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Get secret from environment variable
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET", "default-secret-change-this")
ALGORITHM = "HS256"


def verify_token(token: str) -> int:
    """
    Verify JWT token and extract user_id.

    Args:
        token: JWT token string from Authorization header

    Returns:
        int: User ID extracted from token claims

    Raises:
        HTTPException: 401 Unauthorized if token is invalid or expired
    """
    try:
        logger.info(f"Verifying token: {token[:20]}..." if len(token) > 20 else f"Verifying token: {token}")

        # Decode the JWT token
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])

        logger.info(f"Decoded token payload: {payload}")

        # Extract user_id from 'sub' claim (standard JWT claim for subject/user ID)
        user_id: str = payload.get("sub")

        if user_id is None:
            logger.warning("Token missing user ID in 'sub' claim")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info(f"Extracted user_id: {user_id}")
        return int(user_id)

    except JWTError as e:
        logger.error(f"JWT Error: {str(e)}")
        logger.error(f"Token verification failed for token: {token[:30] if token else 'None'}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValueError as e:
        logger.error(f"Value Error: {str(e)}")
        logger.error(f"Invalid user ID format in token: {token[:30] if token else 'None'}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: user ID must be an integer",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Unexpected error during token verification: {str(e)}")
        logger.error(f"Token that caused error: {token[:30] if token else 'None'}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
