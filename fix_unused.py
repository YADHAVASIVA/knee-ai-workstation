import os

# Fix App.tsx
with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app = f.read()
app = app.replace('patientData={patientData}\n', '')
app = app.replace('oaResult={oaResult}\n', '')
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

# Fix CaseOverview.tsx
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

