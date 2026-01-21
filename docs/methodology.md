# Project Methodology

## Overview
This document describes the approach for mapping NYC transit security cameras.

## Phase 1: Data Collection

### Data Sources
- NYC Transit Authority camera inventory
- Station location database
- **Sample data** created for development

### Data Format
Camera locations stored as CSV with these fields:
- `camera_id` - Unique identifier
- `location_name` - Station or platform name
- `latitude` - WGS84 decimal degrees
- `longitude` - WGS84 decimal degrees

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

### Conversion Pipeline
1. Load CSV data
2. Validate coordinates
3. Convert to GeoJSON
4. Export to KML for visualization

## Phase 3: Spatial Analysis

### Coverage Calculation
- Buffer each camera location (50m radius)
- Calculate total coverage area
- Identify gaps in coverage

### Tools Used
- **Python**: GeoPandas, Pandas, Shapely
- **GIS Software**: ArcGIS Pro (optional)
- **Visualization**: Folium, Matplotlib

## Coordinate Systems

We use **WGS84 (EPSG:4326)** for:
- Input data (standard GPS coordinates)
- Web map compatibility
- KML/KMZ export

*Note: May transform to State Plane NY for accurate area calculations.*

## Quality Assurance

- [ ] All coordinates validated against NYC bounds
- [ ] Visual inspection on base map
- [ ] Cross-reference with known station locations
- [ ] Verify KML displays correctly in Google Earth

## References
- [GeoPandas Documentation](https://geopandas.org)
- [EPSG.io](https://epsg.io) for coordinate systems
- NYC Open Data Portal