import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pydantic import BaseModel, Field, HttpUrl

DB_PATH = os.getenv("CEWIL_DB_PATH", "data/cewil.db")

def _now():
    return datetime.now(timezone.utc).isoformat()

def _connect():
    directory = os.path.dirname(DB_PATH)
    if directory:
        os.makedirs(directory, exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db

def _init():
    with _connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS sources (
            id TEXT PRIMARY KEY, title TEXT NOT NULL, publisher TEXT NOT NULL,
            source_type TEXT NOT NULL, country TEXT, region TEXT, locality TEXT,
            code_family TEXT, edition TEXT, amendment TEXT, effective_date TEXT,
            publication_date TEXT, url TEXT NOT NULL, access_status TEXT NOT NULL,
            verification_status TEXT NOT NULL, notes TEXT NOT NULL,
            created_at TEXT NOT NULL, updated_at TEXT NOT NULL
        )""")
        db.execute("""CREATE TABLE IF NOT EXISTS knowledge_entries (
            id TEXT PRIMARY KEY, title TEXT NOT NULL, summary TEXT NOT NULL,
            jurisdiction_json TEXT NOT NULL, project_type TEXT, material_system TEXT,
            code_edition TEXT, clause_ref TEXT, page_ref TEXT, source_id TEXT NOT NULL,
            source_status TEXT NOT NULL, reviewed_by TEXT, reviewed_at TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(source_id) REFERENCES sources(id)
        )""")

class SourceCreate(BaseModel):
    title: str = Field(min_length=3, max_length=300)
    publisher: str = Field(min_length=2, max_length=200)
    source_type: str = Field(pattern="^(statute|code|standard|government_schedule|authority_rule|contract_document|professional_guidance|research|other)$")
    url: HttpUrl
    country: str | None = None
    region: str | None = None
    locality: str | None = None
    code_family: str | None = None
    edition: str | None = None
    amendment: str | None = None
    effective_date: str | None = None
    publication_date: str | None = None
    access_status: str = "link_only"
    verification_status: str = "unverified"
    notes: str = ""

class KnowledgeEntryCreate(BaseModel):
    title: str = Field(min_length=3, max_length=300)
    summary: str = Field(min_length=10, max_length=5000)
    country: str | None = None
    region: str | None = None
    locality: str | None = None
    project_type: str | None = None
    material_system: str | None = None
    code_edition: str | None = None
    clause_ref: str | None = None
    page_ref: str | None = None
    source_id: str
    source_status: str = "unverified"
    reviewed_by: str | None = None
    reviewed_at: str | None = None

def _source(row):
    return dict(row)

def _entry(row):
    item = dict(row)
    item["jurisdiction"] = json.loads(item.pop("jurisdiction_json"))
    item["citation"] = {
        "source_id": item["source_id"], "source_title": item.pop("source_title"),
        "publisher": item.pop("publisher"), "url": item.pop("url"),
        "edition": item["code_edition"] or item.pop("source_edition"),
        "clause": item["clause_ref"], "page": item["page_ref"],
        "verification_status": item.pop("verification_status")
    }
    return item

def create_source(item: SourceCreate):
    now = _now()
    record = {"id": str(uuid.uuid4()), **item.model_dump(mode="json"), "created_at": now, "updated_at": now}
    record["url"] = str(record["url"])
    columns = ("id", "title", "publisher", "source_type", "country", "region", "locality", "code_family", "edition", "amendment", "effective_date", "publication_date", "url", "access_status", "verification_status", "notes", "created_at", "updated_at")
    placeholders = ", ".join("?" for _ in columns)
    with _connect() as db:
        db.execute(
            f"INSERT INTO sources ({', '.join(columns)}) VALUES ({placeholders})",
            tuple(record[column] for column in columns),
        )
    return record

def list_sources(country=None, region=None, locality=None, query=None):
    sql, params = "SELECT * FROM sources WHERE 1=1", []
    for field, value in (("country", country), ("region", region), ("locality", locality)):
        if value:
            sql += f" AND lower(coalesce({field},''))=lower(?)"
            params.append(value)
    if query:
        sql += " AND (lower(title) LIKE ? OR lower(publisher) LIKE ? OR lower(coalesce(code_family,'')) LIKE ?)"
        term = f"%{query.lower()}%"
        params.extend([term, term, term])
    sql += " ORDER BY publisher, title"
    with _connect() as db:
        rows = db.execute(sql, params).fetchall()
    return [_source(row) for row in rows]

def get_source(source_id):
    with _connect() as db:
        row = db.execute("SELECT * FROM sources WHERE id=?", (source_id,)).fetchone()
    return _source(row) if row else None

def create_entry(item: KnowledgeEntryCreate):
    if not get_source(item.source_id):
        raise KeyError("source_id")
    now = _now()
    record = {"id": str(uuid.uuid4()), "title": item.title, "summary": item.summary,
              "jurisdiction_json": json.dumps({"country": item.country, "region": item.region, "locality": item.locality}),
              "project_type": item.project_type, "material_system": item.material_system,
              "code_edition": item.code_edition, "clause_ref": item.clause_ref, "page_ref": item.page_ref,
              "source_id": item.source_id, "source_status": item.source_status,
              "reviewed_by": item.reviewed_by, "reviewed_at": item.reviewed_at, "created_at": now}
    with _connect() as db:
        db.execute("INSERT INTO knowledge_entries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple(record.values()))
    return record

def search_knowledge(query, country=None, region=None, locality=None, project_type=None):
    terms = [part.strip().lower() for part in query.split() if part.strip()]
    if not terms:
        return []
    sql = """SELECT k.*, s.title AS source_title, s.publisher, s.url,
             s.edition AS source_edition, s.verification_status
             FROM knowledge_entries k JOIN sources s ON s.id=k.source_id WHERE 1=1"""
    params = []
    for term in terms:
        sql += " AND (lower(k.title) LIKE ? OR lower(k.summary) LIKE ? OR lower(coalesce(k.clause_ref,'')) LIKE ?)"
        like = f"%{term}%"
        params.extend([like, like, like])
    jurisdiction = {"country": country, "region": region, "locality": locality}
    for key, value in jurisdiction.items():
        if value:
            sql += f" AND lower(coalesce(json_extract(k.jurisdiction_json, '$.{key}'),''))=lower(?)"
            params.append(value)
    if project_type:
        sql += " AND lower(coalesce(k.project_type,''))=lower(?)"
        params.append(project_type)
    sql += " ORDER BY CASE WHEN k.source_status='reviewed' THEN 0 ELSE 1 END, k.created_at DESC LIMIT 50"
    with _connect() as db:
        rows = db.execute(sql, params).fetchall()
    return [_entry(row) for row in rows]

_init()
