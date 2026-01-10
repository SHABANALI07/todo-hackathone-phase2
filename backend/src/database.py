"""Database connection and session management using SQLModel.

This module provides async database connection using SQLAlchemy's async engine
for PostgreSQL database with SSL support.
"""

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os
from typing import AsyncGenerator
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Check if using PostgreSQL (Neon) vs SQLite
if DATABASE_URL.startswith("postgresql"):
    # PostgreSQL connection with SSL support
    # For asyncpg, SSL is handled via the connection string parameters
    connect_args = {}
    logger.info("Using PostgreSQL with SSL connection")
else:
    # SQLite connection
    connect_args = {"check_same_thread": False}  # Required for SQLite
    logger.info("Using SQLite connection")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True if os.getenv("DEBUG", "False").lower() == "true" else False,
    connect_args=connect_args,
    pool_pre_ping=True  # Verify connections before use
)

# Async session maker
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function that yields database sessions.

    Usage in FastAPI route:
        @app.get("/endpoint")
        async def endpoint(session: AsyncSession = Depends(get_session)):
            ...

    Yields:
        AsyncSession: Database session
    """
    async with async_session_maker() as session:
        yield session


async def init_db():
    """
    Initialize database by creating all tables.

    This should be called on application startup.
    """
    logger.info("Initializing database...")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("Database initialized successfully")
