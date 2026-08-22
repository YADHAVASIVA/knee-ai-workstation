import React from 'react';
import { Settings, User, CheckCircle2 } from 'lucide-react';
import './shell.css';

interface TopBarProps {
  activeRoute: string;
  analysisId: string | null;
  patientName?: string;
  isDemo: boolean;
  isCalibrated: boolean | null;
}

export const TopBar: React.FC<TopBarProps> = ({ 
  activeRoute, 
  analysisId,
  patientName,
  isDemo, 
  isCalibrated 
}) => {
  return (
    <header className="topbar">
      <div className="topbar-left">
        <h2 className="topbar-case-id">{analysisId || 'NEW CASE'}</h2>
        {patientName && (
          <>
            <span className="topbar-divider"></span>
            <span className="topbar-patient-name">{patientName}</span>
          </>
        )}
        <span className="topbar-divider"></span>
        <span className="topbar-route-name">{activeRoute.toUpperCase()}</span>
      </div>

      <div className="topbar-right">
        {isCalibrated != null && (
          <>
            {isCalibrated ? (
              <span className="topbar-meta calibrated"><CheckCircle2 size={14}/> CALIBRATED</span>
            ) : (
              <span className="topbar-meta uncalibrated">UNCALIBRATED</span>
            )}
            <span className="topbar-divider"></span>
          </>
        )}
        
        {isDemo && (
          <>
            <span className="topbar-demo-badge">RESEARCH PROTOTYPE</span>
            <span className="topbar-divider"></span>
          </>
        )}
        
        <button className="topbar-icon-btn">
          <Settings size={18} />
        </button>
        <button className="topbar-icon-btn">
          <User size={18} />
        </button>
      </div>
    </header>
  );
};
