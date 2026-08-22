import os

def fix_file(filepath, replacements):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

step_indicator_component = """
const StepIndicator = ({ activeRoute }: { activeRoute: string }) => {
  const steps = [
    { id: 'overview', label: '01 Overview' },
    { id: 'imaging', label: '02 Imaging' },
    { id: 'anatomy', label: '03 Anatomy' },
    { id: 'analysis', label: '04 Analysis' },
    { id: 'planning', label: '05 Planning' },
    { id: 'report', label: '06 Report' }
  ];
  
  const activeIdx = steps.findIndex(s => s.id === activeRoute);
  
  return (
    <div className="step-indicator">
      {steps.map((s, idx) => (
        <React.Fragment key={s.id}>
          <span className={`step-item ${idx === activeIdx ? 'active' : idx < activeIdx ? 'completed' : 'locked'}`}>
            {s.label}
          </span>
          {idx < steps.length - 1 && <span className="step-arrow">&rarr;</span>}
        </React.Fragment>
      ))}
    </div>
  );
};
"""

fix_file('frontend/src/App.tsx', [
    ("import { useState } from 'react';", "import React, { useState } from 'react';"),
    ("function App() {", step_indicator_component + "\nfunction App() {"),
    ("<ErrorBoundary>", "<StepIndicator activeRoute={activeRoute} />\n          <ErrorBoundary>")
])

fix_file('frontend/src/components/shell/shell.css', [
    ("/* Add shell styles here */", """
.step-indicator {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 32px;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary);
}
.step-item {
  padding: 4px 8px;
  border-radius: 4px;
}
.step-item.active {
  color: var(--color-primary);
  background: var(--color-primary-soft);
  font-weight: 600;
}
.step-item.completed {
  color: var(--color-text);
}
.step-item.locked {
  opacity: 0.5;
}
.step-arrow {
  color: var(--color-border);
}
.topbar-case-id { font-size: 15px; font-weight: 600; margin: 0; color: var(--color-text); }
.topbar-patient-name { font-size: 14px; color: var(--color-text-secondary); }
.topbar-route-name { font-size: 13px; font-weight: 600; letter-spacing: 0.5px; color: var(--color-primary); }
.topbar-meta.calibrated { color: var(--color-success); display: flex; align-items: center; gap: 4px; font-weight: 600; }
""")
])
