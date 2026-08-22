import os
import re

def fix_file(filepath, replacements):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in replacements:
        if isinstance(old, re.Pattern):
            content = old.sub(new, content)
        else:
            content = content.replace(old, new)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('frontend/src/App.tsx', [
    ("api.measureBones", "api.measureBoneAnatomy"),
    ("{ id: 'overview', label: 'Overview', icon: 'FileText' }", "{ id: 'overview', label: 'Overview', icon: 'FileText', category: 'main' }"),
    ("{ id: 'imaging', label: 'Imaging', icon: 'Image' }", "{ id: 'imaging', label: 'Imaging', icon: 'Image', category: 'main' }"),
    ("{ id: 'anatomy', label: 'Anatomy', icon: 'Layers' }", "{ id: 'anatomy', label: 'Anatomy', icon: 'Layers', category: 'main' }"),
    ("{ id: 'analysis', label: 'Analysis', icon: 'Activity' }", "{ id: 'analysis', label: 'Analysis', icon: 'Activity', category: 'main' }"),
    ("{ id: 'planning', label: 'Planning', icon: 'Crosshair' }", "{ id: 'planning', label: 'Planning', icon: 'Crosshair', category: 'main' }"),
    ("{ id: 'report', label: 'Report', icon: 'FileOutput' }", "{ id: 'report', label: 'Report', icon: 'FileOutput', category: 'main' }"),
    (re.compile(r"<TopBar.*?/>", re.DOTALL), "<TopBar activeRoute={activeRoute} analysisId={caseState.caseId} isDemo={true} isCalibrated={caseState.images.some(img => img.metadata?.pixel_spacing)} />"),
    (re.compile(r"<Sidebar \n        activeRoute=\{activeRoute\} \n        onNavigate=\{\(route\) => setActiveRoute\(route as AppRoute\)\}\n        routes=\{navItems\}\n      />"), "<Sidebar activeRoute={activeRoute} analysisId={caseState.caseId} onNavigate={(route) => setActiveRoute(route as AppRoute)} routes={navItems as any} />")
])

fix_file('frontend/src/pages/ImplantPlanning.tsx', [
    ("match.explanation.factors[0]?.split(' ')[0] || 'Manufacturer'", "match.implant.manufacturer"),
    ("match.implant_id", "match.implant.model_name")
])
