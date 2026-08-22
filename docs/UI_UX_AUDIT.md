# UI/UX Audit

## 1. Complete UI Inventory

| Component Name | File | Purpose | Parent | Children | API Dependencies | State Dependencies | Interaction | Current Visual Role | Current UX Problems | Redesign Priority |
|---|---|---|---|---|---|---|---|---|---|---|
| `App` | `src/App.tsx` | Main application shell and routing state | None | `UploadArea`, `MedicalImageViewer`, `ProgressSteps`, `GlobalWarnings`, `AnalysisSummaryCard`, `PatientProfileCard`, `AnatomicalResultsCard`, `ImplantMatchingPanel`, `ReportPreviewModal` | All APIs via hooks | `useAnalysisWorkflow` | Root layout coordination | Main grid | Linear rigid workflow, crammed into a split-pane | P0 |
| `UploadArea` | `src/components/UploadArea.tsx` | Image drag-drop and selection | `App` | None | None | `isProcessing` | Drag/drop, Click | Onboarding | Takes up full left pane until uploaded | P1 |
| `MedicalImageViewer` | `src/components/MedicalImageViewer.tsx` | Primary image and segmentation visualization | `App` | None | Image preview URL, masks | Overlays state | Layer toggle checkboxes | Dominates left pane | Uses static HTML/CSS overlays, no real canvas zoom/pan synchronization | P0 |
| `ProgressSteps` | `src/components/ProgressSteps.tsx` | Visual workflow tracker | `App` | None | None | `workflowState` | None | Top right header | Steps are squished on small screens | P1 |
| `GlobalWarnings` | `src/components/GlobalWarnings.tsx` | Aggregates demo/calibration alerts | `App` | None | None | Calibration, orientation flags | None | Top right banner | Red/Yellow banners stack and clutter vertical space | P1 |
| `AnalysisSummaryCard` | `src/components/AnalysisSummaryCard.tsx` | Displays active metadata and calibration statuses | `App` | None | `/images/{id}/metadata` | `imageMetadata`, `segmentationStatus` | None | Key-value card | Data feels redundant with Global Warnings | P2 |
| `PatientProfileCard` | `src/components/PatientProfileCard.tsx` | Form for Age/Sex entry | `App` | None | `/oa-analysis` | `age`, `sex` | Input fields, Run Analysis button | Form card | Disabled fields during processing lack clear feedback | P1 |
| `AnatomicalResultsCard` | `src/components/AnatomicalResultsCard.tsx` | Displays Meniscus and Bone metrics | `App` | None | None | Measurement results | View Demo Model links | Metric grid | Density is high, hard to distinguish between pixels and physical mm instantly | P1 |
| `ImplantMatchingPanel` | `src/components/ImplantMatchingPanel.tsx` | Calculates and displays ranked implants | `App` | None | `/implant-matching` | Bone results | Reset Matching button | Complex data card | Explainability is presented as raw JSON/lists, hard to read visually | P0 |
| `ReportPreviewModal` | `src/components/ReportPreviewModal.tsx` | Printable summary | `App` | None | None | All states | Print button, Close button | Overlay modal | Relies on raw CSS printing, visual hierarchy is flat | P2 |
| `OAAnalysisPanel` (Legacy) | `src/components/OAAnalysisPanel.tsx` | Standalone OA UI (Deprecating) | None | None | - | - | - | Orphaned | - | P3 |
| `ImplantDatabasePanel` (Legacy) | `src/components/ImplantDatabasePanel.tsx` | Standalone DB viewer | `App` (hidden) | None | `/implants` | - | - | Hidden | - | P3 |

## 2. User Journey Mapping

**Step 1: Application Launch**
- **Sees:** A split pane. Left side: "Drag and drop image here". Right side: Blank/pending placeholders.
- **Action:** User drops a PNG/JPEG/DICOM.
- **Next:** Enters `PREPROCESSING` state.
- **Info:** Loading placeholders.
- **Fails/Prereqs:** File must be under 10MB and valid.
- **Clarity:** Obvious.

**Step 2: Preprocessing & Segmentation**
- **Sees:** "Processing image..." on the left. The `ProgressSteps` increments.
- **Action:** None (Automated).
- **Next:** Segments image, fetches meniscus + bone metrics.
- **Clarity:** Transition is entirely automated. The left pane suddenly populates with the MedicalImageViewer and overlays.

**Step 3: Patient Information & OA Analysis**
- **Sees:** The `PatientProfileCard` unlocks.
- **Action:** Enters Age and Sex, clicks "Run OA Analysis".
- **Next:** OA association likelihood is updated in the UI.
- **Info:** Displays statistical comparison against the demo cohort.

**Step 4: Implant Matching**
- **Sees:** The `ImplantMatchingPanel` activates if measurements succeeded.
- **Action:** None (Automated if calibrated) or clicks "Calculate Matches".
- **Next:** Displays top 3 candidates.
- **Clarity:** Explainability metrics are shown, but dense.

**Step 5: Report Generation**
- **Sees:** "Generate Report" button unlocks in top right.
- **Action:** Clicks button.
- **Next:** Sees `ReportPreviewModal`. Clicks "Print".

## 3. Identify UX Problems

### Navigation
- **Is navigation obvious?** There is no navigation. The app is a single monolithic scrolling page.
- **Can users move backwards?** No.
- **Can users restart?** Yes, via a global "Start New Analysis" button.
- **Are sections logically grouped?** Vertically stacked, but overwhelming on a 1080p screen.

### Information Hierarchy
- **Medical image dominance:** The image viewer is 50% of the screen, which is good, but the right pane is extremely cluttered.
- **Technical details:** The UI exposes technical pipeline details (e.g. "WorkflowState.SEGMENTATION_COMPLETE") directly to the user visually.
- **Warnings:** Global warnings are visible, but push content down aggressively.

### Workflow
- **Prerequisites clear?** Automated steps are clear, but blocked steps (like requiring calibration for implant matching) are greyed out without a localized tooltip.

### Feedback
- **Loading states:** Abrupt. "Processing image..." is static text, not a skeleton or spinner.
- **Error states:** A single red banner at the top of the screen.

### Explainability
- **Ranked implants:** Displays "Width Difference: 0.5" but lacks a visual diagram of the implant vs the bone.
- **AI output vs geometry:** `AnatomicalResultsCard` correctly distinguishes Demo AI vs deterministic math, but relies entirely on text color.

## 4. Medical Image Viewer Audit

- **Image rendering:** Good (loads fast).
- **Zoom/Pan:** **MISSING**. Standard clinical viewers require interactive zooming and panning.
- **Fit/Reset:** **MISSING**.
- **Segmentation overlays:** Pure CSS opacity toggle. Needs improvement (should be canvas-based to scale).
- **Measurement overlays:** Fixed HTML divs positioned absolutely. Will break if the image scales differently.
- **Layer controls:** Floating checkboxes inside the viewer. Good concept, but overlaps critical anatomical regions if the image is tight.
- **Responsive behavior:** Image forces `max-width: 100%`, but aspect ratios can cause clipping.
- **Verdict:** CRITICAL redesign required to implement a Canvas or OpenSeadragon-style interactive viewport.

## 5. Design System Audit

**Inconsistencies:**
- `App.css` defines `--primary-color: #2563eb;`
- `index.css` defines `--accent: #aa3bff;`
- `Card.css` uses hardcoded hex values (`#0ea5e9`, `#059669`) instead of CSS variables.
- Border radius varies between `4px`, `6px`, and `8px`.
- Shadows are defined globally in `index.css` but overridden locally in `Card.css`.
- Typography relies on system fonts, but lacks a strict rem-based scale.

## 6. Accessibility & Responsive

- **Keyboard Navigation:** Poor. Checkboxes inside the image viewer are not reachable via standard tab indexing.
- **Contrast:** Gray text on gray backgrounds (`#94a3b8` on `#f1f5f9`) in disabled form controls fails WCAG AAA.
- **Responsive:** On `< 1024px`, the dual-pane grid collapses into a single column, requiring massive vertical scrolling. The image viewer takes the top, separating it from the data below.
- **Motion:** Abrupt popping when components load. No smooth transitions between workflow states.
