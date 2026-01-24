# Project Methodology

## Overview
This document describes the approach for mapping NYC transit security cameras.

# Project Methodology

## Overview
This document describes the approach for mapping NYC security camera locations across transit stations, parks, cultural institutions, and public infrastructure.

## Phase 1: Data Collection

### Data Sources
- NYC transit station locations (MTA official database)
- NYC Parks Department locations
- Cultural institutions and landmarks
- Google Maps geospatial reference data
- Official borough boundary datasets

### Dataset Overview
- **Total Records:** 100 cameras
- **Geographic Scope:** All five NYC boroughs
- **Installation Dates:** 2020-2025 (5-year span)
- **Status Distribution:** ~70% Active, ~20% Maintenance, ~10% Inactive

### Data Format
Camera locations stored as CSV with 6 fields:
- `camera_id` - Unique identifier (CAM-001 to CAM-100)
- `location_name` - Station, park, or infrastructure name
- `latitude` - WGS84 decimal degrees (4-6 decimal places)
- `longitude` - WGS84 decimal degrees (4-6 decimal places)
- `status` - Operational status (Active, Maintenance, or Inactive)
- `installation_date` - Installation date in ISO 8601 format (YYYY-MM-DD)

## Phase 2: Data Processing

### Coordinate Validation
```python
# Validate NYC boundaries
nyc_bounds = {
    'lat_min': 40.4774,
    'lat_max': 40.9176,
    'lon_min': -74.2591,
    'lon_max': -73.7004
}
```

### Data Processing Pipeline
1. Load CSV data (100 cameras)
2. **Validate Coordinates:**
   - Check against NYC geographic bounds (40.4774-40.9176°N, -74.2591 to -73.7004°W)
   - Verify decimal precision (4-6 places)
   - Confirm WGS84 datum compliance
3. **Validate Status:**
   - Confirm values are Active, Maintenance, or Inactive only
   - Verify distribution: 70 Active, 20 Maintenance, 10 Inactive
4. **Validate Installation Dates:**
   - Check ISO 8601 format compliance
   - Verify dates fall within 2020-2025 range
   - Confirm no future dates
5. **Borough Classification:**
   - Assign cameras to correct boroughs based on coordinates
6. **Export Formats:**
   - Convert to GeoJSON for web applications
   - Export to KML for Google Earth visualization
   - Generate JSON for interactive mapping

## Phase 3: Spatial Analysis

### Spatial Analysis Performed
- **Geographic Distribution:** Borough-level camera counts and percentages
- **Nearest-Neighbor Analysis:** Calculate distances between cameras to identify clusters
- **Spatial Clustering:** Identify groups of cameras within 500m (dense monitoring areas)
- **Isolated Cameras:** Find cameras >1km from nearest neighbor (remote locations)
- **Coverage Metrics:** Distribution spread, geographic extent, density analysis
- **Temporal Analysis:** Installation timeline, status correlation with installation date

### Analysis Tools
- **Python Libraries:**
  - GeoPandas: Geospatial data operations
  - Pandas: Data manipulation and analysis
  - NumPy: Numerical computations
  - Shapely: Geometric operations
  - Folium: Interactive web mapping
  - Matplotlib: Statistical visualization
- **Geospatial Methods:**
  - Haversine formula for distance calculations
  - Coordinate boundary validation
  - Borough polygon intersection analysis
- **Visualization:** Folium interactive maps, Matplotlib statistical charts

## Coordinate Systems

We use **WGS84 (EPSG:4326)** for:
- Input data (standard GPS coordinates)
- Web map compatibility
- KML/KMZ export

*Note: May transform to State Plane NY for accurate area calculations.*

## Quality Assurance Checklist

- [x] All 100 coordinates validated against NYC geographic bounds (40.4774-40.9176°N, -74.2591 to -73.7004°W)
- [x] Status distribution verified (70 Active, 20 Maintenance, 10 Inactive)
- [x] Installation dates span 2020-2025 with realistic temporal distribution
- [x] Borough-level distribution confirmed (30/20/15/15/10 across NYC)
- [x] Cross-reference with official location databases completed
- [x] Coordinate precision validated (4-6 decimal places, ~10-100m accuracy)
- [x] WGS84 datum compliance verified
- [x] Duplicate/invalid records checked and removed
- [ ] Visual inspection on interactive base map (in progress)
- [ ] KML/GeoJSON export validation (planned)
- [ ] Statistical analysis metrics verified (planned)

## References
- [GeoPandas Documentation](https://geopandas.org)
- [EPSG.io](https://epsg.io) for coordinate systems
- NYC Open Data Portal