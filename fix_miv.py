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
    (re.compile(r"onToggleBoneMeasurements\?: \(show: boolean\) => void;\n\}"), "onToggleBoneMeasurements?: (show: boolean) => void;\n  activeTool?: string;\n}"),
    (re.compile(r"showBoneMeasurements = true,\n\}\) => \{"), "showBoneMeasurements = true,\n  activeTool = 'pan',\n}) => {"),
    (re.compile(r"const \[opacity, setOpacity\] = useState\(0\.7\);"), "const [opacity, setOpacity] = useState(0.7);\n  const [brightness, setBrightness] = useState(1);\n  const [contrast, setContrast] = useState(1);"),
    (re.compile(r"const handlePointerMove = \(e: React\.PointerEvent\) => \{\n    if \(!isDragging\) return;\n    const dx = e\.clientX - lastPos\.x;\n    const dy = e\.clientY - lastPos\.y;\n    setPan\(prev => \(\{ x: prev\.x \+ dx, y: prev\.y \+ dy \}\)\);\n    setLastPos\(\{ x: e\.clientX, y: e\.clientY \}\);\n  \};"), """const handlePointerMove = (e: React.PointerEvent) => {
    if (!isDragging) return;
    const dx = e.clientX - lastPos.x;
    const dy = e.clientY - lastPos.y;
    
    if (activeTool === 'pan') {
      setPan(prev => ({ x: prev.x + dx, y: prev.y + dy }));
    } else if (activeTool === 'zoom') {
      const zoomSensitivity = 0.01;
      setScale(prev => Math.min(Math.max(prev - dy * zoomSensitivity, 0.25), 4));
    } else if (activeTool === 'window') {
      const sensitivity = 0.005;
      setContrast(prev => Math.max(prev + dx * sensitivity, 0.1));
      setBrightness(prev => Math.max(prev - dy * sensitivity, 0.1));
    }
    
    setLastPos({ x: e.clientX, y: e.clientY });
  };"""),
    (re.compile(r"const handleReset = \(\) => \{\n    setScale\(1\);\n    setPan\(\{ x: 0, y: 0 \}\);\n  \};"), "const handleReset = () => {\n    setScale(1);\n    setPan({ x: 0, y: 0 });\n    setBrightness(1);\n    setContrast(1);\n  };"),
    (re.compile(r"className=\"miv-base-image\" draggable=\{false\} />"), "className=\"miv-base-image\" draggable={false} style={{ filter: rightness() contrast() }} />"),
    (re.compile(r"style=\{\{ opacity: opacity \}\}\n                draggable=\{false\}"), "style={{ opacity: opacity, filter: rightness() contrast() }}\n                draggable={false}")
])

fix_file('frontend/src/pages/Anatomy.tsx', [
    (re.compile(r"boneResult=\{showBoneMeasurements \? boneMeasurement : null\}\n          />"), "boneResult={showBoneMeasurements ? boneMeasurement : null}\n            activeTool={activeTool}\n          />")
])
