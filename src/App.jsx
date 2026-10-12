import { useMemo, useState } from "react";

const PILOT_AREAS = [
  { value: "mali", label: "Mali" },
  { value: "bamako", label: "Bamako" },
  { value: "kayes", label: "Kayes" },
  { value: "sikasso", label: "Sikasso" },
  { value: "mopti", label: "Mopti" },
  { value: "gao", label: "Gao" },
];

const DEMO_PRODUCTS = [
  {
    id: "demo-001",
    name: "S2A_MSIL2A_20250731_DEMO_001",
    acquisitionDate: "2025-07-31",
    productType: "Sentinel-2 Level-2A",
    cloudCover: 2.85,
    availability: "Available",
  },
  {
    id: "demo-002",
    name: "S2B_MSIL2A_20250726_DEMO_002",
    acquisitionDate: "2025-07-26",
    productType: "Sentinel-2 Level-2A",
    cloudCover: 6.1,
    availability: "Available",
  },
  {
    id: "demo-003",
    name: "S2A_MSIL2A_20250721_DEMO_003",
    acquisitionDate: "2025-07-21",
    productType: "Sentinel-2 Level-2A",
    cloudCover: 9.4,
    availability: "Available",
  },
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
  const [showAnalysis, setShowAnalysis] = useState(false);

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

  function handleSearch(event) {
    event.preventDefault();

    setError("");
    setProducts([]);
    setSearchCompleted(false);
    setSelectedProductId("");
    setShowAnalysis(false);

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

    const filteredProducts = DEMO_PRODUCTS.filter(
      (product) => product.cloudCover <= cloudLimit
    );

    setProducts(filteredProducts);
    setSearchCompleted(true);
  }

  function handleSelectProduct(productId) {
    setSelectedProductId(productId);
    setShowAnalysis(false);
  }

  function handleOpenAnalysis() {
    if (!selectedProductId) {
      setError(
        "Please select a satellite product before opening the analysis."
      );
      return;
    }

    setError("");
    setShowAnalysis(true);
  }

  return (
    <main className="app-shell">
      <header className="app-header s2-header">
        <div className="header-main">
          <p className="eyebrow">Earth Observation Workspace</p>

          <h1>EO Data Finder</h1>

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

        <div className="header-badge">S2 · MVP workspace</div>
      </header>

      <div className="prototype-notice s2-notice">
        <strong>S2 interface preview:</strong>
        <span>
          satellite products are still demonstration data while the Python
          backend, database and catalogue integration are being prepared.
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

          <span className="status-label">Frontend ready</span>
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

            <span className="demo-chip">Demo catalogue</span>
          </div>

          {products.length === 0 ? (
            <p className="empty-message">
              No demonstration product matches this cloud coverage limit. Try a
              value of 10%.
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

                        <td>{product.cloudCover}%</td>

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
                  {selectedProduct
                    ? `Selected: ${selectedProduct.name}`
                    : "Select one product to continue."}
                </div>

                <button
                  className="secondary-button"
                  type="button"
                  onClick={handleOpenAnalysis}
                  disabled={!selectedProductId}
                >
                  Open analysis workspace
                </button>
              </div>
            </>
          )}
        </section>
      )}

      {showAnalysis && selectedProduct && (
        <section className="analysis-card">
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
        EO Data Finder · S2 preparation · Earth Observation MVP
      </footer>
    </main>
  );
}

export default App;