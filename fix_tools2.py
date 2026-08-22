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
    (re.compile(r"<button className=\{na-tool-btn \$\{activeTool === 'select' \? 'active' : ''\}\} >"), "<button className={na-tool-btn } onClick={() => setActiveTool('select')}>"),
    (re.compile(r"<button className=\{na-tool-btn \$\{activeTool === 'window' \? 'active' : ''\}\} >"), "<button className={na-tool-btn } onClick={() => setActiveTool('window')}>")
])
