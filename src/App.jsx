import { useMemo, useState } from "react";
import { Navigate, useLocation, useNavigate } from "react-router";

const PILOT_AREAS = [
  { value: "sikasso", label: "Sikasso, Mali" },
];


const INITIAL_FORM = {
  area: "sikasso",
  startDate: "2025-07-01",
  endDate: "2025-08-01",
  maxCloud: "10",
  analysisType: "drought",
};

function App() {
  const [form, setForm] = useState(INITIAL_FORM);
  const [error, setError] = useState("");
  const [products, setProducts] = useState([]);
  const [searchCompleted, setSearchCompleted] = useState(false);
  const [selectedProductId, setSelectedProductId] = useState("");
  const [saveMessage, setSaveMessage] = useState("");
  const navigate = useNavigate();
  const location = useLocation();

  const isAnalysisPage = location.pathname === "/analysis";

  const selectedProduct = useMemo(
    () =>
      products.find((product) => product.id === selectedProductId) ?? null,
    [products, selectedProductId]
  );

  const selectedAreaLabel =
    PILOT_AREAS.find((area) => area.value === form.area)?.label ?? form.area;

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((currentForm) => ({
      ...currentForm,
      [name]: value,
    }));
  }

async function handleSearch(event) {
  event.preventDefault();

  setError("");
  setProducts([]);
  setSearchCompleted(false);
  setSelectedProductId("");
  setSaveMessage("");

  if (!form.area || !form.startDate || !form.endDate || !form.maxCloud) {
    setError("Please complete all search fields.");
    return;
  }

  if (form.startDate >= form.endDate) {
    setError("The end date must be after the start date.");
    return;
  }

  const cloudLimit = Number(form.maxCloud);

  if (
    Number.isNaN(cloudLimit) ||
    cloudLimit < 0 ||
    cloudLimit > 100
  ) {
    setError("Cloud coverage must be between 0 and 100.");
    return;
  }

  try {
    const params = new URLSearchParams({
      area: form.area,
      max_cloud: String(cloudLimit),
      start_date: form.startDate,
      end_date: form.endDate,
    });

    const response = await fetch(
      `http://127.0.0.1:8000/api/copernicus/products?${params.toString()}`
    );

    if (!response.ok) {
      throw new Error("API request failed");
    }

    const apiProducts = await response.json();

    setProducts(apiProducts);
    setSearchCompleted(true);
  } catch (error) {
    console.error(error);

    setError(
      "Unable to connect to the EO Data Finder backend."
    );
  }
}

  function handleSelectProduct(productId) {
    setSelectedProductId(productId);
    setSaveMessage("");
  }

  function handleOpenAnalysis() {
    if (!selectedProductId) {
      setError(
        "Please select a satellite product before opening the analysis."
      );
      return;
    }

    setError("");
    navigate("/analysis");
  }
  

async function handleSaveProduct() {
  if (!selectedProductId) return;

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/copernicus/products/${selectedProductId}/save`,
      { method: "POST" }
    );

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const result = await response.json();

    if (result.status === "saved") {
      setSaveMessage("Product saved successfully.");
    } else {
      setSaveMessage("This product is already saved.");
    }
  } catch (error) {
    console.error(error);
    alert("Unable to save the product.");
  }
}

  if (isAnalysisPage && !selectedProduct) {
    return <Navigate to="/" replace />;
}

  return (
    <main className="app-shell">
      <header className="app-header s2-header">
        <div className="header-main">
          <p className="eyebrow">Earth Observation Workspace</p>

          
        <div className="s3-brand">
          
<span className="s3-brand-icon" aria-hidden="true">
  <svg
    viewBox="0 0 80 80"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <g
      transform="rotate(-22 40 40)"
      stroke="currentColor"
      strokeWidth="2.4"
      strokeLinejoin="round"
      strokeLinecap="round"
    >
      {/* Left solar panel */}
      <rect
        x="5"
        y="28"
        width="20"
        height="24"
        rx="2"
        fill="currentColor"
        fillOpacity="0.18"
      />
      <path d="M11.7 28V52M18.3 28V52M5 36H25M5 44H25" />

      {/* Right solar panel */}
      <rect
        x="55"
        y="28"
        width="20"
        height="24"
        rx="2"
        fill="currentColor"
        fillOpacity="0.18"
      />
      <path d="M61.7 28V52M68.3 28V52M55 36H75M55 44H75" />

      {/* Connectors */}
      <path d="M25 40H31M49 40H55" />

      {/* Satellite body */}
      <rect
        x="31"
        y="29"
        width="18"
        height="22"
        rx="3"
        fill="currentColor"
        fillOpacity="0.3"
      />
      <path d="M36 34H44M36 40H44M36 46H44" />

      {/* Antenna */}
      <path d="M40 29V17" />
      <circle cx="40" cy="13" r="3" fill="currentColor" />
    </g>
  </svg>
</span>

          <h1>EO Data Finder</h1>
        </div>


          <p className="header-description">
            Search and review Sentinel-2 products for environmental monitoring
            and prepare interpretable vegetation and drought-risk analysis.
          </p>

          <div className="header-tags">
            <span>Sentinel-2</span>
            <span>Vegetation monitoring</span>
            <span>Environmental analytics</span>
          </div>
        </div>

        <div className="header-badge">S3 · Geospatial Workspace</div>
      </header>

      
<nav className="s3-navigation" aria-label="Main navigation">
  <button
    type="button"
    className={!isAnalysisPage ? "active" : ""}
    onClick={() => navigate("/")}
  >
    Satellite Catalogue
  </button>

  <button
    type="button"
    className={isAnalysisPage ? "active" : ""}
    onClick={handleOpenAnalysis}
    disabled={!selectedProduct}
  >
    Analysis Workspace
  </button>
</nav>

{!isAnalysisPage && (
  <>

      <div className="prototype-notice s2-notice">
        <strong>Sprint 3 — Geospatial Workspace:</strong>
          <span>
            React is connected to FastAPI and SQLite. Satellite product searches
            support acquisition dates and cloud coverage, with Sikasso as the
            pilot area. Product metadata and drought analysis remain
            demonstrations; live satellite catalogue integration is planned
            for a future sprint.
          </span>
      </div>

      <section className="search-card">
        <div className="section-heading">
          <div>
            <p className="step-label">01 · Search</p>
            <h2>Satellite data search</h2>
            <p className="section-description">
              Define the geographic area, acquisition period and maximum cloud
              coverage.
            </p>
          </div>

          <span className="status-label">Integrated MVP</span>
        </div>

        <form onSubmit={handleSearch}>
          <div className="form-grid">
            <div className="form-field">
              <label htmlFor="area">Pilot area</label>

              <select
                id="area"
                name="area"
                value={form.area}
                onChange={handleChange}
              >
                {PILOT_AREAS.map((area) => (
                  <option key={area.value} value={area.value}>
                    {area.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-field">
              <label htmlFor="startDate">Start date</label>

              <input
                id="startDate"
                name="startDate"
                type="date"
                value={form.startDate}
                onChange={handleChange}
              />
            </div>

            <div className="form-field">
              <label htmlFor="endDate">End date</label>

              <input
                id="endDate"
                name="endDate"
                type="date"
                value={form.endDate}
                onChange={handleChange}
              />
            </div>

            <div className="form-field">
              <label htmlFor="maxCloud">
                Maximum cloud coverage (%)
              </label>

              <input
                id="maxCloud"
                name="maxCloud"
                type="number"
                min="0"
                max="100"
                step="1"
                value={form.maxCloud}
                onChange={handleChange}
              />
            </div>

            <div className="form-field form-field-wide">
              <label htmlFor="analysisType">Analysis module</label>

              <select
                id="analysisType"
                name="analysisType"
                value={form.analysisType}
                onChange={handleChange}
              >
                <option value="drought">
                  Vegetation and experimental drought-risk monitoring
                </option>
              </select>

              <small>
                Semester scope: one environmental use case and one limited pilot
                workflow.
              </small>
            </div>
          </div>

          <div className="form-actions">
            <button className="primary-button" type="submit">
              Search satellite products
            </button>
          </div>
        </form>

        {error && (
          <p className="message error-message" role="alert">
            {error}
          </p>
        )}
      </section>

      {searchCompleted && (
        <section className="results-card">
          <div className="section-heading">
            <div>
              <p className="step-label">02 · Products</p>
              <h2>Available satellite products</h2>
              <p className="section-description">
                Review the matching Sentinel-2 products and select one for the
                analysis workspace.
              </p>
            </div>

            <span className="result-count">
              {products.length} {products.length === 1 ? "product" : "products"}
            </span>
          </div>

          <div className="search-summary-chips">
            <span>
              Area <strong>{selectedAreaLabel}</strong>
            </span>

            <span>
              Period{" "}
              <strong>
                {form.startDate} → {form.endDate}
              </strong>
            </span>

            <span>
              Cloud ≤ <strong>{form.maxCloud}%</strong>
            </span>

            <span className="demo-chip">Copernicus data · SQLite</span>
          </div>

          {products.length === 0 ? (
            <p className="empty-message">
              No demonstration products match the selected search criteria.
              Try adjusting the acquisition dates or increasing the maximum
              cloud coverage.
            </p>

          ) : (
            <>
              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>Select</th>
                      <th>Product name</th>
                      <th>Acquisition date</th>
                      <th>Product type</th>
                      <th>Cloud coverage</th>
                      <th>Availability</th>
                    </tr>
                  </thead>

                  <tbody>
                    {products.map((product) => (
                      <tr
                        key={product.id}
                        className={
                          selectedProductId === product.id
                            ? "selected-row"
                            : ""
                        }
                      >
                        <td>
                          <input
                            className="product-radio"
                            type="radio"
                            name="selectedProduct"
                            aria-label={`Select ${product.name}`}
                            checked={selectedProductId === product.id}
                            onChange={() =>
                              handleSelectProduct(product.id)
                            }
                          />
                        </td>

                        <td className="product-name">{product.name}</td>

                        <td>{product.acquisitionDate}</td>

                        <td>{product.productType}</td>

                        <td>{Number(product.cloudCover).toFixed(2)}%</td>

                        <td>
                          <span className="available-label">
                            {product.availability}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="results-actions">
                
<div className="selection-help">
  {selectedProduct ? (
    <div className="s3-selected-product">
      <strong>{selectedProduct.name}</strong>
      <span>
        {selectedProduct.acquisitionDate} ·
        {" "}{selectedProduct.productType} ·
        {" "}Cloud {selectedProduct.cloudCover}%
      </span>
    </div>
  ) : (
    "Select one product to continue."
  )}
</div>

                <button
                  className="secondary-button"
                  type="button"
                  onClick={handleSaveProduct}
                  disabled={!selectedProductId}
                >
                  Save Product
                </button>


                <button
                  className="secondary-button"
                  type="button"
                  onClick={handleOpenAnalysis}
                  disabled={!selectedProductId}
                >
                  Open analysis workspace
                </button>
              </div>
              
{saveMessage && (
  <p className="s3-save-message" role="status">
    {saveMessage}
  </p>
)}

            </>
          )}
        </section>
      )}
    </>
  )}
      {isAnalysisPage && selectedProduct && (
        <section className="analysis-card">
          <button
  type="button"
  className="s3-back-button"
  onClick={() => navigate("/")}
>
  ← Back to Satellite Catalogue
</button>
          <div className="section-heading">
            <div>
              <p className="step-label">03 · Analysis</p>
              <h2>Vegetation & drought analysis</h2>

              <p className="section-description">
                Visual preview of the analysis workspace planned for the Python
                processing pipeline.
              </p>
            </div>

            <span className="status-label warning-label">
              Experimental
            </span>
          </div>

          <div className="analysis-product-bar">
            <div>
              <span>Selected Sentinel-2 product</span>
              <strong>{selectedProduct.name}</strong>
            </div>

            <div className="analysis-product-meta">
              <span>{selectedProduct.acquisitionDate}</span>
              <span>{selectedProduct.cloudCover}% cloud</span>
              <span>{selectedAreaLabel}</span>
            </div>
          </div>

          <div className="analysis-layout">
            <article className="map-panel">
              <div className="panel-title">
                <div>
                  <p className="step-label">Vegetation indicator</p>
                  <h3>NDVI condition map</h3>
                </div>

                <span className="demo-label-inline">Simulated</span>
              </div>

              <div className="simulated-map">
                <div className="map-location">
                  <span>Pilot area</span>
                  <strong>{selectedAreaLabel}</strong>
                </div>

                <div className="map-status">
                  SIMULATED NDVI SURFACE
                </div>
              </div>

              <div className="legend">
                <span>
                  <i className="legend-color low-color" />
                  Low vegetation
                </span>

                <span>
                  <i className="legend-color moderate-color" />
                  Moderate
                </span>

                <span>
                  <i className="legend-color healthy-color" />
                  Healthy
                </span>
              </div>
            </article>

            <div className="analysis-details">
              <div className="metrics-grid">
                <article className="metric-card">
                  <span>Mean NDVI</span>
                  <strong className="green-value">0.42</strong>
                  <small>Demonstration value</small>
                </article>

                <article className="metric-card">
                  <span>Rainfall anomaly</span>
                  <strong className="orange-value">−18%</strong>
                  <small>Demonstration value</small>
                </article>

                <article className="metric-card">
                  <span>Drought risk</span>
                  <strong className="risk-value">Moderate</strong>
                  <small>Experimental estimate</small>
                </article>
              </div>

              <article className="indicator-panel">
                <div className="indicator-heading">
                  <div>
                    <p className="step-label">Indicators</p>
                    <h3>Observed conditions</h3>
                  </div>

                  <span className="demo-label-inline">
                    Demo values
                  </span>
                </div>

                <div className="indicator-row">
                  <span>Vegetation condition</span>

                  <div className="progress-track">
                    <div className="progress-fill vegetation-progress" />
                  </div>

                  <strong>42%</strong>
                </div>

                <div className="indicator-row">
                  <span>Rainfall level</span>

                  <div className="progress-track">
                    <div className="progress-fill rainfall-progress" />
                  </div>

                  <strong>32%</strong>
                </div>

                <div className="indicator-row">
                  <span>Model confidence</span>

                  <div className="progress-track">
                    <div className="progress-fill confidence-progress" />
                  </div>

                  <strong>N/A</strong>
                </div>

                <p className="validation-note">
                  A real confidence score will only be displayed after the
                  Python model has been trained, tested and validated using
                  historical data.
                </p>
              </article>
            </div>
          </div>

          <div className="data-sources-heading">
            <p className="step-label">Processing pipeline</p>
            <h3>Planned data sources</h3>
          </div>

          <div className="data-sources">
            <div>
              <span>Satellite source</span>
              <strong>Sentinel-2 Level-2A</strong>
              <small>Copernicus Data Space</small>
            </div>

            <div>
              <span>Rainfall source</span>
              <strong>CHIRPS</strong>
              <small>Historical precipitation data</small>
            </div>

            <div>
              <span>Processing</span>
              <strong>Python · NDVI · analytics</strong>
              <small>Experimental interpretation</small>
            </div>
          </div>

          <p className="analysis-disclaimer">
            This interface currently contains simulated analysis values. It
            must not be interpreted as an operational drought warning or a
            scientifically validated environmental assessment.
          </p>
        </section>
      )}

      <footer className="app-footer">
        EO Data Finder · Sprint 3 · Geospatial Intelligence Workspace
      </footer>
    </main>
  );
}

export default App;