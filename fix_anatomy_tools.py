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
    (re.compile(r"import \{ Eye, EyeOff, MousePointer2, Move, ZoomIn, Contrast \} from 'lucide-react';"), "import { Eye, EyeOff, MousePointer2, Move, ZoomIn, Contrast, RefreshCcw, Maximize } from 'lucide-react';"),
    (re.compile(r"<button className=\{`ana-tool-btn \$\{activeTool === 'window' \? 'active' : ''\}`\} onClick=\{\(\) => setActiveTool\('window'\)\} title=\"Window/Level\"><Contrast size=\{18\} /></button>"), """<button className={`ana-tool-btn ${activeTool === 'window' ? 'active' : ''}`} onClick={() => setActiveTool('window')} title="Window/Level"><Contrast size={18} /></button>
            <div style={{width: '1px', background: 'rgba(255,255,255,0.2)', margin: '0 4px'}}></div>
            <button className="ana-tool-btn" onClick={() => { setActiveTool('reset_trigger'); setTimeout(() => setActiveTool('select'), 50); }} title="Reset"><RefreshCcw size={18} /></button>""")
])
