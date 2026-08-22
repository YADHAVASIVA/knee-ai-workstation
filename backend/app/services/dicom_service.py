import io
import os
import pydicom
from pydicom.errors import InvalidDicomError
import numpy as np
from PIL import Image
from typing import Dict, Any, Optional

class DicomAnonymizationService:
    @staticmethod
    def anonymize_dataset(dataset: pydicom.dataset.FileDataset) -> None:
        """
        Implements a minimal anonymization strategy.
        Removes or replaces identifying tags before any long term storage or processing.
        Production-grade anonymization requires formal validation.
        """
        # Basic tags to clear
        tags_to_clear = [
            'PatientName', 'PatientID', 'PatientBirthDate', 'PatientSex',
            'PatientAge', 'PatientAddress', 'PatientTelephoneNumbers',
            'InstitutionName', 'InstitutionAddress', 'ReferringPhysicianName',
            'PerformingPhysicianName', 'OperatorsName', 'StudyID',
            'AccessionNumber', 'StudyDescription', 'SeriesDescription'
        ]
        
        for tag in tags_to_clear:
            if tag in dataset:
                if dataset.data_element(tag).VR in ['PN', 'LO', 'SH', 'CS']:
                    dataset.data_element(tag).value = 'ANONYMIZED'
                else:
                    dataset.data_element(tag).value = ''

class DicomService:
    @staticmethod
    def is_dicom(file_bytes: bytes) -> bool:
        # Check DICOM magic number at offset 128
        if len(file_bytes) > 132:
            return file_bytes[128:132] == b"DICM"
        return False

    @staticmethod
    def parse_dicom(file_bytes: bytes) -> Dict[str, Any]:
        try:
            dataset = pydicom.dcmread(io.BytesIO(file_bytes))
        except InvalidDicomError:
            raise ValueError("File is not a valid DICOM.")

        # Anonymize
        DicomAnonymizationService.anonymize_dataset(dataset)

        # Extract safely
        metadata = {
            "format": "DICOM",
            "modality": getattr(dataset, "Modality", "UNKNOWN"),
            "rows": getattr(dataset, "Rows", None),
            "columns": getattr(dataset, "Columns", None),
            "study_uid": str(getattr(dataset, "StudyInstanceUID", "")),
            "series_uid": str(getattr(dataset, "SeriesInstanceUID", "")),
            "sop_instance_uid": str(getattr(dataset, "SOPInstanceUID", "")),
            "slice_thickness": float(dataset.SliceThickness) if "SliceThickness" in dataset else None,
            "spatial_calibration_available": False,
            "orientation_available": False,
            "pixel_spacing": None,
            "image_orientation": None,
            "image_position": None,
            "orientation_status": "UNAVAILABLE"
        }

        if "PixelSpacing" in dataset and len(dataset.PixelSpacing) == 2:
            metadata["pixel_spacing"] = {
                "row_mm": float(dataset.PixelSpacing[0]),
                "column_mm": float(dataset.PixelSpacing[1])
            }
            metadata["spatial_calibration_available"] = True

        if "ImageOrientationPatient" in dataset:
            try:
                metadata["image_orientation"] = [float(x) for x in dataset.ImageOrientationPatient]
                metadata["orientation_available"] = True
                metadata["orientation_status"] = "AVAILABLE"
            except Exception:
                metadata["orientation_status"] = "UNKNOWN"
                
        if "ImagePositionPatient" in dataset:
            try:
                metadata["image_position"] = [float(x) for x in dataset.ImagePositionPatient]
            except Exception:
                pass

        return {"metadata": metadata, "dataset": dataset}

    @staticmethod
    def extract_image_array(dataset: pydicom.dataset.FileDataset) -> Image.Image:
        """
        Extracts pixel array and applies DICOM windowing / slope / intercept
        to produce a normal PIL image.
        """
        if not hasattr(dataset, 'pixel_array'):
            raise ValueError("DICOM file does not contain PixelData")

        arr = dataset.pixel_array.astype(float)

        # Apply Rescale Slope / Intercept
        slope = getattr(dataset, 'RescaleSlope', 1.0)
        intercept = getattr(dataset, 'RescaleIntercept', 0.0)
        arr = arr * slope + intercept

        # Apply Window Center / Width
        window_center = getattr(dataset, 'WindowCenter', None)
        window_width = getattr(dataset, 'WindowWidth', None)
        
        if window_center is not None and window_width is not None:
            # Handle multiple windows
            if isinstance(window_center, pydicom.multival.MultiValue):
                window_center = float(window_center[0])
            else:
                window_center = float(window_center)
                
            if isinstance(window_width, pydicom.multival.MultiValue):
                window_width = float(window_width[0])
            else:
                window_width = float(window_width)

            min_val = window_center - window_width / 2.0
            max_val = window_center + window_width / 2.0
            
            arr = np.clip(arr, min_val, max_val)
            arr = ((arr - min_val) / window_width) * 255.0
        else:
            # Auto-window based on min/max
            min_val = arr.min()
            max_val = arr.max()
            if max_val > min_val:
                arr = ((arr - min_val) / (max_val - min_val)) * 255.0
            else:
                arr = np.zeros_like(arr)
                
        arr = arr.astype(np.uint8)
        
        # Photometric Interpretation
        pi = getattr(dataset, 'PhotometricInterpretation', '')
        if pi == 'MONOCHROME1':
            arr = 255 - arr
            
        img = Image.fromarray(arr)
        if len(img.getbands()) == 1:
            img = img.convert("RGB")
            
        return img
