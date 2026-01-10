"""FastAPI application entry point.

This module initializes the FastAPI application with CORS middleware,
authentication middleware, and route registration.
"""

import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import database initialization
from src.database import init_db

# Initialize FastAPI app
app = FastAPI(
    title="Todo API",
    description="Task CRUD Operations API with JWT authentication",
    version="1.0.0",
)

# Get allowed origins from environment variable
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000"
).split(",")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    """Initialize database on application startup."""
    await init_db()


@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Status message indicating API is healthy
    """
    return {"status": "healthy"}


# Register API routes
from src.api import tasks, auth

app.include_router(auth.router)
app.include_router(tasks.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
