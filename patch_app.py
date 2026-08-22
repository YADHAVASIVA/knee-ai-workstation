import re

with open("frontend/src/App.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Replace legacy imports with new components
new_imports = """
import { Anatomy } from './pages/Anatomy';
import { Analysis } from './pages/Analysis';
import { ImplantPlanning } from './pages/ImplantPlanning';
import { Report } from './pages/Report';
"""
content = content.replace("import { CaseOverview } from './pages/CaseOverview';", "import { CaseOverview } from './pages/CaseOverview';" + new_imports)

# Replace the inner render block
start_idx = content.find("{activeRoute === 'overview' ? (")
end_idx = content.find("</AppShell>")

new_render = """
      {activeRoute === 'overview' && (
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
      )}
      {activeRoute === 'anatomy' && (
        <Anatomy
          previewUrl={previewUrl}
          overlays={overlays}
          measurements={meniscusMeasurement?.locations || []}
          boneMeasurement={boneMeasurement}
          onToggleOverlay={toggleOverlay}
          showMeasurements={showMeniscusLines}
          onToggleMeasurements={setShowMeniscusLines}
          showBoneMeasurements={showBoneLines}
          onToggleBoneMeasurements={setShowBoneLines}
          isDemo={true}
        />
      )}
      {activeRoute === 'analysis' && (
        <Analysis
          patientData={patientData}
          oaResult={oaResult}
          boneMeasurement={boneMeasurement}
          meniscusMeasurement={meniscusMeasurement}
          onAnalyze={handleAnalyzeOA}
          isProcessing={workflowState === WorkflowState.OA_ANALYSIS_RUNNING}
        />
      )}
      {activeRoute === 'planning' && (
        <ImplantPlanning
          matchingResult={matchingResult}
          boneMeasurement={boneMeasurement}
          onMatch={() => handleMatchImplants(false)}
          isProcessing={workflowState === WorkflowState.MATCHING}
        />
      )}
      {activeRoute === 'report' && (
        <Report
          analysisId={analysisId}
          patientData={patientData}
          imageMetadata={imageMetadata}
          boneMeasurement={boneMeasurement}
          meniscusMeasurement={meniscusMeasurement}
          oaResult={oaResult}
          matchingResult={matchingResult}
          onPrint={() => window.print()}
        />
      )}
    """

content = content[:start_idx] + new_render + content[end_idx:]

with open("frontend/src/App.tsx", "w", encoding="utf-8") as f:
    f.write(content)
