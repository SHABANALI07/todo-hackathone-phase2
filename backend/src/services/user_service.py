"""User service for authentication operations.

This module provides business logic for user registration, login, and password management.
"""

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
from typing import Optional
import logging

from src.models.user import User
from src.models.auth_schemas import UserRegisterRequest, UserLoginRequest, TokenResponse, UserResponse

# Set up logging
logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET", "default-secret-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24


class UserService:
    """Service class for user authentication operations."""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            str: Hashed password
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against a hash.

        Args:
            plain_password: Plain text password to verify
            hashed_password: Hashed password from database

        Returns:
            bool: True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(user_id: int) -> str:
        """
        Create a JWT access token for a user.

        Args:
            user_id: User ID to encode in token

        Returns:
            str: JWT access token
        """
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        to_encode = {
            "sub": str(user_id),
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        encoded_jwt = jwt.encode(to_encode, BETTER_AUTH_SECRET, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def register_user(
        session: AsyncSession, user_data: UserRegisterRequest
    ) -> TokenResponse:
        """
        Register a new user.

        Args:
            session: Database session
            user_data: User registration data

        Returns:
            TokenResponse: JWT token and user information

        Raises:
            HTTPException: 400 if email already exists
        """
        try:
            logger.info(f"Attempting to register user with email: {user_data.email}")

            # Check if email already exists
            query = select(User).where(User.email == user_data.email)
            result = await session.execute(query)
            existing_user = result.scalar_one_or_none()

            if existing_user:
                logger.warning(f"Registration failed: email {user_data.email} already exists")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

            # Create new user
            hashed_password = UserService.hash_password(user_data.password)
            new_user = User(
                email=user_data.email,
                password_hash=hashed_password,
                full_name=user_data.full_name,
                is_active=True,
            )

            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)

            logger.info(f"User {new_user.id} registered successfully")

            # Create access token
            access_token = UserService.create_access_token(new_user.id)

            # Return token response
            return TokenResponse(
                access_token=access_token,
                token_type="bearer",
                user=UserResponse.model_validate(new_user),
            )
        except HTTPException:
            # Re-raise HTTP exceptions as they are
            raise
        except Exception as e:
            logger.error(f"Unexpected error during user registration: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Registration failed due to server error",
            )

    @staticmethod
    async def login_user(
        session: AsyncSession, login_data: UserLoginRequest
    ) -> TokenResponse:
        """
        Authenticate a user and return JWT token.

        Args:
            session: Database session
            login_data: User login credentials

        Returns:
            TokenResponse: JWT token and user information

        Raises:
            HTTPException: 401 if credentials are invalid
        """
        try:
            logger.info(f"Attempting to login user with email: {login_data.email}")

            # Find user by email
            query = select(User).where(User.email == login_data.email)
            result = await session.execute(query)
            user = result.scalar_one_or_none()

            # Verify user exists and password is correct
            if not user or not UserService.verify_password(
                login_data.password, user.password_hash
            ):
                logger.warning(f"Login failed: invalid credentials for email {login_data.email}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Check if account is active
            if not user.is_active:
                logger.warning(f"Login failed: account {user.id} is inactive")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Account is inactive",
                )

            logger.info(f"User {user.id} logged in successfully")

            # Create access token
            access_token = UserService.create_access_token(user.id)

            # Return token response
            return TokenResponse(
                access_token=access_token,
                token_type="bearer",
                user=UserResponse.model_validate(user),
            )
        except HTTPException:
            # Re-raise HTTP exceptions as they are
            raise
        except Exception as e:
            logger.error(f"Unexpected error during user login: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Login failed due to server error",
            )

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
        """
        Get user by ID.

        Args:
            session: Database session
            user_id: User ID

        Returns:
            Optional[User]: User if found, None otherwise
        """
        try:
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                logger.debug(f"Found user by ID: {user_id}")
            else:
                logger.debug(f"User not found by ID: {user_id}")
            return user
        except Exception as e:
            logger.error(f"Error retrieving user by ID {user_id}: {str(e)}")
            return None

    @staticmethod
    async def get_current_user(session: AsyncSession, user_id: int) -> UserResponse:
        """
        Get current authenticated user information.

        Args:
            session: Database session
            user_id: User ID from JWT token

        Returns:
            UserResponse: User information

        Raises:
            HTTPException: 404 if user not found
        """
        try:
            logger.info(f"Retrieving user information for user_id: {user_id}")
            user = await UserService.get_user_by_id(session, user_id)

            if not user:
                logger.warning(f"User not found for user_id: {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )

            logger.info(f"Successfully retrieved user information for user_id: {user_id}")
            return UserResponse.model_validate(user)
        except HTTPException:
            # Re-raise HTTP exceptions as they are
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve user information",
            )
