# Patient-Specific Implant Size Matching

## 1. Purpose
The Implant Size Matching module satisfies Phase 9 of the project plan. It operates by cross-referencing extracted anatomical patient geometries (Femoral/Tibial AP and Width dimensions) against the SQLite database of implant candidates. The module computes a deterministic "Anatomical Similarity Score" and generates ranked candidates with full numerical explainability.

## 2. Clinical Safety & Constraints
**CRITICAL LIMITATION**: This algorithm produces a mathematical prototype score. It strictly operates within a safely isolated demonstration mode. 
- It does **not** provide surgical recommendation or probability predictions.
- It explicitly refuses to attempt matching if the input image lacks physical calibration metadata (`PixelSpacing`).
- Without DICOM spatial calibration, the engine blocks arbitrary pixel-to-millimeter conversions.
- The UI visibly alerts users that the matches are "Demonstration Match - Not for clinical use" and propagates the `is_demo=True` flags from Phase 8.

## 3. Mathematical Formula
For each candidate implant `C`, error calculation runs on structural width and anteroposterior (AP) parameters:

`width_error = abs(patient_width - C_width) / C_width`
`ap_error = abs(patient_ap - C_ap) / C_ap`

**Weighting Strategy:**
Currently initialized with equal prioritization:
- `WEIGHT_WIDTH = 0.5`
- `WEIGHT_AP = 0.5`

**Score Calculation:**
`combined_error = (WEIGHT_WIDTH * width_error) + (WEIGHT_AP * ap_error)`
`prototype_score = max(0.0, 100.0 * (1.0 - combined_error))`

A `MINIMUM_MATCH_SCORE = 50.0` threshold is enforced. Candidates beneath this threshold are rejected.

## 4. API & Explainability Output
Endpoint: `POST /api/v1/implant-matching/{image_id}`

For qualifying candidates, the algorithm builds a rich `CandidateExplanation` schema:
```json
{
  "rank": 1,
  "size": "3",
  "score": 98.5,
  "explanation": {
    "width_difference": 0.5,
    "width_error": 0.0078,
    "ap_difference": 1.2,
    "ap_error": 0.0206,
    "combined_normalized_error": 0.0142,
    "contribution_to_score": 98.5
  }
}
```
This is fully visualized on the frontend with horizontal comparative bars tracking exact dimension deviations.

## 5. Calibration Integration
The engine now formally supports DICOM physical calibration. 
- If a true DICOM is uploaded with a valid `PixelSpacing` tag, the matching algorithm will calculate natively in physical millimeters.
- For testing with uncalibrated PNG/JPEG images, the system permits passing a testing flag: `?synthetic_pixel_spacing=1.0`. This allows the backend to simulate physical scaling exclusively for showcasing the mathematical engine during hackathon demonstrations.
- The UI strictly differentiates between a `REAL DICOM CALIBRATION` and `DEMONSTRATION CALIBRATION`.
