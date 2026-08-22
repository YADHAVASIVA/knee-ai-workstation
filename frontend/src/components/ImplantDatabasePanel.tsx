import React, { useEffect, useState } from 'react';
import { getFemoralImplants, getTibialImplants } from '../services/api';
import type { ImplantComponent } from '../services/api';
import './ImplantDatabasePanel.css';

export const ImplantDatabasePanel: React.FC = () => {
  const [femoral, setFemoral] = useState<ImplantComponent[]>([]);
  const [tibial, setTibial] = useState<ImplantComponent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchImplants = async () => {
      try {
        const [femData, tibData] = await Promise.all([
          getFemoralImplants(),
          getTibialImplants()
        ]);
        
        // Sort by size
        setFemoral(femData.sort((a, b) => parseInt(a.size) - parseInt(b.size)));
        setTibial(tibData.sort((a, b) => parseInt(a.size) - parseInt(b.size)));
      } catch (err: any) {
        console.error("Failed to fetch implants", err);
        setError("Failed to load implant database.");
      } finally {
        setLoading(false);
      }
    };
    
    fetchImplants();
  }, []);

  if (loading) return <div>Loading Implant Database...</div>;
  if (error) return <div className="error-banner">{error}</div>;

  return (
    <div className="implant-database-panel">
      <h2>Implant Database (Viewer)</h2>
      
      <div className="demo-warning">
        <strong>DEMONSTRATION IMPLANT DATABASE</strong>
        <p>Specifications are synthetic and are NOT for clinical or surgical use.</p>
      </div>

      <div className="tables-container">
        <div className="table-section">
          <h3>Femoral Components</h3>
          <table className="implant-table">
            <thead>
              <tr>
                <th>Size</th>
                <th>Width (mm)</th>
                <th>AP (mm)</th>
                <th>Source</th>
              </tr>
            </thead>
            <tbody>
              {femoral.map(imp => (
                <tr key={imp.id}>
                  <td>{imp.size}</td>
                  <td>{imp.width.toFixed(1)}</td>
                  <td>{imp.ap_dimension.toFixed(1)}</td>
                  <td>
                    {imp.source_type} 
                    {imp.is_demo && <span className="demo-badge">DEMO</span>}
                  </td>
                </tr>
              ))}
              {femoral.length === 0 && (
                <tr><td colSpan={4}>No femoral components found.</td></tr>
              )}
            </tbody>
          </table>
        </div>

        <div className="table-section">
          <h3>Tibial Components</h3>
          <table className="implant-table">
            <thead>
              <tr>
                <th>Size</th>
                <th>Width (mm)</th>
                <th>AP (mm)</th>
                <th>Source</th>
              </tr>
            </thead>
            <tbody>
              {tibial.map(imp => (
                <tr key={imp.id}>
                  <td>{imp.size}</td>
                  <td>{imp.width.toFixed(1)}</td>
                  <td>{imp.ap_dimension.toFixed(1)}</td>
                  <td>
                    {imp.source_type}
                    {imp.is_demo && <span className="demo-badge">DEMO</span>}
                  </td>
                </tr>
              ))}
              {tibial.length === 0 && (
                <tr><td colSpan={4}>No tibial components found.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
