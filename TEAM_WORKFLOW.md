# AROH Team Development Workflow

## Single Source of Truth

The GitHub repository is the authoritative source
for project requirements, architecture, API contracts,
implementation status and technical decisions.

Chat conversations are NOT authoritative.

---

# Before Starting Any Task

Every developer and AI agent MUST:

1. Pull the latest repository changes.
2. Read AGENTS.md.
3. Read docs/PROJECT.md.
4. Read docs/ARCHITECTURE.md.
5. Read docs/API_CONTRACT.md.
6. Read docs/STATUS.md.
7. Check assigned GitHub issue.
8. Check dependencies.

---

# Team Ownership

## Project Lead

Responsible for:
- integration
- architecture
- final merge
- resolving conflicts

## Frontend

Owns:
/frontend

## Backend

Owns:
/backend

## AI/Data

Owns:
/ai
/data

## Documentation

Owns:
/docs

---

# Branch Rules

Never develop major features directly on main.

Use feature branches.

Examples:

frontend/dashboard
frontend/offset-map
backend/well-api
backend/risk-api
ai/analogue-engine
ai/risk-engine

---

# Pull Requests

Every feature must use a Pull Request.

A Pull Request must explain:

- what changed
- files changed
- why it changed
- tests performed
- dependencies
- API changes
- known limitations

---

# Integration Rule

The project lead reviews changes before merging
into develop or main.

---

# Conflict Rule

If two agents disagree about:

- architecture
- API
- database structure
- technology
- domain logic

STOP implementation.

Do not independently choose.

The project lead decides and updates the relevant
documentation.

---

# No Duplicate Work

Before starting a feature:

Check GitHub Issues.

If another developer/agent is working on it,
do not implement the same feature.

---

# Completion Rule

A task is complete only when:

- implementation exists
- tests pass
- documentation is updated if required
- API contract is respected
- GitHub issue is updated
- Pull Request is ready
