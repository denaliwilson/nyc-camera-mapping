# Usage Guide

## Getting Started

This guide walks you through running all analyses included in this project and producing the maps and reports inside `maps/`.

## Prerequisites

- Python 3.8 or higher
- Git installed
- ~2 GB free disk space (more for generated map outputs)

## Installation

### Step 1: Clone repository

```bash
git clone https://github.com/denaliwilson/nyc-camera-mapping.git
cd nyc-camera-mapping
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

If you encounter issues installing `geopandas`, consult your platform package manager; alternatively, install packages individually:

```bash
pip install pandas geopandas folium matplotlib seaborn shapely scikit-learn scipy simplekml
```
 ## Running the Analysis

### Phase 1: Data Validation

First, verify your data is clean and consistent.

```bash
python scripts/load_cameras.py
python scripts/validate_data.py
```

**Expected output:** Summary statistics and a validation report.

### Phase 2: Create Visualizations

Generate interactive maps (output: HTML files in `maps/`):

```bash
python scripts/create_basic_map.py
python scripts/create_heatmap.py
python scripts/create_cluster_map.py
```

Open the produced `.html` files in a browser to inspect interactive maps and popups.
 ### Phase 3: Spatial Analysis

Run the core GIS analyses (outputs: PNG charts and CSV results in `maps/`):

```bash
python scripts/calculate_coverage.py
python scripts/find_gaps.py
python scripts/nearest_neighbor.py
python scripts/detect_clusters.py
python scripts/density_analysis.py
```

### Phase 4: Export Data

Export processed data to GIS formats:

```bash
python scripts/export_to_kml.py
python scripts/export_styled_kml.py
python scripts/export_to_geoJSON.py
```

**Outputs:** KML and GeoJSON files (open in Google Earth Pro or GIS software).

### Phase 5: Generate Report

Create the full analysis report:

```bash
python scripts/generate_reports.py
```

**Output:** `maps/analysis_report.txt`
 ## Viewing Results

### Interactive Maps

1. Navigate to the `maps/` folder.
2. Open any `.html` file in your web browser.
3. Interact with markers and popups to view camera details.
4. Zoom and pan to explore different areas.

### Google Earth Visualization

1. Install Google Earth Pro (free).
2. In Google Earth: File → Open.
3. Select `maps/cameras_styled.kml` and explore in 3D.

### Analysis Charts

All `.png` files in `maps/` are high-resolution charts. Key files include:

- `coverage_zones.png`
- `coverage_gaps.png`
- `camera_clusters.png`
- `camera_density.png`
- `nearest_neighbor_distribution.png`
 ## Troubleshooting

### Common Issues

**ModuleNotFoundError**

```bash
pip install [missing-package]
```

**Maps show blank / tiles not loading**

- Open the browser developer console (F12) to inspect errors.
- Verify the associated `.csv` / GeoJSON files exist and have required columns (`latitude`,`longitude`,`camera_id`, etc.).

**Coordinates outside NYC or reversed lat/lon**

- Run `python scripts/validate_data.py` to check coordinate ranges.
- Ensure longitude values are negative (WGS84) and latitude are within NYC bounds.

**Geopandas installation failures**

- On some systems, `geopandas` needs system dependencies (GDAL, GEOS, PROJ). Use conda or platform package managers, or consult the `geopandas` installation docs.
 ## Customization

### Change buffer radius

Edit `scripts/calculate_coverage.py`:

```python
buffers = calculate_buffers(gdf, radius_meters=100)  # change from 50 to 100 meters
```

### Change base map tiles

Edit `scripts/create_basic_map.py`:

```python
tiles = 'CartoDB positron'  # try 'Stamen Terrain' or 'CartoDB dark_matter'
```

### Adjust cluster sensitivity

Edit `scripts/detect_clusters.py`:

```python
detect_clusters(df, epsilon_km=1.0)  # increase epsilon to merge larger clusters
```

## Next Steps

1. Modify camera data for your own use case.
2. Adapt the scripts to analyze other cities.
3. Integrate real-time camera status feeds.
4. Add automated daily/weekly reporting.

## Support

Open an issue on GitHub or contact: denaliwilson@gmail.com

