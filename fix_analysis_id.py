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

fix_file('frontend/src/hooks/useAnalysisWorkflow.ts', [
    (re.compile(r"analysisId,\n    workflowState,"), "analysisId,\n    setAnalysisId,\n    workflowState,")
])

fix_file('frontend/src/App.tsx', [
    (re.compile(r"const \{ \n    analysisId, workflowState, setWorkflowState"), "const { \n    analysisId, setAnalysisId, workflowState, setWorkflowState"),
    (re.compile(r"setUploadData\(uploadRes\);\n"), "setUploadData(uploadRes);\n      setAnalysisId(uploadRes.image_id);\n")
])
