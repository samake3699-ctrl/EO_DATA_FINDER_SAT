
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
