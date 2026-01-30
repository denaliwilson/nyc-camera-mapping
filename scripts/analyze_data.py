"""
Camera Data Analyzer
====================
Statistical analysis and insights from camera location data.

Usage: python scripts/analyze_data.py
"""

from py_compile import main
import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter

# NYC Borough Boundaries
BOROUGH_BOUNDS = {
    'Manhattan': {'lat_min': 40.7001, 'lat_max': 40.8824, 'lon_min': -74.0250, 'lon_max': -73.9069},
    'Brooklyn': {'lat_min': 40.5603, 'lat_max': 40.7282, 'lon_min': -74.0420, 'lon_max': -73.8332},
    'Queens': {'lat_min': 40.5450, 'lat_max': 40.8097, 'lon_min': -73.9628, 'lon_max': -73.6911},
    'Bronx': {'lat_min': 40.7850, 'lat_max': 40.9176, 'lon_min': -73.9680, 'lon_max': -73.7597},
    'Staten Island': {'lat_min': 40.4774, 'lat_max': 40.6513, 'lon_min': -74.2591, 'lon_max': -74.0300}
}


def load_data(filepath):
    """Load camera data."""
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        print(f"ERROR: Could not load {filepath}: {e}")
        return None


def assign_borough(lat, lon):
    """
    Assign borough based on coordinates (approximate).

    Parameters:
    -----------
    lat : float
        Latitude
    lon : float
        Longitude

    Returns:
    --------
    str : Borough name or 'Unknown'
    """
    for borough, bounds in BOROUGH_BOUNDS.items():
        if (bounds['lat_min'] <= lat <= bounds['lat_max'] and
                bounds['lon_min'] <= lon <= bounds['lon_max']):
            return borough
    return 'Unknown'


def analyze_status_distribution(df):
    """Analyze camera status distribution."""
    print("\n" + "=" * 60)
    print("STATUS DISTRIBUTION ANALYSIS")
    print("=" * 60)

    if 'status' not in df.columns:
        print("ERROR: No status column found")
        return

    status_counts = df['status'].value_counts()
    total = len(df)

    print(f"\nTotal Cameras: {total}")
    print("\nStatus Breakdown:")
    for status, count in status_counts.items():
        percentage = (count / total) * 100
        bar = "█" * int(percentage / 2)
        print(f" {status:12} {count:3} ({percentage:5.1f}%) {bar}")

    # Calculate operational percentage
    if 'Active' in status_counts:
        operational_pct = (status_counts['Active'] / total) * 100
        print(f"\nOperational Rate: {operational_pct:.1f}%")


def analyze_geographic_distribution(df):
    """Analyze camera distribution across boroughs."""
    print("\n" + "=" * 60)
    print("GEOGRAPHIC DISTRIBUTION ANALYSIS")
    print("=" * 60)

    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        print("ERROR: No coordinate columns found")
        return

    # Assign boroughs
    df['borough'] = df.apply(
        lambda row: assign_borough(row['latitude'], row['longitude']),
        axis=1
    )

    borough_counts = df['borough'].value_counts()
    total = len(df)

    print(f"\nCameras by Borough:")
    for borough, count in borough_counts.items():
        percentage = (count / total) * 100
        bar = "█" * int(percentage / 3)
        print(f" {borough:15} {count:3} ({percentage:5.1f}%) {bar}")

    # Calculate bounding box
    lat_min, lat_max = df['latitude'].min(), df['latitude'].max()
    lon_min, lon_max = df['longitude'].min(), df['longitude'].max()

    print(f"\nGeographic Extent:")
    print(f" Latitude: {lat_min:.4f}° to {lat_max:.4f}° (range: {lat_max - lat_min:.4f}°)")
    print(f" Longitude: {lon_min:.4f}° to {lon_max:.4f}° (range: {lon_max - lon_min:.4f}°)")

    # Calculate center point
    lat_center = (lat_min + lat_max) / 2
    lon_center = (lon_min + lon_max) / 2
    print(f" Center: ({lat_center:.4f}°, {lon_center:.4f}°)")


def analyze_installation_timeline(df):
    """Analyze installation dates and timeline."""
    print("\n" + "=" * 60)
    print("INSTALLATION TIMELINE ANALYSIS")
    print("=" * 60)

    if 'installation_date' not in df.columns:
        print("ERROR: No installation_date column found")
        return

    # Convert to datetime
    df['install_dt'] = pd.to_datetime(df['installation_date'], errors='coerce')

    # Remove invalid dates
    valid_dates = df[df['install_dt'].notna()]

    if len(valid_dates) == 0:
        print("ERROR: No valid installation dates found")
        return

    print(f"\nInstallation Date Range:")
    earliest = valid_dates['install_dt'].min()
    latest = valid_dates['install_dt'].max()
    print(f" Earliest: {earliest.strftime('%Y-%m-%d')}")
    print(f" Latest: {latest.strftime('%Y-%m-%d')}")

    days_span = (latest - earliest).days
    print(f" Span: {days_span} days ({days_span / 365.25:.1f} years)")

    # Group by year
    valid_dates['year'] = valid_dates['install_dt'].dt.year
    yearly_counts = valid_dates['year'].value_counts().sort_index()

    print(f"\nInstallations by Year:")
    for year, count in yearly_counts.items():
        bar = "█" * (count * 2)
        print(f" {year}: {count:2} {bar}")

    # Group by month
    valid_dates['year_month'] = valid_dates['install_dt'].dt.to_period('M')
    monthly_counts = valid_dates['year_month'].value_counts().sort_index()

    if len(monthly_counts) <= 12:
        print(f"\nInstallations by Month:")
        for month, count in monthly_counts.items():
            print(f" {month}: {count}")


def analyze_naming_patterns(df):
    """Analyze location naming patterns."""
    print("\n" + "=" * 60)
    print("LOCATION NAMING ANALYSIS")
    print("=" * 60)

    if 'location_name' not in df.columns:
        print("ERROR: No location_name column found")
        return

    # Name length statistics
    name_lengths = df['location_name'].str.len()

    print(f"\nLocation Name Length Statistics:")
    print(f" Shortest: {name_lengths.min()} characters")
    print(f" Longest: {name_lengths.max()} characters")
    print(f" Average: {name_lengths.mean():.1f} characters")
    print(f" Median: {name_lengths.median():.1f} characters")

    # Common words in location names
    all_words = []
    for name in df['location_name'].dropna():
        words = name.lower().split()
        all_words.extend(words)

    word_counts = Counter(all_words)

    # Exclude very common words
    exclude_words = {'the', 'and', 'of', 'to', 'a', 'in', 'at', '-'}
    filtered_words = {word: count for word, count in word_counts.items()
                      if word not in exclude_words}

    most_common = sorted(filtered_words.items(), key=lambda x: x[1], reverse=True)[:10]

    print(f"\nMost Common Words in Location Names:")
    for word, count in most_common:
        print(f" '{word}': {count} times")


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two points using Haversine formula.

    Returns distance in meters.
    """
    from math import radians, sin, cos, sqrt, atan2

    R = 6371000  # Earth radius in meters
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c


def analyze_spatial_distribution(df):
    """Analyze spatial distribution and spacing."""
    print("\n" + "=" * 60)
    print("SPATIAL DISTRIBUTION ANALYSIS")
    print("=" * 60)

    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        print("ERROR: No coordinate columns found")
        return

    if len(df) < 2:
        print("ERROR: Need at least 2 cameras for spatial analysis")
        return

    # Calculate distance to nearest neighbor for each camera
    nearest_distances = []
    for idx, camera in df.iterrows():
        distances = []
        for idx2, other_camera in df.iterrows():
            if idx != idx2:
                dist = calculate_distance(
                    camera['latitude'], camera['longitude'],
                    other_camera['latitude'], other_camera['longitude']
                )
                distances.append(dist)
        if distances:
            nearest_distances.append(min(distances))

    nearest_distances = np.array(nearest_distances)

    print(f"\nNearest Neighbor Distance Statistics:")
    print(f" Minimum: {nearest_distances.min():.0f} meters")
    print(f" Maximum: {nearest_distances.max():.0f} meters")
    print(f" Average: {nearest_distances.mean():.0f} meters")
    print(f" Median: {np.median(nearest_distances):.0f} meters")
    print(f" Std Dev: {nearest_distances.std():.0f} meters")

    # Identify clusters (cameras within 500m of each other)
    close_pairs = nearest_distances < 500
    cluster_count = close_pairs.sum()

    print(f"\nSpatial Clustering:")
    print(f" Cameras within 500m of another: {cluster_count} ({cluster_count/len(df)*100:.1f}%)")

    # Identify isolated cameras (>1km from nearest neighbor)
    isolated = nearest_distances > 1000
    isolated_count = isolated.sum()

    if isolated_count > 0:
        print(f" Isolated cameras (>1km from nearest): {isolated_count}")


def generate_summary(df):
    """Generate overall summary statistics."""
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)

    print(f"\nDataset Overview:")
    print(f" Total Cameras: {len(df)}")
    print(f" Total Columns: {len(df.columns)}")
    print(f" Memory Usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")

    # Data completeness
    completeness = (1 - df.isna().sum() / len(df)) * 100
    avg_completeness = completeness.mean()

    print(f"\nData Completeness:")
    print(f" Average: {avg_completeness:.1f}%")

    for col in df.columns:
        comp = completeness[col]
        if comp < 100:
            missing = df[col].isna().sum()
            print(f" {col}: {comp:.1f}% ({missing} missing)")


def main():
    """Main execution function."""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║ NYC CAMERA DATA ANALYZER ║")
    print("╚═══════════════════════════════════════════════════════════╝")

    # Load data
    filepath = "data/sample_cameras.csv"
    print(f"\nLoading data from: {filepath}")
    df = load_data(filepath)

    if df is None:
        return

    print(f"Loaded {len(df)} cameras")

    # Run analyses
    generate_summary(df)
    analyze_status_distribution(df)
    analyze_geographic_distribution(df)
    analyze_installation_timeline(df)
    analyze_spatial_distribution(df)
    analyze_naming_patterns(df)

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
