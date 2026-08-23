import React, { useState, useRef, useEffect, useMemo } from 'react';
import type { CaseState } from '../types/case';
import { Button } from '../components/ui/Button';
import './ImplantPlanning.css';
import * as api from '../services/api';

interface ImplantPlanningProps {
  caseState: CaseState;
  setCaseState: React.Dispatch<React.SetStateAction<CaseState>>;
  onBack: () => void;
  onNext: () => void;
}

type PlanningTab = 'IMAGING' | 'CALIBRATION' | 'LANDMARKS' | 'SIZE MATCHING' | 'SUMMARY';
interface Point { x: number; y: number; }

const Provenance: React.FC<{type: 'AI'|'MEASURED'|'CALCULATED'|'CATALOG'|'USER'|'DICOM'}> = ({type}) => (
  <span style={{ fontSize: 9, background: 'rgba(0,0,0,0.06)', color: 'var(--color-text-secondary)', padding: '2px 5px', borderRadius: 4, marginLeft: 6, fontWeight: 700, letterSpacing: '0.05em', whiteSpace: 'nowrap' }}>[{type}]</span>
);

export const ImplantPlanning: React.FC<ImplantPlanningProps> = ({ caseState, setCaseState, onBack, onNext }) => {
  const activeImage = caseState.images.find(img => img.id === caseState.activeImageId) || caseState.images[0];
  const isXRay = activeImage?.metadata?.modality !== 'MRI';
  const xrayResult = activeImage ? caseState.xrayAnalysis[activeImage.id] : null;

  const [activeTab, setActiveTab] = useState<PlanningTab>('IMAGING');
  const [refLength, setRefLength] = useState('25.0');
  const [activeLandmarkToPlace, setActiveLandmarkToPlace] = useState<string | null>(null);

  const [femoralCatalog, setFemoralCatalog] = useState<api.ImplantComponent[] | null>(null);
  const [tibialCatalog, setTibialCatalog] = useState<api.ImplantComponent[] | null>(null);
  const [catalogError, setCatalogError] = useState(false);

  const svgRef = useRef<SVGSVGElement>(null);
  const plan = caseState.planning;

  // 1. Fetch catalogs and auto-detect DICOM pixel spacing (Anisotropic support)
  useEffect(() => {
    if (isXRay) {
      api.getFemoralImplants().then(data => setFemoralCatalog(data)).catch(() => setCatalogError(true));
      api.getTibialImplants().then(data => setTibialCatalog(data)).catch(() => setCatalogError(true));
    }
    
    if (activeImage?.metadata?.pixel_spacing && plan.calibration.source !== 'DICOM_PIXEL_SPACING') {
      const sp = activeImage.metadata.pixel_spacing as any;
      const rowMm = sp.row_mm || (Array.isArray(sp) ? sp[0] : sp) || null;
      const colMm = sp.column_mm || (Array.isArray(sp) ? sp[1] : sp) || null;
      
      if (rowMm && colMm) {
        setCaseState(s => ({
          ...s,
          planning: {
            ...s.planning,
            calibration: { source: 'DICOM_PIXEL_SPACING', mmPerPixelX: colMm, mmPerPixelY: rowMm, imageId: activeImage.id }
          }
        }));
      }
    }
  }, [isXRay, activeImage]);

  const updatePlan = (updates: Partial<typeof plan>) => {
    setCaseState(s => ({ ...s, planning: { ...s.planning, ...updates } }));
  };

  const getMouseCoords = (e: React.MouseEvent | MouseEvent): Point | null => {
    if (!svgRef.current) return null;
    const CTM = svgRef.current.getScreenCTM();
    if (!CTM) return null;
    return { x: (e.clientX - CTM.e) / CTM.a, y: (e.clientY - CTM.f) / CTM.d };
  };

  // 2. Anisotropic Distance Calculation
  const calcPhysicalDistanceMm = (p1?: Point, p2?: Point) => {
    if (!p1 || !p2) return null;
    const cal = plan.calibration;
    // Fallback scalar `pixelsPerMm` for manual calibration, or anisotropic X/Y for DICOM
    const mmX = cal.mmPerPixelX || (cal.pixelsPerMm ? 1 / cal.pixelsPerMm : null);
    const mmY = cal.mmPerPixelY || (cal.pixelsPerMm ? 1 / cal.pixelsPerMm : null);
    
    if (!mmX || !mmY) return null;
    
    const dxMm = (p1.x - p2.x) * mmX;
    const dyMm = (p1.y - p2.y) * mmY;
    return Math.sqrt(dxMm * dxMm + dyMm * dyMm);
  };

  // 3. Measurement Persistence Engine
  useEffect(() => {
    const newMeasurements = { ...plan.measurements };
    const lh = plan.landmarks;
    
    // Joint Line Width
    const jlw = calcPhysicalDistanceMm(lh.medialCondyle, lh.lateralCondyle);
    if (jlw !== null) {
      newMeasurements.jointLineWidth = { value: parseFloat(jlw.toFixed(1)), unit: 'mm', source: 'CALCULATED', imageId: activeImage.id, landmarks: ['medialCondyle', 'lateralCondyle'], calculationMethod: 'Anisotropic Euclidean distance' };
    } else { delete newMeasurements.jointLineWidth; }

    // Tibial Width
    const tw = calcPhysicalDistanceMm(lh.medialPlateau, lh.lateralPlateau);
    if (tw !== null) {
      newMeasurements.tibialWidth = { value: parseFloat(tw.toFixed(1)), unit: 'mm', source: 'CALCULATED', imageId: activeImage.id, landmarks: ['medialPlateau', 'lateralPlateau'], calculationMethod: 'Anisotropic Euclidean distance' };
    } else { delete newMeasurements.tibialWidth; }
    
    // HKA Axis - Vector calculation requires physical space if anisotropic
    const cal = plan.calibration;
    const mmX = cal.mmPerPixelX || (cal.pixelsPerMm ? 1/cal.pixelsPerMm : 1);
    const mmY = cal.mmPerPixelY || (cal.pixelsPerMm ? 1/cal.pixelsPerMm : 1);
    
    if (lh.femoralHead && lh.kneeCenter && lh.ankleCenter) {
      const v1 = { x: (lh.femoralHead.x - lh.kneeCenter.x) * mmX, y: (lh.femoralHead.y - lh.kneeCenter.y) * mmY };
      const v2 = { x: (lh.ankleCenter.x - lh.kneeCenter.x) * mmX, y: (lh.ankleCenter.y - lh.kneeCenter.y) * mmY };
      const mag1 = Math.hypot(v1.x, v1.y);
      const mag2 = Math.hypot(v2.x, v2.y);
      if (mag1 === 0 || mag2 === 0) {
        delete newMeasurements.hka;
      } else {
        const dot = v1.x * v2.x + v1.y * v2.y;
        const cosine = Math.max(-1, Math.min(1, dot / (mag1 * mag2)));
        const angleRad = Math.acos(cosine);
        const val = 180 - (angleRad * (180 / Math.PI));
        newMeasurements.hka = { value: parseFloat(val.toFixed(1)), unit: 'degrees', source: 'CALCULATED', imageId: activeImage.id, landmarks: ['femoralHead', 'kneeCenter', 'ankleCenter'], calculationMethod: '3-point vector angle in physical space' };
      }
    } else { delete newMeasurements.hka; }
    
    if (JSON.stringify(newMeasurements) !== JSON.stringify(plan.measurements)) {
      updatePlan({ measurements: newMeasurements });
    }
  }, [plan.landmarks, plan.calibration.mmPerPixelX, plan.calibration.mmPerPixelY, plan.calibration.pixelsPerMm, activeImage.id]);

  const handleSvgClick = (e: React.MouseEvent) => {
    const coords = getMouseCoords(e);
    if (!coords || !activeImage) return;

    if (activeTab === 'CALIBRATION' && plan.calibration.source !== 'DICOM_PIXEL_SPACING') {
      const currentPts = plan.calibration.points || [];
      if (currentPts.length < 2) {
        updatePlan({ calibration: { ...plan.calibration, points: [...currentPts, coords], imageId: activeImage.id } });
      }
    } else if (activeTab === 'LANDMARKS' && activeLandmarkToPlace) {
      updatePlan({
        landmarks: {
          ...plan.landmarks,
          [activeLandmarkToPlace]: { x: coords.x, y: coords.y, imageId: activeImage.id, source: 'USER', timestamp: new Date().toISOString() }
        }
      });
      setActiveLandmarkToPlace(null);
    }
  };

  const handleCalibrate = () => {
    const pts = plan.calibration.points;
    if (pts && pts.length === 2) {
      const distPx = Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y);
      const mm = parseFloat(refLength);
      if (mm > 0) {
        updatePlan({
          calibration: { ...plan.calibration, source: 'MANUAL_REFERENCE', referenceLengthMm: mm, pixelsPerMm: distPx / mm, mmPerPixelX: mm / distPx, mmPerPixelY: mm / distPx, imageId: activeImage?.id }
        });
      }
    }
  };

  // Image Inventory (Strict)
  const viewMetadataAvailable = !!(activeImage?.metadata as any)?.view; // Doesn't exist in current API schema

  // HKA Axis Validation
  const hasFullLimb = !!(plan.landmarks.femoralHead && plan.landmarks.kneeCenter && plan.landmarks.ankleCenter);
  const isLongLegImage = viewMetadataAvailable && (activeImage?.metadata as any)?.view?.toLowerCase().includes('long');
  const hkaObj = plan.measurements.hka;
  
  const hkaStatus = !viewMetadataAvailable ? "UNAVAILABLE (Full-limb imaging status unknown)" : (!isLongLegImage ? "UNAVAILABLE (Current image is not long-leg)" : (!hasFullLimb ? "UNAVAILABLE (Missing required landmarks)" : "VALID"));
  
  const alignmentString = hkaStatus === "VALID" && hkaObj ? `${Math.abs(hkaObj.value)}° ${hkaObj.value > 0 ? 'Varus' : 'Valgus'}` : hkaStatus;

  // Dimensional matching
  const femoralCandidates = useMemo(() => {
    const jlw = plan.measurements.jointLineWidth?.value;
    if (!jlw || !femoralCatalog) return [];
    return [...femoralCatalog]
      .map(c => ({ ...c, diffML: c.width - jlw }))
      .sort((a, b) => Math.abs(a.diffML) - Math.abs(b.diffML))
      .slice(0, 4);
  }, [plan.measurements.jointLineWidth, femoralCatalog]);

  const tibialCandidates = useMemo(() => {
    const tw = plan.measurements.tibialWidth?.value;
    if (!tw || !tibialCatalog) return [];
    return [...tibialCatalog]
      .map(c => ({ ...c, diffML: c.width - tw }))
      .sort((a, b) => Math.abs(a.diffML) - Math.abs(b.diffML))
      .slice(0, 4);
  }, [plan.measurements.tibialWidth, tibialCatalog]);

  // Comprehensive Validation Logic
  const validationLog = useMemo(() => {
    const log: Record<string, 'PASS' | 'INCOMPLETE' | 'UNAVAILABLE' | 'ERROR' | 'READY_FOR_REVIEW' | 'NOT_REQUIRED'> = {
      imaging: !activeImage ? 'ERROR' : (!viewMetadataAvailable ? 'INCOMPLETE' : 'PASS'),
      calibration: (!plan.calibration.mmPerPixelX && !plan.calibration.pixelsPerMm) ? 'INCOMPLETE' : 'PASS',
      landmarks: (['medialCondyle', 'lateralCondyle', 'medialPlateau', 'lateralPlateau'].some(lm => !plan.landmarks[lm])) ? 'INCOMPLETE' : 'PASS',
      measurements: (!plan.measurements.jointLineWidth || !plan.measurements.tibialWidth) ? 'INCOMPLETE' : 'PASS',
      mechanicalAxis: hkaStatus === "VALID" ? 'PASS' : 'UNAVAILABLE',
      implantCatalog: catalogError ? 'ERROR' : (!femoralCatalog || !tibialCatalog ? 'INCOMPLETE' : 'PASS'),
      dimensionalMapping: 'UNAVAILABLE',
      implantGeometry: 'UNAVAILABLE'
    };
    
    // Explicit Overall Status Check
    const hasError = Object.values(log).includes('ERROR');
    const isReady = 
      log.imaging === 'PASS' &&
      log.calibration === 'PASS' &&
      log.landmarks === 'PASS' &&
      log.measurements === 'PASS' &&
      log.implantCatalog === 'PASS' &&
      log.dimensionalMapping === 'PASS' &&
      !hasError;

    log.overall = hasError ? 'ERROR' : (isReady ? 'READY_FOR_REVIEW' : 'INCOMPLETE');
    
    return log;
  }, [activeImage, viewMetadataAvailable, plan.calibration, plan.landmarks, plan.measurements, hkaStatus, catalogError, femoralCatalog, tibialCatalog]);

  const valState = validationLog.overall;

  const exportReport = () => {
    const payload = {
      caseId: caseState.caseId,
      imageIds: caseState.images.map(i => i.id),
      imageMetadata: caseState.images.map(i => i.metadata),
      imagingValidation: validationLog.imaging,
      calibration: plan.calibration,
      landmarks: plan.landmarks,
      measurements: plan.measurements,
      hka: {
        status: hkaStatus === "VALID" ? "AVAILABLE" : "UNAVAILABLE",
        value: hkaStatus === "VALID" ? hkaObj?.value : null,
        reason: hkaStatus !== "VALID" ? hkaStatus : null
      },
      implantCandidates: {
        femoral: femoralCandidates,
        tibial: tibialCandidates
      },
      selectedImplants: plan.implantSelection,
      alignmentStrategy: plan.alignmentStrategy || 'Mechanical',
      notes: plan.notes || '',
      validationLog,
      timestamp: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = `Plan_${caseState.caseId}_${Date.now()}.json`; a.click();
  };

  if (!isXRay) {
    return <div className="ip-container fade-in">MRI Planning currently unavailable in this module.</div>;
  }

  const previewUrl = activeImage?.id ? api.getPreviewUrl(activeImage.id) : '';

  return (
    <div className="ip-container fade-in" style={{ maxWidth: 1400 }}>
      <div className="ip-header" style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 className="ip-title">05 Surgical Planning</h2>
          <p className="ip-subtitle" style={{ color: 'var(--color-text-secondary)', fontWeight: 500 }}>Data-Driven Preoperative TKA Templating &mdash; Clinical Verification Required</p>
        </div>
        <div style={{ padding: '8px 16px', background: valState === 'READY_FOR_REVIEW' ? '#ECFDF5' : (valState === 'INCOMPLETE' ? '#FEF9C3' : '#F1F5F9'), color: valState === 'READY_FOR_REVIEW' ? '#047857' : (valState === 'INCOMPLETE' ? '#854D0E' : '#64748B'), borderRadius: 6, fontWeight: 700, fontSize: 13, border: `1px solid ${valState === 'READY_FOR_REVIEW' ? '#34D399' : (valState === 'INCOMPLETE' ? '#FDE047' : '#CBD5E1')}` }}>
          STATE: {valState.replace(/_/g, ' ')}
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 20, borderBottom: '1px solid var(--color-border)', paddingBottom: 16 }}>
        {(['IMAGING', 'CALIBRATION', 'LANDMARKS', 'SIZE MATCHING', 'SUMMARY'] as PlanningTab[]).map(tab => (
          <Button key={tab} variant={activeTab === tab ? 'primary' : 'ghost'} onClick={() => setActiveTab(tab)} style={{ padding: '6px 12px', fontSize: 13, background: activeTab === tab ? '#172033' : 'transparent', color: activeTab === tab ? 'white' : 'inherit' }}>
            {tab}
          </Button>
        ))}
      </div>

      <div className="ip-layout" style={{ gridTemplateColumns: '1fr 380px' }}>
        
        {/* LEFT COL: VIEWER */}
        <div className="ip-main-col">
          <div className="ip-card" style={{ padding: 0, overflow: 'hidden', background: '#080B10', borderRadius: 8, height: '700px', display: 'flex', justifyContent: 'center', position: 'relative' }}>
            <img src={previewUrl} alt="X-Ray" style={{ maxHeight: '100%', maxWidth: '100%', objectFit: 'contain', position: 'absolute', pointerEvents: 'none' }} />
            
            {activeTab === 'SIZE MATCHING' && (
              <div style={{ position: 'absolute', top: '40%', left: '50%', transform: 'translate(-50%, -50%)', background: 'rgba(255,0,0,0.8)', color: 'white', padding: '12px 24px', borderRadius: 8, fontWeight: 600, fontSize: 14, zIndex: 20, textAlign: 'center' }}>
                Validated implant geometry unavailable.<br/>
                <span style={{ fontSize: 12, fontWeight: 400 }}>Visual templating disabled.</span>
              </div>
            )}

            <svg ref={svgRef} style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', zIndex: 10, cursor: activeLandmarkToPlace || (activeTab==='CALIBRATION' && (plan.calibration.points||[]).length < 2) ? 'crosshair' : 'default' }} onClick={handleSvgClick}>
              {(plan.calibration.points||[]).map((p, i) => <circle key={`calib-${i}`} cx={p.x} cy={p.y} r="5" fill="#F59E0B" stroke="#fff" strokeWidth="2" />)}
              {(plan.calibration.points||[]).length === 2 && <line x1={plan.calibration.points![0].x} y1={plan.calibration.points![0].y} x2={plan.calibration.points![1].x} y2={plan.calibration.points![1].y} stroke="#F59E0B" strokeWidth="2" strokeDasharray="4 4" />}
              
              {plan.landmarks.femoralHead && plan.landmarks.kneeCenter && <line x1={plan.landmarks.femoralHead.x} y1={plan.landmarks.femoralHead.y} x2={plan.landmarks.kneeCenter.x} y2={plan.landmarks.kneeCenter.y} stroke="#EF4444" strokeWidth="2" strokeDasharray="6 4" opacity={0.7} />}
              {plan.landmarks.kneeCenter && plan.landmarks.ankleCenter && <line x1={plan.landmarks.kneeCenter.x} y1={plan.landmarks.kneeCenter.y} x2={plan.landmarks.ankleCenter.x} y2={plan.landmarks.ankleCenter.y} stroke="#10B981" strokeWidth="2" strokeDasharray="6 4" opacity={0.7} />}
              
              {Object.entries(plan.landmarks).map(([key, p]) => (p && <circle key={key} cx={p.x} cy={p.y} r="5" fill="#3B82F6" stroke="#fff" strokeWidth="2" style={{ cursor: 'pointer' }} />))}
            </svg>
          </div>
        </div>

        {/* RIGHT COL: TOOLS */}
        <div className="ip-side-col" style={{ height: '700px', overflowY: 'auto', paddingRight: 8 }}>
          
          {activeTab === 'IMAGING' && (
            <div className="ip-card" style={{ padding: '24px' }}>
              <h3 style={{ fontSize: 13, textTransform: 'uppercase', marginBottom: 16 }}>1. Imaging Inventory</h3>
              
              {!viewMetadataAvailable ? (
                <div style={{ padding: 16, background: '#F1F5F9', border: '1px solid #E2E8F0', borderRadius: 8, color: '#475569', fontSize: 13, fontWeight: 500, textAlign: 'center' }}>
                  VIEW METADATA UNAVAILABLE
                </div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 12, fontSize: 13, background: '#F8FAFC', padding: 16, borderRadius: 8, border: '1px solid #E2E8F0' }}>
                  {/* Future view implementation here once schema supports it */}
                </div>
              )}
              <div style={{ marginTop: 16, fontSize: 12, color: 'var(--color-text-secondary)', lineHeight: 1.5 }}>
                Imaging validation is required for mechanical axis HKA certification. Because view metadata is absent, full-limb validation is incomplete.
              </div>
            </div>
          )}

          {activeTab === 'CALIBRATION' && (
            <div className="ip-card" style={{ padding: '24px' }}>
              <h3 style={{ fontSize: 13, textTransform: 'uppercase', marginBottom: 16 }}>2. Image Calibration</h3>
              {plan.calibration.source === 'DICOM_PIXEL_SPACING' ? (
                <div style={{ padding: 16, background: '#ECFDF5', border: '1px solid #6EE7B7', borderRadius: 8 }}>
                  <div style={{ color: '#065F46', fontWeight: 600, fontSize: 14 }}>✓ DICOM CALIBRATION DETECTED</div>
                  <div style={{ color: '#047857', fontSize: 13, marginTop: 4 }}>Row: {plan.calibration.mmPerPixelY?.toFixed(4)} mm/px<br/>Col: {plan.calibration.mmPerPixelX?.toFixed(4)} mm/px</div>
                </div>
              ) : (
                <>
                  <p style={{ fontSize: 13, color: 'var(--color-text-secondary)', marginBottom: 20 }}>DICOM pixel spacing unavailable. Manual calibration required.</p>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                    <div><label style={{ display: 'block', fontSize: 12, fontWeight: 600, marginBottom: 6 }}>Known Marker Size (mm) <Provenance type="USER" /></label><input type="number" value={refLength} onChange={e=>setRefLength(e.target.value)} style={{ width: '100%', padding: '8px 12px', borderRadius: 6, border: '1px solid var(--color-border)', outline: 'none' }} /></div>
                  </div>
                  <div style={{ display: 'flex', gap: 12, marginTop: 24 }}><Button variant="secondary" onClick={() => updatePlan({ calibration: { ...plan.calibration, points: [] }})} style={{ flex: 1 }}>Clear Points</Button><Button variant="primary" onClick={handleCalibrate} disabled={(plan.calibration.points||[]).length !== 2} style={{ flex: 2 }}>Verify Scale</Button></div>
                  {plan.calibration.pixelsPerMm && <div style={{ marginTop: 24, padding: 16, background: '#ECFDF5', border: '1px solid #6EE7B7', borderRadius: 8 }}><div style={{ color: '#065F46', fontWeight: 600, fontSize: 14 }}>✓ MANUAL CALIBRATION VALID</div><div style={{ color: '#047857', fontSize: 13, marginTop: 4 }}>Scale: {(1/plan.calibration.pixelsPerMm).toFixed(4)} mm/px</div></div>}
                </>
              )}
            </div>
          )}

          {activeTab === 'LANDMARKS' && (
            <div className="ip-card" style={{ padding: '24px' }}>
              <h3 style={{ fontSize: 13, textTransform: 'uppercase', marginBottom: 16 }}>3. Anatomical Landmarking</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                {(['femoralHead', 'kneeCenter', 'ankleCenter', 'medialCondyle', 'lateralCondyle', 'medialPlateau', 'lateralPlateau'] as const).map(key => (
                  <Button key={key} variant={plan.landmarks[key] ? 'secondary' : (activeLandmarkToPlace === key ? 'primary' : 'ghost')} onClick={() => setActiveLandmarkToPlace(key)} style={{ justifyContent: 'space-between', padding: '8px 12px', border: plan.landmarks[key] ? '1px solid var(--color-border)' : '1px dashed var(--color-border)' }}>
                    <span style={{ fontSize: 13 }}>{key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}</span>{plan.landmarks[key] ? <span style={{ color: '#10B981' }}>✓</span> : <span style={{ fontSize: 11, color: 'var(--color-text-muted)' }}>Required</span>}
                  </Button>
                ))}
              </div>
              
              <div style={{ marginTop: 24, padding: 16, background: '#F8FAFC', borderRadius: 8, border: '1px solid #E2E8F0' }}>
                <h4 style={{ fontSize: 11, color: 'var(--color-text-secondary)', marginBottom: 8, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Derived Dimensions</h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 8, fontSize: 13 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}><span>HKA Axis</span><span style={{ fontWeight: 600, color: hkaStatus === 'VALID' ? 'inherit' : 'var(--color-danger)', fontSize: hkaStatus === 'VALID' ? 13 : 11 }}>{alignmentString} {hkaStatus === 'VALID' && <Provenance type="CALCULATED" />}</span></div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}><span>Joint Line W</span><span style={{ fontWeight: 600 }}>{plan.measurements.jointLineWidth?.value || 'N/A'} mm {plan.measurements.jointLineWidth && <Provenance type="CALCULATED" />}</span></div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}><span>Tibial W</span><span style={{ fontWeight: 600 }}>{plan.measurements.tibialWidth?.value || 'N/A'} mm {plan.measurements.tibialWidth && <Provenance type="CALCULATED" />}</span></div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'SIZE MATCHING' && (
            <div className="ip-card" style={{ padding: '24px' }}>
              <h3 style={{ fontSize: 13, textTransform: 'uppercase', marginBottom: 16 }}>4. Size Matching</h3>
              {catalogError ? (
                <div style={{ padding: 16, background: '#FEF2F2', border: '1px solid #FECACA', borderRadius: 8, color: '#991B1B', fontSize: 13 }}><strong>Validated implant catalog unavailable.</strong></div>
              ) : (!plan.calibration.mmPerPixelX && !plan.calibration.pixelsPerMm) ? (
                <div style={{ padding: 16, background: '#FEF2F2', border: '1px solid #FECACA', borderRadius: 8, color: '#991B1B', fontSize: 13 }}><strong>Calibration Required</strong></div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
                  
                  {(!femoralCatalog || femoralCatalog.length === 0) ? (
                    <div style={{ padding: 16, background: '#FEF9C3', border: '1px solid #FDE047', borderRadius: 8, color: '#854D0E', fontSize: 13 }}><strong>Validated implant catalog unavailable.</strong></div>
                  ) : (
                    <>
                      <div>
                        <div style={{ fontSize: 11, textTransform: 'uppercase', color: 'var(--color-text-secondary)', fontWeight: 700, marginBottom: 8 }}>Femoral Dimensional Candidates</div>
                        <div style={{ fontSize: 12, marginBottom: 8 }}>Patient ML: <strong>{plan.measurements.jointLineWidth?.value || 'N/A'} mm</strong> <Provenance type="CALCULATED" /></div>
                        {femoralCandidates.map(c => (
                          <div key={c.id} style={{ padding: '8px 12px', border: '1px solid var(--color-border)', borderRadius: 6, marginBottom: 6, display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: plan.implantSelection.femoralId === c.id ? '#EFF6FF' : 'white', cursor: 'pointer' }} onClick={() => updatePlan({ implantSelection: { ...plan.implantSelection, femoralId: c.id }})}>
                            <div><div style={{ fontSize: 13, fontWeight: 600 }}>Size {c.size} <Provenance type="CATALOG"/></div><div style={{ fontSize: 11, color: 'var(--color-text-secondary)' }}>AP: {c.ap_dimension} | ML: {c.width}</div></div>
                            <div style={{ fontSize: 12, fontWeight: 600, color: Math.abs(c.diffML) > 3 ? '#991B1B' : '#047857' }}>ΔML {c.diffML > 0 ? '+' : ''}{c.diffML.toFixed(1)}</div>
                          </div>
                        ))}
                      </div>

                      <div>
                        <div style={{ fontSize: 11, textTransform: 'uppercase', color: 'var(--color-text-secondary)', fontWeight: 700, marginBottom: 8 }}>Tibial Dimensional Candidates</div>
                        <div style={{ fontSize: 12, marginBottom: 8 }}>Patient ML: <strong>{plan.measurements.tibialWidth?.value || 'N/A'} mm</strong> <Provenance type="CALCULATED" /></div>
                        {tibialCandidates.map(c => (
                          <div key={c.id} style={{ padding: '8px 12px', border: '1px solid var(--color-border)', borderRadius: 6, marginBottom: 6, display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: plan.implantSelection.tibialId === c.id ? '#ECFDF5' : 'white', cursor: 'pointer' }} onClick={() => updatePlan({ implantSelection: { ...plan.implantSelection, tibialId: c.id }})}>
                            <div><div style={{ fontSize: 13, fontWeight: 600 }}>Size {c.size} <Provenance type="CATALOG"/></div><div style={{ fontSize: 11, color: 'var(--color-text-secondary)' }}>AP: {c.ap_dimension} | ML: {c.width}</div></div>
                            <div style={{ fontSize: 12, fontWeight: 600, color: Math.abs(c.diffML) > 3 ? '#991B1B' : '#047857' }}>ΔML {c.diffML > 0 ? '+' : ''}{c.diffML.toFixed(1)}</div>
                          </div>
                        ))}
                      </div>
                    </>
                  )}
                  <div style={{ fontSize: 11, color: 'var(--color-text-secondary)', textAlign: 'center', padding: 8, background: '#F8FAFC', borderRadius: 4 }}>
                    Dimensional mapping validation unavailable.<br/>
                    Candidate sizes are displayed for research/demo purposes only.<br/>
                    Clinician selection required.<br/>
                    No automatic implant recommendation is made.
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'SUMMARY' && (
            <div className="ip-card" style={{ padding: '24px' }}>
              <h3 style={{ fontSize: 13, textTransform: 'uppercase', marginBottom: 16 }}>5. Data Provenance Summary</h3>
              
              <div style={{ display: 'flex', flexDirection: 'column', gap: 12, fontSize: 13, background: '#F8FAFC', padding: 16, borderRadius: 8, border: '1px solid #E2E8F0', marginBottom: 20 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #E2E8F0', paddingBottom: 6 }}><span style={{ color: 'var(--color-text-secondary)' }}>AI KL Grade</span> <span style={{ fontWeight: 600, display: 'flex', alignItems: 'center' }}>KL{xrayResult?.predicted_kl_grade ?? 'N/A'} <Provenance type="AI" /></span></div>
                <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #E2E8F0', paddingBottom: 6 }}><span style={{ color: 'var(--color-text-secondary)' }}>Calibration</span> <span style={{ fontWeight: 600, display: 'flex', alignItems: 'center' }}>{(plan.calibration.mmPerPixelX || plan.calibration.pixelsPerMm) ? 'VALIDATED' : 'MISSING'} {(plan.calibration.mmPerPixelX || plan.calibration.pixelsPerMm) && <Provenance type={plan.calibration.source === 'DICOM_PIXEL_SPACING' ? 'DICOM' : 'USER'} />}</span></div>
                <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #E2E8F0', paddingBottom: 6 }}><span style={{ color: 'var(--color-text-secondary)' }}>Alignment Philosophy</span> 
                  <select value={plan.alignmentStrategy || 'Mechanical'} onChange={e=>updatePlan({ alignmentStrategy: e.target.value })} style={{ outline: 'none', border: '1px solid #ccc', borderRadius: 4, fontSize: 11, padding: 2 }}><option>Mechanical</option><option>Kinematic</option><option>User Defined</option></select>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #E2E8F0', paddingBottom: 6 }}><span style={{ color: 'var(--color-text-secondary)' }}>HKA Axis</span> <span style={{ fontWeight: 600, display: 'flex', alignItems: 'center', fontSize: hkaStatus === 'VALID' ? 13 : 11 }}>{hkaStatus === 'VALID' ? alignmentString : 'UNAVAILABLE'} {hkaStatus === 'VALID' && <Provenance type="CALCULATED" />}</span></div>
                {hkaStatus !== 'VALID' && <div style={{ fontSize: 11, color: 'var(--color-danger)', textAlign: 'right', marginTop: -4, paddingBottom: 6, borderBottom: '1px solid #E2E8F0' }}>Reason: {hkaStatus.replace('UNAVAILABLE ', '')}</div>}
                
                <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #E2E8F0', paddingBottom: 6 }}><span style={{ color: 'var(--color-text-secondary)' }}>Selected Femoral Component</span> <span style={{ fontWeight: 600, display: 'flex', alignItems: 'center' }}>{plan.implantSelection.femoralId ? `${plan.implantSelection.femoralId}` : 'NONE'} {plan.implantSelection.femoralId && <Provenance type="USER" />}</span></div>
                <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #E2E8F0', paddingBottom: 6 }}><span style={{ color: 'var(--color-text-secondary)' }}>Selected Tibial Component</span> <span style={{ fontWeight: 600, display: 'flex', alignItems: 'center' }}>{plan.implantSelection.tibialId ? `${plan.implantSelection.tibialId}` : 'NONE'} {plan.implantSelection.tibialId && <Provenance type="USER" />}</span></div>
                <div style={{ display: 'flex', justifyContent: 'space-between', paddingBottom: 2 }}><span style={{ color: 'var(--color-text-secondary)' }}>Validated Implant Geometry</span> <span style={{ fontWeight: 600, color: 'var(--color-text-muted)' }}>UNAVAILABLE</span></div>
              </div>

              <textarea value={plan.notes || ''} onChange={e=>updatePlan({ notes: e.target.value })} placeholder="Clinical Notes..." style={{ width: '100%', height: 80, padding: 12, borderRadius: 6, border: '1px solid var(--color-border)', marginBottom: 16 }} />

              <div style={{ padding: 12, background: '#FFFBEB', border: '1px solid #FEF3C7', borderRadius: 8, marginBottom: 20, fontSize: 11, color: '#92400E', lineHeight: 1.5 }}>
                <strong>DISCLAIMER:</strong> This is a research prototype. Measurements, outputs, and templates must not be used for direct patient care. Final clinical interpretation is the sole responsibility of the physician.
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}><Button variant="primary" onClick={exportReport}>Export Complete JSON State</Button></div>
            </div>
          )}
        </div>
      </div>
      <div className="ip-actions">
        <Button variant="ghost" onClick={onBack}>&larr; Back to Analysis</Button>
        <Button variant="primary" onClick={onNext}>Continue to Report &rarr;</Button>
      </div>
    </div>
  );
};
