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

fix_file('frontend/src/pages/Analysis.tsx', [
    (re.compile(r"age: parseInt\(caseState\.patient\.age\) \|\| 45,"), "age: parseInt(caseState.patient.age),"),
    (re.compile(r"sex: caseState\.patient\.sex \|\| 'Unknown',"), "sex: caseState.patient.sex || 'Not provided',"),
    (re.compile(r"<Button onClick=\{handleRunOaAnalysis\}>Run Case OA Analysis</Button>"), """{caseState.patient.age && caseState.patient.sex ? (
                  <Button onClick={handleRunOaAnalysis}>Run Case OA Analysis</Button>
                ) : (
                  <div className="an-warning-box">Patient age and sex are required to run OA-associated analysis. Please update them in the Case Overview.</div>
                )}""")
])

fix_file('frontend/src/pages/Analysis.css', [
    (".an-actions {", ".an-warning-box { padding: 12px; background: var(--color-bg); border-left: 4px solid var(--color-warning); color: var(--color-text-secondary); font-size: 13px; text-align: left; margin-top: 16px; }\n.an-actions {")
])

fix_file('frontend/src/pages/Anatomy.tsx', [
    (re.compile(r"color: '#[0-9a-fA-F]+'"), "color: 'var(--color-primary)'"),
    (re.compile(r"className=.text-success."), "style={{color: 'var(--color-success)'}}"),
    (re.compile(r"className=.text-muted."), "style={{color: 'var(--color-text-muted)'}}")
])

