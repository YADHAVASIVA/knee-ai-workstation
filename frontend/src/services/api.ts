import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 5000,
});

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
}

export interface SystemInfoResponse {
  application: string;
  backend: string;
  ai_status: string;
  database_status: string;
  implant_database?: string;
  environment: string;
}

export const checkHealth = async (): Promise<HealthResponse> => {
  const response = await apiClient.get<HealthResponse>('/health');
  return response.data;
};

export const getSystemInfo = async (): Promise<SystemInfoResponse> => {
  const response = await apiClient.get<SystemInfoResponse>('/system/info');
  return response.data;
};

export interface UploadResponse {
  image_id: string;
  filename: string;
  content_type: string;
  file_size: number;
  width: number;
  height: number;
  status: string;
  format?: string;
  spatial_calibration_available?: boolean;
  orientation_available?: boolean;
}

export interface ImageMetadata {
  image_id: string;
  format: string;
  modality: string;
  dimensions: {
    width: number;
    height: number;
  };
  pixel_spacing: {
    row_mm: number;
    column_mm: number;
  } | null;
  orientation_available: boolean;
  spatial_calibration_available: boolean;
}
export interface PreprocessResponse {
  image_id: string;
  status: string;
  original_dimensions: { width: number; height: number };
  processed_dimensions: { width: number; height: number };
  spatial_calibration_available: boolean;
  pixel_spacing: number | null;
  modality: string | null;
}

export const uploadImage = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await apiClient.post<UploadResponse>('/images/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const preprocessImage = async (imageId: string): Promise<PreprocessResponse> => {
  const response = await apiClient.post<PreprocessResponse>(`/images/preprocess/${imageId}`);
  return response.data;
};

export const getPreviewUrl = (imageId: string): string => {
  return `${API_BASE_URL}/api/v1/images/${imageId}/preview`;
};

export interface StructureResult {
  detected: boolean;
  confidence: number | null;
}

export interface SegmentationResult {
  image_id: string;
  model_status: string;
  model_name: string;
  model_version: string;
  clinical_validation: boolean;
  structures: Record<string, StructureResult>;
}

export const analyzeAnatomy = async (imageId: string): Promise<SegmentationResult> => {
  const response = await apiClient.post<SegmentationResult>(`/segmentation/${imageId}`);
  return response.data;
};

export const getMaskUrl = (imageId: string, structure: string): string => {
  return `${API_BASE_URL}/api/v1/segmentation/${imageId}/mask/${structure}`;
};

export interface MeasurementLocation {
  name: string;
  x: number;
  y: number;
  thickness_pixels: number;
  thickness_mm: number | null;
}

export interface MeasurementResult {
  image_id: string;
  measurement_type: string;
  measurement_status: string;
  segmentation_model_status: string;
  calibration_available: boolean;
  locations: MeasurementLocation[];
  mean_thickness_pixels: number;
  mean_thickness_mm: number | null;
  unit: string;
  warning: string | null;
}

export const measureMeniscus = async (imageId: string): Promise<MeasurementResult> => {
  const response = await apiClient.post<MeasurementResult>(`/measurements/meniscus/${imageId}`);
  return response.data;
};

export interface PatientData {
  age: number | null;
  sex: string;
  oa_status: string;
}

export interface OAAnalysisResult {
  image_id: string;
  analysis_status: string;
  data_status: string;
  model_status: string;
  patient: PatientData;
  meniscus_measurement: any;
  oa_vs_non_oa: any;
  male_vs_female: any;
  age_association: any;
  classifier_result: any;
  warning: string;
}

export interface LineCoordinate {
  start_x: number;
  start_y: number;
  end_x: number;
  end_y: number;
}

export interface BoneMetrics {
  width_pixels: number;
  width_mm: number | null;
  ap_dimension_pixels: number;
  ap_dimension_mm: number | null;
  width_line: LineCoordinate;
  ap_line: LineCoordinate;
}

export interface BoneMeasurementResult {
  image_id: string;
  measurement_status: string;
  segmentation_model_status: string;
  calibration_available: boolean;
  orientation_status: string;
  femur: BoneMetrics | null;
  tibia: BoneMetrics | null;
  warning: string;
}

export const analyzeOA = async (imageId: string, patientData: PatientData): Promise<OAAnalysisResult> => {
  const response = await apiClient.post<OAAnalysisResult>(`/oa-analysis/${imageId}`, patientData);
  return response.data;
};

export const measureBoneAnatomy = async (imageId: string): Promise<BoneMeasurementResult> => {
  const response = await apiClient.post<BoneMeasurementResult>(`/measurements/bones/${imageId}`);
  return response.data;
};

export interface ImplantComponent {
  id: string;
  component_type: string;
  size: string;
  width: number;
  ap_dimension: number;
  manufacturer: string;
  model_name: string;
  source_type: string;
  dataset_version: string;
  is_demo: boolean;
  created_at: string;
}

export const getImplants = async (): Promise<ImplantComponent[]> => {
  const response = await apiClient.get<ImplantComponent[]>('/implants');
  return response.data;
};

export const getFemoralImplants = async (): Promise<ImplantComponent[]> => {
  const response = await apiClient.get<ImplantComponent[]>('/implants/femoral');
  return response.data;
};

export const getTibialImplants = async (): Promise<ImplantComponent[]> => {
  const response = await apiClient.get<ImplantComponent[]>('/implants/tibial');
  return response.data;
};

export const getImplantById = async (id: string): Promise<ImplantComponent> => {
  const response = await apiClient.get<ImplantComponent>(`/implants/${id}`);
  return response.data;
};

export interface CandidateExplanation {
  patient_width: number;
  implant_width: number;
  width_difference: number;
  width_error: number;
  patient_ap: number;
  implant_ap: number;
  ap_difference: number;
  ap_error: number;
  combined_normalized_error: number;
  contribution_to_score: number;
}

export interface RankedCandidate {
  rank: number;
  implant_id: string;
  size: string;
  score: number;
  width_difference: number;
  ap_difference: number;
  explanation: CandidateExplanation;
  is_demo: boolean;
  source_type: string;
}

export interface MatchingResult {
  image_id: string;
  matching_status: string;
  data_status: string;
  calibration_available: boolean;
  orientation_status: string;
  femoral_candidates: RankedCandidate[];
  tibial_candidates: RankedCandidate[];
  warning: string;
}

export const matchImplants = async (imageId: string, useSyntheticDemoCalibration: boolean = false): Promise<MatchingResult> => {
  let url = `/implant-matching/${imageId}`;
  if (useSyntheticDemoCalibration) {
    url += `?synthetic_pixel_spacing=1.0`;
  }
  const response = await apiClient.post<MatchingResult>(url);
  return response.data;
};

export const getImageMetadata = async (imageId: string): Promise<ImageMetadata> => {
  const response = await apiClient.get<ImageMetadata>(`/images/${imageId}/metadata`);
  return response.data;
};
