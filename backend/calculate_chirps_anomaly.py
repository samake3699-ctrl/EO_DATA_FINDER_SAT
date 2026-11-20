
from pathlib import Path
from statistics import mean
import math
import numpy as np
import rasterio

# Sikasso pilot point
LONGITUDE = -5.66654
LATITUDE = 11.31755

DATA_DIR = Path(__file__).parent / "data" / "chirps"

# 30-year historical reference
BASELINE_YEARS = range(1991, 2021)

# Month being analyzed
TARGET_YEAR = 2025
MONTH = 10


def read_rainfall(year):
    filename = f"chirps-v3.0.{year}.{MONTH:02d}.tif"
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Missing file: {filename}")

    with rasterio.open(file_path) as src:
        if src.crs is None or src.crs.to_epsg() != 4326:
            raise ValueError(f"Unexpected CRS: {filename}")

        if not (
            src.bounds.left <= LONGITUDE < src.bounds.right
            and src.bounds.bottom < LATITUDE <= src.bounds.top
        ):
            raise ValueError(f"Sikasso outside raster: {filename}")

        value = next(
            src.sample([(LONGITUDE, LATITUDE)], masked=True)
        )[0]

        if np.ma.is_masked(value):
            raise ValueError(f"Missing rainfall data: {filename}")

        rainfall = float(value)

        if not math.isfinite(rainfall) or rainfall < 0:
            raise ValueError(f"Invalid rainfall data: {filename}")

        return rainfall


# Read the 30 historical October values
historical_rainfall = {
    year: read_rainfall(year)
    for year in BASELINE_YEARS
}

# Calculate historical average
historical_average = mean(historical_rainfall.values())

# Read October 2025 rainfall
observed_rainfall = read_rainfall(TARGET_YEAR)

# Calculate rainfall anomalies
anomaly_mm = observed_rainfall - historical_average

if historical_average > 0:
    anomaly_percent = (
        anomaly_mm / historical_average
    ) * 100
else:
    anomaly_percent = None


# Display results
print("\nCHIRPS Rainfall Analysis - Sikasso, Mali")
print("---------------------------------------")

print("Historical reference: 1991-2020")
print("Reference month: October")
print("Number of historical years:", len(historical_rainfall))

print("\nHistorical rainfall values:")

for year, rainfall in historical_rainfall.items():
    print(f"{year}: {rainfall:.2f} mm")

print("\n---------------------------------------")
print(f"Historical average: {historical_average:.2f} mm")
print(f"October 2025 rainfall: {observed_rainfall:.2f} mm")
print(f"Rainfall anomaly: {anomaly_mm:+.2f} mm")

if anomaly_percent is not None:
    print(f"Rainfall anomaly: {anomaly_percent:+.2f}%")
else:
    print("Rainfall anomaly (%): undefined")

# Secondary reference: October 1995-2024
secondary_values = [
    read_rainfall(year)
    for year in range(1995, 2025)
]

secondary_average = mean(secondary_values)

secondary_anomaly_mm = observed_rainfall - secondary_average

secondary_anomaly_percent = (
    secondary_anomaly_mm / secondary_average * 100
    if secondary_average > 0
    else None
)

print("\nSECONDARY REFERENCE: 1995-2024")
print("---------------------------------------")
print(f"Historical average: {secondary_average:.2f} mm")
print(f"October 2025 rainfall: {observed_rainfall:.2f} mm")
print(f"Rainfall anomaly: {secondary_anomaly_mm:+.2f} mm")

if secondary_anomaly_percent is not None:
    print(f"Rainfall anomaly: {secondary_anomaly_percent:+.2f}%")
else:
    print("Rainfall anomaly (%): undefined")

# STEP 3 - Create rainfall comparison chart

import matplotlib.pyplot as plt

labels = [
    "Average\n1991-2020",
    "Average\n1995-2024",
    "October\n2025"
]

values = [
    historical_average,
    secondary_average,
    observed_rainfall
]

colors = ["#297a59", "#65a67b", "#e69a45"]

fig, ax = plt.subplots(figsize=(9, 5))

bars = ax.bar(labels, values, color=colors, width=0.55)

ax.bar_label(bars, fmt="%.2f mm", padding=5)

ax.set_title(
    "CHIRPS Rainfall Comparison - Sikasso, Mali"
)
ax.set_ylabel("Monthly rainfall (mm)")
ax.set_ylim(0, max(values) * 1.25)

ax.grid(axis="y", alpha=0.2)
ax.set_axisbelow(True)

fig.text(
    0.5, 0.02,
    "Source: CHIRPS v3 | October rainfall | Sikasso pilot point",
    ha="center",
    fontsize=9
)

plt.tight_layout(rect=[0, 0.05, 1, 1])

output_path = DATA_DIR / "sikasso_chirps_comparison.png"

fig.savefig(output_path, dpi=180)
plt.close(fig)

print("\nRainfall comparison chart saved:", output_path)
