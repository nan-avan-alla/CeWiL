# CeWiL Engineering Operating System

Governed workflow platform foundation for civil-engineering practice.

## Implemented development modules
- Ten specialist domains and central routing registry.
- FastAPI task routing and advisory risk triage.
- SQLite evidence ledger and RFI/ITP/NCR/submittal/inspection/action workflows.
- Jurisdiction-aware standards/source metadata registry and source-linked knowledge entries.
- Document upload and extraction for PDF text layers, DOCX, TXT, Markdown, XLSX, and optional raster-image OCR.
- SHA-256 duplicate detection and filename-based version chain.
- Text-layer revision diff and SQLite FTS5 chunk search.
- Deterministic quantity utilities, tests, and GitHub Actions CI.

## Local setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
uvicorn cewil_os.main:app --reload
```
Optional image OCR: `pip install -e ".[ocr,dev]"` and install the system Tesseract binary. Database defaults to `data/cewil.db`; document storage defaults to `data/documents`. API docs: `/docs`.

## Document endpoints
- `POST /v1/documents` multipart: project_id, uploaded_by, file
- `GET /v1/documents?project_id=...`
- `GET /v1/documents/{id}`
- `GET /v1/documents/{id}/text`
- `GET /v1/documents/{id}/diff`
- `GET /v1/documents/search?q=...`

## Critical limitations
This is a development foundation, not an engineering authority or certification system. Document search is lexical FTS5, not semantic/vector RAG. Scanned PDF OCR, drawing geometry/visual revision comparison, CAD/DWG/DXF parsing, and automated dimension extraction are not implemented. The API has no authentication/RBAC, malware scanning, tenant isolation, or production-grade storage. Do not expose it publicly or use it with confidential project data. No production deployment is included.
