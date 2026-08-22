import pytest
import io
import os
import numpy as np
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

def create_test_image(format="PNG", size=(100, 100)):
    file = io.BytesIO()
    image = Image.new("RGB", size, color="blue")
    image.save(file, format=format)
    file.seek(0)
    return file.read()

def create_synthetic_mask(image_id: str, structure_name: str, start_r, start_c, height, width):
    mask_dir = os.path.join(settings.DATA_DIR, "masks", image_id)
    os.makedirs(mask_dir, exist_ok=True)
    mask = np.zeros((100, 100, 4), dtype=np.uint8)
    # Set RGBA to red with alpha
    mask[start_r:start_r+height, start_c:start_c+width] = [255, 0, 0, 128]
    img = Image.fromarray(mask, mode="RGBA")
    img.save(os.path.join(mask_dir, f"{structure_name}.png"))

def test_bone_measurements_synthetic():
    # 1. Upload
    img_data = create_test_image("PNG")
    upload_resp = client.post("/api/v1/images/upload", files={"file": ("test.png", img_data, "image/png")})
    image_id = upload_resp.json()["image_id"]
    
    # 2. Mock masks directly
    create_synthetic_mask(image_id, "femur", 10, 15, 30, 40)
    create_synthetic_mask(image_id, "tibia", 50, 20, 20, 35)
    
    resp = client.post(f"/api/v1/measurements/bones/{image_id}")
    assert resp.status_code == 200
    
    data = resp.json()
    assert data["image_id"] == image_id
    assert data["calibration_available"] == False
    assert data["orientation_status"] == "unknown"
    
    # Check Femur
    assert data["femur"]["width_pixels"] == 40
    assert data["femur"]["ap_dimension_pixels"] == 30
    assert data["femur"]["width_mm"] is None
    
    # Check Tibia
    assert data["tibia"]["width_pixels"] == 35
    assert data["tibia"]["ap_dimension_pixels"] == 20
    assert data["tibia"]["width_mm"] is None
    
    # Repeatability
    resp2 = client.post(f"/api/v1/measurements/bones/{image_id}")
    assert resp2.json() == data

def test_bone_measurements_missing_masks():
    img_data = create_test_image("PNG")
    upload_resp = client.post("/api/v1/images/upload", files={"file": ("test.png", img_data, "image/png")})
    image_id = upload_resp.json()["image_id"]
    
    resp = client.post(f"/api/v1/measurements/bones/{image_id}")
    assert resp.status_code == 400
    assert "not found" in resp.json()["detail"].lower()
