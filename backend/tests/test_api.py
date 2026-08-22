from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "knee-ai-analysis"
    assert "version" in data

def test_system_info():
    response = client.get("/api/v1/system/info")
    assert response.status_code == 200
    data = response.json()
    assert "os" in data
    assert "python_version" in data
    assert data["database_status"] == "connected"
    assert "environment" in data
