import pytest
from fastapi.testclient import TestClient
from cewil_os.main import app

client = TestClient(app)

def test_risk_triage_escalates_structural_design():
    result = client.post("/v1/route", json={"task": "Review structural design for a building"})
    assert result.status_code == 200
    assert result.json()["risk_assessment"]["level"] == "high"
    assert result.json()["risk_assessment"]["automated_clearance"] is False

def test_evidence_ledger_round_trip():
    created = client.post("/v1/evidence", json={
        "project_id": "test-project", "evidence_type": "drawing",
        "title": "Foundation drawing", "revision": "A",
        "description": "Drawing received for coordination", "recorded_by": "test-user",
        "metadata": {"discipline": "civil"}
    })
    assert created.status_code == 201
    evidence_id = created.json()["id"]
    fetched = client.get(f"/v1/evidence/{evidence_id}")
    assert fetched.status_code == 200
    assert fetched.json()["metadata"]["discipline"] == "civil"

def test_workflow_state_machine_and_history():
    created = client.post("/v1/workflows", json={
        "project_id": "test-project", "kind": "RFI",
        "title": "Clarify beam opening", "description": "Request design clarification",
        "created_by": "site-engineer", "owner": "design-team"
    })
    assert created.status_code == 201
    workflow_id = created.json()["id"]
    moved = client.post(f"/v1/workflows/{workflow_id}/transition", json={
        "status": "in_review", "actor": "coordinator", "note": "Sent for review"
    })
    assert moved.status_code == 200
    assert moved.json()["status"] == "in_review"
    assert len(moved.json()["history"]) == 2

def test_closed_workflow_cannot_reopen():
    created = client.post("/v1/workflows", json={
        "project_id": "test-project", "kind": "NCR",
        "title": "Concrete surface defect", "description": "Record defect and disposition",
        "created_by": "qa"
    }).json()
    closed = client.post(f"/v1/workflows/{created['id']}/transition", json={
        "status": "closed", "actor": "reviewer"
    })
    assert closed.status_code == 200
    reopened = client.post(f"/v1/workflows/{created['id']}/transition", json={
        "status": "open", "actor": "reviewer"
    })
    assert reopened.status_code == 422
