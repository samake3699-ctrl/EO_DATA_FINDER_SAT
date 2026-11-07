
from pathlib import Path
import rasterio

# 1. Localiser notre image satellitaire
image_path = (
    Path(__file__).parent
    / "data"
    / "sentinel2"
    / "sikasso_20251028_bands.tif"
)

# 2. Ouvrir le fichier GeoTIFF
with rasterio.open(image_path) as src:

    # 3. Examiner ses caractéristiques
    print("Largeur :", src.width, "pixels")
    print("Hauteur :", src.height, "pixels")
    print("Nombre de bandes :", src.count)
    print("Système de coordonnées :", src.crs)
    print("Résolution spatiale :", src.res)
    print("Type de données :", src.dtypes)

    # 4. Lire les trois bandes
    b04 = src.read(1)
    b08 = src.read(2)
    data_mask = src.read(3)

    print("B04 - premier pixel :", b04[0, 0])
    print("B08 - premier pixel :", b08[0, 0])
    print("dataMask - premier pixel :", data_mask[0, 0])

    # Calcul NDVI du premier pixel
    rouge = b04[0, 0]
    infrarouge = b08[0, 0]
    masque = data_mask[0, 0]

    if masque == 1 and (infrarouge + rouge) != 0:
        ndvi = (infrarouge - rouge) / (infrarouge + rouge)
        print("NDVI du premier pixel :", round(float(ndvi), 4))
    else:
        print("Pixel invalide : NDVI non calculé")
