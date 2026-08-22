import React from 'react';
import { StatusBadge } from '../ui/StatusBadge';
import './shell.css';

interface TopBarProps {
  activeRoute: string;
  analysisId: string | null;
  isDemo: boolean;
  isCalibrated: boolean | null;
  imageMetadata?: any;
}

export const TopBar: React.FC<TopBarProps> = ({ 
  activeRoute, 
  analysisId,
  isDemo,
  isCalibrated,
  imageMetadata
}) => {
  const getBreadcrumb = () => {
    switch(activeRoute) {
      case 'overview': return 'CASE / OVERVIEW';
      case 'anatomy': return 'ANATOMY / IMAGE ANALYSIS';
      case 'analysis': return 'ANALYSIS / OA ASSESSMENT';
      case 'planning': return 'PLANNING / IMPLANT PLANNING';
      case 'report': return 'OUTPUT / CLINICAL REPORT';
      default: return '';
    }
  };

  return (
    <header className="app-topbar">
      <div className="topbar-left">
        <div className="topbar-breadcrumb">{getBreadcrumb()}</div>
      </div>
      
      
      
      <div className="topbar-right">
        {analysisId && (
          <div className="topbar-case-id">Case {analysisId.split('-')[0].toUpperCase()}</div>
        )}
        {imageMetadata?.modality && (
          <div className="topbar-meta-item">{imageMetadata.modality}</div>
        )}
        {isCalibrated !== null && (
          <div className="topbar-meta-item">
            {isCalibrated ? 'CALIBRATED' : 'UNCALIBRATED'}
          </div>
        )}
        {isDemo && (
          <StatusBadge status="DEMO" label="RESEARCH PROTOTYPE" />
        )}
      </div>
    </header>
  );
};

