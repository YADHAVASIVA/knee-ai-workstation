# Case Overview

## Purpose
The Case Overview is the first product screen in the Knee AI Workstation. Its primary objective is to answer the immediate questions of a clinical or research user: *What case is this? What image was loaded? Is the data physically calibrated? What analysis has been completed? What is the next logical step?* 

It acts as the central hub and routing point for the rest of the application without overwhelming the user with raw data or technical jargon.

## User Journey
1. **Empty State:** A user is presented with a professional "NO ACTIVE CASE" view containing a central drag-and-drop ingestion area.
2. **Ingestion:** Upon uploading an image (DICOM, PNG, JPEG), the image is auto-preprocessed, and the state dynamically switches to the active Case Workspace.
3. **Active Workspace:** The user views a dual-column summary:
   - **Left Column:** A checklist of analysis statuses, the patient's profile (demographics), and top-level anatomical and measurement snapshots.
   - **Right Column:** A thumbnail of the actual medical scan, core DICOM metadata, spatial calibration flags, and a snapshot of implant matches.
4. **Action:** A prominent "NEXT STEP" card guides the user dynamically (e.g., "Open Anatomy" when segmentation finishes, "Open Analysis" when ready, etc.).

## Information Hierarchy
1. **Case Identity:** TopBar persistent Analysis ID and Case Title.
2. **Analysis Status:** A clear visual checklist of what the AI has accomplished.
3. **Image Information:** The visual proof of the uploaded scan and its physical reliability (`CALIBRATED` vs `UNCALIBRATED`).
4. **Action Routing:** The bottom-right dynamic CTA card.
5. **Key Anatomical Results:** Mean thickness and bone width snapshots.
6. **Patient Data:** Secondary demographic information.

## Components Used
- `AppShell` (Parent Wrapper)
- `Card` (Modular content blocks)
- `StatusBadge` (Semantic state indicators: `SUCCESS`, `PROCESSING`, `UNAVAILABLE`)
- `Button` (Primary CTAs and secondary navigation)
- `SectionHeader` (Title management with reset actions)
- `UploadArea` (Re-integrated cleanly for empty states)

## States
- **IDLE:** Render the "NO ACTIVE CASE" Empty State with a centered upload zone.
- **PROCESSING:** Badges pulse or read `PROCESSING` while the background AI inference (segmentation, measuring) completes.
- **CALIBRATED vs UNCALIBRATED:** Image info clearly dictates if physical mm measurements are valid or if it's a pixel-only demo.
- **DEMO DATA:** TopBar flags the session as a `DEMONSTRATION PROTOTYPE`.

## Responsive Behavior
- **Desktop (>1024px):** Symmetrical 2-column grid (`1fr 1fr`).
- **Tablet/Mobile (<1024px):** Columns collapse into a 1-column stack. The Image Information card re-prioritizes above deep measurements to keep context close to the top.

## Accessibility
- **Semantic HTML:** Relies on clear `h3` tags inside structural cards.
- **Color Independence:** Success (`✓`), Error (`✖`), and Warning (`!`) statuses use distinct icons alongside color to ensure colorblind accessibility.

## Design Decisions
- **No Card Grids:** Avoided a messy 3x3 dashboard layout. Structured content into logical vertical flows.
- **Dynamic CTAs:** Instead of exposing all 5 navigation buttons prominently, the `Next Action` card computes exactly what the user should click next based on the internal `WorkflowState` enum.
- **No Technical Jargon:** Abstracted internal API terms like `MEASURING_BONES` into a simple user-facing "Measurements" checklist item.
