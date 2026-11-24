from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .registry import AGENTS, BY_ID

app = FastAPI(title="CeWiL Engineering Operating System", version="0.1.0")

class RouteRequest(BaseModel):
    task: str = Field(min_length=3, max_length=4000)
    agent_id: str | None = None

@app.get("/health")
def health():
    return {"status": "ok", "service": "cewil-engineering-os"}

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
    return {
        "selected_agent": selected.id,
        "agent_name": selected.name,
        "task": request.task,
        "requires_human_review": True,
        "notice": "Routing suggestion only. A qualified professional must review safety-critical engineering outputs."
    }
