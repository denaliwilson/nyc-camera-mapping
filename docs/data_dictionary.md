# Data Dictionary

## Camera Location Dataset

**File:** `data/sample_cameras.csv`  
**Format:** Comma-Separated Values (CSV)  
**Encoding:** UTF-8  
**Last Updated:** January 22, 2026  
**Total Records:** 25 cameras

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
  - `Active` - Camera is functioning and recording
  - `Maintenance` - Camera is temporarily offline for repairs/upgrades
  - `Offline` - Camera is not functioning, awaiting repair or decommissioned
- **Example:** `Active`, `Maintenance`, `Offline`
- **Validation Rules:**
  - Must be exactly one of the three allowed values
  - Case-sensitive (use exact capitalization)

### installation_date
- **Type:** Date
- **Format:** ISO 8601 (YYYY-MM-DD)
- **Required:** Yes
- **Unique:** No
- **Description:** Date when camera was installed and activated
- **Range:** 2022-01-01 to present (no future dates)
- **Example:** `2023-01-15`, `2024-06-30`
- **Validation Rules:**
  - Must follow YYYY-MM-DD format
  - Must be a valid calendar date
  - Cannot be in the future
  - Should be between 2022 and 2025 for this dataset

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

- **Coordinates:** Obtained via Google Maps geocoding
- **Station Names:** Based on official MTA station list
- **Status Information:** Sample data for demonstration purposes
- **Installation Dates:** Sample data representing realistic deployment timeline

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

- **2026-01-22:** Initial dataset created with 25 camera locations
- **2026-01-21:** Dataset structure defined with 8 sample cameras

---

## Contact

For questions about this dataset or to report data quality issues:
- **Author:** Denali Wilson
- **Email:** denaliwilson@gmail.com
- **GitHub:** https://github.com/denaliwilson