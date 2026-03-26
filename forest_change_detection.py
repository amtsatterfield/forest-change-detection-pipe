import numpy as np
import rasterio
import matplotlib.pyplot as plt
from pystac_client import Client
import planetary_computer

# ---------------------------
# 1. Search Sentinel-2 data
# ---------------------------
catalog = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")

# [min_lon, min_lat, max_lon, max_lat] (WGS84 / EPSG:4326)
bbox = [-84.607430,31.766413,-84.297409,31.952162] # SW GA

def get_image(date_range):
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime=date_range,
        query={"eo:cloud_cover": {"lt": 20}},
    )

    items = list(search.get_items())
    item = items[0]

    signed_item = planetary_computer.sign(item)

    # Get the red and near-infrared bands fro NDVI calculation
    red = signed_item.assets["B04"].href
    nir = signed_item.assets["B08"].href

    return red, nir

# Before and after
red1, nir1 = get_image("2020-06-01/2020-09-01")
red2, nir2 = get_image("2024-06-01/2024-09-01")

# ---------------------------
# 2. Read bands
# ---------------------------
def read_band(url):
    with rasterio.open(url) as src:
        return src.read(1).astype("float32")

red_before = read_band(red1)
nir_before = read_band(nir1)

red_after = read_band(red2)
nir_after = read_band(nir2)

# ---------------------------
# 3. Compute NDVI
# ---------------------------
def ndvi(nir, red):
    return (nir - red) / (nir + red + 1e-6)

ndvi_before = ndvi(nir_before, red_before)
ndvi_after = ndvi(nir_after, red_after)

# ---------------------------
# 4. Change detection
# ---------------------------
ndvi_change = ndvi_after - ndvi_before

# ---------------------------
# 5. Stats
# ---------------------------
mean_change = np.nanmean(ndvi_change)
print("Average NDVI Change:", mean_change)

# ---------------------------
# 6. Visualization
# ---------------------------
plt.figure(figsize=(10, 6))
plt.imshow(ndvi_change, cmap="RdBu", vmin=-0.5, vmax=0.5)
plt.colorbar(label="NDVI Change")
plt.title("NDVI Change (2020 → 2024)")
plt.savefig("ndvi_change.png")
plt.show()
