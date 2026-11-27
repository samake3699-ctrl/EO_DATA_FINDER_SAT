
import sys
import json
from uuid import UUID
from pathlib import Path

import numpy as np
import rasterio
import matplotlib.pyplot as plt


DATA_DIR = Path(__file__).parent / "data" / "sentinel2"


def calculate_selected_ndvi(product_id):
    product_id = str(UUID(product_id))

    input_file = DATA_DIR / f"{product_id}_with_scl.tif"
    metadata_file = DATA_DIR / f"{product_id}_metadata.json"

    if not input_file.exists() or not metadata_file.exists():
        raise FileNotFoundError(
            "Selected product files are missing."
        )

    metadata = json.loads(
        metadata_file.read_text(encoding="utf-8")
    )

    if metadata["productId"] != product_id:
        raise ValueError("Product metadata mismatch.")

    # Read Sentinel-2 bands
    with rasterio.open(input_file) as src:
        if src.count != 4:
            raise ValueError("Expected 4 raster bands.")

        red = src.read(1)
        nir = src.read(2)
        data_mask = src.read(3)
        scl = src.read(4)

        profile = src.profile.copy()
        bounds = src.bounds

    # Select valid vegetation and bare-soil pixels
    denominator = nir + red

    valid = (
        (data_mask == 1)
        & np.isin(scl, [4, 5])
        & np.isfinite(red)
        & np.isfinite(nir)
        & (denominator > 0)
    )

    valid_count = int(np.count_nonzero(valid))

    if valid_count == 0:
        raise ValueError(
            "No valid NDVI pixels for this product."
        )

    # Calculate NDVI
    ndvi = np.full(red.shape, np.nan, dtype=np.float32)

    ndvi[valid] = (
        (nir[valid] - red[valid])
        / denominator[valid]
    )

    # Save NDVI GeoTIFF
    profile.update(
        driver="GTiff",
        count=1,
        dtype="float32",
        nodata=np.nan,
        compress="deflate"
    )

    ndvi_file = DATA_DIR / f"{product_id}_ndvi.tif"

    with rasterio.open(ndvi_file, "w", **profile) as dst:
        dst.write(ndvi, 1)
        dst.set_band_description(1, "NDVI")

    # Generate map preview
    fig, ax = plt.subplots(figsize=(7, 5))

    image = ax.imshow(
        np.ma.masked_invalid(ndvi),
        cmap="RdYlGn",
        vmin=-0.2,
        vmax=0.9,
        extent=[
            bounds.left,
            bounds.right,
            bounds.bottom,
            bounds.top
        ],
        origin="upper",
        interpolation="nearest"
    )

    ax.set_title(
        f"Sentinel-2 NDVI - {metadata['acquisitionDate']}"
    )
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    ax.set_aspect("equal", adjustable="box")

    fig.colorbar(
        image,
        ax=ax,
        label="NDVI",
        fraction=0.045,
        pad=0.02
    )

    fig.tight_layout(pad=0.3)

    preview_file = DATA_DIR / f"{product_id}_ndvi_preview.png"

    fig.savefig(
        preview_file,
        dpi=180,
        bbox_inches="tight",
        pad_inches=0.04
    )
    plt.close(fig)

    # Save calculated statistics
    results = {
        "productId": product_id,
        "productName": metadata["productName"],
        "acquisitionDate": metadata["acquisitionDate"],
        "ndvi": {
            "minimum": round(float(np.nanmin(ndvi)), 4),
            "maximum": round(float(np.nanmax(ndvi)), 4),
            "mean": round(float(np.nanmean(ndvi)), 4),
            "validPixels": valid_count,
            "totalPixels": int(ndvi.size)
        }
    }

    results_file = DATA_DIR / f"{product_id}_analysis.json"

    results_file.write_text(
        json.dumps(results, indent=4),
        encoding="utf-8"
    )

    print(json.dumps(results, indent=4))
    print("\nNDVI map saved:", preview_file)

    return results


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python calculate_selected_ndvi.py PRODUCT_ID"
        )

    calculate_selected_ndvi(sys.argv[1])
