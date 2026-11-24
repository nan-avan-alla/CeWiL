import pytest
from fastapi.testclient import TestClient
from cewil_os.main import app

client = TestClient(app)

def test_source_registry_and_cited_knowledge_entry():
    source = client.post("/v1/standards/sources", json={
        "title": "Test local building rule", "publisher": "Test Authority",
        "source_type": "authority_rule", "url": "https://example.org/building-rule",
        "country": "India", "region": "Karnataka", "locality": "Test City",
        "verification_status": "unverified", "notes": "Test fixture only"
    })
    assert source.status_code == 201
    source_id = source.json()["id"]
    entry = client.post("/v1/knowledge/entries", json={
        "title": "Test building setback note", "summary": "Example summary for verifying source-linked retrieval.",
        "country": "India", "region": "Karnataka", "locality": "Test City",
        "source_id": source_id, "source_status": "unverified"
    })
    assert entry.status_code == 201
    results = client.get("/v1/knowledge/search", params={"q": "setback", "country": "India"})
    assert results.status_code == 200
    assert results.json()["items"][0]["citation"]["source_id"] == source_id
    assert results.json()["items"][0]["citation"]["verification_status"] == "unverified"

def test_knowledge_entry_rejects_unknown_source():
    response = client.post("/v1/knowledge/entries", json={
        "title": "Orphan knowledge entry", "summary": "This entry has no registered source.",
        "source_id": "missing-source"
    })
    assert response.status_code == 422
