import { useState } from "react";

function App() {
  const [message, setMessage] = useState("");
  const [products, setProducts] = useState([]);

  function handleSearch(event) {
    event.preventDefault();

    const formData = new FormData(event.target);

    const area = formData.get("area");
    const startDate = formData.get("startDate");
    const endDate = formData.get("endDate");
    const cloudCover = formData.get("cloudCover");

    setMessage(
      `Search requested for ${area} from ${startDate} to ${endDate} with maximum ${cloudCover}% cloud coverage.`
    );

    setProducts([
      {
        name: "S2A_MSIL2A_20250731_SAMPLE_001",
        date: "2025-07-31",
        cloudCover: "2.85%",
        status: "Available",
      },
      {
        name: "S2B_MSIL2A_20250726_SAMPLE_002",
        date: "2025-07-26",
        cloudCover: "6.10%",
        status: "Available",
      },
      {
        name: "S2A_MSIL2A_20250721_SAMPLE_003",
        date: "2025-07-21",
        cloudCover: "9.40%",
        status: "Available",
      },
    ]);
  }

  return (
    <main>
      <h1>EO Data Finder</h1>

      <p>
        Find Sentinel-2 satellite metadata for a selected area and period.
      </p>

      <section>
        <h2>Search criteria</h2>

        <form onSubmit={handleSearch}>
          <div>
            <label htmlFor="area">Search area</label>

            <select id="area" name="area">
              <option value="Mali">Mali</option>
              <option value="Bamako">Bamako</option>
              <option value="Kayes">Kayes</option>
              <option value="Sikasso">Sikasso</option>
            </select>
          </div>

          <div>
            <label htmlFor="start-date">Start date</label>

            <input id="start-date" name="startDate" type="date" />
          </div>

          <div>
            <label htmlFor="end-date">End date</label>

            <input id="end-date" name="endDate" type="date" />
          </div>

          <div>
            <label htmlFor="cloud-cover">
              Maximum cloud coverage (%)
            </label>

            <input
              id="cloud-cover"
              name="cloudCover"
              type="number"
              min="0"
              max="100"
              placeholder="For example: 10"
            />
          </div>

          <button type="submit">Search satellite data</button>
        </form>

        {message && <p>{message}</p>}
      </section>

      {products.length > 0 && (
        <section>
          <h2>Search results</h2>

          <table>
            <thead>
              <tr>
                <th>Product name</th>
                <th>Acquisition date</th>
                <th>Cloud coverage</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              {products.map((product) => (
                <tr key={product.name}>
                  <td>{product.name}</td>
                  <td>{product.date}</td>
                  <td>{product.cloudCover}</td>
                  <td>{product.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}
    </main>
  );
}

export default App;
