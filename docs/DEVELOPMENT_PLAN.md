# Development Plan

## Phase 1 — Foundation
Set up the initial project repository, folder structure, documentation, and base environments for frontend (Next.js/React), backend (FastAPI), and AI (PyTorch/MONAI). Initialize the SQLite database.

## Phase 2 — Medical Image Input
Develop the frontend upload interface and backend endpoints to accept and store suitable knee medical imaging data. Ensure file formats (e.g., DICOM, NIfTI, or standard image formats for the hackathon) are correctly handled.

## Phase 3 — Image Preprocessing
Implement medical image processing pipelines (OpenCV, SimpleITK) on the backend to normalize, resize, and prepare images for AI inference.

## Phase 4 — AI Segmentation
- [x] Phase 4: AI Segmentation Foundation (Femur/Tibia/Meniscus)
- [x] Phase 5: Medial Meniscus Thickness Measurement
Integrate the AI models (PyTorch/MONAI) to identify and segment the femur, tibia, and medial meniscus. Set up the inference pipeline to generate segmentation masks from preprocessed images.

## Phase 5 — Meniscus Thickness Measurement
Develop the algorithms to locate the medial meniscus within the joint space and calculate its thickness at predefined anatomical locations using the segmentation masks.

## Phase 6 — OA Analysis
- [x] Phase 6: Osteoarthritis-Associated Analysis
Implement the logic to associate measurements with patient data (age, sex, OA status). Build statistical/comparative analysis features to compare OA vs. non-OA cases and male vs. female populations.

## Phase 7 — Femoral/Tibial Measurement
- [x] Phase 7: Femoral and Tibial Anatomical Measurements
Develop the algorithms to extract relevant femoral and tibial anatomical dimensions (e.g., widths, anteroposterior dimensions) required for implant sizing from the segmented bone structures.

## Phase 8 — Implant Database
- [x] Phase 8: Patient-Specific Implant Sizing Database
Create the backend database schema to hold implant specifications. Populate it with demonstration/synthetic data, keeping a strict boundary to avoid fabricating clinical manufacturer specifications. for various femoral and tibial implant components.

## Phase 9 — Implant Size Matching
- [x] Phase 9: Patient-Specific Implant Size Matching
Implement the recommendation engine that compares patient-specific anatomical measurements against the implant database to produce a ranked list of suitable implant sizes. Include transparency/explainability metrics so surgeons understand why a size was matched. frontend dashboard to display the medical images, overlay AI-detected structures (segmentations), show measurement locations, and present the structured analysis results and implant recommendations.

## Phase 10 — Visualization Dashboard
- [x] Phase 10: Integrated Patient-Specific Knee Analysis Dashboard
Build out the frontend dashboard to display the medical images, overlay AI-detected structures (segmentations), show measurement locations, and present the structured analysis results and implant recommendations.

## Phase 11 — Validation and Testing
Write and execute unit and integration tests across the pipelines. Ensure the system behaves reliably with different inputs and gracefully handles errors.

## Phase 12 — Hackathon Demo Polish
Refine the UI/UX, add clear disclaimers that this is an AI-assisted research/decision-support prototype (not an autonomous diagnostic tool), finalize mock data integration, and prepare the final presentation flow.
