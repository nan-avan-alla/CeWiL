import difflib
import hashlib
import os
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

from docx import Document as DocxDocument
from openpyxl import load_workbook
import fitz

DB_PATH = os.getenv("CEWIL_DB_PATH", "data/cewil.db")
STORAGE_DIR = Path(os.getenv("CEWIL_DOCUMENT_DIR", "data/documents"))
MAX_BYTES = int(os.getenv("CEWIL_MAX_UPLOAD_BYTES", str(20 * 1024 * 1024)))
ALLOWED = {".pdf", ".docx", ".txt", ".md", ".xlsx", ".png", ".jpg", ".jpeg", ".tif", ".tiff"}

def _now():
    return datetime.now(timezone.utc).isoformat()

def _connect():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db

def _init():
    with _connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY, project_id TEXT NOT NULL, filename TEXT NOT NULL,
            stored_path TEXT NOT NULL, media_type TEXT NOT NULL, sha256 TEXT NOT NULL,
            version_number INTEGER NOT NULL, previous_document_id TEXT,
            extraction_status TEXT NOT NULL, extraction_note TEXT NOT NULL,
            text_content TEXT NOT NULL, uploaded_by TEXT NOT NULL, uploaded_at TEXT NOT NULL
        )""")
        db.execute("""CREATE TABLE IF NOT EXISTS document_chunks (
            id TEXT PRIMARY KEY, document_id TEXT NOT NULL, project_id TEXT NOT NULL,
            chunk_index INTEGER NOT NULL, text_content TEXT NOT NULL,
            FOREIGN KEY(document_id) REFERENCES documents(id)
        )""")
        db.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS document_chunks_fts
            USING fts5(chunk_id UNINDEXED, document_id UNINDEXED, project_id UNINDEXED, text_content,
                       tokenize='unicode61')""")

def _extract(path: Path):
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        with fitz.open(path) as pdf:
            text = "\n".join(page.get_text("text") for page in pdf)
        if not text.strip():
            return "", "no_text_detected", "PDF appears image-only or has no extractable text; OCR is not enabled for PDFs."
        return text, "extracted", "Text extracted from PDF text layer."
    if suffix == ".docx":
        doc = DocxDocument(path)
        parts = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                parts.append(" | ".join(cell.text for cell in row.cells))
        return "\n".join(parts), "extracted", "Text extracted from DOCX paragraphs and tables."
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8", errors="replace"), "extracted", "Text file decoded as UTF-8."
    if suffix == ".xlsx":
        workbook = load_workbook(path, read_only=True, data_only=True)
        rows = []
        for sheet in workbook.worksheets:
            rows.append(f"[Sheet: {sheet.title}]")
            for row in sheet.iter_rows(values_only=True):
                values = [str(value) for value in row if value is not None]
                if values:
                    rows.append(" | ".join(values))
        workbook.close()
        return "\n".join(rows), "extracted", "Workbook cell values extracted; formulas are not recalculated."
    if suffix in {".png", ".jpg", ".jpeg", ".tif", ".tiff"}:
        try:
            from PIL import Image
            import pytesseract
            text = pytesseract.image_to_string(Image.open(path))
            if text.strip():
                return text, "extracted", "Image OCR completed using optional Tesseract; verify dimensions and technical symbols manually."
            return "", "no_text_detected", "OCR returned no text."
        except ImportError:
            return "", "ocr_unavailable", "Install the optional OCR dependencies and Tesseract binary to process image text."
        except Exception as exc:
            return "", "ocr_error", f"OCR failed: {type(exc).__name__}"
    return "", "unsupported", "Unsupported file type."

def _chunks(text, size=1200, overlap=150):
    clean = re.sub(r"\s+", " ", text).strip()
    if not clean:
        return []
    result, start = [], 0
    while start < len(clean):
        end = min(len(clean), start + size)
        if end < len(clean):
            boundary = clean.rfind(" ", start, end)
            if boundary > start + size // 2:
                end = boundary
        result.append(clean[start:end])
        if end >= len(clean):
            break
        start = max(end - overlap, start + 1)
    return result

def _save_chunks(db, document_id, project_id, text):
    for index, chunk in enumerate(_chunks(text)):
        chunk_id = str(uuid.uuid4())
        db.execute("INSERT INTO document_chunks VALUES (?, ?, ?, ?, ?)",
                   (chunk_id, document_id, project_id, index, chunk))
        db.execute("INSERT INTO document_chunks_fts VALUES (?, ?, ?, ?)",
                   (chunk_id, document_id, project_id, chunk))

def ingest(project_id: str, filename: str, uploaded_by: str, content: bytes):
    if len(content) > MAX_BYTES:
        raise ValueError(f"File exceeds upload limit of {MAX_BYTES} bytes")
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED:
        raise ValueError(f"Unsupported file extension: {suffix}")
    digest = hashlib.sha256(content).hexdigest()
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    with _connect() as db:
        existing = db.execute("SELECT * FROM documents WHERE project_id=? AND sha256=?",
                              (project_id, digest)).fetchone()
        if existing:
            return {**dict(existing), "duplicate": True, "message": "Identical file already ingested for this project."}
        previous = db.execute("SELECT * FROM documents WHERE project_id=? AND filename=? ORDER BY version_number DESC LIMIT 1",
                               (project_id, Path(filename).name)).fetchone()
        version = (previous["version_number"] + 1) if previous else 1
        document_id = str(uuid.uuid4())
        stored = STORAGE_DIR / f"{document_id}{suffix}"
        stored.write_bytes(content)
        try:
            extracted, status, note = _extract(stored)
        except Exception as exc:
            stored.unlink(missing_ok=True)
            raise ValueError(f"Document extraction failed: {type(exc).__name__}") from exc
        record = {
            "id": document_id, "project_id": project_id, "filename": Path(filename).name,
            "stored_path": str(stored), "media_type": suffix[1:], "sha256": digest,
            "version_number": version, "previous_document_id": previous["id"] if previous else None,
            "extraction_status": status, "extraction_note": note, "text_content": extracted,
            "uploaded_by": uploaded_by, "uploaded_at": _now()
        }
        db.execute("INSERT INTO documents VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple(record.values()))
        _save_chunks(db, document_id, project_id, extracted)
        return {**record, "duplicate": False, "character_count": len(extracted)}

def list_documents(project_id):
    with _connect() as db:
        rows = db.execute("""SELECT id, project_id, filename, media_type, sha256, version_number,
            previous_document_id, extraction_status, extraction_note, uploaded_by, uploaded_at
            FROM documents WHERE project_id=? ORDER BY filename, version_number DESC""", (project_id,)).fetchall()
    return [dict(row) for row in rows]

def get_document(document_id):
    with _connect() as db:
        row = db.execute("""SELECT id, project_id, filename, media_type, sha256, version_number,
            previous_document_id, extraction_status, extraction_note, uploaded_by, uploaded_at,
            text_content FROM documents WHERE id=?""", (document_id,)).fetchone()
    return dict(row) if row else None

def compare_versions(document_id, previous_id=None):
    current = get_document(document_id)
    if not current:
        raise KeyError(document_id)
    old_id = previous_id or current["previous_document_id"]
    if not old_id:
        return {"document_id": document_id, "previous_document_id": None, "changes": [], "message": "No earlier version is linked."}
    previous = get_document(old_id)
    if not previous or previous["project_id"] != current["project_id"]:
        raise ValueError("Previous version not found in the same project")
    diff = list(difflib.unified_diff(previous["text_content"].splitlines(), current["text_content"].splitlines(),
                                     fromfile=previous["filename"] + f" v{previous['version_number']}",
                                     tofile=current["filename"] + f" v{current['version_number']}", lineterm=""))
    return {"document_id": document_id, "previous_document_id": old_id, "changes": diff[:2000],
            "note": "Text-layer comparison only. It does not detect drawing geometry, dimensions, symbols, or visual changes."}

def search_chunks(query, project_id=None, limit=20):
    terms = [token for token in re.findall(r"[\w-]+", query) if len(token) > 1]
    if not terms:
        return []
    match = " AND ".join('"' + term.replace('"', '""') + '"' for term in terms)
    sql = """SELECT f.document_id, f.chunk_id, f.text_content, d.filename, d.version_number,
             d.extraction_status, d.sha256
             FROM document_chunks_fts f JOIN documents d ON d.id=f.document_id
             WHERE document_chunks_fts MATCH ?"""
    params = [match]
    if project_id:
        sql += " AND f.project_id=?"
        params.append(project_id)
    sql += " ORDER BY rank LIMIT ?"
    params.append(max(1, min(limit, 100)))
    try:
        with _connect() as db:
            rows = db.execute(sql, params).fetchall()
    except sqlite3.OperationalError:
        return []
    return [dict(row) for row in rows]

_init()
