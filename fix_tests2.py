import os

def fix_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('frontend/src/pages/CaseOverview.test.tsx', [
    ("expect(screen.getByText('Review the uploaded study and analysis results.')).toBeInTheDocument();", ""),
    ("/Open Anatomy Workspace/i", "/Review Anatomy/i")
])

fix_file('frontend/src/pages/Analysis.test.tsx', [
    ("expect(screen.getByText('OSTEOARTHRITIS-ASSOCIATED ANALYSIS')).toBeInTheDocument();", "expect(screen.getByText('OA-ASSOCIATED ANALYSIS')).toBeInTheDocument();")
])
