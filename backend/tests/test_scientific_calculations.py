"""Numerical regression tests for EO Data Finder Sprint 4.

These tests use synthetic data; no Copernicus credentials or CHIRPS downloads
are needed. Copy this file into backend/tests/ and run pytest from backend/.
"""

import json

import matplotlib
matplotlib.use("Agg")  # Use a headless backend to generate PNGs during tests.

import numpy as np
import pytest
import rasterio
from rasterio.transform import from_origin

import analysis_results as rainfall_module
import calculate_selected_ndvi as ndvi_module


PRODUCT_ID = "11111111-1111-4111-8111-111111111111"


def write_fake_satellite_scene(folder, red, nir, data_mask, scl):
    """Create a minimal four-band raster and matching product metadata."""
    raster_path = folder / f"{PRODUCT_ID}_with_scl.tif"
    with rasterio.open(
        raster_path,
        "w",
        driver="GTiff",
        width=2,
        height=2,
        count=4,
        dtype="float32",
        crs="EPSG:4326",
        transform=from_origin(-5.68, 11.33, 0.0001, 0.0001),
    ) as dst:
        for band_number, values in enumerate(
            (red, nir, data_mask, scl), start=1
        ):
            dst.write(np.asarray(values, dtype=np.float32), band_number)

    (folder / f"{PRODUCT_ID}_metadata.json").write_text(
        json.dumps({
            "productId": PRODUCT_ID,
            "productName": "S2A_MSIL2A_SYNTHETIC_TEST.SAFE",
            "acquisitionDate": "2025-10-20",
        }),
        encoding="utf-8",
    )


def test_ndvi_formula_and_valid_pixel_filtering(tmp_path, monkeypatch):
    """NDVI = 0.50 and 0.20 on valid pixels; other pixels are masked."""
    monkeypatch.setattr(ndvi_module, "DATA_DIR", tmp_path)

    write_fake_satellite_scene(
        tmp_path,
        red=[[0.2, 0.4], [0.2, 0.1]],
        nir=[[0.6, 0.6], [0.8, 0.3]],
        data_mask=[[1, 1], [1, 0]],
        scl=[[4, 5], [3, 4]],
    )

    result = ndvi_module.calculate_selected_ndvi(PRODUCT_ID)

    assert result["ndvi"]["validPixels"] == 2
    assert result["ndvi"]["totalPixels"] == 4
    assert result["ndvi"]["minimum"] == pytest.approx(0.2)
    assert result["ndvi"]["maximum"] == pytest.approx(0.5)
    assert result["ndvi"]["mean"] == pytest.approx(0.35)

    with rasterio.open(tmp_path / f"{PRODUCT_ID}_ndvi.tif") as src:
        raster = src.read(1)
        assert raster[0, 0] == pytest.approx(0.5)
        assert raster[0, 1] == pytest.approx(0.2)
        assert np.isnan(raster[1, 0])  # SCL 3 excluded
        assert np.isnan(raster[1, 1])  # dataMask 0 excluded

    assert (tmp_path / f"{PRODUCT_ID}_ndvi_preview.png").is_file()
    assert (tmp_path / f"{PRODUCT_ID}_analysis.json").is_file()


def test_ndvi_rejects_scene_without_valid_pixels(tmp_path, monkeypatch):
    """A scene with no accepted SCL classes cannot produce valid NDVI."""
    monkeypatch.setattr(ndvi_module, "DATA_DIR", tmp_path)

    write_fake_satellite_scene(
        tmp_path,
        red=[[0.2, 0.2], [0.2, 0.2]],
        nir=[[0.6, 0.6], [0.6, 0.6]],
        data_mask=[[1, 1], [1, 1]],
        scl=[[3, 3], [3, 3]],
    )

    with pytest.raises(ValueError, match="No valid NDVI pixels"):
        ndvi_module.calculate_selected_ndvi(PRODUCT_ID)


def test_chirps_anomalies_with_known_historical_values(monkeypatch):
    """Verify both reference periods without requiring 35 large GeoTIFFs."""
    def fake_october_rainfall(year):
        if year == 2025:
            return 50.0
        if year >= 2021:
            return 200.0
        return 100.0

    monkeypatch.setattr(
        rainfall_module, "read_chirps_rainfall", fake_october_rainfall
    )

    result = rainfall_module.get_chirps_results()
    primary = result["primaryReference"]
    secondary = result["secondaryReference"]

    assert result["analysisMonth"] == "2025-10"
    assert result["observedRainfallMm"] == pytest.approx(50.0)
    assert primary["period"] == "1991-2020"
    assert primary["averageMm"] == pytest.approx(100.0)
    assert primary["anomalyMm"] == pytest.approx(-50.0)
    assert primary["anomalyPercent"] == pytest.approx(-50.0)

    assert secondary["period"] == "1995-2024"
    assert secondary["averageMm"] == pytest.approx(113.33)
    assert secondary["anomalyMm"] == pytest.approx(-63.33)
    assert secondary["anomalyPercent"] == pytest.approx(-55.88)
