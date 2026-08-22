# Proposed Design System

## 1. Color System
The UI must feel clinical, professional, and trustworthy. Excessive bright accents (like neon purple) will be replaced with medical slate and teal tones.

- **Primary:** `#0f766e` (Teal 700) - Primary actions, active tabs.
- **Secondary:** `#334155` (Slate 700) - Secondary buttons, neutral actions.
- **Background:** `#f8fafc` (Slate 50) - App background.
- **Surface:** `#ffffff` (White) - Card backgrounds, modals.
- **Border:** `#e2e8f0` (Slate 200) - Dividers, card borders.
- **Text Main:** `#0f172a` (Slate 900) - Primary text, headings.
- **Text Muted:** `#64748b` (Slate 500) - Secondary text, metadata.
- **Success:** `#15803d` (Green 700) - Valid calibration, successful match.
- **Warning:** `#b45309` (Amber 700) - Missing calibration, unknown orientation.
- **Error:** `#b91c1c` (Red 700) - Failed upload, API error.
- **Demo/AI Accent:** `#6d28d9` (Violet 700) - Highlighting synthetic/demo AI features to distinguish from real deterministic math.

## 2. Typography System
- **Font Family:** `Inter`, `-apple-system`, `Roboto`, `sans-serif`
- **Headings:** Bold (600/700). H1 (24px), H2 (20px), H3 (16px).
- **Body:** Regular (400) 14px for dense clinical data, 16px for reading.
- **Metadata/Labels:** Medium (500) 12px, uppercase with tracking for section headers.
- **Monospace:** `ui-monospace`, `SFMono-Regular` 13px for IDs, UUIDs, and raw measurements.

## 3. Spacing System
8px-based grid for consistency:
- `4px` (xs): Inside badges, tiny gaps.
- `8px` (sm): Between inputs, list items.
- `12px` (md): Card padding (internal minor).
- `16px` (lg): Standard padding (cards, panels).
- `24px` (xl): Between major UI sections.
- `32px` (2xl): Page margins, heavy section breaks.

## 4. Component System
Reusable primitives to be implemented:
- `AppShell`: Global layout wrapper (TopNav + MainContent).
- `MetricCard`: Standardized key-value display (e.g., `[Width] [64.8 mm]`).
- `StatusBadge`: Pill-shaped semantic tags.
- `WarningBanner`: Full-width alerts for critical/demo limits.
- `InteractiveViewer`: Canvas-based image container supporting zoom/pan.
- `TabNavigation`: Horizontal/Vertical routing links for IA.

## 5. Status System

| Status | Meaning | Visual Treatment |
|---|---|---|
| **SUCCESS** | API returned 200, task complete. | Green outline / Green text |
| **PROCESSING** | Waiting for API/AI. | Animated spinner, Slate text |
| **WARNING** | Data is degraded (uncalibrated). | Amber outline / Amber background |
| **DEMO** | Synthetic data or unvalidated AI. | Violet badge `[DEMO]` |
| **UNAVAILABLE** | Data missing (e.g. Orientation). | Muted Slate text, italic |

## 6. AI Result UX
AI results (segmentation masks, prototype OA metrics) must never masquerade as deterministic clinical truth. 
- Must include a `[DEMO AI]` badge.
- Must display limitations clearly (e.g., "Model: Prototype U-Net v1").

## 7. Measurement UX
Measurements must explicitly bind Value, Unit, and Calibration context.
- **Calibrated (DICOM):** `Femoral Width: 64.8 mm` (Green badge: `Real Calibration`)
- **Uncalibrated (PNG):** `Femoral Width: 129 px` (Amber badge: `Physical calibration unavailable`)

## 8. Implant Matching UX
Ranked candidates must not read like an autonomous surgical command.
- **Wording:** "Potential Anatomical Matches" instead of "Recommended Implant".
- **Explainability:** Display visual horizontal bar charts showing the delta between Patient Geometry and Implant Geometry.

## 9. Warning System
Warnings must be structurally placed, not hidden in tooltips.
- **Critical (Red):** Blocks progression (e.g., "Invalid DICOM file"). Place at top of active screen.
- **Warning (Amber):** Degrades quality (e.g., "No spatial calibration"). Place immediately adjacent to affected data.
- **Demo (Violet):** Hackathon context. Place persistently in `AppShell` header.

## 10. Responsive Design & Accessibility
- **Minimum Width:** 1024px optimized. Below 1024px, panes stack vertically.
- **Accessibility:** All form inputs need `<label>`, colors must pass WCAG AA contrast (e.g., removing light-gray text on white backgrounds).
- **Motion:** Fade-in (`opacity`) and translate (`transform: translateY`) for card entrances. No bouncy or continuous animations.
