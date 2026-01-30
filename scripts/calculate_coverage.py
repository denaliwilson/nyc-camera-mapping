"""Calculate camera coverage zones using buffer analysis"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt


def load_cameras():
    """Load camera data and convert to GeoDataFrame"""
    df = pd.read_csv("data/sample_cameras.csv")

    # Create Point geometries
    geometry = [
        Point(lon, lat)
        for lon, lat in zip(df['longitude'], df['latitude'])
    ]

    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(
        df,
        geometry=geometry,
        crs='EPSG:4326'  # WGS84
    )

    print(f"✅ Loaded {len(gdf)} cameras")
    return gdf


def calculate_buffers(gdf, radius_meters):
    """Calculate buffer zones around cameras.

    Parameters
    ----------
    gdf : GeoDataFrame
        Camera locations
    radius_meters : int
        Buffer radius in meters

    Returns
    -------
    GeoDataFrame
        with buffer geometries
    """
    print(f"\n📏 Calculating {radius_meters}m buffers...")

    # Project to a metric coordinate system (State Plane NY)
    # This lets us use meters instead of degrees
    gdf_projected = gdf.to_crs('EPSG:2263')  # NY State Plane (feet)

    # Convert meters to feet (EPSG:2263 uses feet)
    radius_feet = radius_meters * 3.28084

    # Create buffers
    buffers = gdf_projected.copy()
    buffers['geometry'] = gdf_projected.geometry.buffer(radius_feet)

    # Project back to WGS84 for display
    buffers = buffers.to_crs('EPSG:4326')
    print(f"✅ Created {len(buffers)} coverage zones")
    return buffers


def calculate_total_coverage(buffers):
    """Calculate total area covered by all cameras"""
    # Project to metric
    buffers_metric = buffers.to_crs('EPSG:2263')

    # Union all buffers (combines overlapping areas)
    total_coverage = buffers_metric.geometry.unary_union

    # Calculate area in square meters
    area_sqft = total_coverage.area
    area_sqm = area_sqft * 0.092903  # Convert sq ft to sq m
    area_sqkm = area_sqm / 1_000_000

    print(f"\n📊 Coverage Statistics:")
    print(f" Total coverage area: {area_sqm:,.0f} m²")
    print(f" Total coverage area: {area_sqkm:.2f} km²")
    print(f" Number of cameras: {len(buffers)}")
    avg_area = area_sqm / len(buffers)
    print(f" Average area per camera: {avg_area:,.0f} m²")

    return total_coverage


def visualize_coverage(gdf, buffers, output_path):
    """Create visualization of coverage zones"""
    print(f"\n🎨 Creating coverage visualization...")

    fig, ax = plt.subplots(figsize=(15, 12))

    # Plot buffers (coverage zones)
    buffers.plot(
        ax=ax,
        alpha=0.3,
        edgecolor='blue',
        facecolor='lightblue',
        linewidth=0.5
    )

    # Plot camera points on top
    gdf.plot(
        ax=ax,
        color='red',
        markersize=20,
        marker='o',
        label='Cameras'
    )

    # Styling
    ax.set_title(
        'Camera Coverage Zones (50m radius)',
        fontsize=16,
        fontweight='bold'
    )
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved visualization to: {output_path}")
    plt.close()


def main():
    print("\n" + "=" * 60)
    print("📏 COVERAGE BUFFER ANALYSIS")
    print("=" * 60)

    # Load cameras
    gdf = load_cameras()

    # Calculate 50m buffers
    buffers = calculate_buffers(gdf, radius_meters=50)

    # Calculate total coverage
    calculate_total_coverage(buffers)

    # Save buffers to file
    buffers.to_file("maps/camera_buffers.geojson", driver='GeoJSON')
    print(f"\n💾 Saved buffers to: maps/camera_buffers.geojson")

    # Visualize
    visualize_coverage(gdf, buffers, "maps/coverage_zones.png")

    print("\n" + "=" * 60)
    print("✅ COVERAGE ANALYSIS COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()