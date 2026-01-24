# NYC Security Camera Mapping

## 🎯 Project Overview

A comprehensive GIS analysis project mapping 100 security camera locations across New York City's five boroughs. This project demonstrates geospatial data processing, spatial analysis, and interactive mapping techniques relevant to public safety and infrastructure monitoring.

**Dataset:** 100 cameras spanning all 5 NYC boroughs (2020-2025 installation dates)

**Status Distribution:** 70% Active, 20% Maintenance, 10% Inactive

## 🎨 Project Status

✅ **Data Collection Complete** - 100-camera dataset with accurate coordinates  
✅ **Data Analysis** - Geographic distribution, borough analysis, temporal trends  
🚧 **In Development** - Interactive mapping and KML export capabilities

## 🛠️ Technologies & Tools

- **Python** - GeoPandas, Pandas, NumPy, Folium, Shapely
- **Geospatial Analysis** - Spatial clustering, distance calculations, coordinate validation
- **Data Formats** - CSV, KML, GeoJSON
- **Visualization** - Folium (interactive maps), Matplotlib (statistical charts)
- **Coordinate System** - WGS84 (EPSG:4326) 
## 📁 Project Structure ``` nyc-camera-mapping/ ├── data/ # Raw and processed camera location data ├── scripts/ # Python scripts for data processing ├── maps/ # Output visualizations and maps ├── docs/ # Documentation and methodology └── README.md # This file ``` 
## 🎯 Project Goals

- [x] Collect and geocode 100 camera locations across NYC
- [x] Validate coordinates and clean data (borough boundaries, accuracy checks)
- [x] Analyze geographic distribution and borough coverage
- [x] Calculate spatial metrics (nearest-neighbor distances, clustering)
- [ ] Create KML/KMZ files for visualization in Google Earth
- [ ] Generate interactive web maps with Folium
- [ ] Analyze installation timeline and status trends
- [x] Document methodology and data quality standards

## 📊 Skills Demonstrated

- Geospatial data collection, validation, and cleaning
- Coordinate system (WGS84/EPSG:4326) and boundary validation
- Spatial analysis: nearest-neighbor analysis, clustering detection, distribution metrics
- Data visualization: statistical analysis, interactive mapping, borough-level breakdowns
- ETL workflows for location data (CSV → GeoJSON → KML)
- Python geospatial libraries: GeoPandas, Shapely, Folium
- Haversine formula implementation for distance calculations
- Data quality assurance and professional documentation ## 🚀 Getting Started

### Prerequisites
```bash
pip install -r requirements.txt
```

### Running Analysis
```bash
python scripts/load_camera_data.py          # Load and validate data
python scripts/analyze_data.py              # Generate comprehensive analysis
```

### Output
- Console reports: Status distribution, geographic analysis, temporal trends
- Statistics: Borough breakdown, operational rates, installation timeline
- Data files: Validated CSV in data/ directory 
## � Dataset Information

**File:** `data/sample_cameras.csv`
- 100 camera records across all NYC boroughs
- Geographic coverage: Manhattan, Brooklyn, Queens, Bronx, Staten Island
- Installation dates: 2020-2025 (realistic deployment timeline)
- Coordinate system: WGS84 (Latitude/Longitude)
- Accuracy: 4-6 decimal places (~10-100m)
- Status: 70 Active, 20 Maintenance, 10 Inactive

See [docs/data_dictionary.md](docs/data_dictionary.md) for complete field definitions and [data/README.md](data/README.md) for collection methodology.

## 📝 Portfolio Context

This project demonstrates practical skills in location intelligence and geospatial analysis:
- Real-world data validation and cleaning workflows
- Spatial analysis for infrastructure monitoring
- Multi-borough coverage and distribution analysis
- Temporal data analysis (5-year installation timeline)
- Professional documentation and methodology standards 
## 👤 Author

**Denali Wilson**
- GitHub: [@denaliwilson](https://github.com/denaliwilson)
- LinkedIn: [linkedin.com/in/denali-wilson/](https://www.linkedin.com/in/denali-wilson/)
- Email: denaliwilson@gmail.com ## 📄 License This project is licensed under the MIT License - see the LICENSE file for details.
