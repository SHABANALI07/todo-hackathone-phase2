# Server Manager Agent

**Purpose**: Automate starting, stopping, and monitoring backend and frontend development servers with proper environment configuration.

**Capabilities**:
- Start/stop backend FastAPI server with uvicorn
- Start/stop frontend Next.js development server
- Verify server health and readiness
- Monitor server logs
- Handle server restarts on configuration changes
- Manage environment variables

## Usage

### Start Backend Server

```bash
# From backend directory
cd backend
source venv/bin/activate
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or use the startup script
./backend/start.sh
```

### Start Frontend Server

```bash
# From frontend directory
cd frontend
npm run dev

# Or use the startup script
./frontend/start.sh
```

### Start Both Servers

```bash
# From project root
cd backend && ./start.sh &
cd ../frontend && ./start.sh &
```

## Workflows

### 1. Fresh Server Startup

**Input**: Project with backend and frontend configured
**Steps**:
1. Verify .env files exist (backend/.env, frontend/.env.local)
2. Activate Python virtual environment for backend
3. Load environment variables from .env
4. Start backend: `uvicorn src.main:app --reload --host 0.0.0.0 --port 8000`
5. Wait for backend health check: `curl http://localhost:8000/health`
6. Start frontend: `npm run dev` in frontend/
7. Wait for frontend ready: `curl http://localhost:3000`

**Output**: Both servers running and healthy

### 2. Server Health Check

**Input**: Running servers
**Steps**:
1. Check backend: `curl http://localhost:8000/health` → expect `{"status":"healthy"}`
2. Check frontend: `curl http://localhost:3000` → expect HTML response
3. Verify processes: `ps aux | grep uvicorn` and `ps aux | grep next`

**Output**: Server status report

### 3. Server Restart

**Input**: Configuration change or code update
**Steps**:
1. For backend: uvicorn auto-reloads with `--reload` flag
2. For frontend: Next.js auto-reloads on file changes
3. Manual restart: Kill processes and restart

**Commands**:
```bash
# Kill backend
pkill -f "uvicorn.*8000"

# Kill frontend
pkill -f "next.*dev"

# Restart
cd backend && ./start.sh &
cd frontend && ./start.sh &
```

**Output**: Servers restarted with new configuration

## Server Configuration

### Backend (FastAPI)

**Port**: 8000
**Host**: 0.0.0.0 (all interfaces)
**Reload**: Enabled in development
**Environment Variables**:
- `DATABASE_URL`: PostgreSQL connection string (must use `postgresql+asyncpg://`)
- `BETTER_AUTH_SECRET`: JWT signing secret (32+ characters)
- `ALLOWED_ORIGINS`: CORS allowed origins
- `LOG_LEVEL`: INFO, DEBUG, ERROR
- `DEBUG`: True/False

**Health Endpoint**: `GET /health` → `{"status":"healthy"}`
**API Docs**: `http://localhost:8000/docs` (Swagger UI)

### Frontend (Next.js)

**Port**: 3000
**Environment Variables**:
- `NEXT_PUBLIC_API_URL`: Backend API URL (http://localhost:8000)
- `BETTER_AUTH_SECRET`: Same as backend
- `BETTER_AUTH_URL`: Auth endpoint URL

## Error Handling

**Backend Won't Start**:
- Check if virtual environment is activated
- Verify DATABASE_URL format: `postgresql+asyncpg://...`
- Check if port 8000 is already in use: `lsof -i :8000`
- Verify all dependencies installed: `pip list`

**Frontend Won't Start**:
- Check if node_modules installed: `npm install`
- Verify port 3000 available: `lsof -i :3000`
- Check .env.local exists and has correct values

**Module Not Found Errors**:
- Backend: Ensure using venv uvicorn: `./venv/bin/uvicorn`
- Frontend: Reinstall dependencies: `npm install`

**Database Connection Errors**:
- Verify DATABASE_URL has `postgresql+asyncpg://` prefix
- Check database is accessible: `psql $DATABASE_URL -c "SELECT 1"`
- Verify SSL mode in connection string

## Monitoring

### Server Logs

**Backend logs**:
```bash
# View uvicorn logs
tail -f /tmp/uvicorn.log

# Or run with logging
uvicorn src.main:app --log-level debug
```

**Frontend logs**:
```bash
# Next.js logs to stdout
npm run dev | tee frontend.log
```

### Process Monitoring

```bash
# Check if servers are running
ps aux | grep -E "(uvicorn|next)"

# Check ports
lsof -i :8000  # Backend
lsof -i :3000  # Frontend

# Monitor resource usage
top -p $(pgrep -f uvicorn)
```

## Integration

This agent can be integrated with:
- Docker Compose for containerized deployment
- Systemd services for production deployment
- Process managers (PM2, supervisor) for reliability
- CI/CD pipelines for automated deployment

## Best Practices

1. **Always use virtual environment** for backend to avoid conflicts
2. **Use startup scripts** for consistency (`start.sh`)
3. **Check health endpoints** before running tests
4. **Monitor logs** for errors and warnings
5. **Graceful shutdown** with SIGTERM signal
6. **Auto-reload in development** for rapid iteration

## Related Skills

- `/skill:start-backend` - Quick backend server startup
- `/skill:start-frontend` - Quick frontend server startup
- `/skill:restart-servers` - Restart both servers
- `/skill:health-check` - Verify server health
- `/skill:view-logs` - Monitor server logs
