import pytest
import io
import json
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def create_test_image(format="PNG", size=(100, 100)):
    file = io.BytesIO()
    image = Image.new("RGB", size, color="blue")
    image.save(file, format=format)
    file.seek(0)
    return file.read()

def test_oa_analysis_pipeline():
    # 1. Upload and segment
    img_data = create_test_image("PNG", size=(100, 100))
    upload_resp = client.post("/api/v1/images/upload", files={"file": ("test.png", img_data, "image/png")})
    image_id = upload_resp.json()["image_id"]
    
    client.post(f"/api/v1/images/preprocess/{image_id}")
    import os, json
    from app.core.config import settings
    meta_path = os.path.join(settings.UPLOAD_DIR, f"{image_id}_meta.json")
    with open(meta_path, "r") as f:
        meta = json.load(f)
    meta["modality"] = "MRI"
    with open(meta_path, "w") as f:
        json.dump(meta, f)
    client.post(f"/api/v1/segmentation/{image_id}")
    
    # We must call measurement internally, or just verify the OA analysis calls it
    patient_data = {
        "age": 45,
        "sex": "Male",
        "oa_status": "Unknown"
    }
    
    oa_resp = client.post(f"/api/v1/oa-analysis/{image_id}", json=patient_data)
    assert oa_resp.status_code == 200
    
    data = oa_resp.json()
    assert data["image_id"] == image_id
    assert data["patient"]["age"] == 45
    assert data["patient"]["sex"] == "Male"
    assert data["data_status"] == "demo"
    assert "oa_vs_non_oa" in data
    assert data["oa_vs_non_oa"]["oa_stats"]["sample_count"] > 0
    assert "warning" in data
    assert "DEMONSTRATION DATA" in data["warning"]

def test_oa_analysis_missing_measurement():
    img_data = create_test_image("PNG")
    upload_resp = client.post("/api/v1/images/upload", files={"file": ("test.png", img_data, "image/png")})
    image_id = upload_resp.json()["image_id"]
    # Missing segmentation and measurement entirely
    
    patient_data = {"age": 50, "sex": "Female", "oa_status": "Unknown"}
    oa_resp = client.post(f"/api/v1/oa-analysis/{image_id}", json=patient_data)
    
    assert oa_resp.status_code == 400
    assert "Measurement required before OA analysis" in oa_resp.json()["detail"]

def test_oa_analysis_invalid_age():
    patient_data = {"age": -5, "sex": "Female", "oa_status": "Unknown"}
    oa_resp = client.post("/api/v1/oa-analysis/fake_id", json=patient_data)
    assert oa_resp.status_code == 422 # Pydantic validation error
