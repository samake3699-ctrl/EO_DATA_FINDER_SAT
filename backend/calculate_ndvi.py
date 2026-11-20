
from pathlib import Path
import numpy as np
import rasterio

# ETAPE 1 : Trouver le fichier satellitaire
image_path = (
    Path(__file__).parent
    / "data"
    / "sentinel2"
    / "sikasso_20251028_with_scl.tif"
)

# ETAPE 2 : Lire les bandes et garder les informations geographiques
with rasterio.open(image_path) as src:
    b04 = src.read(1)
    b08 = src.read(2)
    data_mask = src.read(3)
    scl = src.read(4)

    profile = src.profile.copy()

# ETAPE 3 : Identifier les pixels utilisables
denominator = b08 + b04

valid = (
    (data_mask == 1)
    & np.isin(scl, [4, 5])
    & np.isfinite(b04)
    & np.isfinite(b08)
    & (denominator > 0)
)

# ETAPE 4 : Calculer le NDVI
ndvi = np.full(b04.shape, np.nan, dtype=np.float32)

ndvi[valid] = (
    (b08[valid] - b04[valid])
    / denominator[valid]
)

# ETAPE 5 : Afficher les resultats
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

# ETAPE 6 : Preparer le GeoTIFF de sortie
profile.update(
    driver="GTiff",
    count=1,
    dtype="float32",
    nodata=np.nan,
    compress="deflate"
)

output_path = image_path.with_name(
    "sikasso_20251028_ndvi.tif"
)

# ETAPE 7 : Enregistrer le NDVI
with rasterio.open(output_path, "w", **profile) as dst:
    dst.write(ndvi, 1)
    dst.set_band_description(1, "NDVI")

print("Carte NDVI enregistree :", output_path)

# STEP 8 - Generate a real NDVI map preview for the web interface

import matplotlib.pyplot as plt

with rasterio.open(output_path) as src:
    ndvi_map = src.read(1, masked=True)
    bounds = src.bounds

ndvi_map = np.ma.masked_invalid(ndvi_map)

cmap = plt.get_cmap("RdYlGn").copy()
cmap.set_bad("#e5e7eb")

fig, ax = plt.subplots(figsize=(6, 6))

image = ax.imshow(
    ndvi_map,
    cmap=cmap,
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

ax.set_title("Sentinel-2 NDVI - Sikasso - 28 October 2025")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

colorbar = fig.colorbar(image, ax=ax, shrink=0.85)
colorbar.set_label("NDVI")

fig.tight_layout()

preview_path = output_path.with_name(
    "sikasso_20251028_ndvi_preview.png"
)

fig.savefig(preview_path, dpi=160, bbox_inches="tight")
plt.close(fig)

print("NDVI preview saved:", preview_path)
