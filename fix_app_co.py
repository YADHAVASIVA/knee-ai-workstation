import os

def fix_file(filepath, replacements):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('frontend/src/App.tsx', [
    ("<CaseOverview \n            patient={caseState.patient}\n            onChange={(p) => setCaseState(prev => ({ ...prev, patient: p }))}\n            onNext={() => setActiveRoute('imaging')}\n          />", "<CaseOverview patient={caseState.patient} caseId={caseState.caseId} onChange={(p) => setCaseState(prev => ({ ...prev, patient: p }))} onNext={() => setActiveRoute('imaging')} />")
])
