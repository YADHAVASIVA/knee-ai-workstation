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
    (re.compile(r"const preRes = await preprocessImage\(uploadRes\.id\);"), "const preRes = await preprocessImage(uploadRes.analysis_id);"),
    (re.compile(r"setImageMetadata\(preRes\.metadata \|\| null\);"), "const meta = await api.getImageMetadata(uploadRes.analysis_id);\\n      setImageMetadata(meta);"),
    (re.compile(r"const pUrl = getPreviewUrl\(uploadRes\.id\);"), "const pUrl = getPreviewUrl(uploadRes.analysis_id);")
])

fix_file('frontend/src/pages/CaseOverview.tsx', [
    (re.compile(r"pipeline\.map\(\(step, idx\) => \("), "pipeline.map((step) => (")
])
