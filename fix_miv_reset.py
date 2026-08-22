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

fix_file('frontend/src/components/MedicalImageViewer.tsx', [
    (re.compile(r"const containerRef = useRef<HTMLDivElement>\(null\);\n  const \[scale, setScale\] = useState\(1\);"), """const containerRef = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(1);
  React.useEffect(() => {
    if (activeTool === 'reset_trigger') {
      setScale(1);
      setPan({ x: 0, y: 0 });
      setBrightness(1);
      setContrast(1);
    }
  }, [activeTool]);""")
])
