#!/bin/bash
# Startup script for frontend development server
# Usage: ./start.sh

set -e

echo "🚀 Starting Todo App Frontend..."

# Change to frontend directory
cd "$(dirname "$0")"

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "⚠️  No .env.local file found. Copying from .env.local.example..."
    cp .env.local.example .env.local
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Run the development server
echo "✅ Starting Next.js development server on http://localhost:3000"
echo ""
npm run dev
