
import sys
import json
import re
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np
from rasterio.io import MemoryFile

from copernicus import get_product_by_id
from copernicus_auth import get_access_token


PROCESS_URL = "https://sh.dataspace.copernicus.eu/process/v1"

BBOX = [-5.67654, 11.30755, -5.65654, 11.32755]

DATA_DIR = Path(__file__).parent / "data" / "sentinel2"


def download_selected_product(product_id):
    # Get the exact product metadata from Copernicus
    product = get_product_by_id(product_id)
    product_name = product["Name"]

    match = re.search(
        r"_MSIL2A_(\d{8})T\d{6}_",
        product_name
    )

    if not match:
        raise ValueError(
            "Selected product is not Sentinel-2 L2A."
        )

    date_text = match.group(1)
    date_iso = (
        f"{date_text[:4]}-"
        f"{date_text[4:6]}-"
        f"{date_text[6:8]}"
    )

    target_name = product_name.removesuffix(".SAFE")

    # Select only the requested Sentinel-2 product
    evalscript = """
//VERSION=3

const TARGET_PRODUCT = __TARGET__;

function setup() {
    return {
        input: ["B04", "B08", "dataMask", "SCL"],
        mosaicking: "TILE",
        output: {
            bands: 4,
            sampleType: "FLOAT32"
        }
    };
}

function preProcessScenes(collections) {
    collections.scenes.tiles =
        collections.scenes.tiles.filter(function(tile) {
            const name = (
                tile.sentinel2ProductId ||
                tile.productId ||
                ""
            ).replace(/\\.SAFE$/, "");

            return name === TARGET_PRODUCT;
        });

    return collections;
}

function evaluatePixel(samples) {
    const sample = samples.find(
        sample => sample.dataMask === 1
    );

    if (!sample) {
        return [0, 0, 0, 0];
    }

    return [
        sample.B04,
        sample.B08,
        sample.dataMask,
        sample.SCL
    ];
}
""".replace("__TARGET__", json.dumps(target_name))

    payload = {
        "input": {
            "bounds": {
                "bbox": BBOX,
                "properties": {
                    "crs": (
                        "http://www.opengis.net/def/"
                        "crs/OGC/1.3/CRS84"
                    )
                }
            },
            "data": [{
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {
                        "from": f"{date_iso}T00:00:00Z",
                        "to": f"{date_iso}T23:59:59Z"
                    },
                    "maxCloudCoverage": 100
                }
            }]
        },
        "output": {
            "width": 200,
            "height": 200,
            "responses": [{
                "identifier": "default",
                "format": {"type": "image/tiff"}
            }]
        },
        "evalscript": evalscript
    }

    token = get_access_token()

    request = Request(
        PROCESS_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "image/tiff"
        },
        method="POST"
    )

    with urlopen(request, timeout=120) as response:
        image_data = response.read()

    # Verify that the requested scene returned real data
    with MemoryFile(image_data) as memfile:
        with memfile.open() as src:
            valid_pixels = int(
                np.count_nonzero(src.read(3) == 1)
            )

    if valid_pixels == 0:
        raise ValueError(
            "No valid pixels for the selected product."
        )

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_file = DATA_DIR / f"{product_id}_with_scl.tif"
    output_file.write_bytes(image_data)

    metadata_file = DATA_DIR / f"{product_id}_metadata.json"
    metadata_file.write_text(
        json.dumps({
            "productId": product_id,
            "productName": product_name,
            "acquisitionDate": date_iso,
            "bbox": BBOX,
            "validPixels": valid_pixels
        }, indent=4),
        encoding="utf-8"
    )

    print("Selected product:", product_name)
    print("Acquisition date:", date_iso)
    print("Valid pixels:", valid_pixels)
    print("Satellite bands saved:", output_file)
    print("Metadata saved:", metadata_file)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python download_selected_product.py PRODUCT_ID"
        )

    download_selected_product(sys.argv[1])
