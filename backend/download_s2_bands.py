
import json
from pathlib import Path
from urllib.request import Request, urlopen

from copernicus_auth import get_access_token


PROCESS_URL = "https://sh.dataspace.copernicus.eu/process/v1"

# Small pilot area around Sikasso, Mali.
# Order: west, south, east, north.
BBOX = [-5.67654, 11.30755, -5.65654, 11.32755]

EVALSCRIPT = """
//VERSION=3

function setup() {
    return {
        input: ["B04", "B08", "dataMask"],
        output: {
            bands: 3,
            sampleType: "FLOAT32"
        }
    };
}

function evaluatePixel(sample) {
    return [
        sample.B04,
        sample.B08,
        sample.dataMask
    ];
}
"""

payload = {
    "input": {
        "bounds": {
            "bbox": BBOX,
            "properties": {
                "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
            }
        },
        "data": [
            {
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {
                        "from": "2025-10-28T00:00:00Z",
                        "to": "2025-10-28T23:59:59Z"
                    },
                    "maxCloudCoverage": 10,
                    "mosaickingOrder": "leastCC"
                }
            }
        ]
    },
    "output": {
        "width": 200,
        "height": 200,
        "responses": [
            {
                "identifier": "default",
                "format": {"type": "image/tiff"}
            }
        ]
    },
    "evalscript": EVALSCRIPT
}


def download_bands():
    token = get_access_token()

    request = Request(
        PROCESS_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "image/tiff",
        },
        method="POST"
    )

    with urlopen(request, timeout=120) as response:
        if response.headers.get_content_type() != "image/tiff":
            raise RuntimeError("Unexpected response format")

        image_data = response.read()

    output_dir = Path(__file__).parent / "data" / "sentinel2"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "sikasso_20251028_bands.tif"
    output_file.write_bytes(image_data)

    print("Satellite file downloaded successfully")
    print("File:", output_file)
    print("Size:", len(image_data), "bytes")


if __name__ == "__main__":
    download_bands()
