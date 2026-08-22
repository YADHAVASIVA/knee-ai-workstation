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
    analysisId, setAnalysisId, workflowState, setWorkflowState, setErrorMsg, 
    setUploadData, setPreprocessData,
    segmentationResult, setSegmentationResult, meniscusMeasurement, setMeniscusMeasurement,
    boneMeasurement, setBoneMeasurement, oaResult, setOaResult,
    matchingResult, setMatchingResult, resetAnalysis
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
      setWorkflowState(WorkflowState.IMAGE_UPLOADED); // Used to be UPLOADING, but enum doesn't have it
      
      const uploadRes = await uploadImage(file);
      setUploadData(uploadRes);
      setAnalysisId(uploadRes.image_id);
      
      setWorkflowState(WorkflowState.PREPROCESSING);
      const preRes = await preprocessImage(uploadRes.image_id);
      setPreprocessData(preRes);
      const meta = await api.getImageMetadata(uploadRes.image_id);
      setImageMetadata(meta);
      
      const pUrl = getPreviewUrl(uploadRes.image_id);
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
      const oa = await analyzeOA(analysisId, { age: 65, sex: 'M', oa_status: 'Moderate' });
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
            modality={imageMetadata?.modality || 'UNKNOWN'}
          />
        );
      case 'analysis':
        return (
          <Analysis 
            boneMeasurement={boneMeasurement}
            meniscusMeasurement={meniscusMeasurement}
            onAnalyze={handleRunOAAnalysis}
            isProcessing={workflowState === WorkflowState.OA_ANALYSIS_COMPLETE && !oaResult}
            modality={imageMetadata?.modality || 'UNKNOWN'}
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
            modality={imageMetadata?.modality || 'UNKNOWN'}
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
