# Clinical Data Reconciliation Engine — Work Plan

## TL;DR

> **Quick Summary**: Build a full-stack Clinical Data Reconciliation Engine for a take-home assessment. Python/FastAPI backend with two AI-powered endpoints (medication reconciliation + data quality scoring), React/TypeScript frontend dashboard, GitHub Models (GPT-4o) + Anthropic Claude as LLM providers, SQLite for persistence and caching.
> 
> **Deliverables**:
> - Python/FastAPI REST API with 2 endpoints + auth + input validation
> - LLM integration (GitHub Models primary, Anthropic fallback, mock mode)
> - React/TypeScript dashboard with reconciliation results + quality scores
> - 8-10 unit/integration tests (pytest + Vitest)
> - README with setup instructions, architecture diagram, design decisions
> 
> **Estimated Effort**: Medium-Large (6 day budget)
> **Parallel Execution**: YES - 6 waves
> **Critical Path**: Task 1 → Task 2 → Task 5 → Task 7 → Task 10 → Task 13 → Task 17 → Task 18

---

## Context

### Original Request
Build a full-stack application for a take-home assessment: "Clinical Data Reconciliation Engine (Mini Version)" for a Full Stack Developer - EHR Integration Intern role. The engine uses AI to determine the most likely accurate patient information when conflicting data exists across healthcare systems. 6-day time limit. Submit as GitHub repository with code + README.

### Interview Summary
**Key Discussions**:
- **Backend**: User prefers Python + FastAPI (not TypeScript backend)
- **Frontend**: React + Vite + TypeScript (recommended)
- **AI Provider**: User has GitHub Copilot student benefit (GitHub Models for free GPT-4o access) + Claude subscription (Anthropic API). No OpenAI subscription.
- **Strategy**: GitHub Models as primary, Anthropic as fallback
- **Database**: SQLite for persistence (user preference over in-memory)
- **Testing**: pytest for backend, Vitest for frontend, TDD approach
- **Docker**: Skip for now, possibly add later as bonus
- **Mock mode**: Both mock + real API support for development and demo

**Research Findings**:
- Node.js v24, Python 3.12, pnpm available on system (WSL2)
- Empty workspace — greenfield project
- Docker not configured in WSL2 (skip for now)
- GitHub Models provides GPT-4o via `https://models.inference.ai.azure.com` endpoint with GitHub PAT
- Assessment's "EHR Data" link refers to PyHealth data structures: `https://pyhealth.readthedocs.io/en/latest/api/data.html` — use as reference for EHR data modeling concepts (Event, Patient), NOT as a runtime dependency

### Metis Review
**Identified Gaps** (addressed):
- FHIR compliance depth → Using simplified FHIR-inspired flat schemas (not full R4 nesting)
- GitHub Models API access must be validated early → Task 2 includes API validation step
- LLM response structure → Using `response_format: json_object` with Pydantic validation
- Frontend scope → Single-page two-panel layout (no router)
- CORS configuration needed → Included in backend setup
- Error response format → Standardized error envelope defined
- Mock scenarios → 3 pre-built scenarios shipped for demo/testing
- Rate limiting behavior → 429 response with Retry-After header
- Empty/edge input handling → Comprehensive edge case handling in each service

---

## Work Objectives

### Core Objective
Build a submission-ready full-stack Clinical Data Reconciliation Engine that scores highly on Code Quality (30%), AI Integration (25%), Problem Solving (25%), and Product Thinking (20%).

### Concrete Deliverables
- `POST /api/reconcile/medication` — Reconcile conflicting medication records with AI reasoning
- `POST /api/validate/data-quality` — Score patient data quality (0-100) across 4 dimensions
- `GET /api/health` — Health check endpoint
- LLM provider abstraction (GitHub Models + Anthropic + Mock)
- LLM response caching (SQLite-backed, TTL)
- React dashboard: reconciliation panel + data quality panel
- Approve/reject AI suggestions UI
- Confidence score + reasoning visualization
- Red/yellow/green data quality indicators
- 8-10 automated tests (pytest + Vitest)
- API key authentication (`X-API-Key` header)
- `.env.example` with all configuration
- README with: setup (<5 commands), architecture diagram, design decisions, trade-offs, what you'd improve

### Definition of Done
- [ ] `cd backend && python -m pytest tests/ -v` → all tests PASS
- [ ] `cd frontend && pnpm test` → all tests PASS
- [ ] `curl http://localhost:8000/api/health` → `{"status": "ok"}`
- [ ] Both endpoints return correct response shapes with mock mode
- [ ] Frontend loads at `http://localhost:5173` without errors
- [ ] Dashboard shows reconciliation results + data quality scores
- [ ] README contains all required sections
- [ ] Git history has clean atomic commits

### Must Have
- Clean, modular code architecture (layered: routes → services → models)
- Input validation via Pydantic models with meaningful error messages
- At least 5 unit tests covering core logic (targeting 8-10)
- Basic authentication via `X-API-Key` header
- README with setup instructions and design decisions
- Mock mode that works with ZERO API keys (evaluator can demo immediately)
- Error handling: rate limits, malformed AI output, empty input, timeouts
- CORS middleware (frontend port 5173 → backend port 8000)
- Standardized error response: `{"detail": {"code": "string", "message": "string"}}`

### Must NOT Have (Guardrails)
- NO `fhir.resources` library import — use simplified flat schemas
- NO react-router, Redux, or heavy state management — `useState`/`useReducer` only
- NO Docker, webhooks, duplicate detection, or deployment until ALL core features have tests
- NO Alembic migrations — `SQLModel.metadata.create_all()` is sufficient
- NO comprehensive JSDoc/docstrings on every function — targeted docstrings on public service methods only
- NO user auth system (JWT/OAuth) — API key header check only
- NO Material UI, Ant Design, or Chakra — Tailwind CSS or CSS modules only
- NO over-abstraction or premature generalization — keep it direct and readable
- NO `# type: ignore` or `as any` — proper types throughout
- NO console.log in production code — use proper logging
- NO commented-out code in final submission

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.
> Acceptance criteria requiring "user manually tests/confirms" are FORBIDDEN.

### Test Decision
- **Infrastructure exists**: NO (greenfield — setting up)
- **Automated tests**: YES (TDD)
- **Backend Framework**: pytest with TestClient + in-memory SQLite overrides
- **Frontend Framework**: Vitest + @testing-library/react + jsdom
- **TDD Flow**: Each feature task follows RED (failing test) → GREEN (minimal impl) → REFACTOR
- **Target**: 4 backend tests + 3 frontend tests + 2 integration tests = 9 total

### QA Policy
Every task MUST include agent-executed QA scenarios. Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Backend API**: Use Bash (curl) — Send requests, assert status + response fields
- **Frontend/UI**: Use Playwright (playwright skill) — Navigate, interact, assert DOM, screenshot
- **LLM Integration**: Use Bash (python REPL) — Import provider, call with test input, validate output
- **Database**: Use Bash (sqlite3 CLI) — Query tables, verify schema and data

### Response Shapes (exact assessment spec)

**Reconciliation Response**:
```json
{
  "reconciled_medication": "string",
  "confidence_score": 0.88,
  "reasoning": "string",
  "recommended_actions": ["string"],
  "clinical_safety_check": "PASSED | FAILED | WARNING"
}
```

**Data Quality Response**:
```json
{
  "overall_score": 62,
  "breakdown": {
    "completeness": 60,
    "accuracy": 50,
    "timeliness": 70,
    "clinical_plausibility": 40
  },
  "issues_detected": [
    {"field": "string", "issue": "string", "severity": "low | medium | high"}
  ]
}
```

**Error Response**:
```json
{
  "detail": {"code": "VALIDATION_ERROR", "message": "string", "errors": []}
}
```

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — scaffolding):
├── Task 1: Project structure + git init + .gitignore [quick]
├── Task 2: Backend scaffolding (FastAPI, config, deps, health check) [quick]
└── Task 3: Frontend scaffolding (Vite, React, TypeScript, Vitest, Tailwind) [quick]

Wave 2 (After Wave 1 — data models + abstractions, MAX PARALLEL):
├── Task 4: Pydantic schemas for reconciliation + data quality [quick]
├── Task 5: SQLite database + SQLModel tables (cache, results) [quick]
├── Task 6: LLM provider abstraction (interface + MockProvider + factory) [deep]
├── Task 7: API key authentication middleware [quick]
└── Task 8: Frontend TypeScript types + API client skeleton [quick]

Wave 3 (After Wave 2 — core backend features):
├── Task 9: POST /api/reconcile/medication (route + service + 2 tests) [deep]
├── Task 10: POST /api/validate/data-quality (route + service + 2 tests) [deep]
└── Task 11: LLM response caching service (SQLite-backed, TTL) [unspecified-high]

Wave 4 (After Wave 3 — AI integration + frontend UI, MAX PARALLEL):
├── Task 12: Real LLM providers (GitHub Models + Anthropic) + prompt templates [deep]
├── Task 13: Reconciliation dashboard panel (results, confidence, approve/reject) [visual-engineering]
├── Task 14: Data quality dashboard panel (scores, indicators, breakdown) [visual-engineering]
└── Task 15: Mock data scenarios (3 pre-built for demo/testing) [quick]

Wave 5 (After Wave 4 — integration + polish):
├── Task 16: Frontend-backend wiring (CORS, hooks, API integration) [unspecified-high]
├── Task 17: Error handling + edge cases + loading/error UI states [unspecified-high]
└── Task 18: Frontend component tests (3 Vitest tests) [quick]

Wave 6 (After Wave 5 — documentation):
└── Task 19: README + architecture diagram + design decisions document [writing]

Wave FINAL (After ALL tasks — independent review, 4 parallel):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (unspecified-high)
├── Task F3: Real manual QA (unspecified-high)
└── Task F4: Scope fidelity check (deep)

Critical Path: T1 → T2 → T5 → T6 → T9 → T12 → T16 → T17 → T19 → FINAL
Parallel Speedup: ~65% faster than sequential
Max Concurrent: 5 (Waves 2 & 4)
```

### Dependency Matrix

| Task | Depends On | Blocks | Wave |
|------|-----------|--------|------|
| 1 | — | 2, 3 | 1 |
| 2 | 1 | 4, 5, 6, 7 | 1 |
| 3 | 1 | 8 | 1 |
| 4 | 2 | 9, 10 | 2 |
| 5 | 2 | 6, 9, 10, 11 | 2 |
| 6 | 2, 5 | 9, 10, 11, 12 | 2 |
| 7 | 2 | 9, 10 | 2 |
| 8 | 3 | 13, 14, 16 | 2 |
| 9 | 4, 5, 6, 7 | 12, 16 | 3 |
| 10 | 4, 5, 6, 7 | 12, 16 | 3 |
| 11 | 5, 6 | 12 | 3 |
| 12 | 6, 9, 10, 11 | 16 | 4 |
| 13 | 8 | 16, 18 | 4 |
| 14 | 8 | 16, 18 | 4 |
| 15 | 4 | 16 | 4 |
| 16 | 9, 10, 12, 13, 14, 15 | 17, 18 | 5 |
| 17 | 16 | 19 | 5 |
| 18 | 13, 14, 16 | 19 | 5 |
| 19 | 17, 18 | FINAL | 6 |
| F1-F4 | ALL | — | FINAL |

### Agent Dispatch Summary

- **Wave 1 (3)**: T1 → `quick`, T2 → `quick`, T3 → `quick`
- **Wave 2 (5)**: T4 → `quick`, T5 → `quick`, T6 → `deep`, T7 → `quick`, T8 → `quick`
- **Wave 3 (3)**: T9 → `deep`, T10 → `deep`, T11 → `unspecified-high`
- **Wave 4 (4)**: T12 → `deep`, T13 → `visual-engineering`, T14 → `visual-engineering`, T15 → `quick`
- **Wave 5 (3)**: T16 → `unspecified-high`, T17 → `unspecified-high`, T18 → `quick`
- **Wave 6 (1)**: T19 → `writing`
- **FINAL (4)**: F1 → `oracle`, F2 → `unspecified-high`, F3 → `unspecified-high`, F4 → `deep`

---

## Project Structure

```
clinical-reconciliation-engine/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app, CORS, lifespan
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py               # Dependency injection
│   │   │   └── routes/
│   │   │       ├── __init__.py
│   │   │       ├── reconciliation.py  # POST /api/reconcile/medication
│   │   │       └── data_quality.py    # POST /api/validate/data-quality
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py             # pydantic-settings, .env
│   │   │   ├── database.py           # SQLite + SQLModel setup
│   │   │   └── security.py           # API key auth
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── cache.py              # SQLModel cache table
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── reconciliation.py     # Reconciliation request/response
│   │   │   └── data_quality.py       # Data quality request/response
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── reconciliation.py     # Reconciliation business logic
│   │       ├── data_quality.py       # Data quality scoring logic
│   │       └── llm/
│   │           ├── __init__.py
│   │           ├── base.py           # LLMProvider ABC
│   │           ├── mock.py           # MockProvider
│   │           ├── github_models.py  # GitHub Models (GPT-4o)
│   │           ├── anthropic_provider.py  # Anthropic Claude
│   │           ├── factory.py        # Provider factory
│   │           ├── cache.py          # Response caching
│   │           └── prompts.py        # Prompt templates
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py               # Shared fixtures, TestClient, mock DB
│   │   ├── test_reconciliation.py    # Reconciliation endpoint tests
│   │   ├── test_data_quality.py      # Data quality endpoint tests
│   │   ├── test_llm_providers.py     # LLM provider tests
│   │   └── test_auth.py             # Auth middleware tests
│   ├── requirements.txt
│   ├── .env.example
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── App.tsx                    # Main app layout
│   │   ├── App.css                    # App styles
│   │   ├── main.tsx                   # React entry
│   │   ├── types/
│   │   │   └── index.ts              # Shared TypeScript types
│   │   ├── lib/
│   │   │   └── api.ts                # API client
│   │   ├── hooks/
│   │   │   ├── useReconcile.ts       # Reconciliation hook
│   │   │   └── useDataQuality.ts     # Data quality hook
│   │   ├── components/
│   │   │   ├── ConfidenceBar.tsx      # Confidence score visualization
│   │   │   ├── ScoreIndicator.tsx     # Red/yellow/green indicator
│   │   │   ├── LoadingSpinner.tsx     # Loading state
│   │   │   └── ErrorMessage.tsx       # Error display
│   │   └── features/
│   │       ├── reconciliation/
│   │       │   ├── ReconciliationPanel.tsx   # Main reconciliation UI
│   │       │   └── ReconciliationForm.tsx    # Input form
│   │       └── data-quality/
│   │           ├── DataQualityPanel.tsx      # Main data quality UI
│   │           └── DataQualityForm.tsx       # Input form
│   ├── tests/
│   │   ├── ReconciliationPanel.test.tsx
│   │   ├── DataQualityPanel.test.tsx
│   │   └── ConfidenceBar.test.tsx
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── .gitignore
├── .env.example
└── README.md
```

---

## TODOs

### Wave 1 — Scaffolding (3 parallel, start immediately)

- [ ] 1. Project Structure + Git Init

  **What to do**:
  - Initialize git repository (`git init`)
  - Create `.gitignore` for Python (venv, __pycache__, .env, *.pyc, .pytest_cache) + Node (node_modules, dist, .env) + IDE (.vscode, .idea) + OS (.DS_Store)
  - Create directory skeleton matching the Project Structure section above (all `__init__.py` files, empty directories)
  - Create a `README.md` skeleton with section headers: Overview, Setup, Architecture, Design Decisions, Trade-offs, What I'd Improve, Time Spent
  - Create root `.env.example` with: `GITHUB_TOKEN=`, `ANTHROPIC_API_KEY=`, `API_KEY=your-api-key-here`, `LLM_MOCK_MODE=true`, `LLM_PROVIDER=github_models`

  **Must NOT do**:
  - Do NOT install any dependencies yet (that's Task 2 and 3)
  - Do NOT write any application code yet

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple file creation and git commands, no logic involved
  - **Skills**: [`git-master`]
    - `git-master`: Needed for proper git init and .gitignore setup

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2, 3)
  - **Blocks**: Tasks 2, 3
  - **Blocked By**: None (can start immediately)

  **References**:
  - **Pattern References**: None (greenfield)
  - **External References**: https://github.com/github/gitignore/blob/main/Python.gitignore — Python .gitignore patterns
  - **WHY**: The .gitignore must cover both Python and Node.js since this is a polyglot monorepo

  **Acceptance Criteria**:
  - [ ] `git log --oneline` shows initial commit
  - [ ] `.gitignore` exists and contains `venv/`, `node_modules/`, `__pycache__/`, `.env`
  - [ ] `README.md` exists with section headers
  - [ ] `.env.example` exists with all required variables
  - [ ] All directories from Project Structure exist (`backend/app/api/routes/`, `backend/app/core/`, `backend/app/models/`, `backend/app/schemas/`, `backend/app/services/llm/`, `backend/tests/`, `frontend/src/types/`, `frontend/src/lib/`, `frontend/src/hooks/`, `frontend/src/components/`, `frontend/src/features/reconciliation/`, `frontend/src/features/data-quality/`, `frontend/tests/`)

  **QA Scenarios**:

  ```
  Scenario: Verify project structure completeness
    Tool: Bash
    Preconditions: Fresh workspace
    Steps:
      1. Run `ls -la` — verify .git/ directory exists
      2. Run `cat .gitignore` — verify contains "venv/", "node_modules/", "__pycache__/", ".env"
      3. Run `cat .env.example` — verify contains GITHUB_TOKEN, ANTHROPIC_API_KEY, API_KEY, LLM_MOCK_MODE, LLM_PROVIDER
      4. Run `find backend -name "__init__.py" | wc -l` — verify at least 10 __init__.py files
      5. Run `find frontend/src -type d | sort` — verify types/, lib/, hooks/, components/, features/ directories
      6. Run `cat README.md` — verify contains "## Setup", "## Architecture", "## Design Decisions"
    Expected Result: All checks pass, complete project skeleton
    Failure Indicators: Missing directories, missing .gitignore entries, missing .env.example variables
    Evidence: .sisyphus/evidence/task-1-project-structure.txt
  ```

  **Commit**: YES
  - Message: `chore: init project structure with gitignore`
  - Files: `.gitignore`, `README.md`, `.env.example`, all directory scaffolding
  - Pre-commit: `git status` shows only expected files

- [ ] 2. Backend Scaffolding (FastAPI + Config + Health Check)

  **What to do**:
  - Create `backend/requirements.txt` with pinned versions:
    ```
    fastapi>=0.115.0
    uvicorn[standard]>=0.34.0
    sqlmodel>=0.0.22
    pydantic-settings>=2.7.0
    httpx>=0.28.0
    python-dotenv>=1.0.1
    openai>=1.60.0
    anthropic>=0.42.0
    tenacity>=9.0.0
    pytest>=8.3.0
    pytest-asyncio>=0.25.0
    ```
  - Create `backend/app/core/config.py` using `pydantic-settings`:
    - `Settings` class with fields: `api_key`, `github_token`, `anthropic_api_key`, `llm_provider` (default "mock"), `llm_mock_mode` (default True), `database_url` (default "sqlite:///./reconciliation.db"), `cors_origins` (default ["http://localhost:5173"])
    - Load from `.env` file
  - Create `backend/app/main.py`:
    - FastAPI app with title "Clinical Data Reconciliation Engine"
    - CORS middleware allowing frontend origin (localhost:5173)
    - `GET /api/health` endpoint returning `{"status": "ok", "version": "1.0.0"}`
    - Include routers (empty stubs for now)
  - Create `backend/app/api/deps.py` with dependency injection stubs (get_settings, get_db, get_llm_provider)
  - **CRITICAL**: Validate that GitHub Models API is accessible by adding a startup check: if `GITHUB_TOKEN` is set and `LLM_MOCK_MODE` is false, attempt `curl -H "Authorization: Bearer $GITHUB_TOKEN" https://models.inference.ai.azure.com/models` and log result. Do NOT fail startup — just warn.
  - Set up Python virtual environment: `cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`

  **Must NOT do**:
  - Do NOT implement actual API routes yet (just register empty routers)
  - Do NOT set up database tables yet (just the config field for database_url)
  - Do NOT use Alembic

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Standard FastAPI boilerplate setup, well-documented patterns
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - `playwright`: No browser interaction needed for backend setup

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 1)
  - **Parallel Group**: Wave 1 (with Tasks 1, 3)
  - **Blocks**: Tasks 4, 5, 6, 7
  - **Blocked By**: Task 1

  **References**:
  - **External References**:
    - FastAPI docs: https://fastapi.tiangolo.com/tutorial/cors/ — CORS middleware setup
    - pydantic-settings docs: https://docs.pydantic.dev/latest/concepts/pydantic_settings/ — Settings with .env
    - GitHub Models docs: https://docs.github.com/en/github-models — API endpoint and auth
  - **WHY Each Reference Matters**:
    - FastAPI CORS is critical because frontend (port 5173) and backend (port 8000) are different origins
    - pydantic-settings provides `.env` file loading which the assessment expects
    - GitHub Models docs confirm the correct endpoint URL and auth header format

  **Acceptance Criteria**:
  - [ ] `cd backend && source venv/bin/activate && python -c "from app.main import app; print(app.title)"` → prints "Clinical Data Reconciliation Engine"
  - [ ] `cd backend && source venv/bin/activate && uvicorn app.main:app --port 8000 &` then `curl -s http://localhost:8000/api/health` → `{"status":"ok","version":"1.0.0"}`
  - [ ] `cat backend/app/core/config.py` contains `class Settings` with `api_key`, `github_token`, `llm_mock_mode` fields
  - [ ] `cat backend/requirements.txt` contains fastapi, sqlmodel, pydantic-settings, httpx, openai, anthropic, pytest

  **QA Scenarios**:

  ```
  Scenario: Backend health check responds correctly
    Tool: Bash (curl)
    Preconditions: Backend server running on port 8000
    Steps:
      1. Run `cd backend && source venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8000 &`
      2. Wait 3 seconds for startup
      3. Run `curl -s http://localhost:8000/api/health`
      4. Assert response contains `"status": "ok"`
      5. Assert response contains `"version": "1.0.0"`
      6. Run `kill %1` to stop server
    Expected Result: Health check returns {"status": "ok", "version": "1.0.0"}
    Failure Indicators: Connection refused, 404, missing fields in response
    Evidence: .sisyphus/evidence/task-2-health-check.txt

  Scenario: CORS headers present for frontend origin
    Tool: Bash (curl)
    Preconditions: Backend server running on port 8000
    Steps:
      1. Run `curl -s -H "Origin: http://localhost:5173" -I http://localhost:8000/api/health`
      2. Assert response headers contain `access-control-allow-origin: http://localhost:5173`
    Expected Result: CORS allows localhost:5173
    Failure Indicators: Missing CORS header, wildcard origin, wrong port
    Evidence: .sisyphus/evidence/task-2-cors-headers.txt
  ```

  **Commit**: YES
  - Message: `chore: setup backend with FastAPI and config`
  - Files: `backend/requirements.txt`, `backend/app/main.py`, `backend/app/core/config.py`, `backend/app/api/deps.py`
  - Pre-commit: `cd backend && python -c "from app.main import app"`

- [ ] 3. Frontend Scaffolding (Vite + React + TypeScript + Tailwind)

  **What to do**:
  - Initialize Vite project: `cd frontend && pnpm create vite . --template react-ts`
  - Install dependencies: `pnpm install`
  - Install Tailwind CSS: `pnpm add -D tailwindcss @tailwindcss/vite` and configure
  - Install test dependencies: `pnpm add -D vitest @testing-library/react @testing-library/jest-dom jsdom`
  - Configure `vite.config.ts` with API proxy to `http://localhost:8000` for `/api` routes
  - Configure `vitest.config.ts` (or within vite.config.ts) with jsdom environment
  - Create basic `App.tsx` with two-panel layout skeleton:
    - Header: "Clinical Data Reconciliation Engine"
    - Left panel placeholder: "Medication Reconciliation" 
    - Right panel placeholder: "Data Quality Assessment"
  - Add `data-testid` attributes on key elements for testing: `data-testid="app-header"`, `data-testid="reconciliation-panel"`, `data-testid="data-quality-panel"`
  - Verify `pnpm build` succeeds and `pnpm test` runs (even with 0 tests)

  **Must NOT do**:
  - Do NOT install react-router, Redux, or any state management library
  - Do NOT install Material UI, Ant Design, Chakra, or heavy component libraries
  - Do NOT create actual feature components yet (just placeholder divs)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Standard Vite + React scaffolding with Tailwind, well-documented
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - `frontend-ui-ux`: Not needed yet — just scaffolding, no actual UI design
    - `playwright`: No browser testing at this stage

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 1)
  - **Parallel Group**: Wave 1 (with Tasks 1, 2)
  - **Blocks**: Task 8
  - **Blocked By**: Task 1

  **References**:
  - **External References**:
    - Vite docs: https://vite.dev/guide/ — Project setup with React template
    - Tailwind + Vite: https://tailwindcss.com/docs/installation/using-vite — Vite plugin setup
    - Vitest docs: https://vitest.dev/guide/ — Test configuration
  - **WHY Each Reference Matters**:
    - Vite proxy config is essential for development (avoids CORS issues during dev)
    - Tailwind setup must use the Vite plugin approach (not PostCSS)
    - Vitest needs jsdom environment for React component testing

  **Acceptance Criteria**:
  - [ ] `cd frontend && pnpm build` → Build succeeds with no errors
  - [ ] `cd frontend && pnpm test -- --run` → Test runner executes (0 or more tests, no errors)
  - [ ] `cat frontend/vite.config.ts` contains proxy configuration for `/api` → `http://localhost:8000`
  - [ ] `cat frontend/package.json` contains vitest, @testing-library/react, tailwindcss
  - [ ] `cat frontend/src/App.tsx` contains `data-testid="app-header"`

  **QA Scenarios**:

  ```
  Scenario: Frontend builds and dev server starts
    Tool: Bash
    Preconditions: Dependencies installed via pnpm install
    Steps:
      1. Run `cd frontend && pnpm build`
      2. Assert exit code 0
      3. Assert `frontend/dist/index.html` exists
      4. Run `cd frontend && pnpm dev &`
      5. Wait 5 seconds
      6. Run `curl -s http://localhost:5173` 
      7. Assert response contains "Clinical Data Reconciliation Engine"
      8. Kill dev server
    Expected Result: Build succeeds, dev server serves the app
    Failure Indicators: Build errors, missing dist/, dev server crash, blank page
    Evidence: .sisyphus/evidence/task-3-frontend-build.txt

  Scenario: Vite proxy configured for API routes
    Tool: Bash
    Preconditions: None
    Steps:
      1. Run `cat frontend/vite.config.ts`
      2. Assert contains "proxy" configuration
      3. Assert contains "/api" route pointing to "http://localhost:8000"
    Expected Result: Proxy config present for /api routes
    Failure Indicators: Missing proxy config, wrong port, wrong path
    Evidence: .sisyphus/evidence/task-3-vite-proxy.txt
  ```

  **Commit**: YES
  - Message: `chore: setup frontend with Vite React TypeScript`
  - Files: `frontend/` scaffolding files
  - Pre-commit: `cd frontend && pnpm build`

### Wave 2 — Data Models + Abstractions (5 parallel, after Wave 1)

- [ ] 4. Pydantic Request/Response Schemas

  **What to do**:
  - Create `backend/app/schemas/reconciliation.py`:
    - `PatientContext` model: `age: int`, `conditions: list[str]`, `recent_labs: dict[str, float] = {}`
    - `MedicationSource` model: `system: str`, `medication: str`, `last_updated: str | None = None`, `last_filled: str | None = None`, `source_reliability: Literal["high", "medium", "low"]`
    - `ReconciliationRequest` model: `patient_context: PatientContext`, `sources: list[MedicationSource]` (min_length=1, max_length=50)
    - `ReconciliationResponse` model: `reconciled_medication: str`, `confidence_score: float` (ge=0, le=1), `reasoning: str`, `recommended_actions: list[str]`, `clinical_safety_check: Literal["PASSED", "FAILED", "WARNING"]`
  - Create `backend/app/schemas/data_quality.py`:
    - `Demographics` model: `name: str | None = None`, `dob: str | None = None`, `gender: str | None = None`
    - `VitalSigns` model: `blood_pressure: str | None = None`, `heart_rate: int | None = None`, `temperature: float | None = None`
    - `DataQualityRequest` model: `demographics: Demographics = Demographics()`, `medications: list[str] = []`, `allergies: list[str] = []`, `conditions: list[str] = []`, `vital_signs: VitalSigns = VitalSigns()`, `last_updated: str | None = None`
    - `IssueDetected` model: `field: str`, `issue: str`, `severity: Literal["low", "medium", "high"]`
    - `QualityBreakdown` model: `completeness: int` (ge=0, le=100), `accuracy: int`, `timeliness: int`, `clinical_plausibility: int`
    - `DataQualityResponse` model: `overall_score: int` (ge=0, le=100), `breakdown: QualityBreakdown`, `issues_detected: list[IssueDetected]`
  - Add field validators where appropriate (e.g., age must be 0-150, confidence_score 0.0-1.0)
  - Export all schemas from `backend/app/schemas/__init__.py`

  **Must NOT do**:
  - Do NOT use FHIR R4 nested structures (no `coding[].system`, no `coding[].code`)
  - Do NOT import `fhir.resources`

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Pydantic model definitions are straightforward data classes
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 5, 6, 7, 8)
  - **Blocks**: Tasks 9, 10
  - **Blocked By**: Task 2

  **References**:
  - **API/Type References**:
    - Assessment PDF: exact input/output JSON examples for both endpoints (see Context section)
  - **External References**:
    - Pydantic v2 field validators: https://docs.pydantic.dev/latest/concepts/validators/
    - PyHealth EHR data structures: `https://pyhealth.readthedocs.io/en/latest/api/data.html` — Reference for EHR data concepts (Event, Patient, Visit). Use to inform schema field naming and clinical data modeling. Do NOT import pyhealth as a dependency.
  - **WHY**: The response shapes MUST match the assessment's expected output exactly. Use the PDF examples as the canonical reference. PyHealth docs provide EHR domain context for realistic field naming.

  **Acceptance Criteria**:
  - [ ] `cd backend && python -c "from app.schemas.reconciliation import ReconciliationRequest, ReconciliationResponse; print('OK')"` → OK
  - [ ] `cd backend && python -c "from app.schemas.data_quality import DataQualityRequest, DataQualityResponse; print('OK')"` → OK
  - [ ] `cd backend && python -c "from app.schemas.reconciliation import ReconciliationRequest; ReconciliationRequest(patient_context={'age':67,'conditions':['Diabetes']},sources=[{'system':'Hospital','medication':'Aspirin 81mg','source_reliability':'high'}]); print('VALID')"` → VALID
  - [ ] `cd backend && python -c "from app.schemas.reconciliation import MedicationSource; MedicationSource(system='X',medication='Y',source_reliability='invalid')" 2>&1 | grep -q "validation error"` → validation error for invalid reliability

  **QA Scenarios**:

  ```
  Scenario: Schema validation accepts valid reconciliation input
    Tool: Bash (python)
    Preconditions: Backend venv activated, schemas importable
    Steps:
      1. Run python script that creates ReconciliationRequest with the exact assessment example input
      2. Assert no validation error
      3. Run python script that creates ReconciliationResponse with the exact assessment example output
      4. Assert confidence_score is float between 0 and 1
    Expected Result: Both request and response models validate correctly
    Failure Indicators: ValidationError, missing fields, wrong types
    Evidence: .sisyphus/evidence/task-4-schema-validation.txt

  Scenario: Schema rejects invalid input
    Tool: Bash (python)
    Preconditions: Backend venv activated
    Steps:
      1. Attempt to create ReconciliationRequest with empty sources list → assert ValidationError
      2. Attempt to create MedicationSource with source_reliability="invalid" → assert ValidationError
      3. Attempt to create ReconciliationResponse with confidence_score=1.5 → assert ValidationError
    Expected Result: All invalid inputs rejected with clear error messages
    Failure Indicators: Invalid data accepted without error
    Evidence: .sisyphus/evidence/task-4-schema-rejection.txt
  ```

  **Commit**: YES
  - Message: `feat: add request/response schemas for reconciliation and data quality`
  - Files: `backend/app/schemas/reconciliation.py`, `backend/app/schemas/data_quality.py`, `backend/app/schemas/__init__.py`
  - Pre-commit: `cd backend && python -c "from app.schemas.reconciliation import ReconciliationRequest; from app.schemas.data_quality import DataQualityRequest"`

- [ ] 5. SQLite Database + SQLModel Tables

  **What to do**:
  - Create `backend/app/core/database.py`:
    - Use SQLModel with SQLite: `create_engine("sqlite:///./reconciliation.db", connect_args={"check_same_thread": False})`
    - Engine creation function that reads URL from Settings
    - `get_session` dependency that yields SQLModel Session
    - `init_db()` function that calls `SQLModel.metadata.create_all(engine)`
  - Create `backend/app/models/cache.py`:
    - `LLMCache` SQLModel table: `id: int | None` (primary key), `prompt_hash: str` (indexed, unique), `response_json: str`, `provider: str`, `created_at: datetime` (default utcnow), `ttl_seconds: int` (default 3600)
  - Wire `init_db()` into FastAPI lifespan event in `main.py`
  - For testing: support in-memory SQLite via `StaticPool` (document in conftest.py comments)

  **Must NOT do**:
  - Do NOT use Alembic migrations
  - Do NOT create complex table relationships

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple SQLModel setup with one table
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 4, 6, 7, 8)
  - **Blocks**: Tasks 6, 9, 10, 11
  - **Blocked By**: Task 2

  **References**:
  - **External References**:
    - SQLModel docs: https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/ — Table creation
    - SQLModel + FastAPI: https://sqlmodel.tiangolo.com/tutorial/fastapi/session-with-dep/ — Session dependency injection
  - **WHY**: SQLModel is chosen because it's by the FastAPI author, combines SQLAlchemy + Pydantic, and eliminates model duplication.

  **Acceptance Criteria**:
  - [ ] `cd backend && python -c "from app.core.database import init_db, get_session; init_db(); print('DB OK')"` → DB OK
  - [ ] `cd backend && python -c "from app.models.cache import LLMCache; print(LLMCache.__tablename__)"` → prints table name
  - [ ] After `init_db()`, file `reconciliation.db` exists OR in-memory mode works

  **QA Scenarios**:

  ```
  Scenario: Database initializes and cache table exists
    Tool: Bash (python + sqlite3)
    Preconditions: Backend venv activated
    Steps:
      1. Run `cd backend && python -c "from app.core.database import init_db; init_db()"`
      2. Run `sqlite3 reconciliation.db ".tables"` — assert contains "llmcache" (or equivalent table name)
      3. Run `sqlite3 reconciliation.db ".schema llmcache"` — assert contains prompt_hash, response_json, provider, created_at
      4. Clean up: `rm reconciliation.db`
    Expected Result: Table created with correct schema
    Failure Indicators: Table missing, wrong columns, connection error
    Evidence: .sisyphus/evidence/task-5-database-init.txt
  ```

  **Commit**: YES
  - Message: `feat: add SQLite database setup and cache model`
  - Files: `backend/app/core/database.py`, `backend/app/models/cache.py`
  - Pre-commit: `cd backend && python -c "from app.core.database import engine"`

- [ ] 6. LLM Provider Abstraction (Interface + MockProvider + Factory)

  **What to do**:
  - Create `backend/app/services/llm/base.py`:
    - `LLMProvider` abstract base class (ABC) with methods:
      - `async def reconcile_medications(self, request: ReconciliationRequest) -> ReconciliationResponse` 
      - `async def assess_data_quality(self, request: DataQualityRequest) -> DataQualityResponse`
      - `provider_name: str` property
  - Create `backend/app/services/llm/mock.py`:
    - `MockProvider(LLMProvider)` that returns deterministic responses:
      - For reconciliation: returns the most recent source's medication with confidence 0.85, reasoning referencing recency and source reliability, safety check "PASSED"
      - For data quality: calculates rule-based scores (completeness = % of fields filled, accuracy = basic validation, timeliness = days since last_updated, clinical_plausibility = vital signs range checks)
    - Include 3 pre-built mock scenarios with rich clinical reasoning text
  - Create `backend/app/services/llm/factory.py`:
    - `get_llm_provider(settings: Settings) -> LLMProvider` factory function
    - If `settings.llm_mock_mode` → return MockProvider
    - If `settings.llm_provider == "github_models"` → return GitHubModelsProvider (stub for now)
    - If `settings.llm_provider == "anthropic"` → return AnthropicProvider (stub for now)
    - Fallback to MockProvider with warning log
  - Create `backend/tests/test_llm_providers.py`:
    - **TEST 1**: Test MockProvider.reconcile_medications returns valid ReconciliationResponse with all required fields
    - **TEST 2**: Test MockProvider.assess_data_quality returns valid DataQualityResponse with scores in 0-100 range
    - **TEST 3**: Test factory returns MockProvider when llm_mock_mode=True

  **Must NOT do**:
  - Do NOT implement GitHubModelsProvider or AnthropicProvider yet (just stubs that raise NotImplementedError)
  - Do NOT add prompt templates yet (that's Task 12)

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Abstract interface design + mock implementation with clinical logic + factory pattern + 3 tests. Requires careful design thinking.
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 4, 5, 7, 8)
  - **Blocks**: Tasks 9, 10, 11, 12
  - **Blocked By**: Tasks 2, 5

  **References**:
  - **Pattern References**:
    - Python ABC pattern: `from abc import ABC, abstractmethod`
  - **External References**:
    - Assessment PDF example inputs/outputs — MockProvider must return data matching these shapes exactly
  - **WHY**: The LLM provider abstraction is the architectural core. MockProvider must produce realistic clinical reasoning text, not placeholder strings, because the evaluator will run the app in mock mode first.

  **Acceptance Criteria**:
  - [ ] `cd backend && python -m pytest tests/test_llm_providers.py -v` → 3 tests PASS
  - [ ] MockProvider.reconcile_medications returns response with `confidence_score` between 0 and 1
  - [ ] MockProvider.assess_data_quality returns response with `overall_score` between 0 and 100
  - [ ] Factory returns MockProvider when `llm_mock_mode=True`

  **QA Scenarios**:

  ```
  Scenario: MockProvider returns valid reconciliation response
    Tool: Bash (python)
    Preconditions: Backend venv activated
    Steps:
      1. Import MockProvider and ReconciliationRequest
      2. Create request with assessment example data (Metformin case)
      3. Call await mock_provider.reconcile_medications(request)
      4. Assert response.reconciled_medication is non-empty string
      5. Assert response.confidence_score between 0.0 and 1.0
      6. Assert response.reasoning contains at least 20 characters (not empty placeholder)
      7. Assert response.clinical_safety_check in ["PASSED", "FAILED", "WARNING"]
      8. Assert len(response.recommended_actions) >= 1
    Expected Result: Complete, valid, realistic response
    Failure Indicators: Empty strings, None values, confidence outside range
    Evidence: .sisyphus/evidence/task-6-mock-reconciliation.txt

  Scenario: Factory pattern dispatches correctly
    Tool: Bash (python)
    Preconditions: Backend venv activated
    Steps:
      1. Create Settings with llm_mock_mode=True → call get_llm_provider → assert isinstance MockProvider
      2. Create Settings with llm_mock_mode=False, llm_provider="github_models" → assert raises NotImplementedError or returns stub
    Expected Result: Factory returns correct provider based on settings
    Failure Indicators: Wrong provider type, factory crash
    Evidence: .sisyphus/evidence/task-6-factory-dispatch.txt
  ```

  **Commit**: YES
  - Message: `feat: add LLM provider abstraction with mock provider`
  - Files: `backend/app/services/llm/base.py`, `mock.py`, `factory.py`, `tests/test_llm_providers.py`
  - Pre-commit: `cd backend && python -m pytest tests/test_llm_providers.py -v`

- [ ] 7. API Key Authentication Middleware

  **What to do**:
  - Create `backend/app/core/security.py`:
    - `verify_api_key(x_api_key: str = Header(...))` FastAPI dependency
    - Compare against `settings.api_key` using `secrets.compare_digest` (timing-safe)
    - If no match: raise `HTTPException(status_code=401, detail={"code": "UNAUTHORIZED", "message": "Invalid or missing API key"})`
    - If `settings.api_key` is empty/None: allow all requests (development mode) with warning log
  - Create `backend/tests/test_auth.py`:
    - **TEST 4**: Test that request without `X-API-Key` header returns 401
    - **TEST 5**: Test that request with correct `X-API-Key` returns 200 (using health check or a test endpoint)
  - Wire `verify_api_key` as a dependency on the API router (not on health check)

  **Must NOT do**:
  - Do NOT implement JWT, OAuth, or session-based auth
  - Do NOT create user models or login endpoints

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple header-based auth check, standard FastAPI pattern
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 4, 5, 6, 8)
  - **Blocks**: Tasks 9, 10
  - **Blocked By**: Task 2

  **References**:
  - **External References**:
    - FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/ — Header dependency pattern
  - **WHY**: Assessment requires "Basic authentication/API key protection". Header-based API key is the simplest approach that satisfies this.

  **Acceptance Criteria**:
  - [ ] `cd backend && python -m pytest tests/test_auth.py -v` → 2 tests PASS
  - [ ] `curl -s -w "%{http_code}" http://localhost:8000/api/reconcile/medication` → 401 (or 405/422 if method matters, but auth should reject first)
  - [ ] `curl -s -H "X-API-Key: test-key" http://localhost:8000/api/health` → 200 (health check bypasses auth)

  **QA Scenarios**:

  ```
  Scenario: Unauthenticated request rejected
    Tool: Bash (curl)
    Preconditions: Backend running with API_KEY=test-secret-key
    Steps:
      1. Run `curl -s -w "\n%{http_code}" -X POST http://localhost:8000/api/reconcile/medication -H "Content-Type: application/json" -d '{}'`
      2. Assert HTTP status code is 401
      3. Assert response body contains "UNAUTHORIZED" or "Invalid"
    Expected Result: 401 Unauthorized with clear error message
    Failure Indicators: 200 OK (auth bypassed), 500 (crash), wrong error format
    Evidence: .sisyphus/evidence/task-7-auth-rejection.txt

  Scenario: Authenticated request passes auth layer
    Tool: Bash (curl)
    Preconditions: Backend running with API_KEY=test-secret-key
    Steps:
      1. Run `curl -s -w "\n%{http_code}" http://localhost:8000/api/health`
      2. Assert health check returns 200 WITHOUT API key (health is public)
      3. Run `curl -s -w "\n%{http_code}" -X POST http://localhost:8000/api/reconcile/medication -H "X-API-Key: test-secret-key" -H "Content-Type: application/json" -d '{"patient_context":{"age":67,"conditions":[]},"sources":[{"system":"Test","medication":"Aspirin","source_reliability":"high"}]}'`
      4. Assert returns 200 (or 422 if endpoint not implemented yet — but NOT 401)
    Expected Result: Auth passes with correct API key
    Failure Indicators: 401 with correct key, health check requires auth
    Evidence: .sisyphus/evidence/task-7-auth-pass.txt
  ```

  **Commit**: YES
  - Message: `feat: add API key authentication middleware`
  - Files: `backend/app/core/security.py`, `backend/tests/test_auth.py`
  - Pre-commit: `cd backend && python -m pytest tests/test_auth.py -v`

- [ ] 8. Frontend TypeScript Types + API Client Skeleton

  **What to do**:
  - Create `frontend/src/types/index.ts` mirroring backend schemas:
    - `PatientContext`, `MedicationSource`, `ReconciliationRequest`, `ReconciliationResponse`
    - `Demographics`, `VitalSigns`, `DataQualityRequest`, `IssueDetected`, `QualityBreakdown`, `DataQualityResponse`
    - Use TypeScript interfaces/types (not classes)
    - `ApiError` type: `{ code: string; message: string }`
  - Create `frontend/src/lib/api.ts`:
    - `API_BASE_URL` constant (empty string in dev since Vite proxy handles it, or configurable)
    - `apiClient` wrapper around fetch with:
      - Default headers: `Content-Type: application/json`, `X-API-Key` from config
      - Error handling: parse error response, throw typed error
    - `reconcileMedication(request: ReconciliationRequest): Promise<ReconciliationResponse>`
    - `validateDataQuality(request: DataQualityRequest): Promise<DataQualityResponse>`
    - `checkHealth(): Promise<{status: string; version: string}>`

  **Must NOT do**:
  - Do NOT install axios or any HTTP library — use native `fetch`
  - Do NOT implement React hooks yet (that's Task 16)
  - Do NOT add any UI components

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Type definitions and fetch wrapper, straightforward TypeScript
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 4, 5, 6, 7)
  - **Blocks**: Tasks 13, 14, 16
  - **Blocked By**: Task 3

  **References**:
  - **API/Type References**:
    - Assessment PDF example inputs/outputs — TypeScript types MUST match these shapes exactly
    - `backend/app/schemas/reconciliation.py` (Task 4) — Mirror these Pydantic models in TypeScript
    - `backend/app/schemas/data_quality.py` (Task 4) — Mirror these Pydantic models in TypeScript
  - **WHY**: Types must be 1:1 with backend schemas to prevent runtime type mismatches. The API client is the single point of contact with the backend.

  **Acceptance Criteria**:
  - [ ] `cd frontend && pnpm build` → succeeds with no TypeScript errors
  - [ ] `cat frontend/src/types/index.ts` contains `ReconciliationRequest`, `ReconciliationResponse`, `DataQualityRequest`, `DataQualityResponse`
  - [ ] `cat frontend/src/lib/api.ts` contains `reconcileMedication`, `validateDataQuality`, `checkHealth` functions
  - [ ] API client includes `X-API-Key` header in requests

  **QA Scenarios**:

  ```
  Scenario: TypeScript types compile without errors
    Tool: Bash
    Preconditions: Frontend dependencies installed
    Steps:
      1. Run `cd frontend && npx tsc --noEmit`
      2. Assert exit code 0
      3. Run `cd frontend && pnpm build`
      4. Assert exit code 0
    Expected Result: Zero TypeScript errors
    Failure Indicators: Type errors, missing imports, incompatible types
    Evidence: .sisyphus/evidence/task-8-types-compile.txt
  ```

  **Commit**: YES
  - Message: `feat: add frontend types and API client`
  - Files: `frontend/src/types/index.ts`, `frontend/src/lib/api.ts`
  - Pre-commit: `cd frontend && pnpm build`

### Wave 3 — Core Backend Features (3 parallel, after Wave 2)

- [ ] 9. POST /api/reconcile/medication Endpoint + Tests

  **What to do**:
  - Create `backend/app/api/routes/reconciliation.py`:
    - `POST /api/reconcile/medication` route
    - Accept `ReconciliationRequest` body, return `ReconciliationResponse`
    - Inject `LLMProvider` via dependency injection
    - Input validation: at least 1 source, max 50 sources
    - Call `llm_provider.reconcile_medications(request)`
    - Handle errors: LLM timeout → 503 with retry-after, malformed LLM output → fallback response with confidence 0.0
  - Create `backend/app/services/reconciliation.py`:
    - `ReconciliationService` class:
      - `async def reconcile(request: ReconciliationRequest, llm: LLMProvider) -> ReconciliationResponse`
      - Pre-processing: sort sources by date (most recent first), validate medication names non-empty
      - Post-processing: clamp confidence_score 0.0-1.0, apply safety check logic
    - Clinical safety check (rule-based, not AI):
      - Small hardcoded list of dangerous interactions (e.g., warfarin + aspirin)
      - Dosage ceiling checks (e.g., Metformin > 2550mg/day)
      - If concern found: override `clinical_safety_check` to "WARNING"
  - Register route in `app/main.py`
  - Add to `backend/tests/test_reconciliation.py`:
    - **TEST**: Happy path — valid Metformin example → 200 with all required fields
    - **TEST**: Edge case — single source → reconcile returns that source with high confidence

  **Must NOT do**:
  - Do NOT implement complex clinical logic — keep safety checks simple and rule-based
  - Do NOT call real LLM APIs in tests (use MockProvider via DI override)

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Route + service + safety logic + error handling + 2 tests. Core business logic.
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 10, 11)
  - **Blocks**: Tasks 12, 16
  - **Blocked By**: Tasks 4, 5, 6, 7

  **References**:
  - **API/Type References**:
    - `backend/app/schemas/reconciliation.py` (Task 4) — Request/response models
    - `backend/app/services/llm/base.py` (Task 6) — LLMProvider interface
    - `backend/app/services/llm/mock.py` (Task 6) — MockProvider for testing
    - `backend/app/core/security.py` (Task 7) — Auth dependency
  - **External References**:
    - Assessment PDF: exact reconciliation example input/output
    - Metformin max daily dose: 2550mg
  - **WHY**: Primary assessment endpoint. Response shape MUST match assessment spec exactly.

  **Acceptance Criteria**:
  - [ ] `cd backend && python -m pytest tests/test_reconciliation.py -v` → 2 tests PASS
  - [ ] POST to endpoint with assessment Metformin example → JSON with `reconciled_medication`, `confidence_score`, `reasoning`, `recommended_actions`, `clinical_safety_check`

  **QA Scenarios**:

  ```
  Scenario: Reconciliation returns valid response
    Tool: Bash (curl)
    Preconditions: Backend running, LLM_MOCK_MODE=true, API_KEY=test-key
    Steps:
      1. POST /api/reconcile/medication with Metformin example from assessment PDF
      2. Assert HTTP 200
      3. Assert "reconciled_medication" is non-empty string
      4. Assert "confidence_score" between 0 and 1
      5. Assert "reasoning" length > 20
      6. Assert "recommended_actions" array length >= 1
      7. Assert "clinical_safety_check" in [PASSED, FAILED, WARNING]
    Expected Result: Complete response matching assessment spec
    Failure Indicators: 500, missing fields, empty values
    Evidence: .sisyphus/evidence/task-9-reconciliation-happy.txt

  Scenario: Reconciliation rejects empty sources
    Tool: Bash (curl)
    Preconditions: Backend running
    Steps:
      1. POST with {"patient_context":{"age":30,"conditions":[]},"sources":[]}
      2. Assert HTTP 422
    Expected Result: Validation error for empty sources
    Evidence: .sisyphus/evidence/task-9-reconciliation-empty.txt
  ```

  **Commit**: YES
  - Message: `feat: implement medication reconciliation endpoint`
  - Files: `backend/app/api/routes/reconciliation.py`, `backend/app/services/reconciliation.py`, `backend/tests/test_reconciliation.py`
  - Pre-commit: `cd backend && python -m pytest tests/test_reconciliation.py -v`

- [ ] 10. POST /api/validate/data-quality Endpoint + Tests

  **What to do**:
  - Create `backend/app/api/routes/data_quality.py`:
    - `POST /api/validate/data-quality` route
    - Accept `DataQualityRequest`, return `DataQualityResponse`
    - Inject `LLMProvider` via dependency injection
  - Create `backend/app/services/data_quality.py`:
    - **Completeness (0-100)**: % of fields filled, weight critical fields higher. Empty allergies → "likely incomplete"
    - **Accuracy (0-100)**: Format validation (DOB, gender codes), medication name patterns
    - **Timeliness (0-100)**: <30d=100, 30-90d=80, 90-180d=60, 180-365d=40, >365d=20
    - **Clinical plausibility (0-100)**: Vital sign range checks:
      - Systolic: 60-250 (340 → implausible)
      - Diastolic: 30-150
      - Heart rate: 30-220
      - Temperature: 35-42°C
    - `issues_detected`: List of {field, issue, severity} for each problem
    - `overall_score`: Weighted average (25% each dimension)
  - Register route in `app/main.py`
  - Tests:
    - **TEST**: John Doe example (BP 340/180) → score ~62, plausibility low, BP issue detected
    - **TEST**: Perfect record → score > 85, few/no issues

  **Must NOT do**:
  - Do NOT use external medical databases
  - Do NOT implement complex NLP for medication parsing

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Multi-dimensional scoring + clinical validation + 2 tests
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 9, 11)
  - **Blocks**: Tasks 12, 16
  - **Blocked By**: Tasks 4, 5, 6, 7

  **References**:
  - **API/Type References**:
    - `backend/app/schemas/data_quality.py` (Task 4) — Request/response models
    - `backend/app/services/llm/base.py` (Task 6) — LLMProvider interface
  - **External References**:
    - Assessment PDF: John Doe example → overall_score 62, clinical_plausibility 40
    - Normal vital ranges: systolic 90-140, diastolic 60-90, HR 60-100
  - **WHY**: Scoring must approximate assessment example values. BP 340/180 should produce low plausibility.

  **Acceptance Criteria**:
  - [ ] `cd backend && python -m pytest tests/test_data_quality.py -v` → 2 tests PASS
  - [ ] POST with John Doe example → overall_score between 30-80, issues_detected contains BP issue with severity "high"

  **QA Scenarios**:

  ```
  Scenario: Detects implausible vitals
    Tool: Bash (curl)
    Preconditions: Backend running, LLM_MOCK_MODE=true, API_KEY=test-key
    Steps:
      1. POST John Doe example (BP 340/180, empty allergies, 7-month-old data)
      2. Assert HTTP 200
      3. Assert overall_score between 30 and 80
      4. Assert breakdown.clinical_plausibility < 60
      5. Assert issues_detected contains entry with field containing "blood_pressure" and severity "high"
    Expected Result: Low scores for problematic data
    Evidence: .sisyphus/evidence/task-10-quality-implausible.txt

  Scenario: Perfect record scores high
    Tool: Bash (curl)
    Steps:
      1. POST complete valid record (all fields, normal vitals, recent date)
      2. Assert overall_score > 85
      3. Assert issues_detected is empty or low-severity only
    Expected Result: High score for clean data
    Evidence: .sisyphus/evidence/task-10-quality-perfect.txt
  ```

  **Commit**: YES
  - Message: `feat: implement data quality validation endpoint`
  - Files: `backend/app/api/routes/data_quality.py`, `backend/app/services/data_quality.py`, `backend/tests/test_data_quality.py`
  - Pre-commit: `cd backend && python -m pytest tests/test_data_quality.py -v`

- [ ] 11. LLM Response Caching Service

  **What to do**:
  - Create `backend/app/services/llm/cache.py`:
    - `LLMCacheService`:
      - `_hash_request(provider: str, request_data: dict) -> str` — SHA256 hash
      - `get_cached(provider: str, request_data: dict) -> str | None` — lookup, check TTL
      - `set_cached(provider: str, request_data: dict, response_json: str, ttl: int = 3600)`
      - `clear_expired() -> int` — delete old entries
    - Cache key = provider + serialized request hash
    - TTL default: 1 hour, configurable
  - Create `CachedProvider` wrapper or integrate into factory:
    - Check cache → hit: return cached → miss: call real provider → store → return
  - Log cache hits/misses

  **Must NOT do**:
  - Do NOT use Redis — SQLite only
  - Do NOT cache mock provider responses

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Caching with TTL, hash lookup, provider wrapper pattern
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 9, 10)
  - **Blocks**: Task 12
  - **Blocked By**: Tasks 5, 6

  **References**:
  - **Pattern References**:
    - `backend/app/models/cache.py` (Task 5) — LLMCache table
    - `backend/app/services/llm/base.py` (Task 6) — LLMProvider to wrap
  - **WHY**: Assessment requires "Cache responses where appropriate to minimize API costs."

  **Acceptance Criteria**:
  - [ ] Cache stores and retrieves responses correctly
  - [ ] Cache miss triggers real provider call
  - [ ] Expired entries return None

  **QA Scenarios**:

  ```
  Scenario: Cache hit returns stored response
    Tool: Bash (python)
    Steps:
      1. Store entry with set_cached("test", {"key": "val"}, '{"result": "ok"}')
      2. Retrieve with get_cached("test", {"key": "val"})
      3. Assert returns '{"result": "ok"}'
      4. Retrieve with get_cached("test", {"key": "different"})
      5. Assert returns None
    Expected Result: Hit returns data, miss returns None
    Evidence: .sisyphus/evidence/task-11-cache-hit.txt

  Scenario: TTL expiration works
    Tool: Bash (python)
    Steps:
      1. Store with ttl=1
      2. Retrieve immediately → assert hit
      3. Wait 2 seconds
      4. Retrieve → assert miss
    Expected Result: Expired entries not returned
    Evidence: .sisyphus/evidence/task-11-cache-ttl.txt
  ```

  **Commit**: YES
  - Message: `feat: add LLM response caching with SQLite`
  - Files: `backend/app/services/llm/cache.py`, updates to `factory.py`
  - Pre-commit: `cd backend && python -m pytest tests/ -v`

### Wave 4 — AI Integration + Frontend UI (4 parallel, after Wave 3)

- [ ] 12. Real LLM Providers (GitHub Models + Anthropic) + Prompt Templates

  **What to do**:
  - Create `backend/app/services/llm/github_models.py`:
    - `GitHubModelsProvider(LLMProvider)` using `openai` SDK with custom base URL:
      - `base_url = "https://models.inference.ai.azure.com"`
      - `api_key = settings.github_token`
      - Model: `"gpt-4o"` (or `"gpt-4o-mini"` for cost savings)
    - Implement `reconcile_medications()` and `assess_data_quality()`:
      - Build prompt from template + request data
      - Call API with `response_format={"type": "json_object"}`, `temperature=0.2`
      - Parse JSON response, validate with Pydantic
      - If JSON parse fails: retry once, then return fallback response
    - Error handling: `httpx.TimeoutException` → retry with `tenacity` (3 attempts, exponential backoff)
    - Rate limit handling: catch 429 → raise custom `RateLimitError` with retry-after
  - Create `backend/app/services/llm/anthropic_provider.py`:
    - `AnthropicProvider(LLMProvider)` using `anthropic` SDK:
      - Model: `"claude-3-5-sonnet-20241022"` (or haiku for cost)
    - Same pattern as GitHub Models but using Anthropic API format
    - Prompt template adapted for Claude's style (system message + user message)
  - Create `backend/app/services/llm/prompts.py`:
    - `RECONCILIATION_SYSTEM_PROMPT`: Instructs LLM to act as clinical pharmacist, analyze medication sources, consider patient context, return JSON with specified fields
    - `RECONCILIATION_USER_PROMPT_TEMPLATE`: Formats patient_context + sources into structured prompt
    - `DATA_QUALITY_SYSTEM_PROMPT`: Instructs LLM to assess data quality across 4 dimensions
    - `DATA_QUALITY_USER_PROMPT_TEMPLATE`: Formats patient data for quality assessment
    - All prompts must include: "Return valid JSON matching this exact schema: {schema}"
    - Document prompt engineering approach with inline comments explaining each design choice
  - Update `factory.py` to return real providers based on settings
  - Test with mock API responses (mock the httpx/openai client, not the provider interface)

  **Must NOT do**:
  - Do NOT hardcode API keys — read from settings
  - Do NOT use streaming responses (adds complexity, not needed)
  - Do NOT use function calling — `response_format: json_object` is simpler

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Two LLM provider implementations + prompt engineering + error handling + retry logic. This is 25% of the assessment grade (AI Integration).
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 13, 14, 15)
  - **Blocks**: Task 16
  - **Blocked By**: Tasks 6, 9, 10, 11

  **References**:
  - **Pattern References**:
    - `backend/app/services/llm/base.py` (Task 6) — LLMProvider interface to implement
    - `backend/app/services/llm/mock.py` (Task 6) — MockProvider as reference for response shapes
    - `backend/app/services/llm/cache.py` (Task 11) — Cache integration
  - **External References**:
    - GitHub Models API: https://docs.github.com/en/github-models — endpoint, auth, available models
    - OpenAI Python SDK: https://github.com/openai/openai-python — used for GitHub Models
    - Anthropic Python SDK: https://docs.anthropic.com/en/api/client-sdks — SDK usage
    - Assessment PDF: prompt must produce output matching example response shapes
  - **WHY**: This task is 25% of the grade. Prompt quality directly determines the usefulness of reconciliation and quality scoring. Document every prompt design choice.

  **Acceptance Criteria**:
  - [ ] `GitHubModelsProvider` instantiates with correct base_url and api_key from settings
  - [ ] `AnthropicProvider` instantiates with api_key from settings
  - [ ] Prompts include explicit JSON schema in system message
  - [ ] Both providers handle timeout (30s) and retry (3 attempts)
  - [ ] Both providers handle malformed JSON response (retry once, then fallback)
  - [ ] `prompts.py` contains documented prompt engineering approach (inline comments)
  - [ ] Factory correctly dispatches to GitHub Models or Anthropic based on settings

  **QA Scenarios**:

  ```
  Scenario: GitHub Models provider sends correct request format
    Tool: Bash (python)
    Preconditions: Backend venv activated (no real API call needed — mock httpx)
    Steps:
      1. Mock the openai.AsyncOpenAI client
      2. Create GitHubModelsProvider
      3. Call reconcile_medications with test data
      4. Assert the mock was called with base_url="https://models.inference.ai.azure.com"
      5. Assert model="gpt-4o" was used
      6. Assert response_format={"type": "json_object"} was set
    Expected Result: Correct API call format
    Evidence: .sisyphus/evidence/task-12-github-models-format.txt

  Scenario: Provider handles malformed JSON gracefully
    Tool: Bash (python)
    Steps:
      1. Mock LLM to return "This is not JSON {broken"
      2. Call reconcile_medications
      3. Assert does NOT crash
      4. Assert returns fallback response with confidence_score near 0
    Expected Result: Graceful degradation, not crash
    Evidence: .sisyphus/evidence/task-12-malformed-json.txt
  ```

  **Commit**: YES
  - Message: `feat: integrate GitHub Models and Anthropic LLM providers`
  - Files: `backend/app/services/llm/github_models.py`, `anthropic_provider.py`, `prompts.py`, `factory.py` update
  - Pre-commit: `cd backend && python -m pytest tests/test_llm_providers.py -v`

- [ ] 13. Reconciliation Dashboard Panel

  **What to do**:
  - Create `frontend/src/features/reconciliation/ReconciliationForm.tsx`:
    - Form to input medication reconciliation data:
      - Patient context: age (number input), conditions (tag input or comma-separated text)
      - Medication sources: dynamic list where user can add/remove sources
      - Each source: system name, medication, last_updated (date), source_reliability (dropdown: high/medium/low)
      - Submit button with loading state
    - Pre-fill with assessment's Metformin example as default values (for easy demo)
    - `data-testid="reconciliation-form"`, `data-testid="reconciliation-submit"`
  - Create `frontend/src/features/reconciliation/ReconciliationPanel.tsx`:
    - Displays reconciliation results:
      - `reconciled_medication` in large, prominent text
      - `confidence_score` as visual bar using `ConfidenceBar` component (green >0.8, yellow 0.5-0.8, red <0.5)
      - `reasoning` in a readable paragraph block
      - `recommended_actions` as a checklist
      - `clinical_safety_check` as a badge (green PASSED, red FAILED, yellow WARNING)
      - Approve / Reject buttons (toggle state, no backend call needed — just UI state)
    - `data-testid="reconciliation-result"`, `data-testid="confidence-score"`, `data-testid="safety-check"`
  - Create shared `frontend/src/components/ConfidenceBar.tsx`:
    - Takes `score: number` (0-1), renders colored progress bar
    - Green: >0.8, Yellow: 0.5-0.8, Red: <0.5
    - Shows percentage text
    - `data-testid="confidence-bar"`

  **Must NOT do**:
  - Do NOT install any component library (Material UI, etc.)
  - Do NOT add routing
  - Do NOT connect to real API yet (use static mock data or local state for now)

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: UI component design with clinical-friendly layout, color coding, data visualization
  - **Skills**: [`frontend-ui-ux`]
    - `frontend-ui-ux`: Needed for clinician-friendly design decisions

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 12, 14, 15)
  - **Blocks**: Tasks 16, 18
  - **Blocked By**: Task 8

  **References**:
  - **API/Type References**:
    - `frontend/src/types/index.ts` (Task 8) — ReconciliationRequest, ReconciliationResponse types
  - **External References**:
    - Assessment PDF: "Displays reconciliation results in a clinician-friendly format", "Visualizes confidence scores and reasoning", "Allows users to approve or reject AI suggestions"
  - **WHY**: This directly addresses "Product Thinking" (20% of grade). The UI must be clear, not clever. Clinicians need to see the decision, the reasoning, and the confidence at a glance.

  **Acceptance Criteria**:
  - [ ] `cd frontend && pnpm build` → succeeds
  - [ ] Form renders with pre-filled Metformin example data
  - [ ] Results display shows all 5 response fields
  - [ ] ConfidenceBar renders with correct color for different scores
  - [ ] Approve/Reject buttons toggle state

  **QA Scenarios**:

  ```
  Scenario: Reconciliation panel renders with mock data
    Tool: Playwright (playwright skill)
    Preconditions: Frontend dev server running
    Steps:
      1. Navigate to http://localhost:5173
      2. Assert element with data-testid="reconciliation-form" is visible
      3. Assert form contains pre-filled example data
      4. Click data-testid="reconciliation-submit"
      5. Wait for data-testid="reconciliation-result" to appear (may need mock)
      6. Assert data-testid="confidence-score" displays a number
      7. Assert data-testid="safety-check" badge is visible
      8. Screenshot the panel
    Expected Result: Form and results display correctly
    Evidence: .sisyphus/evidence/task-13-reconciliation-panel.png

  Scenario: Confidence bar colors match score ranges
    Tool: Playwright
    Steps:
      1. Render ConfidenceBar with score=0.9 → assert green color class
      2. Render with score=0.6 → assert yellow
      3. Render with score=0.3 → assert red
    Expected Result: Correct color coding
    Evidence: .sisyphus/evidence/task-13-confidence-colors.png
  ```

  **Commit**: YES
  - Message: `feat: add reconciliation dashboard panel`
  - Files: `frontend/src/features/reconciliation/`, `frontend/src/components/ConfidenceBar.tsx`
  - Pre-commit: `cd frontend && pnpm build`

- [ ] 14. Data Quality Dashboard Panel

  **What to do**:
  - Create `frontend/src/features/data-quality/DataQualityForm.tsx`:
    - Form for patient data input:
      - Demographics: name, DOB, gender
      - Medications: editable list (add/remove)
      - Allergies: editable list
      - Conditions: editable list
      - Vital signs: blood pressure, heart rate
      - Last updated: date picker
    - Pre-fill with assessment's John Doe example as default
    - Submit button with loading state
    - `data-testid="data-quality-form"`, `data-testid="data-quality-submit"`
  - Create `frontend/src/features/data-quality/DataQualityPanel.tsx`:
    - Overall score display: large number with color (green >=80, yellow 50-79, red <50)
    - Dimension breakdown: 4 horizontal bars or gauge charts for completeness, accuracy, timeliness, clinical_plausibility
    - Each dimension: score number + bar + color indicator
    - Issues detected: table/list with field, issue description, severity badge (red high, yellow medium, green low)
    - `data-testid="data-quality-result"`, `data-testid="overall-score"`, `data-testid="issues-list"`
  - Create shared `frontend/src/components/ScoreIndicator.tsx`:
    - Takes `score: number` (0-100), renders colored badge/number
    - Green: >=80, Yellow: 50-79, Red: <50
    - `data-testid="score-indicator"`

  **Must NOT do**:
  - Do NOT install chart libraries (use CSS bars/gauges)
  - Do NOT connect to real API yet

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: Data visualization with color coding, multi-dimensional score display
  - **Skills**: [`frontend-ui-ux`]
    - `frontend-ui-ux`: Clinician-friendly data quality visualization

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 12, 13, 15)
  - **Blocks**: Tasks 16, 18
  - **Blocked By**: Task 8

  **References**:
  - **API/Type References**:
    - `frontend/src/types/index.ts` (Task 8) — DataQualityRequest, DataQualityResponse types
  - **External References**:
    - Assessment PDF: "Shows data quality scores with visual indicators (red/yellow/green)"
  - **WHY**: Red/yellow/green indicators are explicitly required by the assessment. The breakdown visualization is key for product thinking points.

  **Acceptance Criteria**:
  - [ ] `cd frontend && pnpm build` → succeeds
  - [ ] Form renders with pre-filled John Doe example
  - [ ] Overall score shows with correct color
  - [ ] 4 dimension breakdown bars/gauges display
  - [ ] Issues list shows severity-colored badges

  **QA Scenarios**:

  ```
  Scenario: Data quality panel renders with mock data
    Tool: Playwright (playwright skill)
    Preconditions: Frontend dev server running
    Steps:
      1. Navigate to http://localhost:5173
      2. Assert data-testid="data-quality-form" visible
      3. Click data-testid="data-quality-submit"
      4. Wait for data-testid="data-quality-result"
      5. Assert data-testid="overall-score" displays a number between 0-100
      6. Assert 4 dimension bars are visible
      7. Assert data-testid="issues-list" has at least 1 entry
      8. Screenshot
    Expected Result: Complete quality assessment display
    Evidence: .sisyphus/evidence/task-14-quality-panel.png

  Scenario: Score colors match ranges
    Tool: Playwright
    Steps:
      1. Display with overall_score=90 → assert green
      2. Display with overall_score=60 → assert yellow
      3. Display with overall_score=30 → assert red
    Expected Result: Correct color indicators
    Evidence: .sisyphus/evidence/task-14-score-colors.png
  ```

  **Commit**: YES
  - Message: `feat: add data quality dashboard panel`
  - Files: `frontend/src/features/data-quality/`, `frontend/src/components/ScoreIndicator.tsx`
  - Pre-commit: `cd frontend && pnpm build`

- [ ] 15. Mock Data Scenarios for Demo/Testing

  **What to do**:
  - Update `backend/app/services/llm/mock.py` with 3 rich mock scenarios:
    - **Scenario 1 (Assessment Example)**: Metformin dosage conflict across Hospital/PrimaryCare/Pharmacy → reconciles to 500mg based on eGFR, confidence 0.88
    - **Scenario 2 (Brand vs Generic)**: "Lipitor 20mg" vs "Atorvastatin 20mg" vs "Atorvastatin 40mg" → reconciles noting brand/generic equivalence, flags dose discrepancy
    - **Scenario 3 (Status Conflict)**: Aspirin "active" in one system, "discontinued" in another, patient portal says "not taking" → reconciles considering most recent clinical note
  - Each scenario has:
    - Full `ReconciliationResponse` with realistic clinical reasoning text (not placeholder)
    - `recommended_actions` that make clinical sense
    - Appropriate `clinical_safety_check` values
  - MockProvider uses input matching to return the right scenario (fall back to scenario 1 for unknown input)
  - Add mock data quality responses for the John Doe example (score 62) and a "perfect" patient

  **Must NOT do**:
  - Do NOT make mock responses trivial/placeholder — they should read like real clinical decisions
  - Do NOT over-complicate matching logic (simple medication name substring matching is fine)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Data definition, no complex logic. Just writing realistic mock responses.
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 12, 13, 14)
  - **Blocks**: Task 16
  - **Blocked By**: Task 4

  **References**:
  - **Pattern References**:
    - `backend/app/services/llm/mock.py` (Task 6) — Existing MockProvider to enhance
    - `backend/app/schemas/reconciliation.py` (Task 4) — Response shapes
  - **External References**:
    - Assessment PDF example outputs — mock responses should match these closely
    - PyHealth EHR data structures: `https://pyhealth.readthedocs.io/en/latest/api/data.html` — Reference for realistic EHR data patterns to make mock scenarios clinically convincing (medication events, patient demographics, visit structure)
  - **WHY**: Evaluator will likely run in mock mode first. Rich, realistic mock data makes a strong first impression and demonstrates clinical domain understanding. PyHealth data patterns help ensure mock data reflects real-world EHR structure.

  **Acceptance Criteria**:
  - [ ] MockProvider returns scenario-appropriate response based on input
  - [ ] All 3 reconciliation scenarios have reasoning text >50 characters
  - [ ] Mock data quality response for John Doe produces score ~62

  **QA Scenarios**:

  ```
  Scenario: Mock scenarios produce realistic responses
    Tool: Bash (python)
    Steps:
      1. Call MockProvider with Metformin input → assert reasoning mentions "kidney function" or "eGFR"
      2. Call with Lipitor/Atorvastatin input → assert reasoning mentions "brand" or "generic"
      3. Call with Aspirin status conflict → assert reasoning mentions "discontinued"
    Expected Result: Clinically relevant reasoning for each scenario
    Evidence: .sisyphus/evidence/task-15-mock-scenarios.txt
  ```

  **Commit**: YES
  - Message: `feat: add mock data scenarios for demo`
  - Files: `backend/app/services/llm/mock.py` (update)
  - Pre-commit: `cd backend && python -m pytest tests/ -v`

### Wave 5 — Integration + Polish (3 parallel, after Wave 4)

- [ ] 16. Frontend-Backend Wiring (CORS + Hooks + Integration)

  **What to do**:
  - Create `frontend/src/hooks/useReconcile.ts`:
    - Custom hook: `useReconcile()` returning `{ submit, result, loading, error, reset }`
    - `submit(request: ReconciliationRequest)` calls `api.reconcileMedication()`
    - Manages loading/error/success state
  - Create `frontend/src/hooks/useDataQuality.ts`:
    - Custom hook: `useDataQuality()` returning `{ submit, result, loading, error, reset }`
    - `submit(request: DataQualityRequest)` calls `api.validateDataQuality()`
  - Wire hooks into panel components:
    - `ReconciliationForm.tsx` uses `useReconcile().submit` on form submission
    - `ReconciliationPanel.tsx` displays `useReconcile().result`
    - `DataQualityForm.tsx` uses `useDataQuality().submit`
    - `DataQualityPanel.tsx` displays `useDataQuality().result`
  - Update `App.tsx` to compose both panels in a two-column layout
  - Ensure Vite proxy works (already configured in Task 3)
  - Verify CORS is working end-to-end (frontend → Vite proxy → backend)

  **Must NOT do**:
  - Do NOT add Redux, Zustand, or any state library — hooks + useState only
  - Do NOT add routing

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Integration work connecting multiple components, state management, data flow
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on all Wave 3+4 outputs)
  - **Parallel Group**: Wave 5 (with Tasks 17, 18 — but 17 depends on 16)
  - **Blocks**: Tasks 17, 18
  - **Blocked By**: Tasks 9, 10, 12, 13, 14, 15

  **References**:
  - **Pattern References**:
    - `frontend/src/lib/api.ts` (Task 8) — API client functions
    - `frontend/src/features/reconciliation/` (Task 13) — Components to wire
    - `frontend/src/features/data-quality/` (Task 14) — Components to wire
  - **WHY**: This is the integration layer. It must work end-to-end: user fills form → calls API → displays result.

  **Acceptance Criteria**:
  - [ ] `cd frontend && pnpm build` → succeeds
  - [ ] With both servers running: submit reconciliation form → see results displayed
  - [ ] With both servers running: submit data quality form → see scores displayed
  - [ ] Loading spinner shows during API call
  - [ ] Error message shows if backend is down

  **QA Scenarios**:

  ```
  Scenario: End-to-end reconciliation flow
    Tool: Playwright (playwright skill)
    Preconditions: Backend (mock mode) + frontend dev server running
    Steps:
      1. Navigate to http://localhost:5173
      2. Find reconciliation form (data-testid="reconciliation-form")
      3. Click submit (pre-filled with Metformin example)
      4. Wait for loading spinner to appear then disappear (timeout: 10s)
      5. Assert data-testid="reconciliation-result" is visible
      6. Assert data-testid="confidence-score" contains a number
      7. Screenshot full page
    Expected Result: Full round-trip works
    Evidence: .sisyphus/evidence/task-16-e2e-reconciliation.png

  Scenario: End-to-end data quality flow
    Tool: Playwright
    Preconditions: Both servers running
    Steps:
      1. Find data quality form
      2. Click submit (pre-filled with John Doe example)
      3. Wait for result display (timeout: 10s)
      4. Assert data-testid="overall-score" is visible
      5. Assert data-testid="issues-list" has entries
      6. Screenshot
    Expected Result: Quality scores display after submission
    Evidence: .sisyphus/evidence/task-16-e2e-quality.png
  ```

  **Commit**: YES
  - Message: `feat: connect frontend to backend API`
  - Files: `frontend/src/hooks/`, `frontend/src/App.tsx`, panel component updates
  - Pre-commit: `cd frontend && pnpm build`

- [ ] 17. Error Handling + Edge Cases + UI States

  **What to do**:
  - **Backend error handling**:
    - Global exception handler in `main.py` returning standardized error responses
    - LLM timeout → HTTP 503 with `{"detail":{"code":"LLM_TIMEOUT","message":"AI service temporarily unavailable"}}`
    - Rate limit exceeded → HTTP 429 with Retry-After header
    - Invalid input → HTTP 422 with field-specific error messages
    - Unexpected errors → HTTP 500 with generic message (no stack traces in production)
  - **Backend edge cases**:
    - Empty medication list (already handled by validation, but test)
    - Single source → still reconcile (return with confidence 1.0)
    - All sources identical → return with confidence 1.0, reasoning "All sources agree"
    - Very long medication names → truncate to 500 chars
    - Missing optional fields → use defaults gracefully
  - **Frontend states**:
    - Create `frontend/src/components/LoadingSpinner.tsx` with `data-testid="loading-spinner"`
    - Create `frontend/src/components/ErrorMessage.tsx` with `data-testid="error-message"`:
      - Shows error message
      - Retry button
    - Empty state: "Submit patient data to see results" placeholder
    - Loading state: Spinner with "Analyzing..." text
    - Error state: Red error message with retry button
    - Success state: Results display
  - **Frontend edge cases**:
    - Backend unreachable → show "Cannot connect to server. Is the backend running?"
    - 401 → show "Invalid API key. Check your configuration."
    - 429 → show "Rate limit reached. Try again in X seconds."
    - Network timeout → show "Request timed out. The AI analysis may be taking longer than usual."

  **Must NOT do**:
  - Do NOT expose stack traces in error responses
  - Do NOT ignore errors silently (always display something to user)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Cross-cutting error handling across backend + frontend, multiple edge cases
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: PARTIALLY (backend parts can run parallel with 18)
  - **Parallel Group**: Wave 5
  - **Blocks**: Task 19
  - **Blocked By**: Task 16

  **References**:
  - **Pattern References**:
    - `backend/app/main.py` (Task 2) — Add global exception handler
    - `backend/app/api/routes/` (Tasks 9, 10) — Routes to add error handling
    - `frontend/src/hooks/` (Task 16) — Hooks that need error state handling
  - **WHY**: Error handling is 30% of Code Quality grade and 25% of Problem Solving. Edge case handling demonstrates engineering maturity.

  **Acceptance Criteria**:
  - [ ] Backend returns standardized error JSON for all error cases
  - [ ] Frontend shows appropriate message for each error type
  - [ ] Loading spinner appears during API calls
  - [ ] Retry button works after error

  **QA Scenarios**:

  ```
  Scenario: Frontend shows error when backend is down
    Tool: Playwright (playwright skill)
    Preconditions: Frontend running, backend NOT running
    Steps:
      1. Navigate to http://localhost:5173
      2. Submit reconciliation form
      3. Wait for error state (timeout: 10s)
      4. Assert data-testid="error-message" is visible
      5. Assert error text mentions "connect" or "server"
      6. Screenshot
    Expected Result: User-friendly error message, not blank screen
    Evidence: .sisyphus/evidence/task-17-error-no-backend.png

  Scenario: Backend returns 422 for invalid input
    Tool: Bash (curl)
    Preconditions: Backend running
    Steps:
      1. POST /api/reconcile/medication with {"invalid": "data"}
      2. Assert HTTP 422
      3. Assert response has "detail" field with error info
    Expected Result: Structured validation error
    Evidence: .sisyphus/evidence/task-17-validation-error.txt
  ```

  **Commit**: YES
  - Message: `fix: add error handling, loading states, and edge cases`
  - Files: Various backend + frontend files
  - Pre-commit: `cd backend && python -m pytest tests/ -v && cd ../frontend && pnpm build`

- [ ] 18. Frontend Component Tests (3 Vitest Tests)

  **What to do**:
  - Create `frontend/tests/ReconciliationPanel.test.tsx`:
    - **TEST**: Renders reconciliation result with all required fields (mock result data)
    - Mock `useReconcile` hook to return pre-set result
    - Assert: `data-testid="reconciliation-result"` visible, confidence score displayed, safety check badge visible
  - Create `frontend/tests/DataQualityPanel.test.tsx`:
    - **TEST**: Renders data quality scores with correct colors (mock result data)
    - Mock `useDataQuality` hook
    - Assert: `data-testid="overall-score"` shows number, dimension bars visible, issues list populated
  - Create `frontend/tests/ConfidenceBar.test.tsx`:
    - **TEST**: ConfidenceBar renders correct color for different score ranges
    - Render with score=0.9 → assert green class
    - Render with score=0.6 → assert yellow class
    - Render with score=0.3 → assert red class

  **Must NOT do**:
  - Do NOT test implementation details (internal state, private methods)
  - Do NOT use snapshot testing
  - Do NOT test the API client directly (that's integration, not unit)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 3 straightforward component tests following standard testing-library patterns
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (partially, needs components from 13/14)
  - **Parallel Group**: Wave 5 (with Tasks 16, 17)
  - **Blocks**: Task 19
  - **Blocked By**: Tasks 13, 14, 16

  **References**:
  - **Pattern References**:
    - `frontend/src/features/reconciliation/ReconciliationPanel.tsx` (Task 13) — Component to test
    - `frontend/src/features/data-quality/DataQualityPanel.tsx` (Task 14) — Component to test
    - `frontend/src/components/ConfidenceBar.tsx` (Task 13) — Component to test
  - **External References**:
    - Testing Library docs: https://testing-library.com/docs/react-testing-library/intro — Query patterns
  - **WHY**: Assessment requires 5+ tests. These 3 frontend tests + 4+ backend tests = 7+ total, exceeding requirement by 40%.

  **Acceptance Criteria**:
  - [ ] `cd frontend && pnpm test -- --run` → 3 tests PASS
  - [ ] Tests use `screen.getByTestId()` for reliable querying
  - [ ] No snapshot tests

  **QA Scenarios**:

  ```
  Scenario: All frontend tests pass
    Tool: Bash
    Steps:
      1. Run `cd frontend && pnpm test -- --run`
      2. Assert exit code 0
      3. Assert output shows 3 tests passed
    Expected Result: All 3 tests pass
    Evidence: .sisyphus/evidence/task-18-frontend-tests.txt
  ```

  **Commit**: YES
  - Message: `test: add frontend component tests`
  - Files: `frontend/tests/ReconciliationPanel.test.tsx`, `DataQualityPanel.test.tsx`, `ConfidenceBar.test.tsx`
  - Pre-commit: `cd frontend && pnpm test -- --run`

### Wave 6 — Documentation (after Wave 5)

- [ ] 19. README + Architecture + Design Decisions

  **What to do**:
  - Complete `README.md` with all required sections:
    - **Overview**: What the app does, tech stack summary
    - **Setup Instructions** (< 5 commands):
      ```
      1. Clone the repo
      2. cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
      3. cp .env.example .env  # Edit with your API keys (or leave defaults for mock mode)
      4. cd frontend && pnpm install
      5. Start: cd backend && uvicorn app.main:app --reload  |  cd frontend && pnpm dev
      ```
    - **Architecture Diagram** (ASCII or Mermaid):
      ```
      [React Dashboard] → [Vite Proxy] → [FastAPI Backend]
                                              ├── Routes (reconciliation, data_quality)
                                              ├── Services (business logic)
                                              ├── LLM Providers (GitHub Models / Anthropic / Mock)
                                              └── SQLite (cache, results)
      ```
    - **Which LLM API and Why**: GitHub Models (free GPT-4o via student benefit) + Anthropic Claude fallback. Explain provider abstraction pattern.
    - **Key Design Decisions and Trade-offs**:
      - Why FastAPI + React (not full-stack framework)
      - Why SQLite over PostgreSQL (simplicity, zero-config, sufficient for scope)
      - Why provider abstraction pattern (swap LLMs without code changes)
      - Why rule-based + AI hybrid for scoring (deterministic baseline + AI enhancement)
      - Why Tailwind (minimal, utility-first, no heavy dependencies)
    - **Prompt Engineering Approach**: Document prompt design philosophy, system prompts, why JSON output mode, temperature choice
    - **What I'd Improve with More Time**: Docker, more tests, real-time webhooks, duplicate detection, deployment, proper medical ontology (RxNorm/SNOMED)
    - **Estimated Time Spent**: [To be filled by user]
    - **API Documentation**: Both endpoint specs with curl examples
    - **Test Data**: Reference to pre-built mock scenarios

  **Must NOT do**:
  - Do NOT add a separate ARCHITECTURE.md — keep everything in README.md
  - Do NOT make README longer than 300 lines — be concise

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: Technical writing, documentation, clear communication
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 6 (solo)
  - **Blocks**: FINAL wave
  - **Blocked By**: Tasks 17, 18

  **References**:
  - **Pattern References**: All previous tasks (summarizing the full architecture)
  - **External References**:
    - Assessment PDF submission guidelines — README requirements
    - PyHealth EHR data structures: `https://pyhealth.readthedocs.io/en/latest/api/data.html` — Mention in README as the EHR data reference that informed schema design. Demonstrates domain research and clinical awareness.
  - **WHY**: README is the evaluator's first impression. It must be concise, complete, and professional. Setup must be < 5 commands. Referencing PyHealth shows research depth.

  **Acceptance Criteria**:
  - [ ] README contains: Overview, Setup, Architecture, LLM choice, Design Decisions, Trade-offs, Improvements, Time Spent, API docs
  - [ ] Setup instructions are <= 5 commands
  - [ ] Architecture diagram present (ASCII or Mermaid)
  - [ ] At least 3 design decisions documented with trade-off analysis
  - [ ] "What I'd improve" section has 4+ items
  - [ ] README is < 300 lines

  **QA Scenarios**:

  ```
  Scenario: README completeness check
    Tool: Bash
    Steps:
      1. Run `cat README.md | grep -c "##"` — assert >= 8 section headers
      2. Assert contains "Setup" or "Getting Started"
      3. Assert contains "Architecture"
      4. Assert contains "Design Decisions" or "Technical Decisions"
      5. Assert contains "Trade-offs" or "tradeoff"
      6. Assert contains "Improve" or "Future"
      7. Run `wc -l README.md` — assert < 300 lines
    Expected Result: All required sections present, concise
    Evidence: .sisyphus/evidence/task-19-readme-check.txt
  ```

  **Commit**: YES
  - Message: `docs: complete README with architecture and design decisions`
  - Files: `README.md`
  - Pre-commit: none

---

## Final Verification Wave

> 4 review agents run in PARALLEL. ALL must APPROVE. Rejection → fix → re-run.

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, curl endpoint, run command). For each "Must NOT Have": search codebase for forbidden patterns (fhir.resources import, react-router, Redux, Material UI, as any, console.log in non-test files). Check evidence files exist in `.sisyphus/evidence/`. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  Run `cd backend && python -m pytest tests/ -v` + `cd frontend && pnpm test` + `cd frontend && pnpm build`. Review all changed files for: `# type: ignore`, `as any`, empty except blocks, `console.log` in production code, commented-out code, unused imports. Check AI slop: excessive comments, over-abstraction, generic variable names (data/result/item/temp). Verify Pydantic models have proper field validators.
  Output: `Backend Tests [PASS/FAIL] | Frontend Tests [PASS/FAIL] | Build [PASS/FAIL] | Files [N clean/N issues] | VERDICT`

- [ ] F3. **Real Manual QA** — `unspecified-high` (+ `playwright` skill)
  Start from clean state (`pip install -r requirements.txt && pnpm install`). Start backend + frontend. Execute EVERY QA scenario from EVERY task — follow exact steps, capture evidence. Test cross-feature integration: submit reconciliation → view results → submit data quality → view scores. Test edge cases: empty medication list, missing fields, invalid API key. Save to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff (`git log --oneline && git diff main...HEAD`). Verify 1:1 — everything in spec was built (no missing), nothing beyond spec was built (no creep). Check assessment requirements: 2 endpoints exist, AI integration works, frontend displays results, 5+ tests exist, auth works, README complete. Check "Must NOT do" compliance. Flag any bonus features that were added without core completion.
  Output: `Tasks [N/N compliant] | Assessment Requirements [N/N] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

| # | Commit Message | Files | Pre-commit Check |
|---|---------------|-------|-----------------|
| 1 | `chore: init project structure with gitignore` | `.gitignore`, `README.md` skeleton, directory structure | — |
| 2 | `chore: setup backend with FastAPI and config` | `backend/` scaffolding, `requirements.txt`, `app/main.py`, `app/core/config.py`, health check | `cd backend && python -c "from app.main import app"` |
| 3 | `chore: setup frontend with Vite React TypeScript` | `frontend/` scaffolding, `package.json`, `vite.config.ts`, `App.tsx` | `cd frontend && pnpm build` |
| 4 | `feat: add request/response schemas` | `app/schemas/reconciliation.py`, `app/schemas/data_quality.py` | `cd backend && python -c "from app.schemas import reconciliation, data_quality"` |
| 5 | `feat: add SQLite database setup and cache model` | `app/core/database.py`, `app/models/cache.py` | `cd backend && python -c "from app.core.database import engine"` |
| 6 | `feat: add LLM provider abstraction with mock provider` | `app/services/llm/` | `cd backend && python -m pytest tests/test_llm_providers.py -v` |
| 7 | `feat: add API key authentication middleware` | `app/core/security.py`, `tests/test_auth.py` | `cd backend && python -m pytest tests/test_auth.py -v` |
| 8 | `feat: add frontend types and API client` | `frontend/src/types/`, `frontend/src/lib/api.ts` | `cd frontend && pnpm build` |
| 9 | `feat: implement medication reconciliation endpoint` | `app/api/routes/reconciliation.py`, `app/services/reconciliation.py`, `tests/test_reconciliation.py` | `cd backend && python -m pytest tests/test_reconciliation.py -v` |
| 10 | `feat: implement data quality validation endpoint` | `app/api/routes/data_quality.py`, `app/services/data_quality.py`, `tests/test_data_quality.py` | `cd backend && python -m pytest tests/test_data_quality.py -v` |
| 11 | `feat: add LLM response caching with SQLite` | `app/services/llm/cache.py` | `cd backend && python -m pytest tests/ -v` |
| 12 | `feat: integrate GitHub Models and Anthropic LLM providers` | `app/services/llm/github_models.py`, `app/services/llm/anthropic_provider.py`, `app/services/llm/prompts.py` | `cd backend && python -m pytest tests/test_llm_providers.py -v` |
| 13 | `feat: add reconciliation dashboard panel` | `frontend/src/features/reconciliation/` | `cd frontend && pnpm build` |
| 14 | `feat: add data quality dashboard panel` | `frontend/src/features/data-quality/` | `cd frontend && pnpm build` |
| 15 | `feat: add mock data scenarios for demo` | `backend/app/services/llm/mock.py` update, mock data | `cd backend && python -m pytest tests/ -v` |
| 16 | `feat: connect frontend to backend API` | `frontend/src/hooks/`, `frontend/src/lib/api.ts`, CORS config | `cd frontend && pnpm build` |
| 17 | `fix: add error handling, loading states, and edge cases` | Various files | `cd backend && python -m pytest tests/ -v && cd ../frontend && pnpm build` |
| 18 | `test: add frontend component tests` | `frontend/tests/` | `cd frontend && pnpm test` |
| 19 | `docs: complete README with architecture and design decisions` | `README.md` | — |

---

## Success Criteria

### Verification Commands
```bash
# Backend tests
cd backend && python -m pytest tests/ -v  # Expected: 6+ tests PASS

# Frontend tests
cd frontend && pnpm test  # Expected: 3+ tests PASS

# Frontend build
cd frontend && pnpm build  # Expected: Build succeeds, no errors

# Health check
curl -s http://localhost:8000/api/health  # Expected: {"status": "ok"}

# Auth rejection (no API key)
curl -s -w "%{http_code}" http://localhost:8000/api/reconcile/medication  # Expected: 401 or 403

# Reconciliation endpoint (mock mode)
curl -s -X POST http://localhost:8000/api/reconcile/medication \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-key" \
  -d '{"patient_context":{"age":67,"conditions":["Type 2 Diabetes"]},"sources":[{"system":"Hospital","medication":"Metformin 1000mg","last_updated":"2024-10-15","source_reliability":"high"}]}'
# Expected: JSON with reconciled_medication, confidence_score, reasoning, recommended_actions, clinical_safety_check

# Data quality endpoint (mock mode)
curl -s -X POST http://localhost:8000/api/validate/data-quality \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-key" \
  -d '{"demographics":{"name":"John Doe","dob":"1955-03-15","gender":"M"},"medications":["Metformin 500mg"],"allergies":[],"conditions":["Type 2 Diabetes"],"vital_signs":{"blood_pressure":"120/80","heart_rate":72},"last_updated":"2024-06-15"}'
# Expected: JSON with overall_score (0-100), breakdown (4 dimensions), issues_detected array

# Frontend loads
curl -s http://localhost:5173 | grep -q "Clinical" && echo "OK"  # Expected: OK
```

### Final Checklist
- [ ] All "Must Have" items present and verified
- [ ] All "Must NOT Have" items confirmed absent
- [ ] All backend tests pass (`python -m pytest tests/ -v`)
- [ ] All frontend tests pass (`pnpm test`)
- [ ] Frontend builds without errors (`pnpm build`)
- [ ] Both endpoints return correct response shapes
- [ ] Mock mode works without any API keys
- [ ] API key auth rejects unauthenticated requests
- [ ] README contains: setup, architecture, design decisions, trade-offs, improvements
- [ ] Git history has clean atomic commits with conventional messages
- [ ] Assessment evaluation criteria addressed: Code Quality, AI Integration, Problem Solving, Product Thinking
