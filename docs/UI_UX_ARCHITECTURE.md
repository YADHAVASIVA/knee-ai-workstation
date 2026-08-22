# UI/UX Architecture

## 1. Information Architecture Audit

The current application is a monolithic single-page grid (`App.tsx`). This forces the user to digest uploading, anatomy, analysis, and planning simultaneously. 

**Proposal: Reorganize into a Tabbed/Stepped Workspace Architecture**

| Current Structure | Proposed Primary Area | Rationale |
|---|---|---|
| `UploadArea`, `AnalysisSummaryCard`, `GlobalWarnings` | **1. CASE OVERVIEW** | Ingestion, metadata verification, and calibration validation must happen before analysis. |
| `MedicalImageViewer`, `AnatomicalResultsCard` (Partial) | **2. ANATOMY** | Dedicated space for deep-dive image inspection (zoom/pan) and geometry verification (Meniscus, Femur, Tibia). |
| `PatientProfileCard`, `OAAnalysisPanel` | **3. ANALYSIS** | Contextual space for demographic inputs and resulting OA associations. |
| `ImplantMatchingPanel` | **4. IMPLANT PLANNING** | Dedicated workspace for ranking implants and reviewing explainability metrics. |
| `ReportPreviewModal` | **5. REPORT** | Extracted from a modal into a dedicated persistent export view. |

## 2. Screen Architecture (Minimum Professional Architecture)

### Screen 01 — Case Overview [IMPLEMENTED]
- **Primary Goal:** Ingest DICOM/image, verify physical calibration metadata, and provide a top-level hub for the analysis workflow.
- **Primary User:** Technician / Physician.
- **Primary Action:** File Upload / Proceed to Next Available Step.
- **Most Important Info:** DICOM Modality, Pixel Spacing, Global Workflow Status.
- **Components:** `AppShell`, `CaseOverview`, `UploadArea`, `StatusBadge`, `Card`.
- **Interactions:** Drag & Drop, Dynamic "Next Step" routing.

### Screen 02 — Anatomy
- **Primary Goal:** Visualize AI segmentation and geometric measurements on the medical image.
- **Primary Action:** Review and toggle AI layers.
- **Most Important Info:** Medical Image, Femoral/Tibial/Meniscus geometries (Width, AP).
- **Secondary Info:** Source of measurement (Demo vs Real).
- **Components:** `InteractiveImageViewer`, `LayerToolbar`, `MeasurementListPanel`.
- **Interactions:** Zoom, Pan, Opacity Slider, Layer Toggles.

### Screen 03 — Analysis
- **Primary Goal:** OA demographic correlation.
- **Primary Action:** Input patient age/sex.
- **Most Important Info:** OA Cohort Comparison Graph/Table.
- **Components:** `DemographicsForm`, `OAResultCard`.

### Screen 04 — Implant Planning
- **Primary Goal:** Select the correct implant size based on patient geometry.
- **Primary Action:** Review ranked sizes.
- **Most Important Info:** Ranked Implant List, Similarity Score.
- **Secondary Info:** Width/AP Error explainability breakdowns.
- **Components:** `RankedImplantList`, `SimilarityExplanationChart`, `CalibrationWarningBanner`.

### Screen 05 — Report
- **Primary Goal:** Generate a static, printable summary.
- **Primary Action:** Print / Export.
- **Most Important Info:** Integrated summary of Anatomy + Analysis + Chosen Implant.
- **Components:** `PrintableReportLayout`.
