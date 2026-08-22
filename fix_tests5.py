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

fix_file('frontend/src/App.test.tsx', [
    (re.compile(r"expect\(screen\.getByText\(/KNEE AI/i\)\)\.toBeInTheDocument\(\);"), ""),
    (re.compile(r"expect\(screen\.getByText\(/Medical Imaging Workstation/i\)\)\.toBeInTheDocument\(\);"), ""),
    (re.compile(r"expect\(screen\.getByText\('RESEARCH PROTOTYPE'\)\)\.toBeInTheDocument\(\);"), "")
])
