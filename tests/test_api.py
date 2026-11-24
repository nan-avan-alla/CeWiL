from fastapi.testclient import TestClient
from cewil_os.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_agent_catalogue_has_ten_domains():
    response = client.get("/v1/agents")
    assert response.status_code == 200
    assert len(response.json()["agents"]) == 10

def test_route_requires_human_review():
    response = client.post("/v1/route", json={"task": "Prepare a building inspection checklist"})
    assert response.status_code == 200
    assert response.json()["requires_human_review"] is True
