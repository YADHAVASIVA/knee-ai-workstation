# System Architecture

## 1. System Overview
The AI-Assisted Assessment of Medial Meniscus Thickness and Patient-Specific Knee Implant Sizing platform is a unified clinical decision-support prototype. It connects medical image analysis, anatomical measurement, osteoarthritis (OA) assessment, and patient-specific implant planning. The system takes suitable knee medical imaging data as input and provides structured analysis and visualizations.

## 2. Frontend Architecture
- **Framework:** React or Next.js
- **Language:** TypeScript
- **Purpose:** Provides a dashboard for uploading images, displaying AI-detected structures, visualizing measurement locations directly on medical images, and presenting structured analysis results (measurements, OA comparison, implant ranking).

## 3. Backend Architecture
- **Framework:** FastAPI
- **Language:** Python
- **Purpose:** Acts as the integration layer. Exposes REST API endpoints for the frontend, orchestrates the AI pipelines, manages database interactions, and handles business logic for OA comparisons and implant matching.

## 4. AI Architecture
- **Frameworks:** PyTorch, MONAI
- **Language:** Python
- **Purpose:** Handles the deep learning models for segmentation of anatomical structures (femur, tibia, medial meniscus). It processes imaging data into structured masks and measurements.

## 5. Processing Pipeline Architecture
The system employs a unified processing pipeline that links image ingestion directly to database implant retrieval:

1. **DICOM / PNG / JPEG Input:** Accepts medical imaging data.
2. **Input Validation:** Verifies MIME types and DICOM headers.
3. **Metadata Extraction:** Extracts study UID, modality, image orientation, and scrubs sensitive identifiers using `pydicom`.
4. **Spatial Calibration:** Identifies anisotropic `PixelSpacing` data to enable physical mm conversion.
5. **Preprocessing:** Normalizes DICOM/image arrays, applies windowing, and generates AI-ready PNGs and UI thumbnails.
6. **AI Analysis:** Applies deep learning models (e.g., U-Net architectures) to generate binary segmentation masks for the femur, tibia, and medial meniscus.
7. **Physical Measurements:** Calculates vertical meniscus thickness and geometric bone bounding boxes, scaling pixel values to millimeters if calibration is available.
8. **Implant Matching:** Compares the calibrated anatomical dimensions against a structured knee implant database to identify the closest ranked component sizes.

## 11. Database Architecture
- **System:** SQLite (for hackathon MVP)
- **Purpose:** Stores structured data including patient demographics (age, sex, OA status), calculated anatomical measurements, meniscus thickness results, and the knee implant sizing database (manufacturer specifications).

## 12. API Architecture
- **Style:** RESTful
- **Key Endpoints:** Image upload/processing, retrieval of analysis results, implant database queries, and demographic filtering for OA analysis.

## 13. Visualization Architecture
- **Process:** The frontend receives raw/compressed images along with segmentation overlays (masks/contours) and point coordinates for measurement locations. These are rendered on a canvas or medical image viewer component to allow clinicians to verify AI-generated measurements.

## 14. Testing Strategy
- **Approach:**
  - **Unit Tests:** For measurement algorithms (verifying geometric calculations), implant matching logic, and API endpoint validations.
  - **Integration Tests:** Verifying the flow from image upload to final measurement output.
  - **Data Validation:** Ensuring mock clinical data and implant sizes are strictly labeled as such and do not represent real-world clinical thresholds during the prototype phase.
