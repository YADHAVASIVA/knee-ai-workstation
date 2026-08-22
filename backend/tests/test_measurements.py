import pytest
import os
import io
import json
import numpy as np
from PIL import Image
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings
from app.ai.measurements.calibration import CalibrationService
from app.ai.measurements.geometry import calculate_meniscus_thickness

client = TestClient(app)

def create_test_image(format="PNG", size=(100, 100)):
    file = io.BytesIO()
    image = Image.new("RGB", size, color="blue")
    image.save(file, format=format)
    file.seek(0)
    return file.read()

def test_measurement_geometry_synthetic():
    # Create a 20x20 mask where a rectangle from x=2 to 14, y=3 to 6 is the meniscus
    mask = np.zeros((20, 20), dtype=np.uint8)
    mask[3:7, 2:15] = 1 # target_class = 1. Width is 14-2 = 12. Height is 7-3 = 4.
    
    results = calculate_meniscus_thickness(mask, 1)
    
    assert len(results) == 3
    assert results[0]["name"] == "A"
    assert results[0]["x"] == 5
    assert results[0]["thickness_pixels"] == 4.0
    
    assert results[1]["name"] == "B"
    assert results[1]["x"] == 8
    assert results[1]["thickness_pixels"] == 4.0
    
    assert results[2]["name"] == "C"
    assert results[2]["x"] == 11
    assert results[2]["thickness_pixels"] == 4.0

def test_measurement_pipeline():
    # 1. Upload and segment
    img_data = create_test_image("PNG", size=(100, 100))
    upload_resp = client.post("/api/v1/images/upload", files={"file": ("test.png", img_data, "image/png")})
    image_id = upload_resp.json()["image_id"]
    
    client.post(f"/api/v1/images/preprocess/{image_id}")
    client.post(f"/api/v1/segmentation/{image_id}")
    
    # 2. Run Measurement
    measure_resp = client.post(f"/api/v1/measurements/meniscus/{image_id}")
    
    assert measure_resp.status_code == 200
    data = measure_resp.json()
    
    assert data["image_id"] == image_id
    assert data["measurement_type"] == "medial_meniscus_thickness"
    assert data["calibration_available"] is False
    assert len(data["locations"]) == 3
    
    # 3. Repeatability check
    measure_resp_2 = client.post(f"/api/v1/measurements/meniscus/{image_id}")
    assert measure_resp_2.json() == data

def test_measurement_missing_segmentation():
    # Just upload, no segment
    img_data = create_test_image("PNG")
    upload_resp = client.post("/api/v1/images/upload", files={"file": ("test.png", img_data, "image/png")})
    image_id = upload_resp.json()["image_id"]
    client.post(f"/api/v1/images/preprocess/{image_id}")
    
    measure_resp = client.post(f"/api/v1/measurements/meniscus/{image_id}")
    assert measure_resp.status_code == 404
    assert "Segmentation result not found" in measure_resp.json()["detail"]

def test_calibration_service_simulated_valid():
    calib = CalibrationService("fake_id")
    # Manually inject spacing and metadata for test
    calib.pixel_spacing = {"row_mm": 0.5, "column_mm": 0.5}
    calib.metadata["spatial_calibration_available"] = True
    
    assert calib.is_calibrated() is True
    assert calib.pixels_to_mm_x(10.0) == 5.0
    assert calib.pixels_to_mm_y(10.0) == 5.0
