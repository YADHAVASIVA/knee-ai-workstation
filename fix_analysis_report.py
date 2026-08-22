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
    ("interface AnalysisProps {", "interface AnalysisProps {\n  modality?: string;"),
    ("isProcessing: boolean;\n}) => {", "isProcessing: boolean;\n  modality?: string;\n}) => {"),
    (re.compile(r"<div className=\"analysis-measure-group\">\n.*?<h4>Meniscus \(Medial\)</h4>.*?</div>", re.DOTALL), lambda m: "{modality === 'MRI' && (\n" + m.group(0) + "\n)}")
])

fix_file('frontend/src/pages/Report.tsx', [
    ("interface ReportProps {", "interface ReportProps {\n  modality?: string;"),
    ("matchingResult: any;\n}) => {", "matchingResult: any;\n  modality?: string;\n}) => {"),
    (re.compile(r"<div>\n.*?<h3>Soft Tissue</h3>\n.*?<div className=\"report-grid\">\n.*?<span>Medial Meniscus:</span>\n.*?<span>\{meniscusMeasurement\?.+\}</span>\n.*?</div>\n.*?</div>", re.DOTALL), lambda m: "{modality === 'MRI' && (\n" + m.group(0) + "\n)}")
])
