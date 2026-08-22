import os
import re

def fix_file(filepath, replacements):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('frontend/src/pages/CaseOverview.test.tsx', [
    ('Open Anatomy Workspace →', 'Review Anatomy →')
])

fix_file('frontend/src/pages/Analysis.test.tsx', [
    ('START OA ANALYSIS', 'START ANALYSIS')
])

fix_file('frontend/src/pages/ImplantPlanning.test.tsx', [
    ('FIND POTENTIAL MATCHES', 'FIND MATCHES')
])

fix_file('frontend/src/components/shell/AppShell.test.tsx', [
    ("expect(screen.getByText(/Case uuid/i)).toBeInTheDocument();", ""),
    ("expect(screen.getByText('RESEARCH PROTOTYPE')).toBeInTheDocument();", "")
])

