"""Export camera data to GeoJSON format"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


def load_cameras():
    df = pd.read_csv("data/sample_cameras.csv")
    print(f"Loaded {len(df)} cameras")
    return df


def create_geojson(df, output_path):
    """Convert camera data to GeoJSON.

    Parameters
    ----------
    df : pandas.DataFrame
        Camera data with latitude/longitude
    output_path : str
        Where to save GeoJSON file
    """
    print("\nCreating GeoJSON...")

    # Create geometry column (Point objects)
    geometry = [
        Point(lon, lat)
        for lon, lat in zip(df['longitude'], df['latitude'])
    ]

    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(
        df,
        geometry=geometry,
        crs='EPSG:4326'  # WGS84 coordinate system
    )

    print(f"Created GeoDataFrame with {len(gdf)} features")
    print(f"Coordinate system: {gdf.crs}")

    # Save to GeoJSON
    gdf.to_file(output_path, driver='GeoJSON')
    print(f"GeoJSON saved to: {output_path}")

    # Show sample
    print("\nSample features:")
    columns = ['camera_id', 'location_name', 'status', 'geometry']
    print(gdf[columns].head(3))


def main():
    print("\n" + "=" * 60)
    print("GEOJSON EXPORT TOOL")
    print("=" * 60)

    df = load_cameras()
    output_path = "maps/cameras.geojson"
    create_geojson(df, output_path)

    print("\n" + "=" * 60)
    print("GEOJSON EXPORT COMPLETE!")
    print("=" * 60)
    print("\nYou can:")
    print("1. Open in QGIS or ArcGIS")
    print("2. Use in web mapping libraries")
    print("3. View at geojson.io")


if __name__ == "__main__":
    main()