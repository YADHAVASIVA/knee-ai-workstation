import re

# App.tsx
with open("frontend/src/App.tsx", "r", encoding="utf-8") as f:
    content = f.read()

unused_imports = [
    "import { UploadArea } from './components/UploadArea';\n",
    "import { MedicalImageViewer } from './components/MedicalImageViewer';\n",
    "import { OAAnalysisPanel } from './components/OAAnalysisPanel';\n",
    "import { ImplantDatabasePanel } from './components/ImplantDatabasePanel';\n",
    "import { ImplantMatchingPanel } from './components/ImplantMatchingPanel';\n",
    "import { ProgressSteps } from './components/ProgressSteps';\n",
    "import { GlobalWarnings } from './components/GlobalWarnings';\n",
    "import { AnalysisSummaryCard } from './components/AnalysisSummaryCard';\n",
    "import { PatientProfileCard } from './components/PatientProfileCard';\n",
    "import { AnatomicalResultsCard } from './components/AnatomicalResultsCard';\n",
    "import { ReportPreviewModal } from './components/ReportPreviewModal';\n",
]
for imp in unused_imports:
    content = content.replace(imp, "")

content = content.replace("  const [systemInfo, setSystemInfo] = useState<SystemInfoResponse | null>(null);", "")
content = content.replace("        setSystemInfo(sysInfo);", "")
content = content.replace("  const [showReport, setShowReport] = useState<boolean>(false);\n  const [showImplantDb, setShowImplantDb] = useState<boolean>(false);", "")
content = content.replace("errorMsg, setErrorMsg, ", "setErrorMsg, ")
content = content.replace("setPatientData, ", "")
content = content.replace("  const toggleAllOverlays = (show: boolean) => {\n    setOverlays(prev => prev.map(o => ({ ...o, visible: show })));\n  };", "")

with open("frontend/src/App.tsx", "w", encoding="utf-8") as f:
    f.write(content)

# MedicalImageViewer.tsx
with open("frontend/src/components/MedicalImageViewer.tsx", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "onToggleOverlay,\n  showMeasurements = true,\n  onToggleMeasurements,\n  showBoneMeasurements = true,\n  onToggleBoneMeasurements",
    "showMeasurements = true,\n  showBoneMeasurements = true,"
)

with open("frontend/src/components/MedicalImageViewer.tsx", "w", encoding="utf-8") as f:
    f.write(content)

# Report.tsx
with open("frontend/src/pages/Report.tsx", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("  oaResult,\n", "")

with open("frontend/src/pages/Report.tsx", "w", encoding="utf-8") as f:
    f.write(content)
