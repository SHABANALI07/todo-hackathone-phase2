# Implementation Plan: Task CRUD Operations

**Branch**: `001-task-crud` | **Date**: 2026-01-08 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-task-crud/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement complete CRUD operations for task management with JWT-based authentication and strict user isolation. Users can create tasks with title and description, view their task list with status filtering, update task details, delete tasks, and toggle completion status. All operations enforce user_id filtering to ensure complete data isolation between users.

Primary technical approach: FastAPI backend with SQLModel ORM for Neon PostgreSQL, Next.js App Router frontend with TypeScript and Tailwind CSS. RESTful API endpoints under /api/tasks with JWT token verification middleware.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI 0.104+, SQLModel 0.0.14+, Pydantic 2.x, Next.js 14+ (App Router), Tailwind CSS 3.x, Better Auth (JWT), psycopg2/asyncpg (PostgreSQL driver)
**Storage**: Neon PostgreSQL (cloud-hosted)
**Testing**: pytest (backend), Jest + React Testing Library (frontend)
**Target Platform**: Web application (Linux/container for backend, browser for frontend)
**Project Type**: Web (frontend + backend monorepo)
**Performance Goals**: <2s task list load for 1000 tasks, <1s toggle completion, <10s task creation
**Constraints**: 100% user isolation enforcement, JWT required on all endpoints, <200ms API response p95, responsive mobile/desktop
**Scale/Scope**: Multi-user application, ~5 API endpoints, 1 database table (tasks), ~5 frontend pages/components

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Spec-Driven Development (NON-NEGOTIABLE)
- [x] Feature specification complete (spec.md)
- [x] Planning follows SDD workflow (spec → plan → tasks → implementation)
- [x] All code will be generated from specifications
- [x] No manual code changes planned

**Status**: PASS - Following SDD workflow, specification complete, plan precedes implementation.

### ✅ II. Security & User Isolation (NON-NEGOTIABLE)
- [x] JWT authentication via Better Auth
- [x] Every database query filters by user_id
- [x] API endpoints verify tokens before operations
- [x] 401 unauthorized for missing tokens
- [x] 403 forbidden for accessing other users' tasks

**Status**: PASS - All functional requirements (FR-009, FR-010, FR-015) enforce authentication and user isolation.

### ✅ III. Clean Architecture
- [x] Monorepo structure (frontend/ and backend/)
- [x] Frontend: Next.js App Router + TypeScript + Tailwind CSS
- [x] Backend: FastAPI + SQLModel + Neon PostgreSQL
- [x] RESTful API contracts at /api/tasks
- [x] Frontend communicates only through API
- [x] Database operations isolated to backend

**Status**: PASS - Clean separation between frontend and backend with defined API contract.

### ✅ IV. Reusable Intelligence (BONUS OBJECTIVE)
- [x] Plan includes agent/skill development for task operations
- [ ] Agent documentation (to be created during implementation)
- [ ] Skill implementation (to be created during implementation)

**Status**: PARTIAL - Planned for implementation phase. Will create reusable agent for task operations as per user request.

**GATE RESULT**: ✅ PASS - All NON-NEGOTIABLE principles satisfied. Bonus objective planned.

## Project Structure

### Documentation (this feature)

```text
specs/001-task-crud/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technology decisions)
├── data-model.md        # Phase 1 output (database schema)
├── quickstart.md        # Phase 1 output (setup and usage guide)
├── contracts/           # Phase 1 output (API specifications)
│   └── tasks-api.yaml   # OpenAPI spec for task endpoints
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   └── task.py          # Task SQLModel with user_id FK
│   ├── services/
│   │   ├── auth.py          # JWT token verification
│   │   └── task_service.py  # Task CRUD logic with user_id filtering
│   ├── api/
│   │   └── tasks.py         # FastAPI routes for /api/tasks
│   ├── middleware/
│   │   └── auth.py          # JWT authentication middleware
│   ├── database.py          # Neon PostgreSQL connection
│   └── main.py              # FastAPI app entry point
├── tests/
│   ├── test_task_api.py     # API endpoint tests
│   └── test_task_service.py # Service layer tests
├── requirements.txt         # Python dependencies
└── .env.example             # Environment variables template

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home/task list page
│   │   └── tasks/
│   │       ├── new/
│   │       │   └── page.tsx # Create task page
│   │       └── [id]/
│   │           └── page.tsx # Edit task page
│   ├── components/
│   │   ├── TaskList.tsx     # Task list with filtering
│   │   ├── TaskForm.tsx     # Create/edit task form
│   │   └── TaskItem.tsx     # Individual task display
│   └── lib/
│       ├── api.ts           # API client with JWT headers
│       └── types.ts         # TypeScript types for Task
├── tests/
│   └── components/
│       └── TaskList.test.tsx
├── package.json
├── tsconfig.json
└── tailwind.config.js

.specify/
└── agents/
    └── task-operations.md   # Reusable agent for task CRUD (bonus)
```

**Structure Decision**: Web application structure (Option 2) selected based on Next.js frontend + FastAPI backend architecture specified in constitution. Monorepo layout with clear separation between frontend/ and backend/ directories. Database operations centralized in backend, frontend communicates exclusively through RESTful API.

## Complexity Tracking

> No constitution violations - all principles satisfied. Table intentionally left empty.

