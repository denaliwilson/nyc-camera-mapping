"""
Camera Location Data Loader
============================

Loads camera location data from CSV and performs basic validation.

Usage:
    python scripts/load_cameras.py
"""

import pandas as pd
import sys
from pathlib import Path


# NYC Geographic Boundaries
NYC_BOUNDS = {
    'lat_min': 40.4774,
    'lat_max': 40.9176,
    'lon_min': -74.2591,
    'lon_max': -73.7004
}


def load_camera_data(filepath):
    """
    Load camera location data from CSV file.

    Parameters:
    -----------
    filepath : str
        Path to the CSV file containing camera data

    Returns:
    --------
    pandas.DataFrame
        DataFrame containing camera data, or None if loading fails
    """
    try:
        # Check if file exists
        if not Path(filepath).exists():
            print(f"ERROR: File not found - {filepath}")
            print(f" Current directory: {Path.cwd()}")
            return None

        # Load CSV file
        df = pd.read_csv(filepath)
        print("=" * 60)
        print("CAMERA DATA LOADED SUCCESSFULLY")
        print("=" * 60)
        print(f"File: {filepath}")
        print(f"Total cameras: {len(df)}")
        print(f"Columns: {len(df.columns)}")
        return df

    except pd.errors.EmptyDataError:
        print(f"ERROR: File is empty - {filepath}")
        return None

    except pd.errors.ParserError as e:
        print(f"ERROR: Could not parse CSV file")
        print(f" Details: {e}")
        return None

    except Exception as e:
        print(f"ERROR: Unexpected error loading data")
        print(f" Type: {type(e).__name__}")
        print(f" Details: {e}")
        return None


def display_basic_info(df):
    """
    Display basic information about the dataset.

    Parameters:
    -----------
    df : pandas.DataFrame
        Camera data
    """
    print("\n" + "=" * 60)
    print("DATASET INFORMATION")
    print("=" * 60)

    # Column names
    print(f"\nColumns ({len(df.columns)}):")
    for i, col in enumerate(df.columns, 1):
        print(f" {i}. {col}")

    # Data types
    print(f"\nData Types:")
    for col, dtype in df.dtypes.items():
        print(f" {col}: {dtype}")

    # Shape
    print(f"\nShape: {df.shape[0]} rows × {df.shape[1]} columns")

    # Memory usage
    memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
    print(f"Memory Usage: {memory_mb:.2f} MB")


def validate_coordinates(df):
    """
    Validate that coordinates fall within NYC boundaries.

    Parameters:
    -----------
    df : pandas.DataFrame
        Camera data with latitude and longitude columns
    """
    print("\n" + "=" * 60)
    print("COORDINATE VALIDATION")
    print("=" * 60)

    # Check if required columns exist
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        print("ERROR: Missing latitude or longitude columns")
        return

    # Validate latitude
    valid_lat = df[
        (df['latitude'] >= NYC_BOUNDS['lat_min']) &
        (df['latitude'] <= NYC_BOUNDS['lat_max'])
    ]

    # Validate longitude
    valid_lon = df[
        (df['longitude'] >= NYC_BOUNDS['lon_min']) &
        (df['longitude'] <= NYC_BOUNDS['lon_max'])
    ]

    # Both valid
    valid_both = df[
        (df['latitude'] >= NYC_BOUNDS['lat_min']) &
        (df['latitude'] <= NYC_BOUNDS['lat_max']) &
        (df['longitude'] >= NYC_BOUNDS['lon_min']) &
        (df['longitude'] <= NYC_BOUNDS['lon_max'])
    ]

    print(f"\nNYC Boundaries:")
    print(f" Latitude: {NYC_BOUNDS['lat_min']}° to {NYC_BOUNDS['lat_max']}°")
    print(f" Longitude: {NYC_BOUNDS['lon_min']}° to {NYC_BOUNDS['lon_max']}°")

    print(f"\nValidation Results:")
    print(f" Valid latitude: {len(valid_lat)}/{len(df)} cameras")
    print(f" Valid longitude: {len(valid_lon)}/{len(df)} cameras")
    print(f" Both valid: {len(valid_both)}/{len(df)} cameras")

    # Report invalid coordinates
    if len(valid_both) < len(df):
        invalid_count = len(df) - len(valid_both)
        print(f"\n Warning: {invalid_count} cameras have coordinates outside NYC bounds")

        # Show which cameras are invalid
        invalid_df = df[~df.index.isin(valid_both.index)]
        print(f"\n Invalid cameras:")
        for idx, row in invalid_df.iterrows():
            print(f" - {row['camera_id']}: ({row['latitude']}, {row['longitude']})")


def display_status_summary(df):
    """
    Display summary of camera status distribution.

    Parameters:
    -----------
    df : pandas.DataFrame
        Camera data with status column
    """
    print("\n" + "=" * 60)
    print("CAMERA STATUS SUMMARY")
    print("=" * 60)

    if 'status' not in df.columns:
        print("ERROR: No 'status' column found")
        return

    status_counts = df['status'].value_counts()
    total = len(df)

    print(f"\nStatus Distribution:")
    for status, count in status_counts.items():
        percentage = (count / total) * 100
        bar = "█" * int(percentage / 2)  # Visual bar
        print(f" {status:12} {count:3} ({percentage:5.1f}%) {bar}")

    print(f"\nTotal: {total} cameras")


def display_sample_data(df, n=5):
    """
    Display sample rows from the dataset.

    Parameters:
    -----------
    df : pandas.DataFrame
        Camera data
    n : int
        Number of rows to display (default: 5)
    """
    print("\n" + "=" * 60)
    print(f"SAMPLE DATA (First {n} cameras)")
    print("=" * 60)
    print()
    print(df.head(n).to_string(index=False))


def main():
    """Main execution function."""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║ NYC TRANSIT CAMERA DATA LOADER ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print()

    # File path
    filepath = "data/sample_cameras.csv"

    # Load data
    df = load_camera_data(filepath)
    if df is None:
        print("\nFailed to load data. Exiting.")
        sys.exit(1)

    # Display information
    display_basic_info(df)
    validate_coordinates(df)
    display_status_summary(df)
    display_sample_data(df, n=5)

    print("\n" + "=" * 60)
    print("DATA LOADING COMPLETE")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()

