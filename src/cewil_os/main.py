from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from .registry import AGENTS, BY_ID
from .governance import assess_risk
from .ledger import EvidenceCreate, WorkflowCreate, add_evidence, add_workflow, get_evidence, get_workflow, list_evidence, list_workflows, transition_workflow
from .standards import SourceCreate, KnowledgeEntryCreate, create_source, list_sources, get_source, create_entry, search_knowledge

app = FastAPI(title="CeWiL Engineering Operating System", version="0.3.0")

class RouteRequest(BaseModel):
    task: str = Field(min_length=3, max_length=4000)
    agent_id: str | None = None
    jurisdiction: str | None = None
    project_id: str | None = None

@app.get("/health")
def health():
    return {"status": "ok", "service": "cewil-engineering-os", "version": "0.3.0"}

@app.get("/v1/agents")
def list_agents():
    return {"agents": [agent.__dict__ for agent in AGENTS]}

@app.post("/v1/route")
def route_task(request: RouteRequest):
    if request.agent_id:
        agent = BY_ID.get(request.agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Unknown agent_id")
        selected = agent
    else:
        selected = BY_ID["practice-workflow"]
    risk = assess_risk(request.task)
    return {
        "selected_agent": selected.id, "agent_name": selected.name,
        "task": request.task, "project_id": request.project_id,
        "jurisdiction": request.jurisdiction,
        "risk_assessment": risk.model_dump(), "requires_human_review": True,
        "status": "draft_for_review",
        "notice": "Routing and risk triage are advisory. They do not establish engineering adequacy, code compliance, or permission to construct."
    }

@app.post("/v1/evidence", status_code=201)
def create_evidence_record(item: EvidenceCreate):
    return add_evidence(item)

@app.get("/v1/evidence")
def read_evidence(project_id: str | None = None):
    return {"items": list_evidence(project_id)}

@app.get("/v1/evidence/{evidence_id}")
def read_one_evidence(evidence_id: str):
    item = get_evidence(evidence_id)
    if not item:
        raise HTTPException(status_code=404, detail="Evidence record not found")
    return item

@app.post("/v1/workflows", status_code=201)
def create_workflow_record(item: WorkflowCreate):
    return add_workflow(item)

@app.get("/v1/workflows")
def read_workflows(project_id: str | None = None, status: str | None = None):
    return {"items": list_workflows(project_id, status)}

@app.get("/v1/workflows/{workflow_id}")
def read_one_workflow(workflow_id: str):
    item = get_workflow(workflow_id)
    if not item:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return item

@app.post("/v1/workflows/{workflow_id}/transition")
def update_workflow(workflow_id: str, transition: dict):
    try:
        return transition_workflow(workflow_id, transition)
    except KeyError:
        raise HTTPException(status_code=404, detail="Workflow not found")
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

@app.post("/v1/standards/sources", status_code=201)
def register_source(item: SourceCreate):
    return create_source(item)

@app.get("/v1/standards/sources")
def get_sources(country: str | None = None, region: str | None = None,
                locality: str | None = None, query: str | None = None):
    return {"items": list_sources(country, region, locality, query)}

@app.get("/v1/standards/sources/{source_id}")
def get_one_source(source_id: str):
    item = get_source(source_id)
    if not item:
        raise HTTPException(status_code=404, detail="Source not found")
    return item

@app.post("/v1/knowledge/entries", status_code=201)
def add_knowledge_entry(item: KnowledgeEntryCreate):
    try:
        return create_entry(item)
    except KeyError:
        raise HTTPException(status_code=422, detail="source_id must reference a registered source")

@app.get("/v1/knowledge/search")
def knowledge_search(q: str = Query(min_length=2), country: str | None = None,
                     region: str | None = None, locality: str | None = None,
                     project_type: str | None = None):
    return {"query": q, "items": search_knowledge(q, country, region, locality, project_type),
            "notice": "Keyword lookup over explicitly registered summaries, not semantic RAG. Every result includes source metadata; unreviewed entries must not support engineering conclusions."}
