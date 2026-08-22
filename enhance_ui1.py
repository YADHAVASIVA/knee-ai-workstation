import os

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

write_file('frontend/src/App.tsx', '''
import { useEffect, useState } from 'react';
import * as api from './services/api';
import { getSystemInfo, uploadImage, preprocessImage, getPreviewUrl, analyzeAnatomy, getMaskUrl, measureMeniscus, analyzeOA, measureBoneAnatomy, matchImplants } from './services/api';
import { useAnalysisWorkflow, WorkflowState } from './hooks/useAnalysisWorkflow';
import { LayoutDashboard, Layers, Activity, Crosshair, FileText } from 'lucide-react';
import './App.css';

import { AppShell } from './components/shell/AppShell';

import { CaseOverview } from './pages/CaseOverview';
import { Anatomy } from './pages/Anatomy';
import { Analysis } from './pages/Analysis';
import { ImplantPlanning } from './pages/ImplantPlanning';
import { Report } from './pages/Report';
import { ErrorBoundary } from './components/ErrorBoundary';

export type AppRoute = 'overview' | 'anatomy' | 'analysis' | 'planning' | 'report';

function App() {
  const [imageMetadata, setImageMetadata] = useState<api.ImageMetadata | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [overlays, setOverlays] = useState<any[]>([]);
  const [showMeniscusLines, setShowMeniscusLines] = useState<boolean>(true);
  const [showBoneLines, setShowBoneLines] = useState<boolean>(true);

  useEffect(() => {
    const fetchSystemStatus = async () => {
      try {
        await getSystemInfo();
      } catch (err) {
        console.error('Failed to connect to backend', err);
      }
    };
    fetchSystemStatus();
  }, []);

  const workflow = useAnalysisWorkflow();
  const { 
    analysisId, workflowState, setWorkflowState, setErrorMsg, 
    setUploadData, setPreprocessData,
    segmentationResult, setSegmentationResult, meniscusMeasurement, setMeniscusMeasurement,
    boneMeasurement, setBoneMeasurement, oaResult, setOaResult,
    matchingResult, setMatchingResult, patientData, resetAnalysis
  } = workflow;

  const [activeRoute, setActiveRoute] = useState<AppRoute>('overview');

  const navItems = [
    { id: 'overview' as AppRoute, label: 'Overview', category: 'CASE', icon: <LayoutDashboard size={18} /> },
    { id: 'anatomy' as AppRoute, label: 'Anatomy', category: 'ANATOMY', disabled: workflowState === WorkflowState.IDLE, icon: <Layers size={18} /> },
    { id: 'analysis' as AppRoute, label: 'OA Analysis', category: 'ANALYSIS', disabled: !segmentationResult, icon: <Activity size={18} /> },
    { id: 'planning' as AppRoute, label: 'Implant Planning', category: 'PLANNING', disabled: !boneMeasurement, icon: <Crosshair size={18} /> },
    { id: 'report' as AppRoute, label: 'Report', category: 'OUTPUT', disabled: !matchingResult, icon: <FileText size={18} /> }
  ];

  const handleNavigate = (route: AppRoute) => {
    const targetItem = navItems.find(item => item.id === route);
    if (targetItem && !targetItem.disabled) {
      setActiveRoute(route);
    }
  };

  const handleResetAnalysis = () => {
    resetAnalysis();
    setPreviewUrl(null);
    setOverlays([]);
    setImageMetadata(null);
    setActiveRoute('overview');
  };

  const handleFileUpload = async (file: File) => {
    try {
      setErrorMsg(null);
      setWorkflowState(WorkflowState.UPLOADING);
      
      const uploadRes = await uploadImage(file);
      setUploadData(uploadRes);
      
      setWorkflowState(WorkflowState.PREPROCESSING);
      const preRes = await preprocessImage(uploadRes.analysis_id);
      setPreprocessData(preRes);
      setImageMetadata(preRes.metadata);
      
      const pUrl = getPreviewUrl(uploadRes.analysis_id);
      setPreviewUrl(pUrl);
      
      setWorkflowState(WorkflowState.READY_FOR_SEGMENTATION);
      setActiveRoute('overview');
    } catch (err: any) {
      console.error(err);
      setErrorMsg(err.message || 'Analysis could not be completed.');
      setWorkflowState(WorkflowState.ERROR);
    }
  };

  const handleRunAnatomyAnalysis = async () => {
    if (!analysisId) return;
    try {
      setWorkflowState(WorkflowState.SEGMENTING);
      const segRes = await analyzeAnatomy(analysisId);
      setSegmentationResult(segRes);

      const newOverlays = [
        { id: 'femur', name: 'Femur', visible: true, color: '#3b82f6', url: getMaskUrl(analysisId, 'femur') },
        { id: 'tibia', name: 'Tibia', visible: true, color: '#10b981', url: getMaskUrl(analysisId, 'tibia') },
        { id: 'meniscus', name: 'Meniscus', visible: true, color: '#f59e0b', url: getMaskUrl(analysisId, 'medial_meniscus') }
      ];
      setOverlays(newOverlays);

      setWorkflowState(WorkflowState.SEGMENTATION_COMPLETE);

      setWorkflowState(WorkflowState.MEASURING_MENISCUS);
      const menisRes = await measureMeniscus(analysisId);
      setMeniscusMeasurement(menisRes);

      setWorkflowState(WorkflowState.MEASURING_BONES);
      const boneRes = await measureBoneAnatomy(analysisId);
      setBoneMeasurement(boneRes);

      setWorkflowState(WorkflowState.BONE_MEASUREMENTS_COMPLETE);
    } catch (err: any) {
      console.error(err);
      setErrorMsg(err.message || 'Analysis could not be completed.');
      setWorkflowState(WorkflowState.ERROR);
    }
  };

  const handleRunOAAnalysis = async () => {
    if (!analysisId) return;
    try {
      setWorkflowState(WorkflowState.OA_ANALYSIS_COMPLETE);
      const oa = await analyzeOA(analysisId);
      setOaResult(oa);
    } catch (err: any) {
      console.error(err);
      setErrorMsg('Analysis could not be completed.');
    }
  };

  const handleRunImplantMatching = async () => {
    if (!analysisId) return;
    try {
      setWorkflowState(WorkflowState.MATCHING);
      const match = await matchImplants(analysisId);
      setMatchingResult(match);
      setWorkflowState(WorkflowState.MATCHING_COMPLETE);
    } catch (err: any) {
      console.error(err);
      setErrorMsg('Analysis could not be completed.');
    }
  };

  const toggleOverlay = (id: string) => {
    setOverlays(prev => prev.map(o => o.id === id ? { ...o, visible: !o.visible } : o));
  };

  useEffect(() => {
    if (workflowState === WorkflowState.READY_FOR_SEGMENTATION) {
      handleRunAnatomyAnalysis();
    }
  }, [workflowState]);

  const renderPage = () => {
    switch (activeRoute) {
      case 'overview':
        return (
          <CaseOverview 
            workflowState={workflowState}
            analysisId={analysisId}
            imageMetadata={imageMetadata}
            previewUrl={previewUrl}
            onNavigate={handleNavigate as any}
            onUpload={handleFileUpload}
            onReset={handleResetAnalysis}
          />
        );
      case 'anatomy':
        return (
          <Anatomy 
            previewUrl={previewUrl}
            overlays={overlays}
            measurements={meniscusMeasurement ? meniscusMeasurement.locations : []}
            boneMeasurement={boneMeasurement}
            onToggleOverlay={toggleOverlay}
            showMeasurements={showMeniscusLines}
            onToggleMeasurements={setShowMeniscusLines}
            showBoneMeasurements={showBoneLines}
            onToggleBoneMeasurements={setShowBoneLines}
          />
        );
      case 'analysis':
        return (
          <Analysis 
            patientData={patientData}
            oaResult={oaResult}
            boneMeasurement={boneMeasurement}
            meniscusMeasurement={meniscusMeasurement}
            onAnalyze={handleRunOAAnalysis}
            isProcessing={workflowState === WorkflowState.OA_ANALYSIS_COMPLETE && !oaResult}
          />
        );
      case 'planning':
        return (
          <ImplantPlanning 
            matchingResult={matchingResult}
            boneMeasurement={boneMeasurement}
            onMatch={handleRunImplantMatching}
            isProcessing={workflowState === WorkflowState.MATCHING}
          />
        );
      case 'report':
        return (
          <Report 
            onNavigate={handleNavigate as any}
            analysisId={analysisId}
            imageMetadata={imageMetadata}
            boneMeasurement={boneMeasurement}
            meniscusMeasurement={meniscusMeasurement}
            matchingResult={matchingResult}
          />
        );
      default:
        return <div>404 Not Found</div>;
    }
  };

  return (
    <ErrorBoundary>
      <AppShell
        activeRoute={activeRoute}
        onNavigate={handleNavigate as any}
        analysisId={analysisId}
        isDemo={true}
        isCalibrated={imageMetadata?.pixel_spacing ? true : false}
        imageMetadata={imageMetadata}
        routes={navItems}
      >
        {renderPage()}
      </AppShell>
    </ErrorBoundary>
  );
}

export default App;
''')

write_file('frontend/src/components/shell/Sidebar.tsx', '''
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
                    className={
av-btn }
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
            {imageMetadata?.modality || 'MRI'} &bull; {imageMetadata?.dimensions ? ${imageMetadata.dimensions.width} ×  : 'Unavailable'}
          </div>
          <div className={case-context-status }>
            {isCalibrated ? <ShieldCheck size={14} /> : <AlertCircle size={14} />}
            <span>{isCalibrated ? 'Calibrated' : 'Uncalibrated'}</span>
          </div>
        </div>
      )}
    </aside>
  );
};
''')

write_file('frontend/src/components/shell/TopBar.tsx', '''
import React from 'react';
import { ChevronRight, Settings, User } from 'lucide-react';
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
  const getContextName = () => {
    switch(activeRoute) {
      case 'overview': return 'Overview';
      case 'anatomy': return 'Anatomy';
      case 'analysis': return 'OA Analysis';
      case 'planning': return 'Implant Planning';
      case 'report': return 'Report';
      default: return '';
    }
  };

  return (
    <header className="app-topbar">
      <div className="topbar-left">
        <span className="topbar-brand">KNEE AI</span>
        <ChevronRight size={16} className="breadcrumb-slash" />
        <span className="topbar-route">{getContextName()}</span>
      </div>
      
      <div className="topbar-right">
        {analysisId && (
          <>
            <span className="topbar-meta mono">{analysisId.split('-')[0].toUpperCase()}</span>
            <span className="topbar-divider"></span>
            <span className="topbar-meta">{imageMetadata?.modality || 'MRI'}</span>
            <span className="topbar-divider"></span>
            <span className={	opbar-meta }>
              &bull; {isCalibrated ? 'Calibrated' : 'Uncalibrated'}
            </span>
          </>
        )}
        {isDemo && (
          <>
            <span className="topbar-divider"></span>
            <span className="topbar-demo-badge">RESEARCH PROTOTYPE</span>
          </>
        )}
        <span className="topbar-divider"></span>
        <button className="topbar-icon-btn"><Settings size={18} /></button>
        <button className="topbar-icon-btn"><User size={18} /></button>
      </div>
    </header>
  );
};
''')
