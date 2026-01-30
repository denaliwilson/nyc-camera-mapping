"""Find gaps in camera coverage"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon, box
import matplotlib.pyplot as plt


def load_cameras():
    df = pd.read_csv("data/sample_cameras.csv")
    geometry = [
        Point(lon, lat)
        for lon, lat in zip(df['longitude'], df['latitude'])
    ]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')
    return gdf


def find_coverage_gaps(gdf, buffer_meters=50):
    """Find gaps in camera coverage.

    Parameters
    ----------
    gdf : GeoDataFrame
        Camera locations
    buffer_meters : int
        Coverage radius

    Returns
    -------
    GeoDataFrame
        of gap polygons
    """
    print(f"\nFinding coverage gaps...")

    # Project to metric
    gdf_proj = gdf.to_crs('EPSG:2263')

    # Create buffers
    buffer_feet = buffer_meters * 3.28084
    coverage = gdf_proj.geometry.buffer(buffer_feet)

    # Union all coverage zones
    total_coverage = coverage.unary_union

    # Create bounding box around all cameras
    bounds = gdf_proj.total_bounds  # [minx, miny, maxx, maxy]

    # Expand bounds by 500 feet for context
    expansion = 500
    study_area = box(
        bounds[0] - expansion,
        bounds[1] - expansion,
        bounds[2] + expansion,
        bounds[3] + expansion
    )

    # Gaps = Study Area - Coverage
    gaps = study_area.difference(total_coverage)

    # Convert back to WGS84
    gaps_gdf = gpd.GeoDataFrame(
        {'gap_id': [1]},
        geometry=[gaps],
        crs='EPSG:2263'
    ).to_crs('EPSG:4326')

    print(f"Identified coverage gaps")
    return gaps_gdf


def visualize_gaps(gdf, gaps_gdf, output_path):
    """Visualize coverage and gaps"""
    print(f"\nCreating gap visualization...")

    fig, ax = plt.subplots(figsize=(15, 12))

    # Plot gaps in red
    gaps_gdf.plot(
        ax=ax,
        color='red',
        alpha=0.2,
        edgecolor='darkred',
        linewidth=2,
        label='Coverage Gaps'
    )

    # Plot cameras
    gdf.plot(
        ax=ax,
        color='green',
        markersize=30,
        marker='*',
        label='Cameras',
        zorder=5
    )

    ax.set_title('Camera Coverage Gaps Analysis', fontsize=16, fontweight='bold')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to: {output_path}")
    plt.close()


def main():
    print("\n" + "=" * 60)
    print("COVERAGE GAP ANALYSIS")
    print("=" * 60)

    gdf = load_cameras()
    gaps_gdf = find_coverage_gaps(gdf, buffer_meters=50)

    # Save gaps
    gaps_gdf.to_file("maps/coverage_gaps.geojson", driver='GeoJSON')
    print(f"\nSaved gaps to: maps/coverage_gaps.geojson")

    # Visualize
    visualize_gaps(gdf, gaps_gdf, "maps/coverage_gaps.png")

    print("GAP ANALYSIS COMPLETE!")


if __name__ == "__main__":
    main()
