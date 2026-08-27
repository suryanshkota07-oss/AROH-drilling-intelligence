# AROH Team Development Workflow

## 1. Single Source of Truth

The GitHub repository is the single source of truth for:

- Project requirements
- Architecture
- API contracts
- UI rules
- Domain definitions
- Development status
- Technical decisions

ChatGPT, Claude, Gemini, or any other AI conversation is NOT
the source of truth.

AI agents must read the repository before making changes.

---

# 2. Before Starting ANY Task

Every developer and AI agent must:

1. Pull the latest changes.
2. Read `AGENTS.md`.
3. Read `docs/PROJECT.md`.
4. Read `docs/ARCHITECTURE.md`.
5. Read `docs/API_CONTRACT.md`.
6. Read `docs/DOMAIN_RULES.md`.
7. Read `docs/STATUS.md`.
8. Read this file.
9. Check GitHub Issues.
10. Work only on the assigned task.

---

# 3. Team Roles

## Project Lead

Responsible for:

- Overall architecture
- Integration
- GitHub repository
- Final review
- Conflict resolution
- Final demo
- Main branch

## Frontend Developer

Owns:

`/frontend`

Responsible for:

- React application
- Dashboard
- Navigation
- Charts
- Maps
- Risk interface
- Evidence interface

## Backend Developer

Owns:

`/backend`

Responsible for:

- FastAPI
- API endpoints
- Data services
- WebSocket
- Backend testing

## AI/Data Developer

Owns:

`/ai`
`/data`

Responsible for:

- Demonstration datasets
- Analogue matching
- Risk engine
- Evidence retrieval
- AI/RAG prototype

---

# 4. Branch Strategy

Never develop major features directly on `main`.

Use:

`main`
↓
`develop`
↓
feature branches

Examples:

`feature/command-center`

`feature/well-api`

`feature/offset-map`

`feature/analogue-engine`

`feature/risk-ahead`

`feature/evidence-engine`

---

# 5. Before Creating a Feature

Check GitHub Issues.

If another developer is already working on the feature,
do not duplicate the work.

---

# 6. AI Agent Rules

AI agents must:

- Read repository documentation first.
- Inspect existing code before creating files.
- Reuse existing components where possible.
- Follow the existing architecture.
- Follow the API contract.
- Avoid modifying unrelated modules.
- Never delete another developer's work.
- Never invent OIL operational data.
- Never commit API keys or secrets.
- Never claim synthetic data is real OIL data.

---

# 7. API Rule

The API contract is shared between frontend and backend.

If an API needs to change:

1. Discuss the change with the project lead.
2. Update `docs/API_CONTRACT.md`.
3. Update affected frontend/backend code.
4. Test the integration.

Do not silently change API structures.

---

# 8. Pull Request Rule

Completed features must be submitted through a Pull Request.

The Pull Request must contain:

- What was changed
- Why it was changed
- Files modified
- Tests performed
- Known limitations
- API changes, if any

---

# 9. Review Rule

The project lead reviews Pull Requests before merging.

Check:

- Does it work?
- Does it follow the architecture?
- Does it break another module?
- Does it follow the API contract?
- Are tests passing?
- Is documentation updated?

---

# 10. Integration

Feature branch
↓
Pull Request
↓
Project Lead Review
↓
develop
↓
Integration Testing
↓
main

---

# 11. Status

After completing significant work:

Update:

`docs/STATUS.md`

Do not randomly claim a percentage.

Progress should be based on completed GitHub Issues.

---

# 12. Conflict Resolution

If developers or AI agents disagree about:

- Architecture
- Technology
- API design
- Data structure
- Domain logic

STOP implementation.

The project lead decides.

The decision must then be documented.

---

# 13. Prototype Data

The SIH prototype may use:

- Synthetic data
- Public data
- Demonstration data

All synthetic/demo data must be clearly identified.

Never present demonstration data as actual OIL operational data.

---

# 14. Safety

AROH is a decision-support prototype.

It does NOT autonomously control drilling equipment.

AI recommendations must be presented as decision support
and should include evidence and uncertainty where possible.

---

# 15. Completion Checklist

A task is complete only when:

[ ] Feature implemented

[ ] Code tested

[ ] Existing functionality still works

[ ] API contract respected

[ ] Documentation updated if required

[ ] STATUS.md updated if significant

[ ] GitHub Issue updated

[ ] Pull Request created