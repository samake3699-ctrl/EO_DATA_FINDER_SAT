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

const VEGETATION_CELLS = [
  "low",
  "low",
  "moderate",
  "moderate",
  "healthy",
  "healthy",
  "low",
  "moderate",
  "healthy",
  "healthy",
  "moderate",
  "low",
  "moderate",
  "healthy",
  "healthy",
  "moderate",
  "low",
  "low",
  "healthy",
  "healthy",
  "moderate",
  "moderate",
  "low",
  "low",
  "healthy",
  "moderate",
  "moderate",
  "low",
  "low",
  "moderate",
  "moderate",
  "healthy",
  "healthy",
  "moderate",
  "low",
  "low",
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
      setError("Please select a satellite product before opening the analysis.");
      return;
    }

    setError("");
    setShowAnalysis(true);
  }

  return (
    <main className="app-shell">
      <header className="app-header">
        <div>
          <p className="eyebrow">Earth observation application</p>
          <h1>EO Data Finder</h1>
          <p className="header-description">
            Find Sentinel-2 data and prepare an experimental drought-risk
            analysis for a selected pilot area.
          </p>
        </div>

        <div className="header-badge">
          Semester MVP
        </div>
      </header>

      <div className="prototype-notice">
        <strong>S1 prototype:</strong> the satellite products and drought
        indicators displayed on this page are demonstration data. No real
        satellite image processing is performed during S1.
      </div>

      <section className="search-card">
        <div className="section-heading">
          <div>
            <p className="step-label">Step 1</p>
            <h2>Search criteria</h2>
          </div>

          <span className="status-label">Local prototype</span>
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
                Flood mapping and crop-yield prediction are outside the
                semester MVP.
              </small>
            </div>
          </div>

          <button className="primary-button" type="submit">
            Search satellite products
          </button>
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
              <p className="step-label">Step 2</p>
              <h2>Satellite products</h2>
            </div>

            <span className="status-label demo-label">Demo data</span>
          </div>

          <p className="search-summary">
            Area: <strong>{selectedAreaLabel}</strong> · Period:{" "}
            <strong>
              {form.startDate} to {form.endDate}
            </strong>{" "}
            · Maximum cloud coverage:{" "}
            <strong>{form.maxCloud}%</strong>
          </p>

          {products.length === 0 ? (
            <p className="empty-message">
              No demonstration product matches this cloud coverage limit.
              Try a value of 10%.
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

              <button
                className="secondary-button"
                type="button"
                onClick={handleOpenAnalysis}
                disabled={!selectedProductId}
              >
                Open drought analysis preview
              </button>
            </>
          )}
        </section>
      )}

      {showAnalysis && selectedProduct && (
        <section className="analysis-card">
          <div className="section-heading">
            <div>
              <p className="step-label">Step 3</p>
              <h2>Experimental drought-risk preview</h2>
            </div>

            <span className="status-label warning-label">
              Requires validation
            </span>
          </div>

          <p className="analysis-description">
            This S1 screen previews the result expected from the future Python
            processing module. The values below are simulated and must not be
            interpreted as a real environmental assessment.
          </p>

          <div className="selected-product">
            <span>Selected product</span>
            <strong>{selectedProduct.name}</strong>
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

              <div
                className="vegetation-grid"
                aria-label="Simulated vegetation condition map"
              >
                {VEGETATION_CELLS.map((condition, index) => (
                  <span
                    key={`${condition}-${index}`}
                    className={`vegetation-cell ${condition}`}
                  />
                ))}
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
                  <strong className="orange-value">-18%</strong>
                  <small>Demonstration value</small>
                </article>

                <article className="metric-card">
                  <span>One-month drought risk</span>
                  <strong className="risk-value">Moderate</strong>
                  <small>Experimental estimate</small>
                </article>
              </div>

              <article className="indicator-panel">
                <h3>Observed indicators</h3>

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
                  A real confidence score will only be shown after the Python
                  model has been trained, tested, and validated with historical
                  data.
                </p>
              </article>
            </div>
          </div>

          <div className="data-sources">
            <div>
              <span>Planned satellite source</span>
              <strong>Sentinel-2 Level-2A</strong>
            </div>

            <div>
              <span>Planned rainfall source</span>
              <strong>CHIRPS historical rainfall</strong>
            </div>

            <div>
              <span>Planned processing</span>
              <strong>Python, NDVI and interpretable model</strong>
            </div>
          </div>
        </section>
      )}

      <footer className="app-footer">
        EO Data Finder · S1 local interface prototype
      </footer>
    </main>
  );
}

export default App;
