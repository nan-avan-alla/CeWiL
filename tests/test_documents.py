import io
from fastapi.testclient import TestClient
from cewil_os.main import app

client = TestClient(app)

def test_document_text_upload_search_and_duplicate():
    data = {"project_id": "doc-test", "uploaded_by": "tester"}
    files = {"file": ("spec.txt", b"Concrete inspection hold point and test record.", "text/plain")}
    first = client.post("/v1/documents", data=data, files=files)
    assert first.status_code == 201
    doc_id = first.json()["id"]
    assert first.json()["extraction_status"] == "extracted"
    search = client.get("/v1/documents/search", params={"q": "inspection hold", "project_id": "doc-test"})
    assert search.status_code == 200
    assert search.json()["items"][0]["document_id"] == doc_id
    duplicate = client.post("/v1/documents", data=data, files=files)
    assert duplicate.status_code == 201
    assert duplicate.json()["duplicate"] is True

def test_document_revision_text_diff():
    data = {"project_id": "revision-test", "uploaded_by": "tester"}
    first = client.post("/v1/documents", data=data, files={"file": ("drawing-notes.txt", b"Beam size 230 by 450.", "text/plain")})
    second = client.post("/v1/documents", data=data, files={"file": ("drawing-notes.txt", b"Beam size 300 by 500.", "text/plain")})
    assert first.status_code == 201 and second.status_code == 201
    assert second.json()["version_number"] == 2
    diff = client.get(f"/v1/documents/{second.json()['id']}/diff")
    assert diff.status_code == 200
    assert any("300 by 500" in line for line in diff.json()["changes"])

def test_unsupported_document_type_rejected():
    response = client.post("/v1/documents", data={"project_id": "doc-test", "uploaded_by": "tester"},
                           files={"file": ("malware.exe", b"x", "application/octet-stream")})
    assert response.status_code == 422
