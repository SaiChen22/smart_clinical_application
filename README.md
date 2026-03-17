# Clinical Data Reconciliation Engine

AI-powered full-stack application that reconciles medication data from multiple EHR sources and assesses patient data quality using LLM analysis.

## Quick Start

```bash
# 1. Clone and configure
cp .env.example .env  # Edit with your API keys (or leave LLM_MOCK_MODE=true)
cp .env backend/.env  # Backend loads .env from backend/ when started there

# 2. Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 3. Frontend (new terminal)
cd frontend
echo "VITE_API_KEY=your-api-key-here" > .env.local
pnpm install && pnpm dev
```

Open the Vite URL shown in terminal (usually [http://localhost:5173](http://localhost:5173)). The app works immediately in mock mode — no API keys required.

## API Endpoints

### `POST /api/reconcile/medication`
Reconcile conflicting medication records from multiple EHR sources.

**Request:**
```json
{
  "patient_context": {
    "age": 58,
    "conditions": ["type 2 diabetes"],
    "recent_labs": {"hba1c": 7.1}
  },
  "sources": [
    {"system": "Hospital EHR", "medication": "Metformin 500mg", "last_updated": "2024-02-20", "source_reliability": "high"},
    {"system": "Pharmacy", "medication": "Metformin 1000mg", "last_updated": "2024-03-02", "source_reliability": "high"}
  ]
}
```

**Response:** Reconciled medication with confidence score, clinical reasoning, safety check, and recommended actions.

### `POST /api/data-quality/validate`
Assess completeness, accuracy, timeliness, and clinical plausibility of patient data.

**Request:**
```json
{
  "demographics": {"name": "John Doe", "dob": "1975-06-15", "gender": "male"},
  "medications": ["Lisinopril 10mg"],
  "allergies": ["Penicillin"],
  "conditions": ["hypertension"],
  "vital_signs": {"blood_pressure": "120/80", "heart_rate": 72, "temperature": 37.0},
  "last_updated": "2024-01-01"
}
```

**Response:** Overall quality score (0-100), dimensional breakdown, and detected issues with severity levels.

**Auth:** All endpoints require `X-API-Key` header (value from `API_KEY` env var).

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                    React Frontend                     │
│  ┌─────────────┐  ┌────────────┐  ┌───────────────┐ │
│  │ Reconcile   │  │ Data       │  │  Reusable     │ │
│  │ Form/Panel  │  │ Quality    │  │  Components   │ │
│  │             │  │ Form/Panel │  │  (Confidence,  │ │
│  │ useReconcile│  │ useDataQty │  │   Score, etc.) │ │
│  └──────┬──────┘  └─────┬──────┘  └───────────────┘ │
│         │               │                            │
│         └───────┬───────┘                            │
│            API Client (lib/api.ts)                    │
└────────────────────┬─────────────────────────────────┘
                     │ HTTP + X-API-Key
┌────────────────────┴─────────────────────────────────┐
│                  FastAPI Backend                      │
│  ┌─────────┐  ┌────────────┐  ┌──────────────────┐  │
│  │  Auth   │  │   Routes   │  │    Exception     │  │
│  │Middleware│──│ /reconcile │  │    Handlers      │  │
│  │         │  │ /data-qual │  │ (429,503,500)    │  │
│  └─────────┘  └─────┬──────┘  └──────────────────┘  │
│                      │                                │
│              ┌───────┴────────┐                       │
│              │  Service Layer │                       │
│              │ Reconciliation │                       │
│              │ DataQuality    │                       │
│              └───────┬────────┘                       │
│                      │                                │
│         ┌────────────┴─────────────┐                 │
│         │    LLM Provider Layer    │                 │
│         │  ┌──────┐ ┌──────────┐  │                 │
│         │  │ Mock │ │ GitHub   │  │  ┌──────────┐  │
│         │  │      │ │ Models   │  │  │ SQLite   │  │
│         │  └──────┘ │ (GPT-4o) │  │  │ Cache    │  │
│         │           └──────────┘  │  └──────────┘  │
│         │  ┌──────────┐           │                 │
│         │  │ Anthropic │           │                 │
│         │  │ (Claude)  │           │                 │
│         │  └──────────┘           │                 │
│         └──────────────────────────┘                 │
└──────────────────────────────────────────────────────┘
```

### Backend (`backend/`)

| Directory | Purpose |
|---|---|
| `app/api/routes/` | FastAPI endpoint handlers with Pydantic validation |
| `app/core/` | Config (pydantic-settings), API key auth, SQLite DB, custom exceptions |
| `app/schemas/` | Request/response Pydantic models mirroring clinical data structures |
| `app/services/` | Business logic — reconciliation + data quality assessment |
| `app/services/llm/` | Provider abstraction: mock, GitHub Models (GPT-4o), Anthropic (Claude) |
| `tests/` | 13 unit tests: auth, reconciliation, data quality, error handling, LLM providers |

### Frontend (`frontend/`)

| Directory | Purpose |
|---|---|
| `src/features/reconciliation/` | Medication reconciliation form + result panel |
| `src/features/data-quality/` | Data quality form + result panel |
| `src/components/` | Reusable: ConfidenceBar, ScoreIndicator, LoadingSpinner, ErrorMessage |
| `src/hooks/` | Custom hooks managing API state (loading, error, result) |
| `src/lib/` | API client with typed error handling |
| `src/types/` | TypeScript interfaces mirroring backend Pydantic schemas |
| `tests/` | 11 Vitest component tests with React Testing Library |

## Running Tests

```bash
# Backend (13 tests)
cd backend
source venv/bin/activate
python -m pytest tests/ -v

# Frontend (11 tests)
cd frontend
pnpm test -- --run
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `LLM_MOCK_MODE` | No | `true` | Use mock LLM provider (no API keys needed) |
| `LLM_PROVIDER` | No | `mock` | LLM provider: `github_models`, `anthropic`, `mock` |
| `API_KEY` | Yes | — | API key for endpoint authentication |
| `GITHUB_TOKEN` | If using GitHub Models | — | GitHub personal access token with Models scope |
| `ANTHROPIC_API_KEY` | If using Anthropic | — | Anthropic API key |
| `VITE_API_KEY` | Yes (frontend) | — | API key passed to frontend (same as `API_KEY`) |

## Design Decisions

1. **LLM Provider Abstraction** — A `LLMProvider` base class with `reconcile_medications()` and `assess_data_quality()` methods, allowing hot-swappable providers (Mock → GitHub Models → Anthropic) via env var. Mock mode enables instant development and CI without API keys.

2. **Service Layer Separation** — Business logic (`ReconciliationService`, `DataQualityService`) is decoupled from HTTP handlers. This makes testing straightforward: mock the service, not the HTTP layer. Exception handlers convert domain errors to proper HTTP responses.

3. **Custom Exception Hierarchy** — Four exception classes (`LLMTimeoutError`, `RateLimitError`, `ReconciliationError`, `DataQualityError`) with global FastAPI handlers returning appropriate status codes (503, 429, 500) and `Retry-After` headers.

4. **Feature-Based Frontend** — Components grouped by domain (reconciliation, data-quality), each with a Form (input) and Panel (output). Custom hooks (`useReconcile`, `useDataQuality`) encapsulate API state management with `useState` only — no Redux or external state libraries.

5. **Type Parity** — TypeScript interfaces mirror Pydantic schemas field-for-field. This catches contract mismatches at compile time rather than runtime.

6. **SQLite Response Cache** — LLM responses are cached by request hash in SQLite, reducing redundant API calls during development and providing offline capability with the mock provider.

## Trade-offs

| Decision | Chose | Alternative | Why |
|---|---|---|---|
| State management | `useState` hooks | Redux/Zustand | Two independent features with no shared state — hooks are sufficient and simpler |
| Styling | Tailwind CSS | Component library (MUI, Chakra) | Fewer dependencies, full design control, lighter bundle |
| Database | SQLite | PostgreSQL | Zero-config for development; cache-only usage doesn't need relational features |
| LLM prompts | Inline structured prompts | LangChain/DSPy | Direct API calls are more transparent, debuggable, and avoid framework lock-in |
| Monorepo | Single repo, separate dirs | Turborepo/Nx | Assessment scope doesn't justify monorepo tooling overhead |
| Auth | API key in header | JWT/OAuth | Assessment requirement is "basic authentication" — API key is appropriate scope |

## What I'd Improve

1. **FHIR Compliance** — Replace flat schemas with FHIR R4 resources for real-world interoperability. Current schemas are simplified for clarity.

2. **Streaming Responses** — SSE/WebSocket for LLM streaming so users see partial results during long reconciliations.

3. **Audit Trail** — Persist reconciliation decisions (approve/reject) with timestamps and clinician IDs for regulatory compliance.

4. **Structured Output Validation** — Use OpenAI's JSON mode or function calling to guarantee LLM response schema instead of parsing free-text.

5. **CI/CD** — GitHub Actions for automated testing, linting, and type-checking on every PR.

6. **E2E Tests** — Playwright tests for critical user flows (submit reconciliation → view result → approve/reject).

7. **Rate Limiting** — Backend rate limiting per API key to prevent LLM cost overruns.

8. **Observability** — Structured logging with request correlation IDs, LLM latency metrics, and error tracking.

## Tech Stack

**Backend:** Python 3.12, FastAPI, Pydantic, SQLModel, SQLite, httpx, openai, anthropic  
**Frontend:** React 19, TypeScript 5.9, Vite 8, Tailwind CSS 3  
**Testing:** pytest (backend), Vitest + React Testing Library + jest-dom (frontend)
