"""Detect camera clusters using DBSCAN"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN


def load_cameras():
    df = pd.read_csv("data/sample_cameras.csv")
    return df


def detect_clusters(df, epsilon_km=0.5):
    """Detect clusters of cameras using DBSCAN.

    Parameters
    ----------
    df : DataFrame
        Camera data
    epsilon_km : float
        Maximum distance between cameras in same cluster (km)
    """
    print(f"\n🎯 Detecting clusters (epsilon={epsilon_km}km)...")

    # Prepare coordinates
    coords = df[['latitude', 'longitude']].values

    # Convert epsilon from km to degrees (approximate)
    # At NYC latitude (~40.7°), 1 degree ≈ 111km
    epsilon_deg = epsilon_km / 111.0

    # Run DBSCAN
    dbscan = DBSCAN(eps=epsilon_deg, min_samples=3)
    clusters = dbscan.fit_predict(coords)
    df['cluster'] = clusters

    # Analyze results
    n_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)
    n_noise = list(clusters).count(-1)

    print(f"\n📊 Cluster Analysis Results:")
    print(f" Number of clusters found: {n_clusters}")
    print(f" Cameras in clusters: {len(df[df['cluster'] != -1])}")
    print(f" Isolated cameras (noise): {n_noise}")

    # Detail each cluster
    for cluster_id in range(n_clusters):
        cluster_cameras = df[df['cluster'] == cluster_id]
        print(f"\n Cluster {cluster_id}:")
        print(f" Cameras: {len(cluster_cameras)}")

        camera_ids = cluster_cameras['camera_id'].tolist()[:5]
        print(f" Camera IDs: {', '.join(camera_ids)}")

        if len(cluster_cameras) > 5:
            remaining = len(cluster_cameras) - 5
            print(f" ... and {remaining} more")

    return df


def visualize_clusters(df, output_path):
    """Visualize detected clusters"""
    print(f"\n🎨 Creating cluster visualization...")

    fig, ax = plt.subplots(figsize=(15, 12))

    # Plot each cluster in different color
    unique_clusters = df['cluster'].unique()
    colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_clusters)))

    for cluster_id, color in zip(sorted(unique_clusters), colors):
        cluster_data = df[df['cluster'] == cluster_id]

        if cluster_id == -1:
            # Noise points (not in any cluster)
            ax.scatter(
                cluster_data['longitude'],
                cluster_data['latitude'],
                c='gray',
                marker='x',
                s=100,
                alpha=0.5,
                label='Isolated cameras'
            )
        else:
            label = f'Cluster {cluster_id} ({len(cluster_data)} cameras)'
            ax.scatter(
                cluster_data['longitude'],
                cluster_data['latitude'],
                c=[color],
                marker='o',
                s=150,
                label=label,
                edgecolors='black',
                linewidth=1.5
            )

    ax.set_title('Camera Clusters (DBSCAN)', fontsize=16, fontweight='bold')
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.legend(
        bbox_to_anchor=(1.05, 1),
        loc='upper left',
        fontsize=10
    )
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved to: {output_path}")
    plt.close()


def main():
    print("\n" + "=" * 60)
    print("🎯 CLUSTER DETECTION ANALYSIS")
    print("=" * 60)

    df = load_cameras()
    df_clustered = detect_clusters(df, epsilon_km=0.5)

    # Save results
    df_clustered.to_csv("maps/camera_clusters.csv", index=False)
    print(f"\n💾 Saved cluster assignments to: maps/camera_clusters.csv")

    # Visualize
    visualize_clusters(df_clustered, "maps/camera_clusters.png")

    print("\n✅ CLUSTER DETECTION COMPLETE!")


if __name__ == "__main__":
    main()