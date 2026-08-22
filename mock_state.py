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
    (re.compile(r"workflowState: WorkflowState.IDLE,"), "workflowState: WorkflowState.MATCHING_COMPLETE,"),
    (re.compile(r"analysisId: null,"), "analysisId: '62650854-c46f-43ba-bb5d-88a8d5665d34',")
])
