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
    mask[start_r:start_r+height, start_c:start_c+width] = [255, 0, 0, 128]
    img = Image.fromarray(mask, mode="RGBA")
    img.save(os.path.join(mask_dir, f"{structure_name}.png"))

def test_implant_matching_calibration_refusal():
    img_data = create_test_image("PNG")
    upload_resp = client.post("/api/v1/images/upload", files={"file": ("test.png", img_data, "image/png")})
    image_id = upload_resp.json()["image_id"]
    
    # Femur width 39, ap 29. Tibia width 34, ap 19
    create_synthetic_mask(image_id, "femur", 10, 15, 30, 40)
    create_synthetic_mask(image_id, "tibia", 50, 20, 20, 35)
    
    # No demo calibration provided
    resp = client.post(f"/api/v1/implant-matching/{image_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["matching_status"] == "calibration_required"
    assert "Physical calibration is required" in data["warning"]
    assert len(data["femoral_candidates"]) == 0

def test_implant_matching_demo_success():
    img_data = create_test_image("PNG")
    upload_resp = client.post("/api/v1/images/upload", files={"file": ("test.png", img_data, "image/png")})
    image_id = upload_resp.json()["image_id"]
    
    # Let's target Femoral size 3 which is width 64.0, ap 58.0
    # Patient px dimensions:
    # to get 64mm with spacing 1.0, width=64px. to get 58mm, ap=58px
    create_synthetic_mask(image_id, "femur", 10, 15, 58, 64)
    create_synthetic_mask(image_id, "tibia", 50, 20, 48, 68) # matches tibial size 3 exactly!
    
    # Run with synthetic_pixel_spacing = 1.0
    resp = client.post(f"/api/v1/implant-matching/{image_id}?synthetic_pixel_spacing=1.0")
    assert resp.status_code == 200
    data = resp.json()
    
    assert data["matching_status"] == "success"
    assert data["calibration_available"] == True
    
    fem_candidates = data["femoral_candidates"]
    assert len(fem_candidates) > 0
    assert len(fem_candidates) <= 3
    
    best_fem = fem_candidates[0]
    assert best_fem["size"] == "3"
    assert best_fem["score"] == 100.0 # exact match
    
    tib_candidates = data["tibial_candidates"]
    best_tib = tib_candidates[0]
    assert best_tib["size"] == "3"
    assert best_tib["score"] == 100.0
    
    # Check explanations
    assert best_fem["explanation"]["width_difference"] == 0
    assert best_fem["explanation"]["ap_difference"] == 0
    
    # Demo status
    assert best_fem["is_demo"] == True
    assert best_fem["source_type"] == "synthetic_demo"
    assert "NOT for clinical or surgical use" in data["warning"]

def test_implant_matching_ranking():
    img_data = create_test_image("PNG")
    upload_resp = client.post("/api/v1/images/upload", files={"file": ("test.png", img_data, "image/png")})
    image_id = upload_resp.json()["image_id"]
    
    # Make patient slightly larger than size 3 (64x58), closer to size 4 (68x62)
    create_synthetic_mask(image_id, "femur", 10, 15, 62, 67) # ap=61, width=66
    create_synthetic_mask(image_id, "tibia", 50, 20, 20, 35) # random
    
    resp = client.post(f"/api/v1/implant-matching/{image_id}?synthetic_pixel_spacing=1.0")
    data = resp.json()
    
    cands = data["femoral_candidates"]
    assert len(cands) >= 2
    # Ensure they are ranked descending by score
    assert cands[0]["score"] >= cands[1]["score"]
    
    # Repeatability
    resp2 = client.post(f"/api/v1/implant-matching/{image_id}?synthetic_pixel_spacing=1.0")
    assert resp2.json() == data
