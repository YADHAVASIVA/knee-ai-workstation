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

fix_file('backend/tests/test_measurements.py', [
    (re.compile(r"client\.post\(f\"/api/v1/images/preprocess/\{image_id\}\"\)"), """client.post(f"/api/v1/images/preprocess/{image_id}")
    import json
    from app.core.config import settings
    meta_path = os.path.join(settings.UPLOAD_DIR, f"{image_id}_meta.json")
    with open(meta_path, "r") as f:
        meta = json.load(f)
    meta["modality"] = "MRI"
    with open(meta_path, "w") as f:
        json.dump(meta, f)""")
])

fix_file('backend/tests/test_oa_analysis.py', [
    (re.compile(r"client\.post\(f\"/api/v1/images/preprocess/\{image_id\}\"\)"), """client.post(f"/api/v1/images/preprocess/{image_id}")
    import json
    from app.core.config import settings
    meta_path = os.path.join(settings.UPLOAD_DIR, f"{image_id}_meta.json")
    with open(meta_path, "r") as f:
        meta = json.load(f)
    meta["modality"] = "MRI"
    with open(meta_path, "w") as f:
        json.dump(meta, f)""")
])
