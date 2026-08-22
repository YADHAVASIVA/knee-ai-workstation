import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from PIL import Image
import io

client = TestClient(app)

def create_test_image(format="PNG", size=(100, 100)):
    file = io.BytesIO()
    image = Image.new("RGB", size, color="blue")
    image.save(file, format=format)
    file.seek(0)
    return file.read()

def test_segmentation_pipeline():
    # 1. Upload
    img_data = create_test_image("PNG")
    upload_resp = client.post(
        "/api/v1/images/upload",
        files={"file": ("test.png", img_data, "image/png")}
    )
    image_id = upload_resp.json()["image_id"]
    
    # 2. Preprocess
    process_resp = client.post(f"/api/v1/images/preprocess/{image_id}")
    assert process_resp.status_code == 200
    
    # 3. Run Segmentation
    seg_resp = client.post(f"/api/v1/segmentation/{image_id}")
    assert seg_resp.status_code == 200
    data = seg_resp.json()
    
    assert data["image_id"] == image_id
    assert data["model_status"] == "demo"
    assert "femur" in data["structures"]
    assert "tibia" in data["structures"]
    assert "medial_meniscus" in data["structures"]
    
    # Check that mask storage occurred
    assert os.path.exists(os.path.join(settings.MASKS_DIR, image_id, "femur.png"))
    assert os.path.exists(os.path.join(settings.MASKS_DIR, image_id, "tibia.png"))
    assert os.path.exists(os.path.join(settings.MASKS_DIR, image_id, "medial_meniscus.png"))
    assert os.path.exists(os.path.join(settings.MASKS_DIR, image_id, "result.json"))

    # 4. Fetch masks
    mask_resp = client.get(f"/api/v1/segmentation/{image_id}/mask/femur")
    assert mask_resp.status_code == 200
    assert mask_resp.headers["content-type"] == "image/png"

def test_segmentation_missing_image():
    response = client.post("/api/v1/segmentation/fake-id")
    assert response.status_code == 404
