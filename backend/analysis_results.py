from statistics import mean
from pathlib import Path
import json

import numpy as np
import rasterio


DATA_DIR = Path(__file__).parent / "data"

NDVI_FILE = (
    DATA_DIR
    / "sentinel2"
    / "sikasso_20251028_ndvi.tif"
)


def get_ndvi_results():
    if not NDVI_FILE.exists():
        raise FileNotFoundError(
            f"NDVI file not found: {NDVI_FILE}"
        )

    with rasterio.open(NDVI_FILE) as src:
        # Read the raster and exclude NoData pixels
        ndvi = src.read(1, masked=True)

        # Keep only valid numeric values
        valid_values = ndvi.compressed()
        valid_values = valid_values[
            np.isfinite(valid_values)
        ]

        if valid_values.size == 0:
            raise ValueError(
                "No valid NDVI pixels found."
            )

        return {
            "pilotArea": "Sikasso, Mali",
            "acquisitionDate": "2025-10-28",
            "source": "Sentinel-2 Level-2A",
            "ndvi": {
                "minimum": round(
                    float(valid_values.min()), 4
                ),
                "maximum": round(
                    float(valid_values.max()), 4
                ),
                "mean": round(
                    float(valid_values.mean()), 4
                ),
                "validPixels": int(valid_values.size),
                "totalPixels": int(
                    src.width * src.height
                )
            },
            "geography": {
                "crs": str(src.crs),
                "bounds": list(src.bounds)
            }
        }


# CHIRPS rainfall results for the Sikasso pilot point

CHIRPS_DIR = DATA_DIR / "chirps"

LONGITUDE = -5.66654
LATITUDE = 11.31755


def read_chirps_rainfall(year):
    file_path = (
        CHIRPS_DIR / f"chirps-v3.0.{year}.10.tif"
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"Missing CHIRPS file: {file_path.name}"
        )

    with rasterio.open(file_path) as src:
        if src.crs is None or src.crs.to_epsg() != 4326:
            raise ValueError(
                f"Invalid CHIRPS coordinate system: {year}"
            )

        if not (
            src.bounds.left <= LONGITUDE < src.bounds.right
            and src.bounds.bottom < LATITUDE <= src.bounds.top
        ):
            raise ValueError(
                f"Sikasso is outside CHIRPS raster: {year}"
            )

        value = next(
            src.sample(
                [(LONGITUDE, LATITUDE)],
                masked=True
            )
        )[0]

        if np.ma.is_masked(value):
            raise ValueError(
                f"Missing CHIRPS rainfall value: {year}"
            )

        rainfall = float(value)

        if not np.isfinite(rainfall) or rainfall < 0:
            raise ValueError(
                f"Invalid CHIRPS rainfall value: {year}"
            )

        return rainfall


def get_chirps_results():
    # Read October rainfall values from 1991 to 2025
    rainfall = {
        year: read_chirps_rainfall(year)
        for year in range(1991, 2026)
    }

    observed = rainfall[2025]

    def calculate_reference(start_year, end_year):
        historical_average = mean(
            rainfall[year]
            for year in range(start_year, end_year + 1)
        )

        anomaly_mm = observed - historical_average
        anomaly_percent = (
            anomaly_mm / historical_average * 100
            if historical_average > 0
            else None
        )

        return {
            "period": f"{start_year}-{end_year}",
            "averageMm": round(historical_average, 2),
            "anomalyMm": round(anomaly_mm, 2),
            "anomalyPercent": (
                round(anomaly_percent, 2)
                if anomaly_percent is not None
                else None
            )
        }

    return {
        "pilotArea": "Sikasso, Mali",
        "source": "CHIRPS v3",
        "analysisMonth": "2025-10",
        "observedRainfallMm": round(observed, 2),
        "primaryReference": calculate_reference(
            1991, 2020
        ),
        "secondaryReference": calculate_reference(
            1995, 2024
        )
    }


if __name__ == "__main__":
    results = {
        "ndviAnalysis": get_ndvi_results(),
        "rainfallAnalysis": get_chirps_results()
    }

    print(json.dumps(results, indent=4))