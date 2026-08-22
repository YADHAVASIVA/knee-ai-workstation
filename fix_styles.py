import os
import re

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

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
  width: 260px;
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

.brand-logo {
  display: flex;
  align-items: center;
  gap: var(--space-12);
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
  margin-top: 2px;
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
  padding: var(--space-12) var(--space-24);
  color: var(--shell-text);
  font-size: 14px;
  font-family: var(--font-sans);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  border-left: 3px solid transparent;
  transition: all 0.2s;
}

.nav-btn:hover:not(:disabled) {
  background-color: rgba(255,255,255,0.02);
  color: #FFFFFF;
}

.nav-btn.active {
  background-color: rgba(15, 118, 110, 0.1);
  border-left-color: var(--color-primary);
  color: #FFFFFF;
  font-weight: 500;
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.8;
  width: 20px;
}

.nav-btn.active .nav-icon {
  opacity: 1;
  color: var(--color-primary);
}

.nav-label {
  flex: 1;
}

.nav-btn:disabled {
  opacity: 0.3;
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
  font-weight: 600;
}

.case-context-id {
  font-family: var(--font-mono);
  font-size: 14px;
  color: #FFFFFF;
  margin-bottom: var(--space-4);
}

.case-context-meta {
  font-size: 12px;
  color: var(--dark-text-secondary);
  margin-bottom: var(--space-8);
}

.case-context-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
}

.case-context-status.success { color: #10B981; }
.case-context-status.warning { color: #F59E0B; }

.app-main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.app-topbar {
  height: 60px;
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
  gap: 16px;
}

.topbar-brand {
  font-weight: 600;
  color: #FFFFFF;
  font-size: 14px;
}

.breadcrumb-slash {
  color: var(--dark-text-secondary);
  display: flex;
  align-items: center;
}

.topbar-route {
  color: var(--shell-text);
  font-size: 14px;
  font-weight: 500;
}

.topbar-meta {
  font-size: 13px;
  color: var(--dark-text-secondary);
}

.topbar-meta.mono {
  font-family: var(--font-mono);
}

.topbar-divider {
  width: 1px;
  height: 20px;
  background-color: var(--shell-border);
  margin: 0 4px;
}

.topbar-demo-badge {
  background-color: rgba(124, 58, 237, 0.15);
  color: #A78BFA;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.05em;
}

.topbar-icon-btn {
  background: none;
  border: none;
  color: var(--dark-text-secondary);
  cursor: pointer;
  padding: var(--space-4);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.topbar-icon-btn:hover {
  color: #FFFFFF;
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
  padding: var(--space-64) var(--space-48);
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
  font-size: 28px;
  font-weight: 700;
  color: var(--light-text);
  margin: 0 0 var(--space-8) 0;
  letter-spacing: -0.02em;
}

.co-subtitle {
  font-size: 16px;
  color: var(--light-text-secondary);
  margin: 0 0 var(--space-48) 0;
}

.co-dropzone {
  border: 2px dashed #CBD5E1;
  background-color: #FFFFFF;
  padding: var(--space-64) var(--space-48);
  border-radius: 12px;
  cursor: pointer;
  width: 100%;
  max-width: 600px;
  transition: all 0.2s;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.co-dropzone:hover {
  border-color: var(--color-primary);
  background-color: #F8FAFC;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.co-drop-icon {
  color: var(--color-primary);
  margin-bottom: var(--space-24);
}

.co-drop-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--light-text);
  margin-bottom: var(--space-8);
}

.co-drop-subtitle {
  font-size: 15px;
  color: var(--color-primary);
  margin-bottom: var(--space-16);
}

.co-drop-meta {
  font-size: 13px;
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
  font-size: 15px;
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
  border: 1px solid var(--light-border-strong);
  border-radius: 8px;
  overflow: hidden;
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.co-image-preview img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.co-placeholder {
  color: var(--dark-text-secondary);
  font-size: 15px;
}

.co-panel {
  background-color: var(--light-surface);
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  padding: var(--space-24);
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.co-panel-title {
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--light-text);
  margin: 0 0 var(--space-16) 0;
  letter-spacing: 0.05em;
  border-bottom: 1px solid #E2E8F0;
  padding-bottom: var(--space-12);
}

.co-info-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-12);
}

.co-info-item {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
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
  gap: 12px;
  padding: 12px 16px;
  background-color: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 6px;
  opacity: 0.7;
}

.co-pipe-item.active {
  opacity: 1;
  background-color: #FFFFFF;
  border-left: 4px solid var(--color-primary);
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.co-pipe-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.co-pipe-name {
  flex: 1;
  font-size: 14px;
  font-weight: 500;
}

.co-pipe-state {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.co-pipe-state.complete { color: #16A34A; }
.co-pipe-state.running { color: #2563EB; }
.co-pipe-state.ready { color: var(--color-primary); }
.co-pipe-state.waiting { color: var(--light-text-muted); }

.mt-6 { margin-top: var(--space-24); }
''')
