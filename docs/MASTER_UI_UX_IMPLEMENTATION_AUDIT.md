# KNEE AI WORKSTATION - UI/UX & Architecture Audit

## 1. Current Architecture & Workflow
The application recently migrated from a Single-Image pipeline to a Multi-Image Patient Case Workflow (Phase 13). 
The frontend is built with React + Vite, utilizing a global `CaseState` managed in `App.tsx`.
The backend is a FastAPI application with Pytest coverage.

## 2. Issues Discovered

### Duplicated State & Data Leakage
- While `CaseState` exists, the "Start New Case" reset function does not reset all UI components correctly if they have local state.
- `AppRoute` navigation does not strictly block future steps if prerequisites (like Patient Info) are missing.

### Hardcoded Values
- In `Analysis.tsx`, the `handleRunOaAnalysis` defaults `age: 45` if `parseInt` fails. This violates the prompt instructions ("NEVER: age: 45 as fallback").
- In `Analysis.tsx`, the `sex` falls back to `'Unknown'`. Prompt instructs: `"Not provided"`.

### UI Inconsistencies & CSS Conflicts
- `tokens.css` uses Teal (`#0F766E`) instead of the requested Blue (`#2563EB`).
- The viewer background is `#050709`, requested is `#080B10`.
- Button colors and shadow borders are inconsistent.
- Missing `Success`, `Warning`, `Danger` semantic tokens in `tokens.css`.
- The Anatomy viewer has hardcoded overlay colors instead of using CSS classes.

### Navigation Problems
- The `Sidebar` and `TopBar` use `routes={navItems as any}`, highlighting a TypeScript mismatch.
- The `TopBar` currently lacks the `Case ID`, `Patient Name`, and `Current Step` as explicitly requested in the Phase 14 prompt.
- The top-level `App.tsx` lacks a clear Step Indicator (1 to 6 arrows).

### Image-Processing & API Problems
- Missing a true queue for `Analyze All Valid Images` in `Anatomy.tsx`.
- The `MedicalImageViewer` uses pointer events to pan/zoom, but there are no actual "Zoom In", "Zoom Out", "Fit", "Reset" UI buttons on the viewer toolbar.

## 3. Plan for Corrections
1. **Design System Update**: Rewrite `tokens.css` with the exact hex codes provided. Update `ui.css` buttons.
2. **TopBar & Sidebar Redesign**: Rebuild `TopBar.tsx` to include the Case ID and Patient Name. Build a linear Step Indicator.
3. **Strict Validation**: Fix `CaseOverview.tsx` and `Analysis.tsx` to ensure `age` and `sex` are never fabricated.
4. **Viewer Toolbar**: Implement actual Zoom/Fit/Reset buttons in `MedicalImageViewer.tsx`.
5. **Report & Analysis**: Ensure source image tracking for every finding. Ensure "Not applicable" is strictly followed.
