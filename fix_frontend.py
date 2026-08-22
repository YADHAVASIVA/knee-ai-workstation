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
    (re.compile(r"const newOverlays = \[\n          \{ id: 'femur',.*?url: getMaskUrl\(analysisId, 'femur'\) \},\n          \{ id: 'tibia',.*?url: getMaskUrl\(analysisId, 'tibia'\) \},\n          \{ id: 'meniscus',.*?url: getMaskUrl\(analysisId, 'medial_meniscus'\) \}\n        \];"), """const newOverlays = [
          { id: 'femur', name: 'Femur', visible: true, color: '#3b82f6', url: getMaskUrl(analysisId, 'femur') },
          { id: 'tibia', name: 'Tibia', visible: true, color: '#10b981', url: getMaskUrl(analysisId, 'tibia') }
        ];
        if (imageMetadata?.modality === 'MRI') {
          newOverlays.push({ id: 'meniscus', name: 'Meniscus', visible: true, color: '#f59e0b', url: getMaskUrl(analysisId, 'medial_meniscus') });
        }"""),
    (re.compile(r"<Anatomy \n.*?/>", re.DOTALL), lambda m: m.group(0).replace("/>", "  modality={imageMetadata?.modality || 'UNKNOWN'}\n          />")),
    (re.compile(r"<Analysis \n.*?/>", re.DOTALL), lambda m: m.group(0).replace("/>", "  modality={imageMetadata?.modality || 'UNKNOWN'}\n          />")),
    (re.compile(r"<Report \n.*?/>", re.DOTALL), lambda m: m.group(0).replace("/>", "  modality={imageMetadata?.modality || 'UNKNOWN'}\n          />"))
])

fix_file('frontend/src/pages/Anatomy.tsx', [
    ("interface AnatomyProps {", "interface AnatomyProps {\n  modality?: string;"),
    ("onToggleBoneMeasurements: (show: boolean) => void;\n}) => {", "onToggleBoneMeasurements: (show: boolean) => void;\n  modality?: string;\n}) => {"),
    (re.compile(r"<div className=\"ana-layer-item\" onClick=\{\(\) => onToggleMeasurements\(!showMeasurements\)\}>\n.*?<span>Meniscus</span>\n              </div>", re.DOTALL), "{modality === 'MRI' && (\n              <div className=\"ana-layer-item\" onClick={() => onToggleMeasurements(!showMeasurements)}>\n                <button className=\"ana-layer-toggle\">\n                  {showMeasurements ? <Eye size={16} className=\"text-success\" /> : <EyeOff size={16} className=\"text-muted\" />}\n                </button>\n                <span>Meniscus</span>\n              </div>\n            )}")
])
