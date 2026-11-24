# Document intelligence foundation

## Supported uploads
PDF text layer, DOCX paragraphs/tables, TXT, Markdown, XLSX cell values, and common raster images. Uploads are limited to 20 MiB by default and are stored under `data/documents` using generated UUID filenames. SHA-256 is used for duplicate detection within a project. Repeated filenames create a new version record linked to the previous version.

## Extraction
- PDF: PyMuPDF text-layer extraction. Image-only/scanned PDFs are explicitly marked `no_text_detected`; OCR for scanned PDFs is not implemented.
- DOCX: paragraph and table text.
- XLSX: displayed cell values, not formula recalculation.
- Images: optional Tesseract OCR for raster images only; install the `ocr` extra and the system Tesseract binary. OCR text, dimensions, symbols, and engineering annotations require manual verification.
- CAD/DWG/DXF: not parsed in this increment.

## Revision comparison
The diff endpoint compares extracted text between same-project versions. It does not compare drawing geometry, dimensions, linework, layers, or visual changes. Never treat a clean text diff as proof that drawings are unchanged.

## Search
Extracted text is chunked with overlap and indexed in SQLite FTS5. This is keyword/full-text search, not embedding-based semantic RAG. Results include document ID, filename, version, and hash to preserve traceability.

## Security and operations
The API currently has no authentication, authorisation, malware scanning, tenant isolation, encryption-at-rest policy, retention workflow, or upload quarantine. Keep it local/private only. Before production, implement authentication/RBAC, project-level access checks, antivirus/content scanning, quotas, backups, storage lifecycle, audit events, and migration to managed object/database storage.
