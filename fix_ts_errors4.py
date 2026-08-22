import os

def fix_file(filepath, replacements):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('frontend/src/pages/ImplantPlanning.tsx', [
    ("match.implant.manufacturer", "'Generic Manufacturer'"),
    ("match.implant.model_name", "match.implant_id")
])
