# CeWiL Engineering Operating System

Governed workflow platform foundation for civil-engineering practice.

## Implemented modules
- Ten specialist domains and central routing registry.
- FastAPI service for health, agent catalogue, task routing, evidence, and workflows.
- Advisory keyword risk triage with professional-review guardrails.
- SQLite evidence ledger and RFI/ITP/NCR/submittal/inspection/action workflow register.
- Jurisdiction-aware standards/source metadata registry.
- Source-linked knowledge-entry registration and keyword lookup with citation metadata.
- Deterministic quantity utilities, tests, and GitHub Actions CI.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
uvicorn cewil_os.main:app --reload
```
SQLite defaults to `data/cewil.db`; set `CEWIL_DB_PATH` to change it. API docs: `/docs`.

## Standards and knowledge endpoints
- `POST /v1/standards/sources`
- `GET /v1/standards/sources` (filters: country, region, locality, query)
- `GET /v1/standards/sources/{id}`
- `POST /v1/knowledge/entries`
- `GET /v1/knowledge/search?q=...` (optional jurisdiction/project filters)

Search is keyword-based over explicitly registered summaries, not semantic RAG. Each knowledge result includes source metadata. Verify source edition, amendments, effective dates, local adoption, contract hierarchy, and licensing before operational use.

## Safety and security
This is not an engineering authority or certification system. Routing and risk triage are advisory. Structural design, structural audits, concrete test interpretation, statutory compliance, and safety-critical outputs require qualified professional review.

The API currently has no authentication/RBAC, verified reviewer identity, tenant isolation, or production-grade database operations. Do not expose it publicly or use it with confidential project data. No production deployment is included.
