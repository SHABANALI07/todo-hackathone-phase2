---
id: 0001
title: Initial constitution for todo hackathon
stage: constitution
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5
feature: none
branch: main
user: shaban
command: /sp.constitution
labels: ["constitution", "initialization", "project-setup", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```text
# Todo Hackathon Phase II Constitution

## Project
Full-stack multi-user web todo app with authentication and persistent storage.

## Core Principles
- Spec-Driven: All code from specs via Claude – no manual coding.
- Secure: JWT auth, user isolation (only own tasks).
- Clean Architecture: Monorepo with frontend/backend separation.
- Reusable Intelligence: Agents and skills for task operations (bonus points).

## Key Standards
- Frontend: Next.js App Router, TypeScript, Tailwind CSS
- Backend: FastAPI, SQLModel, Neon PostgreSQL
- Auth: Better Auth with JWT tokens
- API: REST endpoints under /api/tasks with user filtering
- Database: tasks table with user_id foreign key

## Constraints
- No manual code changes
- All API calls require valid JWT
- Data filtered by authenticated user_id
- Shared secret: BETTER_AUTH_SECRET env var

## Success Criteria
- Login/signup working
- Task CRUD for logged-in user only
- Data persists in Neon DB
- Agents/skills implemented
- Responsive UI
- All from specs
```

## Response snapshot

Successfully created the project constitution at `.specify/memory/constitution.md` version 1.0.0.

The constitution establishes four core principles:
1. **Spec-Driven Development (NON-NEGOTIABLE)**: All code generated from specifications via Claude Code agents
2. **Security & User Isolation (NON-NEGOTIABLE)**: JWT authentication with complete user data isolation
3. **Clean Architecture**: Monorepo with Next.js frontend and FastAPI backend
4. **Reusable Intelligence (BONUS)**: Agents and skills for workflow automation

The document includes comprehensive sections on:
- Technology stack (Next.js, FastAPI, Neon PostgreSQL, Better Auth)
- Development, security, and quality constraints
- Six-part success criteria covering auth, CRUD, persistence, UX, advanced features, and compliance
- Governance rules for amendments, compliance verification, versioning, PHR creation, and ADR management

Template validation confirms alignment with plan-template.md, spec-template.md, and tasks-template.md.

## Outcome

- ✅ Impact: Initial project constitution ratified, establishing governance framework and core principles for Todo Hackathon Phase II
- 🧪 Tests: No tests required for constitution document
- 📁 Files: Created `.specify/memory/constitution.md` (version 1.0.0)
- 🔁 Next prompts: `/sp.specify` to create feature specifications, `/sp.plan` for implementation planning
- 🧠 Reflection: Constitution provides clear guidance for spec-driven development with strong security requirements. All four principles are testable and actionable.

## Evaluation notes (flywheel)

- Failure modes observed: None - template fully populated with no unresolved placeholders
- Graders run and results (PASS/FAIL): Template validation PASS - all dependent templates align with constitution principles
- Prompt variant (if applicable): Standard constitution creation from user-provided principles
- Next experiment (smallest change to try): Apply constitution to first feature specification to validate governance workflow
