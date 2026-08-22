import type { ImageMetadata, SegmentationResult, MeasurementResult, BoneMeasurementResult, MatchingResult } from '../services/api';

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

export interface CaseState {
  caseId: string;
  patient: PatientInfo;
  images: CaseImage[];
  activeImageId: string | null;
  oaAnalysis: any | null; // Aggregate or per-image depending on backend
  implantMatches: MatchingResult | null; 
}
