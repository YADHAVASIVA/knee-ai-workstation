import os
with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('patientData={patientData}', '')
content = content.replace('oaResult={oaResult}', '')
with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
