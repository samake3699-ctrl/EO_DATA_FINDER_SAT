
from pathlib import Path
import numpy as np
import rasterio

image_path = (
    Path(__file__).parent
    / "data"
    / "sentinel2"
    / "sikasso_20251028_with_scl.tif"
)

with rasterio.open(image_path) as src:
    print("Dimensions :", src.width, "x", src.height)
    print("Nombre de bandes :", src.count)

    if src.count != 4:
        raise ValueError("Le fichier doit contenir 4 bandes.")

    scl = src.read(4)

# Compter les pixels de chaque classe SCL
classes, counts = np.unique(scl, return_counts=True)

print("\nClasses SCL présentes :")

for classe, count in zip(classes, counts):
    print(f"Classe {int(classe)} : {count} pixels")

print("\nNombre total de pixels :", scl.size)
