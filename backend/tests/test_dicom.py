import pytest
import io
from fastapi.testclient import TestClient
import numpy as np
import pydicom
from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.uid import UID

from app.main import app
from app.services.dicom_service import DicomService
from app.ai.measurements.calibration import CalibrationService, OrientationService

client = TestClient(app)

def create_synthetic_dicom(has_pixel_data=True, anisotropic=False):
    # Minimal DICOM for testing
    file_meta = FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = UID('1.2.840.10008.5.1.4.1.1.4') # MR Image Storage
    file_meta.MediaStorageSOPInstanceUID = UID('1.2.3')
    file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
    
    ds = FileDataset(None, {}, file_meta=file_meta, preamble=b"\0" * 128)
    ds.PatientName = "Test^Patient"
    ds.PatientID = "123456"
    ds.Modality = "MR"
    ds.StudyInstanceUID = "1.2.3.4"
    ds.SeriesInstanceUID = "1.2.3.4.5"
    ds.SOPInstanceUID = "1.2.3.4.5.6"
    
    # Image size
    ds.Rows = 100
    ds.Columns = 100
    
    if anisotropic:
        ds.PixelSpacing = ["0.6", "0.4"] # [row_mm, col_mm] -> y, x
    else:
        ds.PixelSpacing = ["0.5", "0.5"]
        
    ds.ImageOrientationPatient = ["1", "0", "0", "0", "1", "0"]
    ds.ImagePositionPatient = ["0", "0", "0"]
    
    if has_pixel_data:
        ds.BitsAllocated = 16
        ds.BitsStored = 16
        ds.HighBit = 15
        ds.PixelRepresentation = 0
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
        # Synthetic pixel data
        pixel_array = np.zeros((100, 100), dtype=np.uint16)
        ds.PixelData = pixel_array.tobytes()
        
    # Write to memory
    with io.BytesIO() as fp:
        ds.save_as(fp)
        return fp.getvalue()

def test_dicom_parsing():
    dcm_bytes = create_synthetic_dicom()
    assert DicomService.is_dicom(dcm_bytes)
    
    res = DicomService.parse_dicom(dcm_bytes)
    meta = res["metadata"]
    assert meta["modality"] == "MR"
    assert meta["pixel_spacing"]["row_mm"] == 0.5
    assert meta["spatial_calibration_available"] == True
    assert meta["orientation_available"] == True
    
    # Verify Anonymization
    ds = res["dataset"]
    assert ds.PatientName == "ANONYMIZED"

def test_dicom_upload_and_metadata_endpoint():
    dcm_bytes = create_synthetic_dicom()
    upload_resp = client.post("/api/v1/images/upload", files={"file": ("test.dcm", dcm_bytes, "application/dicom")})
    assert upload_resp.status_code == 200
    data = upload_resp.json()
    assert data["format"] == "DICOM"
    assert data["spatial_calibration_available"] == True
    
    image_id = data["image_id"]
    
    # GET Metadata
    meta_resp = client.get(f"/api/v1/images/{image_id}/metadata")
    assert meta_resp.status_code == 200
    meta_data = meta_resp.json()
    assert meta_data["format"] == "DICOM"
    assert meta_data["pixel_spacing"]["row_mm"] == 0.5

def test_anisotropic_spacing_and_calibration():
    dcm_bytes = create_synthetic_dicom(anisotropic=True)
    upload_resp = client.post("/api/v1/images/upload", files={"file": ("test.dcm", dcm_bytes, "application/dicom")})
    image_id = upload_resp.json()["image_id"]
    
    calib = CalibrationService(image_id)
    assert calib.is_calibrated()
    # 10 pixels x-axis -> column_mm (0.4) -> 4.0
    # 10 pixels y-axis -> row_mm (0.6) -> 6.0
    assert calib.pixels_to_mm_x(10) == 4.0
    assert calib.pixels_to_mm_y(10) == 6.0
