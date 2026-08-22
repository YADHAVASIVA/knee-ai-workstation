# System Architecture

## Application Pipeline
`Analysis Session` -> `Workflow State` -> `Image` -> `AI Results` -> `Measurements` -> `OA Analysis` -> `Implant Matching` -> `Integrated Report` -> `Dashboard`

## Overview
The Knee AI Analysis Platform is built using a modern React + Vite frontend and a FastAPI backend, designed for rapid MVP prototyping of medical imaging analysis.

## Core Services

### 1. Medical Image Pipeline
Handles file uploads, robust format validation (PNG/JPG), RGB normalization, and resizing. Extracts metadata (e.g., DICOM spatial calibration if present).

### 2. Segmentation Pipeline
Segments anatomical structures:
- Femur
- Tibia
- Medial Meniscus

Currently powered by a `DemonstrationSegmentationModel` (mock deterministic logic) to ensure development safety without requiring massive pretrained AI weights in the repository.

### 3. Measurement Engines
**Meniscus Engine:** 
Extracts vertical thickness at predefined widths (25%, 50%, 75%) from the segmented mask. Returns pixel coordinates and physical geometry (if calibrated).

**Bone Engine:**
Calculates 2D maximum geometrical bounding-box properties (width, AP dimension) for the femur and tibia masks.

### 4. Osteoarthritis (OA) Analysis
Compares the measured dimensions against a demonstration dataset using `pandas` for demographic insights (Age, Sex, Clinical Status).

### 5. Implant Database
A lightweight SQLite / SQLAlchemy persistent store containing standard dimensions for synthetic demonstration implant components (Femoral and Tibial). Ensures the data structure is fully prepared for future patient-specific measurement matching.

### 6. Implant Size Matching Engine
A deterministic scoring module that:
1. Receives Bone Measurements
2. Validates Unit Calibration & Image Orientation
3. Retrieves DB Implant Candidates
4. Computes Absolute Percentage Distance Error 
5. Emits an Anatomical Similarity Score (0-100)
6. Ranks Top 3 Candidates
7. Generates transparent Explanations for why specific sizes ranked higher.
