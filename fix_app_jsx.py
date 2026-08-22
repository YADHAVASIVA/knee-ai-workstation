import re
with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app = f.read()

# Fix Report block
report_block = re.search(r'<Report\s+.*?\s*/>', app, re.DOTALL).group(0)
new_report_block = re.sub(r'\s*patientData=\{patientData\}', '', report_block)
new_report_block = re.sub(r'\s*oaResult=\{oaResult\}', '', new_report_block)
new_report_block = re.sub(r'\s*onPrint=\{\(\) => window\.print\(\)\}', '', new_report_block)
app = app.replace(report_block, new_report_block)

# Fix CaseOverview block
co_block = re.search(r'<CaseOverview\s+.*?\s*/>', app, re.DOTALL).group(0)
new_co_block = re.sub(r'\s*patientData=\{patientData\}', '', co_block)
new_co_block = re.sub(r'\s*segmentationResult=\{segmentationResult\}', '', new_co_block)
new_co_block = re.sub(r'\s*boneMeasurement=\{boneMeasurement\}', '', new_co_block)
new_co_block = re.sub(r'\s*meniscusMeasurement=\{meniscusMeasurement\}', '', new_co_block)
new_co_block = re.sub(r'\s*oaResult=\{oaResult\}', '', new_co_block)
new_co_block = re.sub(r'\s*matchingResult=\{matchingResult\}', '', new_co_block)
app = app.replace(co_block, new_co_block)

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(app)
