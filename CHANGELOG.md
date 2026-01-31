# Changelog

All notable changes to this project are documented in this file. This project follows [Semantic Versioning](https://semver.org/).

## [1.0.1] - 2026-01-31

### Changed

- Documentation reformatted for clarity (README, USAGE.md, CHANGELOG).
- README: corrected badge links, updated sample outputs and project structure to reflect repository contents, and added dataset statistics and deployment date range.
- USAGE.md: improved structure, fixed clone URL, and corrected script names and examples.
- Noted missing analysis dependencies (`scikit-learn`, `scipy`) and recommended adding them to `requirements.txt`.
- Updated README sample outputs to reference actual `maps/` files and interactive HTML maps.

### Fixed

- Resolved Shields.io "repo not found" by updating badges to point to `denaliwilson/nyc-camera-mapping`.
- Fixed incorrect script names in documentation (`generate_reports.py`, `export_to_geoJSON.py`, `export_styled_kml.py`).
- Minor formatting corrections across documentation.


## [1.0.0] - 2026-01-30

### Added

- Initial project release
- 100 camera locations across NYC
- Interactive web mapping (basic map, heat map, cluster map)
- Comprehensive spatial analysis suite including:
  - Coverage buffer calculations (50m)
  - Coverage gap detection
  - Nearest neighbor statistics
  - DBSCAN clustering implementation
  - Kernel density estimation
- Exports: KML/KMZ for Google Earth, GeoJSON for web GIS
- Professional documentation and an analysis report

### Data

- Camera dataset with 6 fields (camera_id, location_name, latitude, longitude, status, installation_date)
- Data dictionary and validation scripts
- Geographic coverage across all 5 boroughs

### Visualizations

- Interactive HTML maps and PNG charts for analysis outputs
- Google Earth 3D visualization files

### Documentation

- README, Usage guide, and Methodology documentation
- Code comments and docstrings in scripts



