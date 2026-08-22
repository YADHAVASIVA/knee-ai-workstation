# DICOM and Physical Calibration Pipeline

This document describes the DICOM input and physical calibration foundation implemented in Phase 11.

## DICOM Support
The system now accepts native DICOM files alongside standard PNG/JPEG images. DICOM parsing is handled using `pydicom`, safely abstracting standard pixel extraction and windowing before sending normalized frames into the existing AI segmentation pipeline.

## Metadata Extraction
When a DICOM is ingested, the system extracts critical metadata:
- `Modality` (e.g., MR, CT)
- `Rows` and `Columns`
- `StudyInstanceUID`, `SeriesInstanceUID`, `SOPInstanceUID`
- `SliceThickness`
- `PixelSpacing` (for physical calibration)
- `ImageOrientationPatient` (for anatomical validation)
- `ImagePositionPatient`

## PixelSpacing and Calibration
DICOM `PixelSpacing` typically contains `[row_spacing, column_spacing]`. The `CalibrationService` captures this explicitly to support anisotropic pixel spacing.
- Measurements across the x-axis (e.g., width) use `column_mm`.
- Measurements across the y-axis (e.g., height/AP) use `row_mm`.

## Orientation and ImagePosition
The system extracts `ImageOrientationPatient` and `ImagePositionPatient`. The `OrientationService` determines if anatomical axes (AP, ML) can be formally validated, preventing the system from falsely equating image-plane XY measurements with true anatomical dimensions when orientation is unavailable.

## Privacy and Security
A `DicomAnonymizationService` sits at the ingestion border. It immediately scrubs standard identifiers (`PatientName`, `PatientID`, `PatientBirthDate`, etc.) before any long-term storage or processing occurs. *Note: This is a minimal strategy; production-grade anonymization requires formal validation.*

## Limitations
- Synthetic DICOM testing proves the architecture works, but real-world DICOM datasets often contain proprietary metadata tags or corrupted pixel streams that may require more robust normalization strategies.
- 3D volume reconstruction is not implemented in this phase. Image position metadata is stored for future multi-planar rendering.
