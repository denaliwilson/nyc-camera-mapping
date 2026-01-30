"""Nearest neighbor analysis"""

import pandas as pd
import matplotlib.pyplot as plt
from math import radians, sin, cos, sqrt, atan2


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in meters"""
    R = 6371000  # Earth radius in meters
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def nearest_neighbor_analysis(df):
    """Calculate nearest neighbor distances for all cameras"""
    print(f"\nCalculating nearest neighbors for {len(df)} cameras...")

    results = []
    for idx, camera in df.iterrows():
        min_distance = float('inf')
        nearest_id = None

        for idx2, other in df.iterrows():
            if idx != idx2:
                dist = haversine_distance(
                    camera['latitude'],
                    camera['longitude'],
                    other['latitude'],
                    other['longitude']
                )

                if dist < min_distance:
                    min_distance = dist
                    nearest_id = other['camera_id']

        results.append({
            'camera_id': camera['camera_id'],
            'location_name': camera['location_name'],
            'nearest_neighbor': nearest_id,
            'distance_m': min_distance,
            'distance_km': min_distance / 1000
        })

    results_df = pd.DataFrame(results)

    # Calculate statistics
    print(f"\nNearest Neighbor Statistics:")
    print(f" Minimum distance: {results_df['distance_m'].min():.0f} m")
    print(f" Maximum distance: {results_df['distance_m'].max():.0f} m")
    print(f" Mean distance: {results_df['distance_m'].mean():.0f} m")
    print(f" Median distance: {results_df['distance_m'].median():.0f} m")
    print(f" Std deviation: {results_df['distance_m'].std():.0f} m")

    # Find isolated cameras (>1km from nearest neighbor)
    isolated = results_df[results_df['distance_m'] > 1000]
    if len(isolated) > 0:
        print(f"\nIsolated cameras (>1km from nearest):")
        for _, row in isolated.iterrows():
            print(f" {row['camera_id']}: {row['distance_m']:.0f}m from nearest")

    # Find clustered cameras (<200m from nearest)
    clustered = results_df[results_df['distance_m'] < 200]
    print(f"\nClustered cameras (<200m): {len(clustered)}")

    return results_df


def visualize_nearest_neighbor(results_df, output_path):
    """Create histogram of nearest neighbor distances"""
    print(f"\nCreating distance distribution plot...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Histogram
    ax1.hist(
        results_df['distance_m'],
        bins=30,
        edgecolor='black',
        alpha=0.7,
        color='steelblue'
    )
    mean_dist = results_df['distance_m'].mean()
    ax1.axvline(
        mean_dist,
        color='red',
        linestyle='--',
        linewidth=2,
        label=f'Mean: {mean_dist:.0f}m'
    )
    ax1.set_xlabel('Distance to Nearest Neighbor (meters)', fontsize=12)
    ax1.set_ylabel('Frequency', fontsize=12)
    ax1.set_title(
        'Distribution of Nearest Neighbor Distances',
        fontsize=14,
        fontweight='bold'
    )
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Box plot
    ax2.boxplot(results_df['distance_m'], vert=True)
    ax2.set_ylabel('Distance (meters)', fontsize=12)
    ax2.set_title(
        'Nearest Neighbor Distance - Box Plot',
        fontsize=14,
        fontweight='bold'
    )
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to: {output_path}")
    plt.close()


def main():
    print("\n" + "=" * 60)
    print("📏 NEAREST NEIGHBOR ANALYSIS")
    print("=" * 60)

    df = pd.read_csv("data/sample_cameras.csv")
    results_df = nearest_neighbor_analysis(df)

    # Save results
    results_df.to_csv("maps/nearest_neighbor_results.csv", index=False)
    print(f"\nSaved results to: maps/nearest_neighbor_results.csv")

    # Visualize
    visualize_nearest_neighbor(
        results_df,
        "maps/nearest_neighbor_distribution.png"
    )

    print("NEAREST NEIGHBOR ANALYSIS COMPLETE!")


if __name__ == "__main__":
    main()
