import re
with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app = f.read()

app = app.replace('analysisId={analysisId}', 'onNavigate={handleNavigate as any}\n              analysisId={analysisId}')

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(app)
