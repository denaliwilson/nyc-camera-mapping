"""Generate comprehensive analysis report"""

import pandas as pd
from datetime import datetime


def generate_report():
    """Generate aggregated textual analysis report using existing results."""
    print("\nGenerating comprehensive analysis report...")

    # Load data
    df = pd.read_csv("data/sample_cameras.csv")

    # Load analysis results
    try:
        nn_results = pd.read_csv("maps/nearest_neighbor_results.csv")
        clusters = pd.read_csv("maps/camera_clusters.csv")
    except FileNotFoundError:
        print("Run previous analyses first!")
        return

    # Create report
    report = []
    report.append("=" * 70)
    report.append("NYC TRANSIT CAMERA NETWORK - SPATIAL ANALYSIS REPORT")
    report.append("=" * 70)
    report.append(
        f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    report.append("Analyst: Denali Wilson")
    report.append("\n" + "=" * 70)

    # Section 1: Dataset Overview
    report.append("\n1. DATASET OVERVIEW")
    report.append("-" * 70)
    report.append(f"Total Cameras: {len(df)}")
    report.append(
        f"Date Range: {df['installation_date'].min()} to {df['installation_date'].max()}"
    )
    report.append("\nStatus Distribution:")
    for status, count in df['status'].value_counts().items():
        pct = (count / len(df)) * 100
        report.append(f" {status}: {count} ({pct:.1f}%)")

    # Section 2: Spatial Distribution
    report.append("\n\n2. SPATIAL DISTRIBUTION")
    report.append("-" * 70)
    bounds = [
        df['latitude'].min(),
        df['latitude'].max(),
        df['longitude'].min(),
        df['longitude'].max(),
    ]
    report.append("Geographic Extent:")
    report.append(f" Latitude: {bounds[0]:.4f}° to {bounds[1]:.4f}°")
    report.append(f" Longitude: {bounds[2]:.4f}° to {bounds[3]:.4f}°")

    # Section 3: Nearest Neighbor Analysis
    report.append("\n\n3. NEAREST NEIGHBOR ANALYSIS")
    report.append("-" * 70)
    report.append("Statistics (distance to nearest camera):")
    report.append(f" Minimum: {nn_results['distance_m'].min():.0f} meters")
    report.append(f" Maximum: {nn_results['distance_m'].max():.0f} meters")
    report.append(f" Mean: {nn_results['distance_m'].mean():.0f} meters")
    report.append(f" Median: {nn_results['distance_m'].median():.0f} meters")
    isolated = nn_results[nn_results['distance_m'] > 1000]
    report.append(f"\nIsolated Cameras (>1km from nearest): {len(isolated)}")

    # Section 4: Cluster Analysis
    report.append("\n\n4. CLUSTER ANALYSIS")
    report.append("-" * 70)
    n_clusters = len(clusters['cluster'].unique()) - (
        1 if -1 in clusters['cluster'].values else 0
    )
    report.append(f"Clusters Detected: {n_clusters}")
    report.append(f"Cameras in Clusters: {len(clusters[clusters['cluster'] != -1])}")
    report.append(f"Isolated Cameras: {len(clusters[clusters['cluster'] == -1])}")

    # Section 5: Coverage Analysis
    report.append("\n\n5. COVERAGE ANALYSIS")
    report.append("-" * 70)
    report.append("Assumed Coverage Radius: 50 meters")
    report.append("Individual Coverage Area per Camera: ~7,854 m²")
    report.append(f"Theoretical Total Coverage: ~{len(df) * 7854:,} m²")
    report.append("Note: Actual coverage less due to overlapping zones")

    # Section 6: Recommendations
    report.append("\n\n6. RECOMMENDATIONS")
    report.append("-" * 70)
    report.append("• Review isolated cameras for strategic importance")
    report.append("• Consider additional cameras in identified gap areas")
    report.append("• Clusters may indicate high-traffic zones requiring monitoring")
    report.append("• Regular maintenance needed for offline/maintenance cameras")

    # Section 7: Visualizations Generated
    report.append("\n\n7. VISUALIZATIONS GENERATED")
    report.append("-" * 70)
    report.append("• maps/coverage_zones.png - Coverage buffer zones")
    report.append("• maps/coverage_gaps.png - Coverage gap analysis")
    report.append("• maps/nearest_neighbor_distribution.png - Distance distribution")
    report.append("• maps/camera_clusters.png - Cluster detection results")
    report.append("• maps/camera_density.png - Density heatmap")

    report.append("\n\n" + "=" * 70)
    report.append("END OF REPORT")
    report.append("=" * 70)

    # Save report
    report_text = "\n".join(report)
    with open("maps/analysis_report.txt", "w") as f:
        f.write(report_text)

    print("Report saved to: maps/analysis_report.txt")
    print("\n" + report_text)


def main():
    print("\n" + "=" * 60)
    print("ANALYSIS REPORT GENERATOR")
    print("=" * 60)
    generate_report()
    print("\nREPORT GENERATION COMPLETE!")
    print()


if __name__ == "__main__":
    main()