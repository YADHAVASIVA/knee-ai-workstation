import React, { useState } from 'react';
import type { CaseState, CaseImage } from '../types/case';
import { Button } from '../components/ui/Button';
import './Analysis.css';
import * as api from '../services/api';

interface AnalysisProps {
  caseState: CaseState;
  setCaseState: React.Dispatch<React.SetStateAction<CaseState>>;
  onBack: () => void;
  onNext: () => void;
}

export const Analysis: React.FC<AnalysisProps> = ({ caseState, setCaseState, onBack, onNext }) => {
  const [oaLoading, setOaLoading] = useState(false);
  const [oaError, setOaError] = useState<string | null>(null);

  const [xrayLoading, setXrayLoading] = useState<Record<string, boolean>>({});
  const [xrayError, setXrayError] = useState<Record<string, string | null>>({});


  const [selectedOaImageId, setSelectedOaImageId] = useState<string | null>(null);

  // OA analysis requires an MRI image that has been segmented (has meniscus mask)
  const mriImages = caseState.images.filter(img => img.metadata?.modality === 'MRI');
  const analyzedMriImages = mriImages.filter(img => img.segmentation !== null);


  // Pick best MRI image for OA analysis
  const oaTargetImage = analyzedMriImages.find(img => img.id === selectedOaImageId) ?? analyzedMriImages[0] ?? caseState.images.find(img => img.segmentation !== null);

  const handleRunXRayAnalysis = async (imageId: string) => {
    setXrayLoading(prev => ({ ...prev, [imageId]: true }));
    setXrayError(prev => ({ ...prev, [imageId]: null }));
    try {
      const result = await api.analyzeXRay(imageId);
      setCaseState(prev => ({ ...prev, xrayAnalysis: { ...prev.xrayAnalysis, [imageId]: result } }));
    } catch (err: any) {
      console.error('Failed to run X-Ray analysis:', err);
      setXrayError(prev => ({ ...prev, [imageId]: err.response?.data?.detail || err.message || 'Failed to run X-Ray analysis' }));
    } finally {
      setXrayLoading(prev => ({ ...prev, [imageId]: false }));
    }
  };

  const handleRunOaAnalysis = async () => {
    if (!oaTargetImage) return;
    setOaLoading(true);
    setOaError(null);
    try {
      const oaRes = await api.analyzeOA(oaTargetImage.id, {
        age: parseInt(caseState.patient.age),
        sex: caseState.patient.sex,
        oa_status: 'Unknown'
      });
      setCaseState(prev => ({ ...prev, oaAnalysis: { ...prev.oaAnalysis, [oaTargetImage.id]: oaRes } }));
    } catch (e: unknown) {
      // Axios errors: e.response.data.detail contains FastAPI error message
      let msg = 'OA analysis failed.';
      const err = e as Error & { response?: { data?: { detail?: string } } };
      if (err?.response?.data?.detail) {
        msg = err.response.data.detail;
      } else if (err?.message) {
        msg = err.message;
      }
      setOaError(msg);
    } finally {
      setOaLoading(false);
    }
  };

  const renderMeasurementCard = (img: CaseImage) => {
    const isMRI = img.metadata?.modality === 'MRI';
    const femurW = img.measurements.bones?.femur?.width_mm;
    const tibiaW = img.measurements.bones?.tibia?.width_mm;
    const meniscusT = img.measurements.meniscus?.mean_thickness_mm;
    const modLabel = img.metadata?.modality || 'UNKNOWN';

    return (
      <div key={img.id} className="an-card">
        <h4>{modLabel} &mdash; {img.file?.name || 'Image'}</h4>
        <div className="an-measure-grid">
          <div className="an-measure-col">
            <h5>Femur Width</h5>
            <div className={`an-measure-val ${femurW == null ? 'na' : ''}`}>
              {femurW != null ? `${femurW.toFixed(1)} mm` : 'N/A'}
            </div>
          </div>
          <div className="an-measure-col">
            <h5>Tibia Width</h5>
            <div className={`an-measure-val ${tibiaW == null ? 'na' : ''}`}>
              {tibiaW != null ? `${tibiaW.toFixed(1)} mm` : 'N/A'}
            </div>
          </div>
          <div className="an-measure-col">
            <h5>Medial Meniscus</h5>
            {isMRI ? (
              <div className={`an-measure-val ${meniscusT == null ? 'na' : ''}`}>
                {meniscusT != null ? `${meniscusT.toFixed(2)} mm` : 'N/A'}
              </div>
            ) : (
              <div className="an-measure-val na">Not applicable</div>
            )}
          </div>
        </div>
      </div>
    );
  };

  const processedImages = caseState.images.filter(img => img.segmentation !== null);


  const renderXRayPanel = (img: CaseImage) => {
    const activeXray = (caseState.xrayAnalysis || {})[img.id];
    const isLoading = xrayLoading[img.id];
    const error = xrayError[img.id];

    if (activeXray) {
      if (activeXray.status === "MODEL_NOT_READY") {
        return (
          <div className="an-demo-notice" style={{ fontSize: 11, color: "var(--color-danger)", background: "#FEE2E2", padding: 8, borderRadius: 4, marginBottom: 12, border: "1px solid #FCA5A5" }}>
            <strong>MODEL NOT READY</strong><br/><br/>
            {activeXray.message}
          </div>
        );
      }
      if (activeXray.status === "IMAGE_QUALITY_INSUFFICIENT" || activeXray.status === "INFERENCE_FAILED") {
        return (
          <div className="an-demo-notice" style={{ fontSize: 11, color: "var(--color-danger)", background: "#FEE2E2", padding: 8, borderRadius: 4, marginBottom: 12, border: "1px solid #FCA5A5" }}>
            <strong>{activeXray.status}</strong><br/><br/>
            {activeXray.message}
          </div>
        );
      }

      const probs = activeXray.probabilities;
      
      return (
        <div className="an-oa-results">
          <div className="an-demo-notice" style={{ fontSize: 11, color: "var(--color-primary)", background: "#EFF6FF", padding: 8, borderRadius: 4, marginBottom: 16, border: "1px solid #BFDBFE" }}>
            <strong>AI X-RAY ASSESSMENT</strong><br/><br/>
            {activeXray.message}
          </div>
          
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
            <div style={{ flex: 1, padding: 12, background: 'var(--color-surface)', border: '1px solid var(--color-border)', borderRadius: 6, marginRight: 8 }}>
              <div style={{ fontSize: 11, color: 'var(--color-text-secondary)', fontWeight: 600, marginBottom: 4 }}>Predicted Severity</div>
              <div style={{ fontSize: 18, fontWeight: 700, color: activeXray.status === "AI_ASSESSMENT_UNCERTAIN" ? 'var(--color-text-secondary)' : 'var(--color-text)' }}>
                {activeXray.status === "AI_ASSESSMENT_UNCERTAIN" ? "Uncertain" : `KL Grade ${activeXray.predicted_kl_grade}`}
              </div>
            </div>
            <div style={{ flex: 1, padding: 12, background: 'var(--color-surface)', border: '1px solid var(--color-border)', borderRadius: 6, marginLeft: 8 }}>
              <div style={{ fontSize: 11, color: 'var(--color-text-secondary)', fontWeight: 600, marginBottom: 4 }}>Confidence</div>
              <div style={{ fontSize: 18, fontWeight: 700, color: activeXray.status === "AI_ASSESSMENT_UNCERTAIN" ? 'var(--color-warning)' : 'var(--color-text)' }}>
                {(activeXray.confidence! * 100).toFixed(1)}%
              </div>
            </div>
          </div>

          <div style={{ marginBottom: 16 }}>
            <div style={{ fontSize: 11, color: 'var(--color-text-secondary)', fontWeight: 600, marginBottom: 8, textTransform: 'uppercase' }}>Probability Distribution</div>
            {probs && [0, 1, 2, 3, 4].map((kl) => (
              <div key={kl} style={{ display: 'flex', alignItems: 'center', marginBottom: 6 }}>
                <div style={{ width: 40, fontSize: 12, fontWeight: 600 }}>KL {kl}</div>
                <div style={{ flex: 1, background: '#E5E7EB', height: 8, borderRadius: 4, overflow: 'hidden', marginRight: 8 }}>
                  <div style={{ width: `${(probs as any)[`KL${kl}`] * 100}%`, background: kl === activeXray.predicted_kl_grade ? 'var(--color-primary)' : '#9CA3AF', height: '100%' }}></div>
                </div>
                <div style={{ width: 45, fontSize: 11, textAlign: 'right', color: 'var(--color-text-secondary)' }}>
                  {((probs as any)[`KL${kl}`] * 100).toFixed(1)}%
                </div>
              </div>
            ))}
          </div>
          
          <div style={{ borderTop: '1px solid var(--color-border)', paddingTop: 12, fontSize: 11, color: 'var(--color-text-secondary)' }}>
            <div><strong>Model:</strong> {activeXray.model_version}</div>
            <div><strong>Device:</strong> {activeXray.inference_device}</div>
            <div><strong>Status:</strong> {activeXray.status}</div>
          </div>
        </div>
      );
    }

    return (
      <div className="an-empty-state">
        <p>Run the DenseNet121 KL grading model on <strong>{img.file?.name}</strong>.</p>
        <Button onClick={() => handleRunXRayAnalysis(img.id)} disabled={isLoading}>
          {isLoading ? 'Running X-Ray Analysis...' : 'Run X-Ray Analysis'}
        </Button>
        {error && <div className="an-warning-box" style={{ marginTop: 12 }}>{error}</div>}
      </div>
    );
  };

  const renderOaPanel = () => {
    const activeOa = oaTargetImage ? caseState.oaAnalysis[oaTargetImage.id] : null;

    if (activeOa) {
      if (activeOa.analysis_status === "MODEL_UNAVAILABLE") {
        return (
          <div className="an-oa-results">
            <div className="an-demo-notice" style={{ fontSize: 11, color: "var(--color-danger)", background: "#FEE2E2", padding: 8, borderRadius: 4, marginBottom: 12, border: "1px solid #FCA5A5" }}>
              <strong>MODEL UNAVAILABLE</strong><br/><br/>
              {activeOa.warning || "No compatible validated research model is available."}
            </div>
          </div>
        );
      }
      return (
        <div className="an-oa-results">
          <div className="an-demo-notice" style={{ fontSize: 11, color: "var(--color-demo)", background: "var(--color-demo-soft)", padding: 8, borderRadius: 4, marginBottom: 12, border: "1px solid var(--color-demo-border)" }}>
            <strong>RESEARCH PROTOTYPE - NOT CLINICALLY VALIDATED</strong><br/><br/>
            <strong>Source:</strong> {oaTargetImage?.file?.name || "MRI"}<br/>
            <strong>Unit:</strong> Pixels (Calibration not required for demo)
          </div>
          <div className="an-oa-row">
            <span>Model Status</span>
            <strong>{activeOa.model_status?.toUpperCase()}</strong>
          </div>
          {activeOa.classifier_result && (
            <>
              {activeOa.classifier_result.prediction_label === "REVIEW REQUIRED" ? (
                <div className="an-oa-row" style={{ color: "var(--color-warning)" }}>
                  <span>Status</span>
                  <strong>{activeOa.classifier_result.prediction_label}</strong>
                  <div style={{ fontSize: "11px", marginTop: "4px" }}>
                    {activeOa.classifier_result.explanation}
                  </div>
                </div>
              ) : (
                <>
                  <div className="an-oa-row">
                    <span>Research Finding</span>
                    <strong>{activeOa.classifier_result.prediction_label}</strong>
                  </div>
                  <div className="an-oa-row">
                    <span>Research Probability</span>
                    <strong>
                      {(activeOa.classifier_result.prediction_probability * 100).toFixed(1)}%
                    </strong>
                  </div>
                </>
              )}
            </>
          )}
          {activeOa.warning && (
            <div className="an-warning-box" style={{ marginTop: 8 }}>
              {activeOa.warning}
            </div>
          )}
        </div>
      );
    }

    // Not yet run - show guard or button
    if (!caseState.patient.age || !caseState.patient.sex) {
      return (
        <div className="an-empty-state">
          <div className="an-warning-box">
            Patient <strong>age</strong> and <strong>sex</strong> are required. Update them in Case Overview.
          </div>
        </div>
      );
    }

    if (analyzedMriImages.length === 0) {
      return (
        <div className="an-empty-state">
          <div className="an-warning-box">
            OA-associated analysis requires an <strong>MRI image</strong> with completed anatomy segmentation.
            {mriImages.length === 0
              ? ' No MRI images in this case - please upload one in the Imaging step.'
              : ' Please go back to Anatomy and run segmentation on the MRI image.'}
          </div>
        </div>
      );
    }
    
    // Check if the target MRI has a valid meniscus measurement
    const hasMeniscus = oaTargetImage?.segmentation?.structures?.medial_meniscus?.detected === true && oaTargetImage?.measurements?.meniscus?.mean_thickness_pixels != null;
    
    if (!hasMeniscus) {
      return (
        <div className="an-empty-state">
          <div className="an-warning-box">
            The selected MRI (<strong>{oaTargetImage?.file?.name}</strong>) does not have a valid meniscus measurement. 
            OA Analysis requires a detectable medial meniscus.
          </div>
        </div>
      );
    }


    return (
      <div className="an-empty-state">
        {analyzedMriImages.length > 1 && (
          <div style={{ marginBottom: 16, textAlign: 'left' }}>
            <label style={{ display: 'block', fontSize: 11, fontWeight: 700, color: 'var(--color-text-secondary)', marginBottom: 4, textTransform: 'uppercase' }}>Select MRI for Analysis</label>
            <select 
              value={oaTargetImage?.id || ''} 
              onChange={(e) => setSelectedOaImageId(e.target.value)}
              style={{ width: '100%', padding: '8px 12px', borderRadius: 4, border: '1px solid var(--color-border)' }}
            >
              {analyzedMriImages.map(img => (
                <option key={img.id} value={img.id}>{img.file?.name || 'MRI Image'}</option>
              ))}
            </select>
          </div>
        )}
        <p>
          Research prototype analysis using the demo dataset against{' '}
          <strong>{oaTargetImage?.file?.name || 'MRI image'}</strong>.
        </p>
        <Button onClick={handleRunOaAnalysis} disabled={oaLoading}>
          {oaLoading ? 'Running Research Analysis...' : 'Run OA Analysis'}
        </Button>
        {oaError && (
          <div className="an-warning-box" style={{ marginTop: 12 }}>{oaError}</div>
        )}
      </div>
    );
  };

  return (
    <div className="an-container fade-in">
      <div className="an-header">
        <h2 className="an-title">Case Analysis</h2>
        <p className="an-subtitle">
          {processedImages.length > 0
            ? `Anatomical measurements from ${processedImages.length} processed imaging ${processedImages.length === 1 ? 'study' : 'studies'}.`
            : 'No images have been analyzed yet.'}
        </p>
      </div>

      {processedImages.length === 0 ? (
        <div className="an-card">
          <div className="an-empty-state">
            <p>Go back to <strong>Anatomy</strong> and run segmentation on your imaging studies to see measurements here.</p>
          </div>
        </div>
      ) : (
        <div className="an-layout">
          <div className="an-main-col">
            <h3 className="an-section-title">Anatomical Measurements</h3>
            {processedImages.map(renderMeasurementCard)}
          </div>

          <div className="an-side-col">
            {processedImages.filter(img => img.metadata?.modality === 'MRI').length > 0 && (
              <div className="an-card" style={{ marginBottom: 16 }}>
                <h3 className="an-section-title">MRI OA-Associated Analysis</h3>
                {renderOaPanel()}
              </div>
            )}
            
            {processedImages.filter(img => img.metadata?.modality !== 'MRI').map(img => (
              <div key={img.id} className="an-card" style={{ marginBottom: 16 }}>
                <h3 className="an-section-title">X-Ray AI Assessment</h3>
                {renderXRayPanel(img)}
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="an-actions">
        <Button variant="ghost" onClick={onBack}>&larr; Back to Anatomy</Button>
        <Button variant="primary" onClick={onNext}>Continue to Implant Planning &rarr;</Button>
      </div>
    </div>
  );
};















