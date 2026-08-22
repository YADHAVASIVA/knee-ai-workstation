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
    ("<TopBar activeRoute={activeRoute} analysisId={caseState.caseId} isDemo={true} isCalibrated={caseState.images.some(img => img.metadata?.pixel_spacing)} />", "<TopBar activeRoute={activeRoute} analysisId={caseState.caseId} patientName={caseState.patient.name} isDemo={true} isCalibrated={caseState.images.length > 0 ? caseState.images.some(img => img.metadata?.pixel_spacing) : null} />")
])
