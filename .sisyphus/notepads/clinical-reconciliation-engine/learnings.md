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

---

## Task 4: Pydantic Request/Response Schemas

### Completed
✓ Created reconciliation.py with 4 models (PatientContext, MedicationSource, ReconciliationRequest, ReconciliationResponse)
✓ Created data_quality.py with 6 models (Demographics, VitalSigns, DataQualityRequest, IssueDetected, QualityBreakdown, DataQualityResponse)
✓ Updated schemas/__init__.py to export all 10 models
✓ Added field validators for age (0-150) and confidence_score (0.0-1.0)
✓ Executed QA Scenario 1: All valid inputs accepted (4 test cases)
✓ Executed QA Scenario 2: All invalid inputs rejected (8 test cases)
✓ Saved evidence to .sisyphus/evidence/task-4-schema-*.txt

### Patterns Established

1. **Pydantic v2 BaseModel Usage**:
   - All schemas inherit from `pydantic.BaseModel`
   - Field constraints use `Field(..., ge=X, le=Y, min_length=Z, max_length=W)`
   - Field descriptors always include description parameter for clarity

2. **Type Annotations**:
   - Used `Literal` from typing for enum-like constraints (source_reliability, clinical_safety_check, severity)
   - Used optional fields with `str | None = Field(default=None)` syntax (Python 3.10+)
   - Used `list[str]` and `dict[str, float]` for collections (generic syntax)

3. **Validators**:
   - Implemented `@field_validator` decorators with `@classmethod` for custom validation logic
   - Added explicit validation for confidence_score (0.0-1.0) and overall_score (0-100)
   - Field constraints (ge, le) provide first-line validation; validators add explicit logic

4. **Model Composition**:
   - PatientContext and Demographics are standalone models used in requests
   - MedicationSource is a component used in ReconciliationRequest (list)
   - QualityBreakdown is a component embedded in DataQualityResponse
   - Response models match exact JSON shape from assessment spec

5. **Export Strategy**:
   - Central __init__.py imports all models from submodules
   - __all__ list ensures explicit exports (prevents namespace pollution)
   - Enables clean imports: `from app.schemas import ReconciliationRequest`

### Key Decisions

- **Literal over Enum**: Used `Literal["high", "medium", "low"]` instead of creating Enum classes for simplicity and JSON serialization
- **Default dict/list**: Used `default_factory=dict` and implicit list defaults to prevent mutable default issues
- **Optional fields**: Made Demographics and VitalSigns fields optional (None default) since real EHR data often sparse
- **Dual validation**: Used both Field constraints (ge/le/min_length) and @field_validator for defense-in-depth
- **Response shapes**: Structured DataQualityResponse with nested QualityBreakdown to match assessment spec exactly

### Gotchas

1. **Field constraints vs validators**: `Field(..., ge=0.0, le=1.0)` validates range, but field_validator adds explicit error message
2. **Mutable defaults**: Must use `default_factory=dict` not `default={}` for collections
3. **Literal vs string**: `Literal["PASSED"]` requires exact case; "passed" would fail validation
4. **Import paths**: Schemas module needs `sys.path.insert(0, backend_path)` in tests unless run from backend directory

### Testing Summary

**QA Scenario 1: Valid Input Acceptance**
- ✓ ReconciliationRequest with 2 sources, age=65, confidence_score=0.88
- ✓ ReconciliationResponse with all fields valid
- ✓ DataQualityRequest with full demographics and vitals
- ✓ DataQualityResponse with scores 0-100
- Result: 4/4 tests passed

**QA Scenario 2: Invalid Input Rejection**
- ✓ Empty sources list (violates min_length=1)
- ✓ Invalid reliability="invalid" (not in Literal)
- ✓ confidence_score=1.5 (violates le=1.0)
- ✓ confidence_score=-0.5 (violates ge=0.0)
- ✓ age=151 (violates le=150)
- ✓ age=-1 (violates ge=0)
- ✓ overall_score=101 (violates le=100)
- ✓ severity="critical" (not in Literal)
- Result: 8/8 tests passed (all rejected correctly)

### Time Log
- reconciliation.py creation: 2 min
- data_quality.py creation: 2 min
- __init__.py exports: 1 min
- QA testing (scenarios 1 & 2): 2 min
- Evidence documentation: 1 min
- Total: ~8 min

### Next Task Considerations
- Endpoint handlers in backend/app/api/routes/ will use these schemas for request/response validation
- May need to add more validators for business logic (e.g., age consistency with DOB)
- Response serialization tested via Pydantic model_dump() (not required for this task)

---

## Task 5: SQLite Database Setup and Cache Model

### Completed
✓ Created backend/app/core/database.py with create_engine, get_session dependency, init_db() function
✓ Created backend/app/models/cache.py with LLMCache SQLModel table
✓ Updated backend/app/main.py to call init_db() in lifespan startup
✓ Database initialization creates reconciliation.db with llmcache table
✓ All QA scenarios pass: database file creation, table schema verification, constraint verification

### Patterns Established

1. **SQLModel + FastAPI Integration**:
   - SQLModel combines SQLAlchemy ORM with Pydantic validation
   - Models must be imported in database.py before init_db() to register with SQLModel.metadata
   - Engine creation uses connect_args={"check_same_thread": False} for FastAPI compatibility

2. **Database Session Management**:
   - SessionLocal factory created with autocommit=False, autoflush=False
   - get_session() dependency yields sessions and ensures proper cleanup via try/finally
   - Can be injected into route handlers via Depends(get_session)

3. **LLMCache Model Design**:
   - 6 fields: id (PK), prompt_hash (unique indexed), response_json, provider, created_at, ttl_seconds
   - prompt_hash uses sha_column=Column(String(64), nullable=False, index=True, unique=True)
   - Unique constraints must be applied via sa_column Column definition, not Field parameters
   - created_at defaults to datetime.utcnow (callable, not static value)

4. **SQLite Configuration**:
   - Database URL: "sqlite:///./reconciliation.db" (relative path in backend directory)
   - check_same_thread=False required for FastAPI async request handling
   - Indexes created automatically by SQLModel from sa_column config

5. **Field Constraint Syntax**:
   - Mixing Field() constraints with sa_column parameters raises RuntimeError
   - Solution: Put all SQLAlchemy-specific constraints in sa_column Column()
   - Use sa_column for: nullable, index, unique, String length, DateTime type

### Key Decisions

- **Sync Engine**: Used synchronous create_engine (not async) for SQLite simplicity
- **Field vs sa_column**: All index/unique constraints applied via Column, not Field parameters
- **TTL Field**: Included ttl_seconds with default 3600 (1 hour) for cache expiration logic
- **Import Order**: Models imported in database.py to ensure registration before init_db()
- **Lifespan Integration**: init_db() called early in lifespan (before API checks) to ensure DB ready

### Gotchas

1. **SQLModel Constraint Conflicts**: 
   - Using `unique=True` in Field() with `sa_column` raises RuntimeError
   - Solution: Apply constraints entirely in Column(), not Field()
   
2. **Model Registration**:
   - LLMCache table won't be created if model isn't imported before init_db()
   - Must import in database.py: `from app.models.cache import LLMCache`

3. **Default Factories**:
   - created_at defaults to `datetime.utcnow` (callable) not `datetime.utcnow()` (static)
   - Using () would create single static timestamp for all records

4. **SQLite Thread Safety**:
   - check_same_thread=False allows FastAPI's async event loop to use same connection safely
   - Required because FastAPI may handle requests across multiple threads

### Schema Verification Results

Database: reconciliation.db (created successfully)

**Tables**: ✓ llmcache

**Columns**:
- id: INTEGER (primary key)
- prompt_hash: VARCHAR(64) (unique, indexed)
- response_json: VARCHAR
- provider: VARCHAR(50)
- created_at: DATETIME
- ttl_seconds: INTEGER

**Indexes**:
- ix_llmcache_prompt_hash: unique=1, columns=['prompt_hash']

**Constraints**:
- Primary Key: id
- Unique: prompt_hash (via unique index)

### File Changes Summary

**Created**:
- backend/app/core/database.py (44 lines)
- backend/app/models/cache.py (38 lines)

**Modified**:
- backend/app/main.py (added init_db import + call in lifespan)

### Time Log
- database.py creation: 2 min
- cache.py creation + constraint fixes: 3 min
- main.py integration: 1 min
- Dependencies installation: 1 min
- QA testing + schema verification: 2 min
- Evidence documentation: 1 min
- Total: ~10 min

### Next Task Considerations
- Cache lookup endpoints can query by prompt_hash (indexed for performance)
- TTL validation logic needed in service layer (check created_at + ttl_seconds vs now())
- May need cache cleanup job to purge expired entries
- Response caching can be wrapped in service layer with try/except on cache miss

## Task 7: API Key Authentication Middleware

### Completed
✓ Created backend/app/core/security.py with verify_api_key dependency
✓ Created backend/tests/test_auth.py with 2 pytest tests (unauthenticated rejected, authenticated passes)
✓ Tests execute with pytest and both PASS
✓ Created QA evidence file (task-7-auth-evidence.txt)

### Patterns Established

1. **FastAPI Dependency Injection**:
   - Used `Annotated[str, Header()]` to extract X-API-Key from request headers
   - Function signature: `async def verify_api_key(x_api_key: Annotated[str, Header()] = "")`
   - Returns API key on success (allows dependency chaining)
   - Can be added to routes via `dependencies=[Depends(verify_api_key)]`

2. **Timing-Safe Comparison**:
   - Used `secrets.compare_digest(x_api_key, settings.api_key)` for timing-attack resistance
   - Prevents attackers from guessing API key character-by-character via timing
   - Compares both empty string and invalid keys consistently

3. **Development Mode Support**:
   - If `settings.api_key` is empty string, function logs warning and allows all requests
   - Enables development without requiring API_KEY in .env
   - Production must set non-empty API_KEY for authentication to activate

4. **Error Response Format**:
   - HTTPException with status_code=401
   - Detail is dict with structure: `{"code": "UNAUTHORIZED", "message": "Invalid or missing API key"}`
   - FastAPI automatically serializes to JSON response

5. **Pytest Async Testing**:
   - Used `@pytest.mark.asyncio` to enable async test functions
   - Used `unittest.mock.patch` to mock `get_settings()` function
   - Mock returns `Settings(api_key=test_key)` for test isolation
   - Tests don't require TestClient (direct function invocation)

6. **Import and Path Handling**:
   - Tests add backend path via `sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))`
   - Allows relative imports from app.* modules
   - Must activate venv before running pytest (system pytest doesn't have dependencies)

### Key Decisions

- **No Route Wiring**: Task 7 creates dependency but does NOT wire it to routes
  - Routes remain unauthenticated until explicitly added to dependencies
  - Allows gradual adoption: `/api/health` stays open, protected routes use `depends=...`
- **Header Parameter Name**: Used `x_api_key` (lowercase) as convention matches FastAPI style
- **Default Empty String**: `x_api_key=""` default allows optional header, then check happens in function
- **Mock over TestClient**: Direct async function testing cleaner than TestClient + route setup

### Gotchas

1. **Annotated Required for Headers**: FastAPI requires `Annotated[str, Header()]` syntax
   - Using `x_api_key: str = Header(...)` without Annotated causes import errors
   - Pattern: `from typing import Annotated` + `Annotated[type, Header()]`

2. **Async Function Syntax**: `verify_api_key` is async even though it doesn't await anything
   - FastAPI allows both sync and async dependencies
   - Using async allows future database lookups without changing signature

3. **Pydantic Config Deprecation Warning**: Settings class uses deprecated `Config` inner class
   - Warning: "Support for class-based `config` is deprecated, use ConfigDict instead"
   - Safe to ignore for now (still works in Pydantic v2)
   - Fix requires: `from pydantic import ConfigDict` + `model_config = ConfigDict(...)`

4. **pytest-asyncio Mode Strict**: Tests default to `Mode.STRICT`
   - Each test must mark async functions with `@pytest.mark.asyncio`
   - Can't mix sync and async tests without proper markers

5. **Venv Required for Tests**: System Python doesn't have fastapi/pytest installed
   - Always use `source venv/bin/activate` before running pytest
   - Or use `/venv/bin/pytest` directly

### Security Implementation Details

- **timing-safe**: secrets.compare_digest ensures O(n) time regardless of mismatch position
- **empty check**: Not needed (compare_digest handles empty string safely)
- **header extraction**: FastAPI normalizes header names (X-API-Key → x_api_key)
- **error message**: Generic "Invalid or missing API key" (doesn't leak if key exists)

### QA Scenarios Passing

1. ✓ Unauthenticated request (empty API key) → 401 UNAUTHORIZED with correct detail
2. ✓ Authenticated request (valid API key) → Returns API key, no exception

### Testing Notes

- Tests mock `get_settings()` to avoid loading .env file
- Each test gets fresh Settings instance with different api_key values
- Mock applied via `patch("app.core.security.get_settings")`
- No need for database, file system, or external services

### Files Created/Modified

- backend/app/core/security.py (NEW) - 47 lines
- backend/tests/test_auth.py (NEW) - 40 lines
- No modifications to existing files (backward compatible)

### Time Log

- security.py creation: 1 min
- test_auth.py (first attempt, then fixed): 2 min
- pytest debugging (venv activation): 1 min
- evidence documentation: 1 min
- notepad learning: 1 min
- Total: ~6 min

### Next Task Considerations

- Router files in backend/app/api/routes/ can add `dependencies=[Depends(verify_api_key)]` to enable auth
- /api/health endpoint explicitly excluded from auth (no dependencies)
- Could add more granular auth (e.g., different keys for different roles) via middleware
- API key rotation strategy (could add expiry/revocation table) for future enhancement

