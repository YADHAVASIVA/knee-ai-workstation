import os
import io
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_dirs():
    settings.create_dirs()
    yield

def create_test_image(format="JPEG", size=(100, 100)):
    file = io.BytesIO()
    image = Image.new("RGB", size, color="blue")
    image.save(file, format=format)
    file.seek(0)
    return file.read()

def test_upload_valid_jpeg():
    img_data = create_test_image("JPEG")
    response = client.post(
        "/api/v1/images/upload",
        files={"file": ("test.jpg", img_data, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "image_id" in data
    assert data["status"] == "uploaded"
    assert data["width"] == 100
    assert data["height"] == 100

def test_upload_valid_png():
    img_data = create_test_image("PNG")
    response = client.post(
        "/api/v1/images/upload",
        files={"file": ("test.png", img_data, "image/png")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content_type"] == "image/png"

def test_upload_unsupported_file():
    response = client.post(
        "/api/v1/images/upload",
        files={"file": ("test.txt", b"hello world", "text/plain")}
    )
    assert response.status_code == 400
    assert "Unsupported" in response.json()["detail"]

def test_upload_empty_file():
    response = client.post(
        "/api/v1/images/upload",
        files={"file": ("test.jpg", b"", "image/jpeg")}
    )
    assert response.status_code == 400
    assert "Empty" in response.json()["detail"]

def test_upload_corrupted_image():
    response = client.post(
        "/api/v1/images/upload",
        files={"file": ("corrupt.jpg", b"this is not an image", "image/jpeg")}
    )
    assert response.status_code == 400
    assert "Invalid medical image" in response.json()["detail"]

def test_preprocessing():
    # First upload
    img_data = create_test_image("JPEG")
    upload_resp = client.post(
        "/api/v1/images/upload",
        files={"file": ("test.jpg", img_data, "image/jpeg")}
    )
    image_id = upload_resp.json()["image_id"]

    # Then preprocess
    process_resp = client.post(f"/api/v1/images/preprocess/{image_id}")
    assert process_resp.status_code == 200
    data = process_resp.json()
    assert data["status"] == "processed"
    assert data["spatial_calibration_available"] is False
    assert data["original_dimensions"]["width"] == 100

    # Then fetch preview
    preview_resp = client.get(f"/api/v1/images/{image_id}/preview")
    assert preview_resp.status_code == 200
    assert preview_resp.headers["content-type"] == "image/jpeg"

def test_missing_image():
    response = client.post("/api/v1/images/preprocess/fake-id")
    assert response.status_code == 404

def test_invalid_preview():
    response = client.get("/api/v1/images/fake-id/preview")
    assert response.status_code == 404
