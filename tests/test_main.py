from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_create_and_list_task():
    r = client.post("/tasks", json={"title": "Apprendre Kubernetes"})
    assert r.status_code == 201
    assert any(t["title"] == "Apprendre Kubernetes" for t in client.get("/tasks").json())
