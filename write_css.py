import os

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

write_file('frontend/src/styles/tokens.css', '''
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  /* CLINICAL WORKSPACE (LIGHT) */
  --light-bg: #F5F7F9;
  --light-surface: #FFFFFF;
  --light-border: #E8EEF2;
  --light-text: #1C2329;
  --light-text-secondary: #576573;
  --light-text-muted: #8696A7;

  /* IMAGING WORKSTATION (DARK) */
  --dark-bg: #050709;
  --dark-surface: #0B0F12;
  --dark-border: #182026;
  --dark-text: #F0F4F8;
  --dark-text-secondary: #99A8B6;
  
  /* SHELL (DARK) */
  --shell-bg: #030406;
  --shell-border: #131A20;
  --shell-text: #D5DFE8;
  
  /* BRAND COLORS */
  --color-primary: #0F766E;
  --color-primary-hover: #115E59;
  
  /* TYPOGRAPHY */
  --font-sans: 'Inter', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  
  /* SPACING - 8px Grid */
  --space-4: 4px;
  --space-8: 8px;
  --space-16: 16px;
  --space-24: 24px;
  --space-32: 32px;
  --space-48: 48px;
  --space-64: 64px;
}
''')

write_file('frontend/src/components/shell/shell.css', '''
.app-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  background-color: var(--shell-bg);
  color: var(--shell-text);
  font-family: var(--font-sans);
  overflow: hidden;
}

.app-sidebar {
  width: 240px;
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--shell-border);
  background-color: var(--shell-bg);
  flex-shrink: 0;
}

.sidebar-brand {
  padding: var(--space-24);
  border-bottom: 1px solid var(--shell-border);
}

.brand-title {
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: #FFFFFF;
}

.brand-subtitle {
  font-size: 11px;
  color: var(--dark-text-secondary);
  margin-top: var(--space-4);
  text-transform: uppercase;
}

.sidebar-nav {
  flex: 1;
  padding: var(--space-24) 0;
  overflow-y: auto;
}

.nav-section {
  margin-bottom: var(--space-24);
}

.nav-section-title {
  font-size: 11px;
  font-weight: 600;
  color: var(--dark-text-secondary);
  padding: 0 var(--space-24);
  margin-bottom: var(--space-8);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-btn {
  width: 100%;
  text-align: left;
  background: none;
  border: none;
  padding: var(--space-8) var(--space-24);
  color: var(--shell-text);
  font-size: 13px;
  font-family: var(--font-sans);
  cursor: pointer;
  display: flex;
  align-items: center;
  border-left: 2px solid transparent;
}

.nav-btn:hover:not(:disabled) {
  background-color: rgba(255,255,255,0.02);
}

.nav-btn.active {
  background-color: rgba(15, 118, 110, 0.1);
  border-left-color: var(--color-primary);
  color: #FFFFFF;
  font-weight: 500;
}

.nav-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.sidebar-case-context {
  padding: var(--space-24);
  border-top: 1px solid var(--shell-border);
  background-color: rgba(255,255,255,0.01);
}

.case-context-title {
  font-size: 10px;
  color: var(--dark-text-secondary);
  margin-bottom: var(--space-8);
}

.case-context-id {
  font-family: var(--font-mono);
  font-size: 13px;
  color: #FFFFFF;
  margin-bottom: var(--space-4);
}

.case-context-meta {
  font-size: 11px;
  color: var(--dark-text-secondary);
}

.app-main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.app-topbar {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-24);
  border-bottom: 1px solid var(--shell-border);
  background-color: var(--shell-bg);
  flex-shrink: 0;
}

.topbar-left, .topbar-right {
  display: flex;
  align-items: center;
  gap: var(--space-16);
}

.topbar-brand {
  font-weight: 600;
  color: #FFFFFF;
  font-size: 13px;
}

.breadcrumb-slash {
  color: var(--dark-text-secondary);
  font-size: 13px;
}

.topbar-route {
  color: var(--shell-text);
  font-size: 13px;
}

.topbar-meta {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--dark-text-secondary);
}

.topbar-divider {
  width: 1px;
  height: 16px;
  background-color: var(--shell-border);
}

.topbar-demo-badge {
  background-color: rgba(124, 58, 237, 0.15);
  color: #A78BFA;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.05em;
}

.app-main-content {
  flex: 1;
  overflow: auto;
  position: relative;
}

.workspace-light {
  background-color: var(--light-bg);
  color: var(--light-text);
}

.workspace-dark {
  background-color: var(--dark-bg);
  color: var(--dark-text);
}

.content-container {
  height: 100%;
}
''')

write_file('frontend/src/pages/CaseOverview.css', '''
.co-page {
  padding: var(--space-48);
  max-width: 1200px;
  margin: 0 auto;
}

.co-intake-workspace {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
}

.co-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--light-text);
  margin: 0 0 var(--space-8) 0;
  letter-spacing: -0.02em;
}

.co-subtitle {
  font-size: 14px;
  color: var(--light-text-secondary);
  margin: 0 0 var(--space-48) 0;
}

.co-dropzone {
  border: 1px dashed var(--light-border-strong, #D1D5DB);
  background-color: var(--light-surface);
  padding: var(--space-64) var(--space-48);
  border-radius: 8px;
  cursor: pointer;
  width: 100%;
  max-width: 600px;
  transition: all 0.2s;
}

.co-dropzone:hover {
  border-color: var(--color-primary);
  background-color: #F8FAFC;
}

.co-drop-title {
  font-size: 16px;
  font-weight: 500;
  color: var(--light-text);
  margin-bottom: var(--space-8);
}

.co-drop-subtitle {
  font-size: 14px;
  color: var(--color-primary);
  margin-bottom: var(--space-16);
}

.co-drop-meta {
  font-size: 12px;
  color: var(--light-text-muted);
}

.co-dashboard {
  width: 100%;
}

.co-header {
  display: flex;
  align-items: center;
  gap: var(--space-16);
  margin-bottom: var(--space-32);
}

.co-header-meta {
  display: flex;
  align-items: center;
  gap: var(--space-8);
  color: var(--light-text-secondary);
  font-size: 14px;
}

.mono {
  font-family: var(--font-mono);
}

.co-grid {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: var(--space-32);
  align-items: start;
}

.co-image-preview {
  background-color: var(--dark-bg);
  border: 1px solid var(--light-border);
  border-radius: 4px;
  overflow: hidden;
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.co-image-preview img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.co-placeholder {
  color: var(--dark-text-secondary);
  font-size: 14px;
}

.co-panel {
  background-color: var(--light-surface);
  border: 1px solid var(--light-border);
  padding: var(--space-24);
}

.co-panel-title {
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--light-text);
  margin: 0 0 var(--space-16) 0;
  letter-spacing: 0.05em;
  border-bottom: 1px solid var(--light-border);
  padding-bottom: var(--space-8);
}

.co-info-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-12);
}

.co-info-item {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.co-info-label {
  color: var(--light-text-secondary);
}

.co-info-val {
  font-weight: 500;
  color: var(--light-text);
}

.co-pipeline-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
}

.co-pipe-item {
  display: flex;
  align-items: center;
  gap: var(--space-12);
  padding: var(--space-12);
  background-color: var(--light-bg);
  border: 1px solid var(--light-border);
  opacity: 0.6;
}

.co-pipe-item.active {
  opacity: 1;
  background-color: #FFFFFF;
  border-left: 3px solid var(--color-primary);
}

.co-pipe-num {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--light-text-muted);
}

.co-pipe-name {
  flex: 1;
  font-size: 13px;
  font-weight: 500;
}

.co-pipe-state {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
}

.co-pipe-state.complete { color: #16A34A; }
.co-pipe-state.running { color: #2563EB; }
.co-pipe-state.ready { color: var(--color-primary); }
.co-pipe-state.waiting { color: var(--light-text-muted); }

.mt-6 { margin-top: var(--space-24); }
''')

write_file('frontend/src/pages/Anatomy.css', '''
.ana-workstation {
  display: flex;
  height: 100%;
  width: 100%;
  background-color: var(--dark-bg);
  color: var(--dark-text);
}

.ana-sidebar {
  width: 280px;
  background-color: var(--dark-surface);
  border-right: 1px solid var(--dark-border);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  overflow-y: auto;
}

.ana-sidebar-right {
  border-right: none;
  border-left: 1px solid var(--dark-border);
}

.ana-panel {
  border-bottom: 1px solid var(--dark-border);
}

.ana-panel-header {
  padding: var(--space-16);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.05em;
  color: var(--dark-text-secondary);
  text-transform: uppercase;
}

.ana-layer-list, .ana-measure-controls, .ana-measure-summary {
  padding: 0 var(--space-16) var(--space-16);
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
}

.ana-layer-item {
  display: flex;
  align-items: center;
  gap: var(--space-8);
  font-size: 13px;
  color: var(--dark-text);
  cursor: pointer;
}

.ana-layer-status {
  margin-left: auto;
  font-size: 11px;
  color: var(--dark-text-secondary);
}

.ana-tool-list {
  padding: 0 var(--space-16) var(--space-16);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.ana-tool-btn {
  background: transparent;
  border: 1px solid var(--dark-border);
  color: var(--dark-text);
  padding: var(--space-8);
  font-size: 12px;
  text-align: left;
  cursor: pointer;
}

.ana-tool-btn:hover:not(:disabled) {
  background-color: rgba(255,255,255,0.05);
}

.ana-tool-btn.active {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
  color: #FFF;
}

.ana-tool-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.ana-viewer-container {
  flex: 1;
  position: relative;
  background-color: var(--dark-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 0;
}

.ana-empty {
  color: var(--dark-text-secondary);
  font-size: 14px;
}

.ana-findings-list {
  padding: 0 var(--space-16) var(--space-16);
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
}

.ana-finding-item {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  padding: var(--space-8);
  background-color: rgba(255,255,255,0.02);
  border: 1px solid var(--dark-border);
}

.ana-finding-status {
  color: #10B981;
  font-size: 11px;
  text-transform: uppercase;
}

.ana-summary-item {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  padding: var(--space-4) 0;
  border-bottom: 1px dashed var(--dark-border);
}

.ana-summary-label {
  color: var(--dark-text-secondary);
}
''')

write_file('frontend/src/pages/Analysis.css', '''
.analysis-page, .planning-page {
  padding: var(--space-48);
  max-width: 1200px;
  margin: 0 auto;
}

.analysis-header, .planning-header {
  margin-bottom: var(--space-48);
}

.analysis-title, .planning-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--light-text);
  margin: 0 0 var(--space-8) 0;
  letter-spacing: -0.02em;
}

.analysis-empty, .planning-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
}

.analysis-workspace, .planning-workspace {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: var(--space-48);
  align-items: start;
}

.analysis-section, .planning-section {
  background-color: var(--light-surface);
  border: 1px solid var(--light-border);
  padding: var(--space-24);
  margin-bottom: var(--space-24);
}

.analysis-section-title, .planning-section-title {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--light-text);
  margin: 0 0 var(--space-24) 0;
  letter-spacing: 0.05em;
  border-bottom: 1px solid var(--light-border);
  padding-bottom: var(--space-8);
}

.analysis-metric-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-12);
}

.analysis-metric {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.analysis-metric-label {
  color: var(--light-text-secondary);
}

.analysis-metric-value {
  font-weight: 500;
}

.analysis-measure-group, .planning-measure-group {
  margin-bottom: var(--space-24);
}

.analysis-measure-group h4, .planning-measure-group h4 {
  font-size: 12px;
  color: var(--light-text-secondary);
  margin: 0 0 var(--space-8) 0;
}

.analysis-measure-row, .planning-measure-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  padding: var(--space-4) 0;
  border-bottom: 1px dashed var(--light-border);
}

.analysis-prototype-warning, .planning-demo-warning {
  background-color: #FEF3C7;
  border: 1px solid #F59E0B;
  padding: var(--space-16);
  color: #92400E;
  font-size: 13px;
}

.analysis-prototype-warning strong, .planning-demo-warning strong {
  display: block;
  font-size: 11px;
  text-transform: uppercase;
  margin-bottom: var(--space-4);
  letter-spacing: 0.05em;
}

.comparison-track {
  display: flex;
  align-items: center;
  gap: var(--space-16);
  padding: var(--space-32) 0;
}

.comp-label {
  font-size: 12px;
  color: var(--light-text-muted);
}

.comp-line {
  flex: 1;
  height: 2px;
  background-color: var(--light-border-strong, #D1D5DB);
  position: relative;
}

.comp-marker {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  color: var(--color-primary);
  font-size: 18px;
}

.comp-marker-label {
  position: absolute;
  top: 15px;
  transform: translateX(-50%);
  font-size: 12px;
  font-weight: 600;
  color: var(--color-primary);
  text-align: center;
}
''')

write_file('frontend/src/pages/ImplantPlanning.css', '''
.planning-matches-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-16);
}

.planning-match-card {
  border: 1px solid var(--light-border);
  padding: var(--space-16);
  background-color: var(--light-bg);
  display: flex;
  gap: var(--space-16);
}

.match-rank {
  font-weight: 600;
  font-size: 14px;
  color: var(--color-primary);
  width: 60px;
}

.match-details {
  flex: 1;
}

.match-name {
  font-weight: 500;
  font-size: 15px;
  color: var(--light-text);
}

.match-comparison {
  background-color: #FFF;
  padding: var(--space-12);
  border: 1px solid var(--light-border);
}

.match-comp-row {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  padding: 2px 0;
}

.match-comp-row.border-top {
  border-top: 1px dashed var(--light-border);
  margin-top: 4px;
  padding-top: 4px;
  font-weight: 500;
}

.match-comp-label {
  color: var(--light-text-secondary);
}

.match-score {
  font-size: 12px;
  font-weight: 600;
  color: #16A34A;
  text-align: right;
}
''')

write_file('frontend/src/pages/Report.css', '''
.report-workspace {
  padding: var(--space-48);
  max-width: 800px;
  margin: 0 auto;
}

.report-controls {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--space-32);
}

.report-document {
  background-color: #FFF;
  border: 1px solid var(--light-border-strong, #D1D5DB);
  padding: var(--space-64);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.report-header {
  border-bottom: 2px solid var(--light-text);
  padding-bottom: var(--space-16);
  margin-bottom: var(--space-32);
}

.report-header h1 {
  margin: 0;
  font-size: 24px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.report-section {
  margin-bottom: var(--space-32);
}

.report-section h2 {
  font-size: 14px;
  color: var(--light-text-secondary);
  border-bottom: 1px solid var(--light-border);
  padding-bottom: var(--space-8);
  margin-bottom: var(--space-16);
}

.report-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-16);
  font-size: 13px;
}

.report-grid-3 {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: var(--space-16);
  font-size: 13px;
}

.report-grid-3 h3 {
  font-size: 13px;
  margin: 0 0 var(--space-8) 0;
}

.report-warning {
  margin-top: var(--space-64);
  border: 2px solid #000;
  padding: var(--space-16);
  text-align: center;
}

.report-warning strong {
  font-size: 16px;
  text-transform: uppercase;
  display: block;
  margin-bottom: var(--space-8);
}

@media print {
  .app-sidebar, .app-topbar, .report-controls {
    display: none !important;
  }
  .app-main-content {
    background: #FFF;
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    padding: 0;
  }
  .report-workspace {
    padding: 0;
    max-width: none;
  }
  .report-document {
    box-shadow: none;
    border: none;
    padding: 0;
  }
}
''')

