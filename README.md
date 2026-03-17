# Clinical Data Reconciliation Engine

## Overview

A full-stack application for reconciling clinical EHR data using AI-powered analysis. The system integrates with GitHub Models and Anthropic APIs to provide intelligent data quality assessment and automated reconciliation workflows.

## Setup

### Prerequisites
- Python 3.12+
- Node.js v24+
- pnpm

### Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (once available)
pip install -r requirements.txt
```

### Frontend Setup
```bash
# Install dependencies (once available)
pnpm install

# Run development server (once available)
pnpm dev
```

### Environment Configuration
Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

## Architecture

### Backend Structure
- `backend/app/api/routes/` - API endpoint handlers
- `backend/app/core/` - Core configuration and utilities
- `backend/app/models/` - Data models (SQLAlchemy, Pydantic)
- `backend/app/schemas/` - Request/response schemas
- `backend/app/services/llm/` - LLM integration services
- `backend/tests/` - Unit and integration tests

### Frontend Structure
- `frontend/src/components/` - Reusable UI components
- `frontend/src/features/reconciliation/` - Reconciliation feature module
- `frontend/src/features/data-quality/` - Data quality feature module
- `frontend/src/hooks/` - Custom React hooks
- `frontend/src/lib/` - Utility functions and helpers
- `frontend/src/types/` - TypeScript type definitions
- `frontend/tests/` - Frontend tests

## Design Decisions

1. **Modular Structure**: Separated backend and frontend with clear domain boundaries
2. **Feature-Based Organization**: Frontend organized by feature (reconciliation, data-quality)
3. **Service Layer Pattern**: LLM services decoupled from API routes for testability
4. **Type Safety**: Full TypeScript frontend and Pydantic-validated backend schemas
5. **Environment Configuration**: Externalized config via `.env` for multi-environment support

## Trade-offs

1. **Monorepo vs Multi-Repo**: Chose monorepo for faster initial development and easier cross-service coordination
2. **API Design**: RESTful API chosen for simplicity; GraphQL could be considered for complex queries
3. **Frontend Framework**: React selected for ecosystem maturity; could explore alternatives if performance critical
4. **LLM Integration**: Multiple provider support (GitHub Models, Anthropic) for flexibility but adds complexity

## What I'd Improve

1. **Documentation**: Add OpenAPI/Swagger documentation for API endpoints
2. **Testing**: Implement comprehensive test coverage with fixtures and factories
3. **CI/CD**: Add GitHub Actions workflows for automated testing and deployment
4. **Logging**: Structured logging with correlation IDs for distributed tracing
5. **Error Handling**: Standardized error responses with specific error codes
6. **Performance**: Add caching layer and query optimization as needed
7. **Security**: Implement authentication/authorization framework
8. **Monitoring**: Add observability with metrics and error tracking

## Time Spent

- Project Structure Setup: [To be filled in during development]
- Backend Implementation: [To be filled in during development]
- Frontend Implementation: [To be filled in during development]
- Integration & Testing: [To be filled in during development]
- Deployment: [To be filled in during development]
