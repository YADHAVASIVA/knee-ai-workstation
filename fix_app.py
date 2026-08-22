import os

filepath = os.path.join("frontend", "src", "App.tsx")
content = '''import { useEffect, useState } from 'react';
import * as api from './services/api';
import { getSystemInfo, uploadImage, preprocessImage, getPreviewUrl, analyzeAnatomy, getMaskUrl, measureMeniscus, analyzeOA, measureBoneAnatomy, matchImplants } from './services/api';
import { useAnalysisWorkflow, WorkflowState } from './hooks/useAnalysisWorkflow';
import './App.css';

import { AppShell } from './components/shell/AppShell';
import type { RouteId } from './components/shell/Sidebar';
import { CaseOverview } from './pages/CaseOverview';
import { Anatomy } from './pages/Anatomy';
import { Analysis } from './pages/Analysis';
import { ImplantPlanning } from './pages/ImplantPlanning';
import { Report } from './pages/Report';
import { ErrorBoundary } from './components/ErrorBoundary';

export type AppRoute = 'overview' | 'anatomy' | 'analysis' | 'planning' | 'report';

function App() {
  const [imageMetadata, setImageMetadata] = useState<api.ImageMetadata | null>(null);

  // View Controls
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [overlays, setOverlays] = useState<any[]>([]);
  const [showMeniscusLines, setShowMeniscusLines] = useState<boolean>(true);
  const [showBoneLines, setShowBoneLines] = useState<boolean>(true);

  // Load system info
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

  // Workflow State
  const workflow = useAnalysisWorkflow();
  const { 
    analysisId, workflowState, setWorkflowState, setErrorMsg, 
    uploadData, setUploadData, setPreprocessData,
    segmentationResult, setSegmentationResult, meniscusMeasurement, setMeniscusMeasurement,
    boneMeasurement, setBoneMeasurement, oaResult, setOaResult,
    matchingResult, setMatchingResult, patientData, resetAnalysis
  } = workflow;

  // Navigation State
  const [activeRoute, setActiveRoute] = useState<AppRoute>('overview');

  const navItems = [
    { id: 'overview' as AppRoute, label: 'Overview', category: 'CASE' },
    { id: 'anatomy' as AppRoute, label: 'Anatomy', category: 'ANATOMY', disabled: workflowState === WorkflowState.IDLE },
    { id: 'analysis' as AppRoute, label: 'Analysis', category: 'ANALYSIS', disabled: !segmentationResult },
    { id: 'planning' as AppRoute, label: 'Implant Planning', category: 'PLANNING', disabled: !boneMeasurement },
    { id: 'report' as AppRoute, label: 'Report', category: 'OUTPUT', disabled: !matchingResult }
  ];

  const handleNavigate = (route: AppRoute) => {
    const targetItem = navItems.find(item => item.id === route);
    if (targetItem && !targetItem.disabled) {
      console.log("[Navigation] " + activeRoute + " -> " + route);
      setActiveRoute(route);
    } else {
      console.warn("[Navigation] Blocked: " + route + " is disabled or invalid.");
    }
  };

  const handleResetAnalysis = () => {
    resetAnalysis();
    setPreviewUrl(null);
    setOverlays([]);
    setImageMetadata(null);
    handleNavigate('overview');
  };

  // Handlers
  const handleFileUpload = async (file: File) => {
    try {
      setWorkflowState(WorkflowState.IMAGE_UPLOADED);
      setErrorMsg(null);
      const res = await uploadImage(file);
      setUploadData(res);
      setPreviewUrl(getPreviewUrl(res.image_id));
      
      handlePreprocess(res.image_id);
    } catch (err: any) {
      setErrorMsg('Failed to upload image. Please try again.');
      setWorkflowState(WorkflowState.IDLE);
    }
  };

  const handlePreprocess = async (imgId: string) => {
    try {
      setWorkflowState(WorkflowState.PREPROCESSING);
      const preRes = await preprocessImage(imgId);
      setPreprocessData(preRes);
      
      try {
        const meta = await api.getImageMetadata(imgId);
        setImageMetadata(meta);
      } catch (e) {
        console.error("Failed to fetch metadata", e);
      }

      setWorkflowState(WorkflowState.READY_FOR_SEGMENTATION);
      handleSegment(imgId);
    } catch (err) {
      setErrorMsg('Preprocessing failed.');
      setWorkflowState(WorkflowState.ERROR);
    }
  };

  const handleSegment = async (imgId: string) => {
    try {
      setWorkflowState(WorkflowState.SEGMENTING);
      const segRes = await analyzeAnatomy(imgId);
      setSegmentationResult(segRes);
      
      const newOverlays = [];
      if (segRes.structures.femur?.detected) {
        newOverlays.push({ id: 'femur', url: getMaskUrl(imgId, 'femur'), name: 'Femur', visible: true, color: '#3b82f6' });
      }
      if (segRes.structures.tibia?.detected) {
        newOverlays.push({ id: 'tibia', url: getMaskUrl(imgId, 'tibia'), name: 'Tibia', visible: true, color: '#10b981' });
      }
      if (segRes.structures.medial_meniscus?.detected) {
        newOverlays.push({ id: 'meniscus', url: getMaskUrl(imgId, 'medial_meniscus'), name: 'Medial Meniscus', visible: true, color: '#f59e0b' });
      }
      setOverlays(newOverlays);
      setWorkflowState(WorkflowState.SEGMENTATION_COMPLETE);

      handleMeasureMeniscus(imgId);
    } catch (err) {
      setErrorMsg('Segmentation failed.');
      setWorkflowState(WorkflowState.ERROR);
    }
  };

  const handleMeasureMeniscus = async (imgId: string) => {
    try {
      setWorkflowState(WorkflowState.MEASURING_MENISCUS);
      const mesRes = await measureMeniscus(imgId);
      setMeniscusMeasurement(mesRes);
      setShowMeniscusLines(true);
      setWorkflowState(WorkflowState.MENISCUS_COMPLETE);

      handleMeasureBones(imgId);
    } catch (err) {
      setErrorMsg('Meniscus measurement failed.');
      setWorkflowState(WorkflowState.ERROR);
    }
  };

  const handleMeasureBones = async (imgId: string) => {
    try {
      setWorkflowState(WorkflowState.MEASURING_BONES);
      const boneRes = await measureBoneAnatomy(imgId);
      setBoneMeasurement(boneRes);
      setShowBoneLines(true);
      setWorkflowState(WorkflowState.BONE_MEASUREMENTS_COMPLETE);
    } catch (err) {
      setErrorMsg('Bone anatomy measurement failed.');
      setWorkflowState(WorkflowState.ERROR);
    }
  };

  const handleAnalyzeOA = async () => {
    if (!uploadData) return;
    try {
      setWorkflowState(WorkflowState.OA_ANALYSIS_RUNNING);
      const oaRes = await analyzeOA(uploadData.image_id, patientData);
      setOaResult(oaRes);
      setWorkflowState(WorkflowState.OA_ANALYSIS_COMPLETE);
    } catch (err) {
      setErrorMsg('OA analysis failed.');
      setWorkflowState(WorkflowState.ERROR);
    }
  };

  const handleMatchImplants = async (useSyntheticCalibration = false) => {
    if (!uploadData) return;
    try {
      setWorkflowState(WorkflowState.MATCHING);
      const matchRes = await matchImplants(uploadData.image_id, useSyntheticCalibration);
      setMatchingResult(matchRes);
      setWorkflowState(WorkflowState.MATCHING_COMPLETE);
    } catch (err) {
      setErrorMsg('Implant matching failed.');
      setWorkflowState(WorkflowState.ERROR);
    }
  };

  const toggleOverlay = (id: string) => {
    setOverlays(prev => prev.map(o => o.id === id ? { ...o, visible: !o.visible } : o));
  };

  // 9. MAIN CONTENT - Single Source of Truth Render Switch
  const renderMainContent = () => {
    switch (activeRoute) {
      case 'overview':
        return (
          <CaseOverview 
            workflowState={workflowState}
            analysisId={analysisId}
            imageMetadata={imageMetadata}
            previewUrl={previewUrl}
            patientData={patientData}
            segmentationResult={segmentationResult}
            boneMeasurement={boneMeasurement}
            meniscusMeasurement={meniscusMeasurement}
            oaResult={oaResult}
            matchingResult={matchingResult}
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
            measurements={meniscusMeasurement?.locations || []}
            boneMeasurement={boneMeasurement}
            onToggleOverlay={toggleOverlay}
            showMeasurements={showMeniscusLines}
            onToggleMeasurements={setShowMeniscusLines}
            showBoneMeasurements={showBoneLines}
            onToggleBoneMeasurements={setShowBoneLines}
            isDemo={true}
          />
        );
      case 'analysis':
        return (
          <Analysis
            patientData={patientData}
            oaResult={oaResult}
            boneMeasurement={boneMeasurement}
            meniscusMeasurement={meniscusMeasurement}
            onAnalyze={handleAnalyzeOA}
            isProcessing={workflowState === WorkflowState.OA_ANALYSIS_RUNNING}
          />
        );
      case 'planning':
        return (
          <ImplantPlanning
            matchingResult={matchingResult}
            boneMeasurement={boneMeasurement}
            onMatch={() => handleMatchImplants(false)}
            isProcessing={workflowState === WorkflowState.MATCHING}
          />
        );
      case 'report':
        return (
          <Report
            analysisId={analysisId}
            patientData={patientData}
            imageMetadata={imageMetadata}
            boneMeasurement={boneMeasurement}
            meniscusMeasurement={meniscusMeasurement}
            oaResult={oaResult}
            matchingResult={matchingResult}
            onPrint={() => window.print()}
          />
        );
      default:
        return <div style={{padding: "40px"}}>Route not found</div>;
    }
  };

  return (
    <AppShell
      activeRoute={activeRoute}
      onNavigate={handleNavigate as any}
      analysisId={analysisId}
      isDemo={true}
      isCalibrated={boneMeasurement?.calibration_available || null}
      routes={navItems as any}
    >
      <ErrorBoundary>
        {renderMainContent()}
      </ErrorBoundary>
    </AppShell>
  );
}

export default App;
'''

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
