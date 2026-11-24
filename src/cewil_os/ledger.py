import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pydantic import BaseModel, Field

DB_PATH = os.getenv("CEWIL_DB_PATH", "data/cewil.db")
WORKFLOW_STATUSES = {"open", "in_review", "blocked", "closed"}
TRANSITIONS = {
    "open": {"in_review", "blocked", "closed"},
    "in_review": {"open", "blocked", "closed"},
    "blocked": {"open", "in_review"},
    "closed": set(),
}

def _now():
    return datetime.now(timezone.utc).isoformat()

def _connect():
    directory = os.path.dirname(DB_PATH)
    if directory:
        os.makedirs(directory, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def _init():
    with _connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS evidence (
            id TEXT PRIMARY KEY, project_id TEXT NOT NULL, evidence_type TEXT NOT NULL,
            title TEXT NOT NULL, source_ref TEXT, revision TEXT, description TEXT NOT NULL,
            recorded_by TEXT NOT NULL, recorded_at TEXT NOT NULL, metadata_json TEXT NOT NULL
        )""")
        db.execute("""CREATE TABLE IF NOT EXISTS workflows (
            id TEXT PRIMARY KEY, project_id TEXT NOT NULL, kind TEXT NOT NULL,
            title TEXT NOT NULL, description TEXT NOT NULL, status TEXT NOT NULL,
            owner TEXT, due_date TEXT, created_by TEXT NOT NULL, created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL, history_json TEXT NOT NULL
        )""")

class EvidenceCreate(BaseModel):
    project_id: str = Field(min_length=1, max_length=120)
    evidence_type: str = Field(min_length=2, max_length=60)
    title: str = Field(min_length=2, max_length=240)
    source_ref: str | None = None
    revision: str | None = None
    description: str = Field(min_length=2, max_length=4000)
    recorded_by: str = Field(min_length=2, max_length=120)
    metadata: dict = Field(default_factory=dict)

class WorkflowCreate(BaseModel):
    project_id: str = Field(min_length=1, max_length=120)
    kind: str = Field(pattern="^(RFI|ITP|NCR|SUBMITTAL|INSPECTION|ACTION)$")
    title: str = Field(min_length=3, max_length=240)
    description: str = Field(min_length=3, max_length=4000)
    created_by: str = Field(min_length=2, max_length=120)
    owner: str | None = None
    due_date: str | None = None

def add_evidence(item: EvidenceCreate):
    record = {"id": str(uuid.uuid4()), **item.model_dump(), "recorded_at": _now()}
    metadata = record.pop("metadata")
    record["metadata"] = metadata
    with _connect() as db:
        db.execute("INSERT INTO evidence VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
            record["id"], record["project_id"], record["evidence_type"], record["title"],
            record["source_ref"], record["revision"], record["description"], record["recorded_by"],
            record["recorded_at"], json.dumps(metadata, sort_keys=True)))
    return record

def _evidence(row):
    item = dict(row)
    item["metadata"] = json.loads(item.pop("metadata_json"))
    return item

def list_evidence(project_id=None):
    with _connect() as db:
        if project_id:
            rows = db.execute("SELECT * FROM evidence WHERE project_id=? ORDER BY recorded_at DESC", (project_id,)).fetchall()
        else:
            rows = db.execute("SELECT * FROM evidence ORDER BY recorded_at DESC").fetchall()
    return [_evidence(row) for row in rows]

def get_evidence(evidence_id):
    with _connect() as db:
        row = db.execute("SELECT * FROM evidence WHERE id=?", (evidence_id,)).fetchone()
    return _evidence(row) if row else None

def add_workflow(item: WorkflowCreate):
    now = _now()
    record = {"id": str(uuid.uuid4()), **item.model_dump(), "status": "open",
              "created_at": now, "updated_at": now,
              "history": [{"status": "open", "actor": item.created_by, "at": now, "note": "Created"}]}
    with _connect() as db:
        db.execute("INSERT INTO workflows VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
            record["id"], record["project_id"], record["kind"], record["title"], record["description"],
            record["status"], record["owner"], record["due_date"], record["created_by"],
            record["created_at"], record["updated_at"], json.dumps(record["history"])))
    return record

def _workflow(row):
    item = dict(row)
    item["history"] = json.loads(item.pop("history_json"))
    return item

def list_workflows(project_id=None, status=None):
    query, params = "SELECT * FROM workflows WHERE 1=1", []
    if project_id:
        query += " AND project_id=?"; params.append(project_id)
    if status:
        if status not in WORKFLOW_STATUSES:
            raise ValueError("Invalid workflow status")
        query += " AND status=?"; params.append(status)
    query += " ORDER BY updated_at DESC"
    with _connect() as db:
        rows = db.execute(query, params).fetchall()
    return [_workflow(row) for row in rows]

def get_workflow(workflow_id):
    with _connect() as db:
        row = db.execute("SELECT * FROM workflows WHERE id=?", (workflow_id,)).fetchone()
    return _workflow(row) if row else None

def transition_workflow(workflow_id, transition):
    target = transition.get("status")
    actor = transition.get("actor")
    note = transition.get("note", "")
    if target not in WORKFLOW_STATUSES:
        raise ValueError("Invalid workflow status")
    if not isinstance(actor, str) or len(actor.strip()) < 2:
        raise ValueError("actor is required")
    with _connect() as db:
        row = db.execute("SELECT * FROM workflows WHERE id=?", (workflow_id,)).fetchone()
        if not row:
            raise KeyError(workflow_id)
        current = row["status"]
        if target not in TRANSITIONS[current]:
            raise ValueError(f"Transition from {current} to {target} is not allowed")
        history = json.loads(row["history_json"])
        history.append({"status": target, "actor": actor, "at": _now(), "note": str(note)[:1000]})
        updated = _now()
        db.execute("UPDATE workflows SET status=?, updated_at=?, history_json=? WHERE id=?",
                   (target, updated, json.dumps(history), workflow_id))
        result = db.execute("SELECT * FROM workflows WHERE id=?", (workflow_id,)).fetchone()
    return _workflow(result)

_init()
