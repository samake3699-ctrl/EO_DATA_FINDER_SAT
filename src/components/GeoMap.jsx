
import { useEffect } from "react";

import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Tooltip,
  useMap,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

// Geographic coordinates
const SIKASSO = [11.31755, -5.66654];

// Approximate viewing bounds of Mali
const MALI_BOUNDS = [
  [10.1, -12.3],
  [25.1, 4.3],
];

// Controls automatic map movement
function MapController({ searchCompleted }) {
  const map = useMap();

  useEffect(() => {
    if (searchCompleted) {
      // Zoom automatically to Sikasso
      map.flyTo(SIKASSO, 10, {
        animate: true,
        duration: 1.5,
      });
    } else {
      // Return to the general Mali view
      map.fitBounds(MALI_BOUNDS, {
        padding: [20, 20],
      });
    }
  }, [map, searchCompleted]);

  return null;
}

// Main map component
export default function GeoMap({ searchCompleted = false }) {
  return (
    <section className="s4-map-card">

      <div className="s4-map-heading">
        <div>
          <p className="step-label">
            Geographic workspace
          </p>

          <h2>Geographic preview</h2>

          <p className="section-description">
            {searchCompleted
              ? "Search location: Sikasso, Mali"
              : "Explore Mali and the surrounding region."}
          </p>
        </div>
      </div>

      <div className="s4-map-canvas">
        <MapContainer
          bounds={MALI_BOUNDS}
          boundsOptions={{
            padding: [20, 20],
          }}
          minZoom={3}
          maxZoom={18}
          scrollWheelZoom={true}
          className="s4-leaflet-map"
        >

          <TileLayer
            attribution="&copy; OpenStreetMap contributors"
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          <MapController
            searchCompleted={searchCompleted}
          />

          {searchCompleted && (
            <>
              <CircleMarker
                center={SIKASSO}
                radius={22}
                pathOptions={{
                  color: "#087a4c",
                  weight: 3,
                  fillColor: "#38b879",
                  fillOpacity: 0.25,
                }}
              >
                <Tooltip
                  permanent
                  direction="top"
                  offset={[0, -15]}
                >
                  Sikasso — Search location
                </Tooltip>
              </CircleMarker>

              <CircleMarker
                center={SIKASSO}
                radius={6}
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
    </section>
  );
}
