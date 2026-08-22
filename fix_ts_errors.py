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

fix_file('frontend/src/types/case.ts', [
    ("import { ImageMetadata", "import type { ImageMetadata")
])

fix_file('frontend/src/App.tsx', [
    ("import { CaseState, PatientInfo }", "import type { CaseState, PatientInfo }"),
    ("import { useState, useCallback }", "import { useState }"),
    ("api.measureBones", "api.measureBone"),
    (re.compile(r"category: string; disabled\?: boolean \| undefined;"), "")
])

fix_file('frontend/src/pages/Analysis.tsx', [
    ("import { CaseState, CaseImage }", "import type { CaseState, CaseImage }"),
    ("femur_width_mm", "femur_width"),
    ("tibia_width_mm", "tibia_width"),
    ("thickness_mm", "thickness")
])

fix_file('frontend/src/pages/Anatomy.tsx', [
    ("import { CaseImage }", "import type { CaseImage }"),
    (re.compile(r"\{ id: 'femur', url: getMaskUrl\(activeImage\.id, 'femur'\), visible: true, name: 'Femur' \}"), "{ id: 'femur', url: getMaskUrl(activeImage.id, 'femur'), visible: true, name: 'Femur', color: '#3b82f6' }"),
    (re.compile(r"\{ id: 'tibia', url: getMaskUrl\(activeImage\.id, 'tibia'\), visible: true, name: 'Tibia' \}"), "{ id: 'tibia', url: getMaskUrl(activeImage.id, 'tibia'), visible: true, name: 'Tibia', color: '#10b981' }"),
    (re.compile(r"\{ id: 'meniscus', url: getMaskUrl\(activeImage\.id, 'medial_meniscus'\), visible: true, name: 'Meniscus' \}"), "{ id: 'meniscus', url: getMaskUrl(activeImage.id, 'medial_meniscus'), visible: true, name: 'Meniscus', color: '#f59e0b' }"),
    ("activeImage.measurements.meniscus?.measurements", "activeImage.measurements.meniscus?.locations")
])

fix_file('frontend/src/pages/CaseOverview.tsx', [
    ("import { PatientInfo }", "import type { PatientInfo }")
])

fix_file('frontend/src/pages/ImagingStudies.tsx', [
    ("import { CaseImage }", "import type { CaseImage }"),
    ("Upload, X, FileImage", "X, FileImage"),
    ("variant=\"outline\"", "variant=\"secondary\"")
])

fix_file('frontend/src/pages/ImplantPlanning.tsx', [
    ("import { CaseState }", "import type { CaseState }"),
    ("implantMatches.matches", "implantMatches.candidates"),
    ("femur_width_mm", "femur_width"),
    ("tibia_width_mm", "tibia_width"),
    ("match.component", "match.implant"),
    ("match.explanation.final_score", "match.score"),
    ("match.explanation.width_error_mm", "match.explanation.width_diff")
])

fix_file('frontend/src/pages/Report.tsx', [
    ("import { CaseState, CaseImage }", "import type { CaseState, CaseImage }"),
    ("femur_width_mm", "femur_width"),
    ("tibia_width_mm", "tibia_width"),
    ("thickness_mm", "thickness"),
    ("variant=\"outline\"", "variant=\"secondary\"")
])
