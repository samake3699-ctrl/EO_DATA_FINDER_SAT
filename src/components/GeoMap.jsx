
import { useEffect, useState } from "react";
import L from "leaflet";

import {
  MapContainer,
  TileLayer,
  GeoJSON,
  CircleMarker,
  Tooltip,
  useMap,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

// Same search point as the Copernicus backend
const SIKASSO = [11.31755, -5.66654];

const MALI_BOUNDS = [
  [10.1, -12.3],
  [25.1, 4.3],
];

const MALI_STYLE = {
  color: "#168653",
  weight: 2.5,
  fillColor: "#62bd7a",
  fillOpacity: 0.18,
};

const FOOTPRINT_STYLE = {
  color: "#f28c28",
  weight: 3,
  fillColor: "#f28c28",
  fillOpacity: 0.12,
  dashArray: "7 4",
};

function getGeometryBounds(geometry) {
  try {
    if (!geometry) return null;

    const bounds = L.geoJSON(geometry).getBounds();
    return bounds.isValid() ? bounds : null;
  } catch (error) {
    console.error("Invalid geographic geometry:", error);
    return null;
  }
}

function MapController({
  searchCompleted,
  maliBoundary,
  footprint,
  resetRequest,
}) {
  const map = useMap();

  // Automatically frame the selected data
  useEffect(() => {
    const footprintBounds = getGeometryBounds(footprint);

    if (footprintBounds) {
      map.flyToBounds(footprintBounds, {
        padding: [35, 35],
        maxZoom: 11,
        duration: 1.2,
      });
      return;
    }

    if (searchCompleted) {
      map.flyTo(SIKASSO, 10, {
        duration: 1.2,
      });
      return;
    }

    const maliBounds = getGeometryBounds(maliBoundary);

    if (maliBounds) {
      map.fitBounds(maliBounds, {
        padding: [15, 15],
        maxZoom: 6,
      });
    }
  }, [map, searchCompleted, maliBoundary, footprint]);

  // Explicit return to the Mali overview
  useEffect(() => {
    if (resetRequest === 0) return;

    const bounds =
      getGeometryBounds(maliBoundary) ??
      L.latLngBounds(MALI_BOUNDS);

    map.flyToBounds(bounds, {
      padding: [15, 15],
      maxZoom: 6,
      duration: 1.2,
    });
  }, [map, maliBoundary, resetRequest]);

  return null;
}

export default function GeoMap({
  searchCompleted = false,
  selectedProduct = null,
}) {
  const [maliBoundary, setMaliBoundary] = useState(null);
  const [boundaryError, setBoundaryError] = useState(false);
  const [resetRequest, setResetRequest] = useState(0);
  const [baseLayer, setBaseLayer] = useState("map");

  const footprint = selectedProduct?.geoFootprint ?? null;
  const footprintBounds = getGeometryBounds(footprint);
  const validFootprint = footprintBounds ? footprint : null;

  useEffect(() => {
    const controller = new AbortController();

    fetch("/geo/mali.geojson", {
      signal: controller.signal,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to load Mali boundary");
        }
        return response.json();
      })
      .then((data) => {
        setMaliBoundary(data);
        setBoundaryError(false);
      })
      .catch((error) => {
        if (error.name !== "AbortError") {
          console.error(error);
          setBoundaryError(true);
        }
      });

    return () => controller.abort();
  }, []);

  return (
    <section className="s4-map-card">
      <div className="s4-map-heading">
        <div>
          <p className="step-label">
            Geographic workspace
          </p>
          <h2>Geographic preview</h2>
        </div>

        <div style={{
          display: "flex",
          gap: "6px",
          flexWrap: "wrap",
        }}>
          <button
            type="button"
            className="s4-reset-map"
            onClick={() => setBaseLayer("map")}
            aria-pressed={baseLayer === "map"}
            style={{
              background: baseLayer === "map"
                ? "#ccebd9"
                : "#e5f3e9",
            }}
          >
            Map
          </button>

          <button
            type="button"
            className="s4-reset-map"
            onClick={() => setBaseLayer("satellite")}
            aria-pressed={baseLayer === "satellite"}
            style={{
              background: baseLayer === "satellite"
                ? "#ccebd9"
                : "#e5f3e9",
            }}
          >
            Satellite
          </button>

          <button
            type="button"
            className="s4-reset-map"
            onClick={() => setResetRequest((n) => n + 1)}
          >
            View Mali
          </button>
        </div>
      </div>

      <div className="s4-map-canvas">
        <MapContainer
          bounds={MALI_BOUNDS}
          boundsOptions={{ padding: [15, 15] }}
          minZoom={3}
          maxZoom={18}
          scrollWheelZoom={true}
          className="s4-leaflet-map"
        >
          {baseLayer === "map" ? (
            <TileLayer
              key="osm"
              attribution="&copy; OpenStreetMap contributors"
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
          ) : (
            <TileLayer
              key="esri"
              attribution="Imagery &copy; Esri and its data providers"
              url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
            />
          )}

          <MapController
            searchCompleted={searchCompleted}
            maliBoundary={maliBoundary}
            footprint={validFootprint}
            resetRequest={resetRequest}
          />

          {maliBoundary && (
            <GeoJSON
              data={maliBoundary}
              style={MALI_STYLE}
            />
          )}

          {validFootprint && (
            <GeoJSON
              key={selectedProduct.id}
              data={validFootprint}
              style={FOOTPRINT_STYLE}
            >
              <Tooltip>
                Sentinel-2 product footprint
              </Tooltip>
            </GeoJSON>
          )}

          {searchCompleted && (
            <>
              <CircleMarker
                center={SIKASSO}
                radius={15}
                pathOptions={{
                  color: "#087a4c",
                  weight: 3,
                  fillColor: "#38b879",
                  fillOpacity: 0.2,
                }}
              >
                <Tooltip permanent direction="top">
                  Sikasso · Search point
                </Tooltip>
              </CircleMarker>

              <CircleMarker
                center={SIKASSO}
                radius={5}
                pathOptions={{
                  color: "#ffffff",
                  weight: 2,
                  fillColor: "#087a4c",
                  fillOpacity: 1,
                }}
              />
            </>
          )}
        </MapContainer>
      </div>

      <div className="s4-map-info-grid">
        <div className="s4-map-info-item">
          <span className="s4-map-info-icon">🇲🇱</span>
          <div>
            <small>Country</small>
            <strong>Mali</strong>
          </div>
        </div>

        <div className="s4-map-info-item">
          <span className="s4-map-info-icon">⌖</span>
          <div>
            <small>Pilot area</small>
            <strong>Sikasso</strong>
          </div>
        </div>

        <div className="s4-map-info-item">
          <span className="s4-map-info-icon">▧</span>
          <div>
            <small>Product footprint</small>
            <strong>
              {validFootprint
                ? "Visible"
                : "Not selected"}
            </strong>
          </div>
        </div>

        <div className="s4-map-info-item">
          <span className="s4-map-info-icon">⊕</span>
          <div>
            <small>Map layer</small>
            <strong>
              {baseLayer === "map"
                ? "Street map"
                : "Satellite"}
            </strong>
          </div>
        </div>
      </div>

      {selectedProduct && !validFootprint && (
        <p className="validation-note">
          The selected product has no valid
          geographic footprint available.
        </p>
      )}

      {boundaryError && (
        <p className="message error-message" role="alert">
          Mali boundary could not be loaded.
        </p>
      )}
    </section>
  );
}
