# AROH AI DEVELOPMENT RULES

## Project

AROH — Adaptive Reservoir & Offset Intelligence Hub

SIH Problem Statement:
SIH26121 — eRTMAC-NWIS

---

# IMPORTANT

This repository is a multi-agent software project.

Multiple AI coding agents and human developers may work
on different parts of the project simultaneously.

The GitHub repository is the single source of truth.

Before making changes, read the relevant documentation
under /docs.

---

# RULES

1. Do not modify another agent's module unless explicitly
   requested.

2. Do not rewrite unrelated code.

3. Do not invent OIL operational data.

4. Prototype data must be clearly identified as
   demonstration/synthetic/public data.

5. Do not expose API keys, passwords or secrets.

6. Never commit secrets to GitHub.

7. Follow API_CONTRACT.md.

8. Follow ARCHITECTURE.md.

9. Follow UI_DESIGN.md.

10. Every significant feature must have tests.

11. Do not mark a task complete when tests fail.

12. Do not directly merge major features into main.

13. Use branches and pull requests for feature work.

14. Preserve backward compatibility where possible.

15. If an API changes, update the API contract.

16. If a database structure changes, update the database
    documentation.

17. AI predictions must show evidence where possible.

18. The system is decision support, not autonomous drilling
    control.

19. Never present AI-generated information as verified
    operational fact without supporting evidence.

20. If information is uncertain, clearly label it as uncertain.

---

# DEVELOPMENT PRINCIPLE

Situation
    ↓
Risk
    ↓
Evidence
    ↓
Context
    ↓
Decision Support

The interface should help an engineer understand a situation
quickly rather than forcing them to interact with a chatbot.

---

# CODE QUALITY

Prefer:

- simple architecture
- readable code
- typed interfaces
- reusable components
- meaningful variable names
- automated tests
- small commits

Avoid:

- unnecessary dependencies
- duplicated code
- huge files
- hard-coded production assumptions
- unnecessary complexity

---

# BEFORE COMPLETING A TASK

Check:

□ Requirements understood
□ Correct module modified
□ Tests written
□ Tests passing
□ API compatibility checked
□ Documentation updated
□ No secrets committed
□ GitHub issue updated
□ STATUS.md updated when appropriate
