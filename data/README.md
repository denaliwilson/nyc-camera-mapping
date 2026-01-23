# Camera Location Data

## Overview

This directory contains camera location data for NYC transit stations. The dataset includes geographic coordinates, operational status, and installation dates for security cameras deployed across the transit system.

## Files

### sample_cameras.csv
- **Description:** Primary dataset containing camera locations and metadata
- **Format:** CSV (Comma-Separated Values)
- **Rows:** 25 cameras
- **Columns:** 6 (camera_id, location_name, latitude, longitude, status, installation_date)
- **Size:** ~2KB
- **Encoding:** UTF-8

## Data Collection Methodology

### Coordinate Acquisition
Coordinates were obtained using the following process:

1. **Station Identification:** Selected 25 major NYC transit stations representing:
   - All five boroughs (Manhattan, Brooklyn, Queens, Bronx, Staten Island)
   - Mix of major hubs and smaller stations
   - Variety of operational contexts (terminals, transfer points, neighborhood stations)

2. **Geocoding Method:** 
   - Used Google Maps to obtain precise coordinates
   - Right-clicked on station locations to extract lat/long
   - Verified coordinates fall within NYC boundaries
   - Cross-referenced with MTA official station locations where possible

3. **Coordinate Precision:**
   - 6 decimal places (~10cm accuracy)
   - WGS84 datum (EPSG:4326)
   - Coordinates represent approximate station center or main entrance

### Station Selection Criteria

Stations were selected to provide:
- **Geographic diversity:** Coverage across all NYC boroughs
- **Traffic variety:** Mix of high-traffic hubs and moderate-traffic stations
- **Network representation:** Different subway lines and transfer points
- **Spatial distribution:** Spread across NYC to enable meaningful spatial analysis

### Status and Date Assignment

**Important:** This is **sample/demonstration data**. Status and installation dates are:
- Realistic but not actual operational data
- Designed to show variety for analysis purposes
- Installation dates range from 2022-2024 to represent phased deployment
- Status distribution reflects typical operational patterns (~70% active, ~20% maintenance, ~10% offline)

## Data Limitations

### Known Limitations

1. **Sample Data:** This is demonstration data for portfolio purposes, not actual NYC Transit Authority data
2. **Incomplete Coverage:** Only 25 cameras represented; actual system has hundreds
3. **Simplified Model:** Real camera systems include additional metadata (camera type, resolution, viewing angle, etc.)
4. **Point Locations:** Coordinates represent general station locations, not exact camera mounting positions
5. **Temporal Validity:** Status information is static snapshot, not real-time data

### Geographic Boundaries

All coordinates validated against NYC boundaries:
- **Latitude Range:** 40.4774°N to 40.9176°N
- **Longitude Range:** 74.2591°W to 73.7004°W
- **Coordinate System:** WGS84 (EPSG:4326)

## Data Quality

### Validation Performed
- ✅ All coordinates within NYC bounds
- ✅ No duplicate camera IDs
- ✅ All required fields populated
- ✅ Dates in valid ISO format
- ✅ Status values use controlled vocabulary
- ✅ Coordinates verified against Google Maps

### Quality Metrics
- **Completeness:** 100% (no missing values)
- **Uniqueness:** 100% (all camera IDs unique)
- **Spatial Accuracy:** ±10 meters (based on Google Maps precision)
- **Temporal Accuracy:** Sample data (not real installation dates)

## Usage Guidelines

### Appropriate Uses
✅ Learning GIS analysis techniques  
✅ Testing spatial analysis workflows  
✅ Demonstrating data visualization methods  
✅ Portfolio project development  
✅ Understanding geospatial data structures

### Inappropriate Uses
❌ Actual security planning  
❌ Representing real NYC Transit camera deployment  
❌ Making operational decisions  
❌ Publishing as actual transit data

## Future Enhancements

Potential improvements to this dataset:
- [ ] Expand to 100+ cameras for more robust analysis
- [ ] Add camera specifications (type, resolution, field of view)
- [ ] Include coverage polygons showing monitored areas
- [ ] Add associated station metadata (ridership, lines, zone)
- [ ] Incorporate real-time status updates (if API available)
- [ ] Add hierarchical organization (by line, borough, district)

## Related Documentation

- See `../docs/data_dictionary.md` for detailed field definitions
- See `../docs/methodology.md` for project methodology
- See `../README.md` for overall project documentation

## Data Updates

| Date | Change | Author |
|------|--------|--------|
| 2026-01-21 | Expanded dataset to 25 cameras across all boroughs | Denali Wilson |
| 2026-01-17 | Initial dataset created with 8 sample cameras | Denali Wilson |

## Contact

For questions about this dataset:
- **Author:** Denali Wilson
- **Email:** denaliwilson@gmail.com
- **GitHub:** https://github.com/denaliwilson

---

*This is demonstration data created for educational and portfolio purposes.*