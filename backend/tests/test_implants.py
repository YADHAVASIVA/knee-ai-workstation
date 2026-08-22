import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.session import SessionLocal

client = TestClient(app)

def test_implant_database_seeded():
    # Database initialization and seeding is done on startup
    with TestClient(app) as local_client:
        # Get all implants
        resp = local_client.get("/api/v1/implants")
        assert resp.status_code == 200
        implants = resp.json()
        assert len(implants) >= 10  # 5 femoral, 5 tibial

        # All records should be demo
        for imp in implants:
            assert imp["is_demo"] is True
            assert imp["source_type"] == "synthetic_demo"

def test_implant_filters():
    with TestClient(app) as local_client:
        # Get femoral
        resp_fem = local_client.get("/api/v1/implants/femoral")
        fem_implants = resp_fem.json()
        assert len(fem_implants) >= 5
        assert all(imp["component_type"] == "femoral" for imp in fem_implants)

        # Get tibial
        resp_tib = local_client.get("/api/v1/implants/tibial")
        tib_implants = resp_tib.json()
        assert len(tib_implants) >= 5
        assert all(imp["component_type"] == "tibial" for imp in tib_implants)

        # Filter by size
        resp_size = local_client.get("/api/v1/implants?component_type=femoral&size=3")
        size_implants = resp_size.json()
        assert len(size_implants) == 1
        assert size_implants[0]["size"] == "3"
        assert size_implants[0]["component_type"] == "femoral"

def test_implant_by_id():
    with TestClient(app) as local_client:
        implants = local_client.get("/api/v1/implants").json()
        first_id = implants[0]["id"]
        
        resp = local_client.get(f"/api/v1/implants/{first_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == first_id

        # Missing ID
        resp_miss = local_client.get("/api/v1/implants/not-a-real-id")
        assert resp_miss.status_code == 404

def test_invalid_component_type():
    with TestClient(app) as local_client:
        resp = local_client.get("/api/v1/implants?component_type=invalid_type")
        assert resp.status_code == 400

def test_system_info_database_status():
    with TestClient(app) as local_client:
        resp = local_client.get("/api/v1/system/info")
        data = resp.json()
        assert data["database_status"] == "connected"
        assert data["implant_database"] == "demo"
