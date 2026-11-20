
from pathlib import Path
import rasterio

# CHIRPS monthly rainfall file
file_path = (
    Path(__file__).parent
    / "data"
    / "chirps"
    / "chirps-v3.0.2025.10.tif"
)

# Sikasso pilot point (longitude, latitude)
longitude = -5.66654
latitude = 11.31755

with rasterio.open(file_path) as src:
    rainfall = next(
        src.sample([(longitude, latitude)])
    )[0]

    print("Coordinate system:", src.crs)
    print("Rainfall date: October 2025")
    print("Location: Sikasso, Mali")
    print(f"Estimated rainfall: {float(rainfall):.2f} mm")
