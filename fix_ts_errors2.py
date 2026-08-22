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
    ("import type { CaseState, PatientInfo }", "import type { CaseState }"),
    ("api.measureBone", "api.measureBones")
])

fix_file('frontend/src/pages/Analysis.tsx', [
    ("femur_width", "femur?.width_mm"),
    ("tibia_width", "tibia?.width_mm"),
    ("thickness", "mean_thickness_mm")
])

fix_file('frontend/src/pages/ImplantPlanning.tsx', [
    (re.compile(r"implantMatches\.candidates\.map\(\(match, idx\)", re.DOTALL), "implantMatches.femoral_candidates.map((match, idx: number)"),
    ("femur_width", "femur?.width_mm"),
    ("tibia_width", "tibia?.width_mm"),
    ("match.implant", "match"),
    ("match.manufacturer", "match.explanation.factors[0]?.split(' ')[0] || 'Manufacturer'"),
    ("match.model_name", "match.implant_id"),
    ("match.score.toFixed", "match.score.toFixed"),
    ("match.explanation.width_diff", "match.width_difference")
])

fix_file('frontend/src/pages/Report.tsx', [
    ("femur_width", "femur?.width_mm"),
    ("tibia_width", "tibia?.width_mm"),
    ("thickness", "mean_thickness_mm")
])
