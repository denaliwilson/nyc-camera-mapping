# Data Dictionary

## Camera Location Dataset

**File:** `data/sample_cameras.csv`  
**Format:** Comma-Separated Values (CSV)  
**Encoding:** UTF-8  
**Last Updated:** January 31, 2026  
**Total Records:** 100 cameras  
**Date Range:** 2020-02-14 to 2025-09-22  
**Geographic Coverage:** All 5 NYC boroughs

---

## Field Definitions

### camera_id
- **Type:** String (Text)
- **Format:** CAM-XXX where XXX is a 3-digit number
- **Required:** Yes
- **Unique:** Yes (primary key)
- **Description:** Unique identifier for each security camera
- **Example:** `CAM-001`, `CAM-015`
- **Validation Rules:** 
  - Must start with "CAM-"
  - Must be followed by exactly 3 digits
  - No duplicates allowed
  - Sequential numbering preferred

### location_name
- **Type:** String (Text)
- **Format:** Free text
- **Required:** Yes
- **Unique:** No (multiple cameras can be at same location)
- **Description:** Human-readable name of the station or platform where camera is installed
- **Example:** `Times Square Station - Platform A`, `Grand Central Terminal - Main Concourse`
- **Validation Rules:**
  - Must not be empty
  - Should include station name and specific location (platform, entrance, etc.)
  - Use standard station names from MTA

### latitude
- **Type:** Float (Decimal number)
- **Format:** Decimal degrees (WGS84)
- **Required:** Yes
- **Unique:** No
- **Description:** Latitude coordinate of camera location in WGS84 coordinate system
- **Range:** 40.4774 to 40.9176 (NYC boundaries)
- **Precision:** 6 decimal places recommended
- **Example:** `40.7580`, `40.7128`
- **Validation Rules:**
  - Must be within NYC latitude bounds
  - Must be a valid decimal number
  - Positive values only (Northern Hemisphere)
  - Should have 4-6 decimal places for accuracy

### longitude
- **Type:** Float (Decimal number)
- **Format:** Decimal degrees (WGS84)
- **Required:** Yes
- **Unique:** No
- **Description:** Longitude coordinate of camera location in WGS84 coordinate system
- **Range:** -74.2591 to -73.7004 (NYC boundaries)
- **Precision:** 6 decimal places recommended
- **Example:** `-73.9855`, `-74.0060`
- **Validation Rules:**
  - Must be within NYC longitude bounds
  - Must be a valid decimal number
  - Negative values only (Western Hemisphere)
  - Should have 4-6 decimal places for accuracy

### status
- **Type:** String (Text)
- **Format:** Enumerated values (controlled vocabulary)
- **Required:** Yes
- **Unique:** No
- **Description:** Current operational status of the camera
- **Allowed Values:**
  - `Active` - Camera is functioning and recording (~70% of dataset)
  - `Maintenance` - Camera is temporarily offline for repairs/upgrades (~20% of dataset)
  - `Inactive` - Camera is not functioning, awaiting repair or decommissioned (~10% of dataset)
- **Example:** `Active`, `Maintenance`, `Inactive`
- **Validation Rules:**
  - Must be exactly one of the three allowed values
  - Case-sensitive (use exact capitalization)
  - Newer installations (2024-2025) predominantly Active

### installation_date
- **Type:** Date
- **Format:** ISO 8601 (YYYY-MM-DD)
- **Required:** Yes
- **Unique:** No
- **Description:** Date when camera was installed and activated in the field
- **Range:** 2020-01-01 to 2025-09-22 (5-year deployment window)
- **Example:** `2020-03-15`, `2023-08-25`, `2025-05-10`
- **Validation Rules:**
  - Must follow YYYY-MM-DD format strictly
  - Must be a valid calendar date (no impossible dates)
  - Cannot be in the future
  - Must fall within 2020-2025 range for this dataset
  - Newer installations correlate with Active status

---

## Coordinate Reference System

**System:** WGS84 (World Geodetic System 1984)  
**EPSG Code:** 4326  
**Units:** Decimal Degrees  
**Description:** Standard GPS coordinate system used worldwide

**Why WGS84?**
- Compatible with web mapping libraries (Folium, Leaflet)
- Standard for GPS devices
- Compatible with Google Earth and Google Maps
- Easy to convert to other coordinate systems if needed

---

## Data Quality Standards

### Completeness
- All fields must be populated (no null/empty values)
- Each record represents a valid camera installation

### Accuracy
- Coordinates verified against Google Maps
- Location names use official MTA station names
- Dates represent actual or plausible installation timeline

### Consistency
- All dates use ISO 8601 format
- Status values use exact capitalization
- Camera IDs follow sequential numbering

### Validity
- All coordinates fall within NYC geographic bounds
- All dates are in the past (no future installations)
- All camera IDs are unique

---

## Data Sources

- **Coordinates:** Obtained via Google Maps geocoding and geospatial reference verification
- **Location Names:** Based on official MTA stations, NYC Parks Department, and cultural institutions
- **Borough Distribution:** Not stored as a field in the current dataset. To compute borough counts, add a `borough` column or derive boroughs via a spatial join with an authoritative NYC boroughs shapefile (GeoJSON/ESRI Shapefile). This allows reproducible counts and borough-based analysis.
- **Status Information:** Active: 72 (72%), Maintenance: 18 (18%), Inactive: 10 (10%) (values verified from `data/sample_cameras.csv`)
- **Installation Dates:** Demonstration data spanning realistic 5-year deployment timeline (2020-2025)

---

## Usage Notes

### For Analysis
- Filter by `status` to analyze operational cameras only
- Use `latitude` and `longitude` for spatial analysis and mapping
- Group by `installation_date` to analyze deployment timeline

### For Visualization
- Plot points using lat/long coordinates
- Color-code markers by status
- Show location_name in popups/tooltips

### For Export
- Coordinates are ready for KML export (WGS84)
- Can be imported into ArcGIS, QGIS, or other GIS software
- Compatible with web mapping libraries without transformation

---

## Change Log

- **2026-01-31:** Data dictionary updated: corrected date range, added exact status counts, removed inaccurate borough distribution and recommended adding a `borough` field or deriving boroughs by spatial join.
- **2026-01-23:** Dataset expanded to 100 camera locations; installation dates and records updated.
- **2026-01-22:** Initial dataset created with 25 camera locations
- **2026-01-21:** Dataset structure defined with 8 sample cameras

---

## Contact

For questions about this dataset or to report data quality issues:
- **Author:** Denali Wilson
- **Email:** denaliwilson@gmail.com
- **GitHub:** https://github.com/denaliwilson