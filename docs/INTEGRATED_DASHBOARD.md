# Integrated Patient-Specific Knee Analysis Dashboard

## 1. User Workflow
The dashboard integrates independent analytical components (Phases 4 through 9) into a single, cohesive workflow:
1. **Image Upload**: Users upload a standard or DICOM-extracted medical knee image.
2. **Preprocessing & Segmentation**: The image undergoes automated anatomical segmentation (Femur, Tibia, Medial Meniscus).
3. **Anatomical Measurements**: Automated calculation of medial meniscus thickness and geometric bone dimensions.
4. **Patient Profiling**: Optional inclusion of age, sex, and clinical OA label.
5. **OA-Associated Analysis**: Demonstration statistical analysis running against an integrated synthetic database.
6. **Implant Matching**: Prototype extraction matching patient anatomy against physical component databases.
7. **Reporting**: Aggregation into a single exportable preview panel.

## 2. State Machine (`useAnalysisWorkflow.ts`)
The orchestrator relies on `WorkflowState` to enforce sequential dependencies.
```ts
export const WorkflowState = {
  IDLE: 'IDLE',
  IMAGE_UPLOADED: 'IMAGE_UPLOADED',
  PREPROCESSING: 'PREPROCESSING',
  READY_FOR_SEGMENTATION: 'READY_FOR_SEGMENTATION',
  SEGMENTING: 'SEGMENTING',
  ...
  ERROR: 'ERROR'
}
```

## 3. Dashboard Architecture
- **Left Panel (Primary Visuals)**: Houses the interactive `MedicalImageViewer`. Visual primacy is given to the underlying evidence.
- **Right Panel (Results & Input)**: Stacked cards detailing Analysis Summary, Anatomical Results, Patient Profiling, OA Analysis, and Implant Matching.
- **Modals**: The `ReportPreviewModal` dynamically aggregates all state values without redundant database storage, ready for print/export.

## 4. Image Viewer Layers
The `MedicalImageViewer` was refactored into a Unified Viewer, supporting deterministic toggles for:
- Base Image
- Segmentation Masks (Femur, Tibia, Meniscus)
- Meniscus Measurements (Locations A, B, C)
- Bone Measurements (Width, AP lines)

## 5. Results Aggregation & Error Recovery
Components gracefully fallback to "Not available" instead of crashing if a phase fails. Uncalibrated states do not permit physical matching unless explicitly forced via the Demo flag.

## 6. Analysis ID & Report Model
Each session generates a temporary `uuid` serving as the `analysis_id`. The report model relies entirely on the aggregation of current front-end states, ensuring it perfectly represents the visible screen and contains no hallucinatory data.

## 7. Demo Limitations
Global banners strictly enforce the prototype nature of the software. Physical mm measurements, orientation, and implant sizing are mathematically transparent but purely synthetic until properly validated clinical DICOM pipelines are introduced.
