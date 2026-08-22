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

fix_file('frontend/src/pages/Anatomy.tsx', [
    (re.compile(r"disabled title=\"Coming soon\""), ""),
    (re.compile(r"\(Coming soon\)"), ""),
    (re.compile(r"onClick=\{\(\) => setActiveTool\('select'\)\} disabled"), "onClick={() => setActiveTool('select')}"),
    (re.compile(r"onClick=\{\(\) => setActiveTool\('window'\)\} disabled"), "onClick={() => setActiveTool('window')}")
])
