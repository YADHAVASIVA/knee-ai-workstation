import React, { useState } from 'react';
import { Sidebar } from './components/shell/Sidebar';
import { FileText, Image as ImageIcon, Layers, Activity, Crosshair, FileOutput } from 'lucide-react';
import { TopBar } from './components/shell/TopBar';
import { CaseOverview } from './pages/CaseOverview';
import { ImagingStudies } from './pages/ImagingStudies';
import { Anatomy } from './pages/Anatomy';
import { Analysis } from './pages/Analysis';
import { ImplantPlanning } from './pages/ImplantPlanning';
import { Report } from './pages/Report';
import { ErrorBoundary } from './components/ErrorBoundary';
import type { CaseState } from './types/case';
import * as api from './services/api';

export type AppRoute = 'overview' | 'imaging' | 'anatomy' | 'analysis' | 'planning' | 'report';


const StepIndicator = ({ activeRoute }: { activeRoute: string }) => {
  const steps = [
    { id: 'overview', label: 'Overview', num: 1 },
    { id: 'imaging',  label: 'Imaging',  num: 2 },
    { id: 'anatomy',  label: 'Anatomy',  num: 3 },
    { id: 'analysis', label: 'Analysis', num: 4 },
    { id: 'planning', label: 'Planning', num: 5 },
    { id: 'report',   label: 'Report',   num: 6 },
  ];
  const activeIdx = steps.findIndex(s => s.id === activeRoute);
  return (
    <div className="step-indicator">
      {steps.map((s, idx) => {
        const state = idx < activeIdx ? 'completed' : idx === activeIdx ? 'active' : 'locked';
        return (
          <React.Fragment key={s.id}>
            <div className={`step-item ${state}`}>
              <div className="step-circle">{state === 'completed' ? '✓' : s.num}</div>
              <span className="step-label">{s.label}</span>
            </div>
            {idx < steps.length - 1 && (
              <div className={`step-connector ${idx < activeIdx ? 'completed' : ''}`} />
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
};

function App() {
  const [activeRoute, setActiveRoute] = useState<AppRoute>('overview');
  
  const [caseState, setCaseState] = useState<CaseState>({
    caseId: `KAI-2026-${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
    patient: {
      name: '',
      age: '',
      sex: '',
      patientId: '',
      laterality: '',
      notes: ''
    },
    images: [],
    activeImageId: null,
    oaAnalysis: {},
    xrayAnalysis: {},
    implantMatches: {}, planning: { calibration: {}, landmarks: {}, measurements: {}, implantSelection: {} }
  });

  const handleProcessImage = async (imageId: string) => {
    try {
      setCaseState(prev => ({
        ...prev,
        images: prev.images.map(img => img.id === imageId ? { ...img, status: 'PROCESSING' } : img)
      }));

      const seg = await api.analyzeAnatomy(imageId);
      
      let meniscus = null;
      let bones = null;
      
      try {
        bones = await api.measureBoneAnatomy(imageId);
      } catch (e) { console.error(e) }

      const img = caseState.images.find(i => i.id === imageId);
      if (img?.metadata?.modality === 'MRI') {
        try {
          meniscus = await api.measureMeniscus(imageId);
        } catch (e) { console.error(e) }
      }

      setCaseState(prev => ({
        ...prev,
        images: prev.images.map(img => img.id === imageId ? { 
          ...img, 
          status: 'COMPLETED',
          segmentation: seg,
          measurements: { meniscus, bones }
        } : img)
      }));
    } catch (err) {
      console.error(err);
      setCaseState(prev => ({
        ...prev,
        images: prev.images.map(img => img.id === imageId ? { ...img, status: 'FAILED' } : img)
      }));
    }
  };

  const navItems = [
    { id: 'overview', label: 'Overview', icon: <FileText size={18} />, category: 'main' },
    { id: 'imaging', label: 'Imaging', icon: <ImageIcon size={18} />, category: 'main' },
    { id: 'anatomy', label: 'Anatomy', icon: <Layers size={18} />, category: 'main' },
    { id: 'analysis', label: 'Analysis', icon: <Activity size={18} />, category: 'main' },
    { id: 'planning', label: 'Planning', icon: <Crosshair size={18} />, category: 'main' },
    { id: 'report', label: 'Report', icon: <FileOutput size={18} />, category: 'main' }
  ];

  const handleNewCase = () => {
    if(window.confirm('Start a new case? All unsaved progress will be lost.')) {
      setCaseState({
        caseId: `KAI-2026-${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
        patient: { name: '', age: '', sex: '', patientId: '', laterality: '', notes: '' },
        images: [],
        activeImageId: null,
        oaAnalysis: {},
    xrayAnalysis: {},
        implantMatches: {}, planning: { calibration: {}, landmarks: {}, measurements: {}, implantSelection: {} }
      });
      setActiveRoute('overview');
    }
  };

  const renderPage = () => {
    switch (activeRoute) {
      case 'overview':
        return (
          <CaseOverview patient={caseState.patient}  onChange={(p) => setCaseState(prev => ({ ...prev, patient: p }))} onNext={() => setActiveRoute('imaging')} />
        );
      case 'imaging':
        return (
          <ImagingStudies 
            images={caseState.images}
            setImages={(action) => {
              if (typeof action === 'function') {
                setCaseState(prev => {
                  const newImages = action(prev.images);
                  return { ...prev, images: newImages, activeImageId: newImages.length > 0 ? newImages[0].id : null };
                });
              }
            }}
            onBack={() => setActiveRoute('overview')}
            onNext={() => setActiveRoute('anatomy')}
          />
        );
      case 'anatomy':
        return (
          <Anatomy 
            images={caseState.images}
            activeImageId={caseState.activeImageId}
            setActiveImageId={(id) => setCaseState(prev => ({ ...prev, activeImageId: id }))}
            onProcessImage={handleProcessImage}
            onBack={() => setActiveRoute('imaging')}
            onNext={() => setActiveRoute('analysis')}
          />
        );
      case 'analysis':
        return (
          <Analysis 
            caseState={caseState}
            setCaseState={setCaseState}
            onBack={() => setActiveRoute('anatomy')}
            onNext={() => setActiveRoute('planning')}
          />
        );
      case 'planning':
        return (
          <ImplantPlanning 
            caseState={caseState}
            setCaseState={setCaseState}
            onBack={() => setActiveRoute('analysis')}
            onNext={() => setActiveRoute('report')}
          />
        );
      case 'report':
        return (
          <Report 
            caseState={caseState}
            onBack={() => setActiveRoute('planning')}
            onNewCase={handleNewCase}
          />
        );
      default:
        return <div>Page not found</div>;
    }
  };

  return (
    <div className={`app-shell theme-${activeRoute === 'anatomy' ? 'dark' : 'light'}`}>
      <Sidebar activeRoute={activeRoute} analysisId={caseState.caseId} onNavigate={(route) => setActiveRoute(route as AppRoute)} routes={navItems} />
      <div className="main-content">
        <TopBar activeRoute={activeRoute} analysisId={caseState.caseId} patientName={caseState.patient.name} isDemo={true} isCalibrated={caseState.images.length > 0 ? caseState.images.some(img => img.metadata?.pixel_spacing) : null} />
        <main className="page-container" style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column' }}>
          <StepIndicator activeRoute={activeRoute} />
          <ErrorBoundary>
            {renderPage()}
          </ErrorBoundary>
        </main>
      </div>
    </div>
  );
}

export default App;





