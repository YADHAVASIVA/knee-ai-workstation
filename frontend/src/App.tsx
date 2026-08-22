import React, { useState } from 'react';
import { Sidebar } from './components/shell/Sidebar';
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
    oaAnalysis: null,
    implantMatches: null
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
    { id: 'overview', label: 'Overview', icon: 'FileText', category: 'main' },
    { id: 'imaging', label: 'Imaging', icon: 'Image', category: 'main' },
    { id: 'anatomy', label: 'Anatomy', icon: 'Layers', category: 'main' },
    { id: 'analysis', label: 'Analysis', icon: 'Activity', category: 'main' },
    { id: 'planning', label: 'Planning', icon: 'Crosshair', category: 'main' },
    { id: 'report', label: 'Report', icon: 'FileOutput', category: 'main' }
  ];

  const handleNewCase = () => {
    if(window.confirm('Start a new case? All unsaved progress will be lost.')) {
      setCaseState({
        caseId: `KAI-2026-${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
        patient: { name: '', age: '', sex: '', patientId: '', laterality: '', notes: '' },
        images: [],
        activeImageId: null,
        oaAnalysis: null,
        implantMatches: null
      });
      setActiveRoute('overview');
    }
  };

  const renderPage = () => {
    switch (activeRoute) {
      case 'overview':
        return (
          <CaseOverview patient={caseState.patient} caseId={caseState.caseId} onChange={(p) => setCaseState(prev => ({ ...prev, patient: p }))} onNext={() => setActiveRoute('imaging')} />
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
      <Sidebar activeRoute={activeRoute} analysisId={caseState.caseId} onNavigate={(route) => setActiveRoute(route as AppRoute)} routes={navItems as any} />
      <div className="main-content">
        <TopBar activeRoute={activeRoute} analysisId={caseState.caseId} patientName={caseState.patient.name} isDemo={true} isCalibrated={caseState.images.length > 0 ? caseState.images.some(img => img.metadata?.pixel_spacing) : null} />
        <main className="page-container">
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
