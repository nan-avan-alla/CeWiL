# CeWiL Engineering Operating System

A governed engineering workflow platform foundation for civil-engineering practice.

## Implemented foundation
- Ten specialist domains and a central routing registry.
- FastAPI API for health, agent catalogue, and task routing.
- Conservative keyword-based risk triage; advisory only, not an engineering risk model.
- SQLite evidence ledger for project-linked evidence metadata and source/revision references.
- Workflow register for RFI, ITP, NCR, submittal, inspection, and action records.
- Explicit workflow state transitions with an append-only status history.
- Deterministic quantity utilities, tests, and GitHub Actions CI.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
uvicorn cewil_os.main:app --reload
```

The local SQLite database defaults to `data/cewil.db`. Set `CEWIL_DB_PATH` to change its location.

## Main API
- `GET /health`
- `GET /v1/agents`
- `POST /v1/route`
- `POST /v1/evidence`, `GET /v1/evidence`, `GET /v1/evidence/{id}`
- `POST /v1/workflows`, `GET /v1/workflows`, `GET /v1/workflows/{id}`
- `POST /v1/workflows/{id}/transition`

Interactive API documentation is available at `/docs` when the service is running.

## Safety and deployment boundary
This is a development foundation, not an engineering authority or certification system. Routing and risk triage are advisory and must never be treated as approval or permission to construct. Structural design, structural audits, concrete test interpretation, statutory compliance, and safety-critical outputs require qualified professional review.

The API currently has no authentication or role-based access control. Do not expose it to the public internet or use it with confidential project data until identity, authorisation, tenant isolation, encryption, backups, retention, and security controls are implemented. SQLite is suitable for local development only; production storage and migration strategy remain future work.
