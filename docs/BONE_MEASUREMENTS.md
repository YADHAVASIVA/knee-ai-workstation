# Femoral and Tibial Anatomical Measurements

## 1. Purpose
This module provides automated extraction of patient-specific femoral and tibial anatomical dimensions from the segmented image masks. It fulfills the geometric calculation requirement of Phase 7, forming the prerequisite step before database-driven knee implant sizing.

## 2. Methodology & Geometric Definitions
The current MVP operates strictly on 2D image slices (PNG/JPEG formats). True 3D or volumetrically aligned anatomical dimensions cannot be derived from a single unknown projection.

Therefore, the measurements employ a deterministic 2D bounding-box method applied to the binary segmentation masks:
- **Femoral Width:** The maximum horizontal (X-axis) span of the femur segmentation mask.
- **Femoral AP / Image-plane dimension:** The maximum vertical (Y-axis) span of the femur segmentation mask.
- **Tibial Width:** The maximum horizontal (X-axis) span of the tibia segmentation mask.
- **Tibial AP / Image-plane dimension:** The maximum vertical (Y-axis) span of the tibia segmentation mask.

## 3. Anatomical Orientation Status
When analyzing DICOM inputs, the system queries the `ImageOrientationPatient` tags via the `OrientationService`.
- If orientation is available, `orientation_status` = "Known DICOM orientation".
- If orientation is missing or input is PNG/JPEG, `orientation_status` = "Orientation unknown/unavailable".

The frontend application uses this to append a mandatory warning if unknown:
> *Anatomical orientation unknown. AP values represent vertical image-plane geometry.*

This guarantees that a technical vertical span is not confused for a clinically validated Anterior-Posterior (AP) surgical measurement.

## 4. Calibration Handling
The measurement module integrates directly with the `CalibrationService`:
- If `PixelSpacing` data is available, it calculates physical dimension equivalents (`width_mm`, `ap_dimension_mm`).
- If no spatial calibration exists, physical measurements default safely to `null`. The system explicitly blocks fabricating physical measurements.

## 5. Demonstration Mode
If the underlying segmentation originates from the `DemonstrationSegmentationModel` (Phase 4), this status propagates forward. The results clearly display:
> *Measurement based on demonstration segmentation.*

## 6. Frontend Visualization
Bone measurements are overlaid on the `MedicalImageViewer` component.
- **Width:** Rendered as a blue horizontal dashed line `<------>`.
- **AP:** Rendered as an amber vertical dashed line `^|v`.
The endpoints coordinate exact starting and ending points for these overlay drawings directly from the backend bounding-box results.

## 7. Validation
- The endpoint securely verifies the presence of the source image and segmentation prior to execution.
- If a mask is missing or completely empty, the API aborts with `HTTP 400`.
- Synthetic geometry tests in `tests/test_bone_measurements.py` confirm correct width/height numerical calculation using deterministic boolean arrays.
- Measurements are mathematically repeatable.

## 8. Limitations & Future Roadmap
- True clinical preoperative planning relies on DICOM MR/CT images with physical scaling metadata (`PixelSpacing`).
- Measuring AP dimensions accurately often relies on assessing the medial and lateral condyles, which necessitates multi-planar (3D) reconstruction or strictly aligned sagittal views, not arbitrary frontal projections.
