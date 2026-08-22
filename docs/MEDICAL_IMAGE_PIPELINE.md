# Medical Image Pipeline

## 1. Input
The system accepts medical imaging data in the following formats:
- DICOM (`.dcm` or by content verification)
- PNG
- JPG / JPEG
Max file size is limited to 10MB to prevent denial of service.

## 2. Validation & Parsing
- Extension, MIME type, and file size verification
- DICOM headers are parsed with `pydicom` to ensure it is a valid medical imaging file
- Integrity verification ensures the file is not corrupted

## 3. Storage
Uploaded and processed images are kept locally in the `data/` directory:
- `data/uploads/dicom/`: Original uploaded DICOM files.
- `data/uploads/images/`: Original uploaded PNG/JPEG files.
- `data/processed/`: Normalized representation (RGB, PNG) ready for AI inference.
- `data/previews/`: Downscaled JPEG representations (max 800x800) for fast UI rendering.

Internal filenames are generated as UUIDs (`image_id`) to ensure no path traversal or original filename leaks.

## 4. Metadata
Metadata extraction grabs available information safely:
- Dimensions (width, height)
- Pixel spacing (`row_mm`, `column_mm`) for DICOM
- Orientation (`ImageOrientationPatient`) for DICOM
- Modality (e.g. MR, CR)
- Sensitive identifiers (PatientName, PatientID, etc.) are explicitly scrubbed and set to "ANONYMIZED" before saving to prevent privacy leaks.

## 5. Preprocessing
The preprocessing pipeline executed for every valid image:
1. Load image (extracting PixelData applying slope, intercept, and windowing for DICOM).
2. Convert to standard RGB representation.
3. Preserve original dimensions for processed output.
4. Save processed output to `data/processed/`.
5. Generate a thumbnail (max 800x800) and save to `data/previews/`.

## 6. Spatial Calibration & Orientation
- **DICOM**: When valid `PixelSpacing` is present, `spatial_calibration_available` is `True`.
- **PNG/JPEG**: Do not inherently contain clinical spatial calibration metadata, so `spatial_calibration_available` is `False`.
- The measurement and implant matching modules use this metadata to determine whether to perform physical measurement conversions and physical implant matching.

## 7. Preview
The preview endpoint serves the lightweight JPEG thumbnail generated during preprocessing to ensure the frontend Viewer remains performant.

## 8. Current Limitations
- Does not automatically enforce image orientation constraints for analysis (only reads it).
- Not meant for production clinical diagnostic use. Anonymization is basic and lacks formal HIPAA validation.
