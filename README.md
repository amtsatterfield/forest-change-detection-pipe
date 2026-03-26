# forest-change-detection-pipe

Simple Python pipeline for detecting vegetation/forest change over time using Sentinel-2 imagery and NDVI.

## How it works

The script in `forest_change_detection.py` does the following:

1. Connects to the Microsoft Planetary Computer STAC API.
2. Searches Sentinel-2 L2A imagery for a bounding box (`bbox`) and date range.
3. Loads red (`B04`) and near-infrared (`B08`) bands for a "before" and "after" period.
4. Computes NDVI for each period.
5. Computes NDVI change (`after - before`).
6. Prints a summary statistic and saves a visualization image.

## Configure your region (bbox)

Set the `bbox` value in `forest_change_detection.py`:

```python
# [min_lon, min_lat, max_lon, max_lat] (WGS84 / EPSG:4326)
bbox = [-84.607430, 31.766413, -84.297409, 31.952162]
```

Use [bbox.com](https://bbox.com) to find a bounding box for your target region, then copy the coordinates in this format:

`[min_lon, min_lat, max_lon, max_lat]`

## Setup and run

From the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python forest_change_detection.py
```

## Outputs

Running the script produces:

- Console output:
  - `Average NDVI Change: <value>`
  - This is the mean of `ndvi_after - ndvi_before` across the analyzed pixels.
- Image file:
  - `ndvi_change.png`
  - A heatmap using `RdBu` colormap with limits `-0.5` to `0.5`.
  - Negative change (vegetation decline) appears toward red.
  - Positive change (vegetation increase) appears toward blue.

## Notes

- If no scenes match your search constraints, selection of the first item may fail.
- You can tune cloud filtering in the query (`"eo:cloud_cover": {"lt": 20}`) and/or adjust date ranges for your region.
