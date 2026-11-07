
from pathlib import Path
import numpy as np
import rasterio

image_path = (
    Path(__file__).parent
    / "data"
    / "sentinel2"
    / "sikasso_20251028_bands.tif"
)

with rasterio.open(image_path) as src:
    b04 = src.read(1)
    b08 = src.read(2)
    data_mask = src.read(3)

# Dénominateur de la formule NDVI
denominator = b08 + b04

# Pixels exploitables pour ce premier calcul
valid = (
    (data_mask == 1)
    & np.isfinite(b04)
    & np.isfinite(b08)
    & (denominator > 0)
)

# Matrice initialement remplie de NaN
ndvi = np.full(b04.shape, np.nan, dtype=np.float32)

# Calculer le NDVI uniquement sur les pixels valides
ndvi[valid] = (
    (b08[valid] - b04[valid])
    / denominator[valid]
)

print("Dimensions NDVI :", ndvi.shape)
print("Pixels valides :", np.count_nonzero(valid))
print("Pixels exclus :", np.count_nonzero(~valid))

if np.any(valid):
    print("NDVI minimum :", round(float(np.nanmin(ndvi)), 4))
    print("NDVI maximum :", round(float(np.nanmax(ndvi)), 4))
    print("NDVI moyen :", round(float(np.nanmean(ndvi)), 4))
    print("Premier pixel :", round(float(ndvi[0, 0]), 4))
else:
    print("Aucun pixel valide pour le calcul NDVI.")
