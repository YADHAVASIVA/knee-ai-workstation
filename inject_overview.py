import re

with open("frontend/src/App.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add import for CaseOverview
if "import { CaseOverview }" not in content:
    content = content.replace(
        "import type { RouteId } from './components/shell/Sidebar';",
        "import type { RouteId } from './components/shell/Sidebar';\nimport { CaseOverview } from './pages/CaseOverview';"
    )

# Replace the content inside AppShell
shell_start_idx = content.find("{/* LEGACY DASHBOARD - Temporarily placed inside the new shell */}")

new_content = """
      {activeRoute === 'overview' ? (
        <CaseOverview 
          workflowState={workflowState}
          analysisId={analysisId}
          imageMetadata={imageMetadata}
          previewUrl={previewUrl}
          patientData={patientData}
          segmentationResult={segmentationResult}
          boneMeasurement={boneMeasurement}
          meniscusMeasurement={meniscusMeasurement}
          oaResult={oaResult}
          matchingResult={matchingResult}
          onNavigate={setActiveRoute}
          onUpload={handleFileUpload}
          onReset={resetAnalysis}
        />
      ) : (
        <div className="legacy-container-wrapper">
"""
content = content.replace("{/* LEGACY DASHBOARD - Temporarily placed inside the new shell */}", new_content)

# We need to close the `legacy-container-wrapper` before `</AppShell>`
content = content.replace("    </AppShell>", "      </div>\n      )}\n    </AppShell>")

with open("frontend/src/App.tsx", "w", encoding="utf-8") as f:
    f.write(content)
