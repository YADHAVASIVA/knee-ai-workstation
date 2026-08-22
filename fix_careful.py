import re

# Restore from refactor
import os
os.system('python c:/Users/omen1/.gemini/antigravity/brain/dfc99f97-3a3c-47ef-9f9a-c416bb95b80d/scratch/refactor.py')

with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app = f.read()

# carefully remove patientData and oaResult ONLY from Report
# It looks like:
#       case 'report':
#         return (
#           <Report 
#             analysisId={analysisId}
#             imageMetadata={imageMetadata}
#             patientData={patientData}
#             boneMeasurement={boneMeasurement}
#             meniscusMeasurement={meniscusMeasurement}
#             oaResult={oaResult}
#             matchingResult={matchingResult}
#             onNavigate={handleNavigate as any}
#           />
#         );
report_block = re.search(r'<Report\s+.*?\s*/>', app, re.DOTALL).group(0)
new_report_block = re.sub(r'\s*patientData={patientData}', '', report_block)
new_report_block = re.sub(r'\s*oaResult={oaResult}', '', new_report_block)
app = app.replace(report_block, new_report_block)

# Remove onPrint if it exists (wait, does refactor.py add onPrint? No. refactor.py doesn't add onPrint)

# Wait, there's another TS error: 'oaResult' is declared but its value is never read.
# Let's remove oaResult from the destructuring in useAnalysisWorkflow if it's completely unused
app = re.sub(r'oaResult,\s*setOaResult', 'setOaResult', app)

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(app)

# Fix Report.tsx
with open('frontend/src/pages/Report.tsx', 'r', encoding='utf-8') as f:
    rep = f.read()
rep = rep.replace('  patientData: any;\n', '')
rep = rep.replace('  oaResult: any;\n', '')
rep = rep.replace('  patientData,\n', '')
rep = rep.replace('  oaResult,\n', '')
with open('frontend/src/pages/Report.tsx', 'w', encoding='utf-8') as f:
    f.write(rep)

# Fix CaseOverview.tsx unused destructuring
with open('frontend/src/pages/CaseOverview.tsx', 'r', encoding='utf-8') as f:
    co = f.read()
co = co.replace('  patientData,\n', '')
co = co.replace('  segmentationResult,\n', '')
co = co.replace('  boneMeasurement,\n', '')
co = co.replace('  meniscusMeasurement,\n', '')
co = co.replace('  oaResult,\n', '')
co = co.replace('  matchingResult,\n', '')
with open('frontend/src/pages/CaseOverview.tsx', 'w', encoding='utf-8') as f:
    f.write(co)

