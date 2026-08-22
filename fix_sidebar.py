import os

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

write_file('frontend/src/components/shell/Sidebar.tsx', """
import React from 'react';
import { Activity, ShieldCheck, AlertCircle } from 'lucide-react';
import './shell.css';

interface SidebarProps {
  activeRoute: string;
  onNavigate: (route: string) => void;
  analysisId: string | null;
  routes: Array<{ id: string; label: string; category: string; disabled?: boolean; icon?: React.ReactNode }>;
  imageMetadata?: any;
  isCalibrated?: boolean | null;
}

export const Sidebar: React.FC<SidebarProps> = ({ 
  activeRoute, 
  onNavigate, 
  analysisId,
  routes,
  imageMetadata,
  isCalibrated
}) => {
  const sections = routes.reduce((acc, route) => {
    if (!acc[route.category]) acc[route.category] = [];
    acc[route.category].push(route);
    return acc;
  }, {} as Record<string, typeof routes>);

  return (
    <aside className="app-sidebar">
      <div className="sidebar-brand">
        <div className="brand-logo">
          <Activity size={24} color="var(--color-primary)" />
          <div className="brand-text">
            <div className="brand-title">KNEE AI</div>
            <div className="brand-subtitle">Clinical Workstation</div>
          </div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {Object.entries(sections).map(([category, items]) => (
          <div key={category} className="nav-section">
            <h3 className="nav-section-title">{category}</h3>
            <ul className="nav-list">
              {items.map(item => (
                <li key={item.id}>
                  <button
                    className={`nav-btn ${activeRoute === item.id ? 'active' : ''}`}
                    onClick={() => onNavigate(item.id)}
                    disabled={item.disabled}
                  >
                    <span className="nav-icon">{item.icon}</span>
                    <span className="nav-label">{item.label}</span>
                  </button>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </nav>

      {analysisId && (
        <div className="sidebar-case-context">
          <div className="case-context-title">CURRENT CASE</div>
          <div className="case-context-id">{analysisId.split('-')[0].toUpperCase()}</div>
          <div className="case-context-meta">
            {imageMetadata?.modality || 'MRI'} &bull; {imageMetadata?.dimensions ? `${imageMetadata.dimensions.width} x ${imageMetadata.dimensions.height}` : 'Unavailable'}
          </div>
          <div className={`case-context-status ${isCalibrated ? 'success' : 'warning'}`}>
            {isCalibrated ? <ShieldCheck size={14} /> : <AlertCircle size={14} />}
            <span>{isCalibrated ? 'Calibrated' : 'Uncalibrated'}</span>
          </div>
        </div>
      )}
    </aside>
  );
};
""")
