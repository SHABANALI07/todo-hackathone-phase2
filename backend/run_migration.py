"""Run database migration script for SQLite"""
import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Error: DATABASE_URL not set in .env file")
    exit(1)

# Extract database file path from URL (remove 'sqlite:///' prefix)
if DATABASE_URL.startswith('sqlite:///'):
    db_path = DATABASE_URL[len('sqlite:///'):]
else:
    print("Error: DATABASE_URL must start with 'sqlite:///'")
    exit(1)

# Read migration SQL (adapted for SQLite)
migration_sql = """
-- Migration: Create tasks table for SQLite
-- Created: 2026-01-08
-- Feature: Task CRUD Operations

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL CHECK(length(title) >= 1 AND length(title) <= 200),
    description TEXT CHECK(description IS NULL OR length(description) <= 1000),
    is_complete BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_user_id_status ON tasks(user_id, is_complete);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at DESC);

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Insert default test user (for existing tasks with user_id=1)
INSERT OR IGNORE INTO users (id, email, password_hash, full_name, is_active)
VALUES (1, 'test@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVCjDxJFa', 'Test User', 1);
"""

print("Connecting to database...")
try:
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Running migration...")
    cursor.executescript(migration_sql)
    conn.commit()

    print("✅ Migration completed successfully!")

    # Verify tables were created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('tasks', 'users')")
    tables = cursor.fetchall()
    print(f"✅ Tables verified: {[table[0] for table in tables]}")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"❌ Error running migration: {e}")
    exit(1)
