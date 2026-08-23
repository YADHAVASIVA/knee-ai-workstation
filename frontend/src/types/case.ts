import type { ImageMetadata, SegmentationResult, MeasurementResult, BoneMeasurementResult, MatchingResult, OAAnalysisResult } from '../services/api';

export interface PatientInfo {
  name: string;
  age: string;
  sex: string;
  patientId: string;
  laterality: string;
  notes: string;
}

export type ProcessingStatus = 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED' | 'NEEDS_REVIEW';

export interface CaseImage {
  id: string; // The backend image_id
  metadata: ImageMetadata | null;
  file?: File; // To support preview
  previewUrl: string | null;
  status: ProcessingStatus;
  segmentation: SegmentationResult | null;
  measurements: {
    meniscus: MeasurementResult | null;
    bones: BoneMeasurementResult | null;
  };
}


export interface PlanningState {
  calibration: {
    source?: 'DICOM_PIXEL_SPACING' | 'CALIBRATION_MARKER' | 'MANUAL_REFERENCE';
    pixelsPerMm?: number;
    mmPerPixelX?: number;
    mmPerPixelY?: number;
    points?: {x: number, y: number}[];
    referenceLengthMm?: number;
    imageId?: string;
  };
  landmarks: Record<string, {x: number, y: number, imageId: string, source: 'USER', timestamp: string}>;
  measurements: Record<string, {value: number, unit: string, source: string, imageId: string, landmarks: string[], calculationMethod: string}>;
  implantSelection: {
    femoralId?: string;
    tibialId?: string;
  };
  alignmentStrategy?: string;
  notes?: string;
}

export interface CaseState {
  caseId: string;
  patient: PatientInfo;
  images: CaseImage[];
  activeImageId: string | null;
  oaAnalysis: Record<string, OAAnalysisResult>;
  xrayAnalysis: Record<string, import('../services/api').XRayInferenceOutput>;
  implantMatches: Record<string, MatchingResult>;
  planning: PlanningState;
}




