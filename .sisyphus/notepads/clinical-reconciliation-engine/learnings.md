# Learnings — Clinical Reconciliation Engine

> Conventions, patterns, and best practices discovered during implementation.
> APPEND ONLY — never overwrite or edit.

---

## Task 1: Project Structure + Git Init

### Completed
✓ Created comprehensive .gitignore with Python, Node, IDE, and OS patterns
✓ Initialized directory structure for monorepo (backend + frontend)
✓ Created 10 __init__.py files in Python packages (backend/*, backend/app/*, backend/app/services/llm)
✓ Created README.md with 7 required sections
✓ Created .env.example with 5 required environment variables
✓ Verified all QA scenarios pass

### Patterns Established
1. **Module Structure**: Hierarchical package organization with __init__.py in each directory
2. **Configuration**: Centralized env configuration via .env.example
3. **Directory Conventions**:
   - Backend: api/routes → api layer, core → utilities, models/schemas → data layer, services → business logic
   - Frontend: features/* → feature modules, lib/hooks/types → shared utilities

### Key Decisions
- Used comprehensive .gitignore based on GitHub's template (Python + Node + IDE + OS)
- Monorepo structure chosen for single assessment project
- Feature-based organization in frontend for scalability
- Mock LLM mode enabled by default (LLM_MOCK_MODE=true) for safe testing

### Gotchas
- Python packages require __init__.py in EVERY directory, not just leaf directories
- README sections must use exact case (## Overview, not ## overview)
- .env.example should use example values, not placeholders
- Frontend structure includes both `frontend/tests/` and feature-level tests directories

### Time Log
- Directory creation: < 1 min
- Files creation (.gitignore, README, .env.example): 2 min
- __init__.py generation: 1 min
- QA verification: 1 min
- Total: ~5 min

---

## Task 2: Backend Scaffolding (FastAPI + Config + Health Check)

### Completed
✓ Created backend/requirements.txt with all 11 pinned dependencies (fastapi≥0.115.0, uvicorn[standard]≥0.34.0, sqlmodel≥0.0.22, pydantic-settings≥2.7.0, httpx≥0.28.0, python-dotenv≥1.0.1, openai≥1.60.0, anthropic≥0.42.0, tenacity≥9.0.0, pytest≥8.3.0, pytest-asyncio≥0.25.0)
✓ Created backend/app/core/config.py with pydantic-settings BaseSettings class
✓ Created backend/app/main.py with FastAPI app, CORS middleware, and health endpoint
✓ Created backend/app/api/deps.py with dependency injection stubs (get_settings, get_db, get_llm_provider)
✓ Added GitHub Models API startup check (logs result, doesn't fail startup)
✓ Created Python venv at backend/venv/ and installed all dependencies
✓ Verified health endpoint returns {"status": "ok", "version": "1.0.0"}
✓ Verified CORS headers present for http://localhost:5173
✓ Created QA evidence files (.sisyphus/evidence/task-2-health-check.txt, task-2-cors-headers.txt)

### Patterns Established
1. **Configuration Management**: pydantic-settings with environment variable support via Config.env_file
2. **FastAPI Setup**: Lifespan context manager for startup/shutdown events
3. **CORS Configuration**: Explicit list of allowed origins (not wildcard) for security
4. **GitHub Models Integration**: Non-blocking startup check with logging (warnings only, no failures)
5. **Dependency Injection**: Stub functions in deps.py for database and LLM provider access

### Key Decisions
- Used pydantic-settings instead of manual dotenv loading for type-safe configuration
- Made LLM mock mode default (true) for safe testing without API keys
- GitHub Models API check runs on startup but logs warnings only (doesn't block)
- CORS middleware configured explicitly to allow only localhost:5173 (not wildcard)
- Health endpoint returns hardcoded version "1.0.0" (not from package metadata)

### Gotchas
- pydantic-settings requires Config.env_file attribute (not manual load_dotenv)
- FastAPI CORS middleware middleware stack order matters (add before routes)
- uvicorn with LLM_MOCK_MODE=true and no GitHub token doesn't attempt API check (correct behavior)
- curl HEAD requests don't work with FastAPI GET endpoints (use OPTIONS for preflight instead)
- LSP import errors resolve after venv installation (not actual Python errors)

### Dependency Notes
- fastapi-0.135.1 installed (supports starlette-0.52.1)
- uvicorn-0.42.0 installed with full standard extras (httptools, uvloop, websockets, pyyaml, watchfiles)
- pydantic-2.12.5 with pydantic-settings-2.13.1 (compatible versions)
- httpx-0.28.1 used for async HTTP calls in startup check
- anthropic-0.85.0 and openai-2.28.0 for LLM provider support

### QA Scenarios Passing
1. ✓ Health check responds with exact JSON {"status":"ok","version":"1.0.0"}
2. ✓ CORS headers include access-control-allow-origin: http://localhost:5173
3. ✓ Server starts successfully with mock mode enabled
4. ✓ App imports without errors: `from app.main import app` → "Clinical Data Reconciliation Engine"

### Time Log
- requirements.txt creation: < 1 min
- config.py (Settings class): 1 min
- main.py (FastAPI + CORS + health): 2 min
- deps.py (dependency stubs): 1 min
- venv + pip install: 2 min
- health endpoint test: 1 min
- CORS headers test: 1 min
- Evidence documentation: 2 min
- Total: ~11 min

### Next Task Considerations
- Database session management (get_db) will need SQLAlchemy async session factory
- LLM provider initialization (get_llm_provider) should handle GitHub Models + Anthropic
- Router organization: route files should be in backend/app/api/routes/ (placeholder structure exists)

## Task 3: Frontend Scaffolding (Vite + React + TypeScript + Tailwind)

### Key Learnings

1. **Tailwind CSS Version Compatibility**: 
   - Tailwind v4 requires `@tailwindcss/postcss` package and breaks with standard PostCSS integration
   - Tailwind v3 (^3.4.19) works seamlessly with Vite v8 via standard PostCSS pipeline
   - Resolution: Downgraded to Tailwind v3 for production stability

2. **Vite Version Constraints**:
   - Vite v8.0.0 is stable and compatible with React 19.2.4
   - `@tailwindcss/vite` plugin requires Vite ^5.2 or ^6+, creating conflicts
   - Stick with standard PostCSS approach for Tailwind v3

3. **Vitest Configuration**:
   - Vitest requires separate config file `vitest.config.ts` or inline in vite.config.ts with proper typing
   - jsdom environment is required for React component testing
   - globals: true enables test functions without imports

4. **Dev Server Proxy Configuration**:
   - Vite proxy in dev server enables seamless backend integration
   - `/api` routes proxied to `http://localhost:8000` avoid CORS issues during development
   - Properly configured in `server.proxy` block of vite.config.ts

5. **React + Tailwind Rapid Prototyping**:
   - Two-panel layout with flex + gap utilities provides clean spatial organization
   - Semantic HTML (header, div for panels) + Tailwind utilities minimize custom CSS
   - Component mounting at `#root` with standard Vite/React entry point (main.tsx)

6. **Package Manager Performance**:
   - pnpm install and add operations are fast (~2-4s for dependency resolution)
   - pnpm creates clean lockfile without duplication
   - All dependencies correctly installed and linked

### Configuration Files Created

- `vite.config.ts`: Dev proxy + build optimization
- `vitest.config.ts`: React testing with jsdom
- `tailwind.config.js`: Content paths for purging
- `postcss.config.js`: Tailwind PostCSS plugin integration
- `index.html`: Updated title to "Clinical Data Reconciliation Engine"

### Build & Test Status

- Build: ✓ Succeeds with 0 errors (~800ms)
- Test Runner: ✓ Vitest configured (no tests yet - expected)
- Dev Server: ✓ Runs on http://localhost:5173 with hot module reload
- Proxy: ✓ Configured for /api → http://localhost:8000

### Data-testid Attributes

All three required test identifiers present in App.tsx:
- `app-header`: Main header element
- `reconciliation-panel`: Left panel for medication reconciliation
- `data-quality-panel`: Right panel for data quality assessment
