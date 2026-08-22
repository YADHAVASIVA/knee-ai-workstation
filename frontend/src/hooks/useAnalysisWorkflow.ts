import { useState, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';
import * as api from '../services/api';

export const WorkflowState = {
  IDLE: 'IDLE',
  IMAGE_UPLOADED: 'IMAGE_UPLOADED',
  PREPROCESSING: 'PREPROCESSING',
  READY_FOR_SEGMENTATION: 'READY_FOR_SEGMENTATION',
  SEGMENTING: 'SEGMENTING',
  SEGMENTATION_COMPLETE: 'SEGMENTATION_COMPLETE',
  MEASURING_MENISCUS: 'MEASURING_MENISCUS',
  MENISCUS_COMPLETE: 'MENISCUS_COMPLETE',
  MEASURING_BONES: 'MEASURING_BONES',
  BONE_MEASUREMENTS_COMPLETE: 'BONE_MEASUREMENTS_COMPLETE',
  PATIENT_INFO_REQUIRED: 'PATIENT_INFO_REQUIRED',
  OA_ANALYSIS_RUNNING: 'OA_ANALYSIS_RUNNING',
  OA_ANALYSIS_COMPLETE: 'OA_ANALYSIS_COMPLETE',
  MATCHING: 'MATCHING',
  MATCHING_COMPLETE: 'MATCHING_COMPLETE',
  ERROR: 'ERROR'
} as const;

export type WorkflowState = typeof WorkflowState[keyof typeof WorkflowState];

export const useAnalysisWorkflow = () => {
  const [analysisId, setAnalysisId] = useState<string>(uuidv4());
  const [workflowState, setWorkflowState] = useState<WorkflowState>(WorkflowState.IDLE);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Data states
  const [uploadData, setUploadData] = useState<api.UploadResponse | null>(null);
  const [preprocessData, setPreprocessData] = useState<api.PreprocessResponse | null>(null);
  const [segmentationResult, setSegmentationResult] = useState<api.SegmentationResult | null>(null);
  const [meniscusMeasurement, setMeniscusMeasurement] = useState<api.MeasurementResult | null>(null);
  const [boneMeasurement, setBoneMeasurement] = useState<api.BoneMeasurementResult | null>(null);
  const [oaResult, setOaResult] = useState<api.OAAnalysisResult | null>(null);
  const [matchingResult, setMatchingResult] = useState<api.MatchingResult | null>(null);

  const [patientData, setPatientData] = useState<api.PatientData>({
    age: null,
    sex: 'Unknown',
    oa_status: 'Unknown'
  });

  const resetAnalysis = useCallback(() => {
    setAnalysisId(uuidv4());
    setWorkflowState(WorkflowState.IDLE);
    setErrorMsg(null);
    setUploadData(null);
    setPreprocessData(null);
    setSegmentationResult(null);
    setMeniscusMeasurement(null);
    setBoneMeasurement(null);
    setOaResult(null);
    setMatchingResult(null);
    setPatientData({ age: null, sex: 'Unknown', oa_status: 'Unknown' });
  }, []);

  return {
    analysisId,
    workflowState,
    setWorkflowState,
    errorMsg,
    setErrorMsg,
    uploadData,
    setUploadData,
    preprocessData,
    setPreprocessData,
    segmentationResult,
    setSegmentationResult,
    meniscusMeasurement,
    setMeniscusMeasurement,
    boneMeasurement,
    setBoneMeasurement,
    oaResult,
    setOaResult,
    matchingResult,
    setMatchingResult,
    patientData,
    setPatientData,
    resetAnalysis
  };
};
