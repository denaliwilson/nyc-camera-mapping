"""
Camera Data Validator
=====================

Comprehensive validation of camera location data.

Usage: python scripts/validate_data.py
"""

import pandas as pd
import sys
from pathlib import Path
from datetime import datetime


# NYC Geographic Boundaries
NYC_BOUNDS = {
    'lat_min': 40.4774,
    'lat_max': 40.9176,
    'lon_min': -74.2591,
    'lon_max': -73.7004
}

# Allowed status values
VALID_STATUSES = ['Active', 'Maintenance', 'Inactive']

# Required columns
REQUIRED_COLUMNS = [
    'camera_id',
    'location_name',
    'latitude',
    'longitude',
    'status',
    'installation_date'
]


class ValidationReport:
    """Track validation results."""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed = []

    def add_error(self, message):
        self.errors.append(message)

    def add_warning(self, message):
        self.warnings.append(message)

    def add_pass(self, message):
        self.passed.append(message)

    def print_report(self):
        """Print validation report."""
        print("\n" + "=" * 60)
        print("VALIDATION REPORT")
        print("=" * 60)

        # Passed checks
        if self.passed:
            print(f"\nPASSED ({len(self.passed)} checks):")
            for msg in self.passed:
                print(f" - {msg}")

        # Warnings
        if self.warnings:
            print(f"\nWARNINGS ({len(self.warnings)}):")
            for msg in self.warnings:
                print(f" ! {msg}")

        # Errors
        if self.errors:
            print(f"\nERRORS ({len(self.errors)}):")
            for msg in self.errors:
                print(f" - {msg}")

        # Summary
        print("\n" + "=" * 60)
        if self.errors:
            print("VALIDATION FAILED")
        elif self.warnings:
            print("VALIDATION PASSED WITH WARNINGS")
        else:
            print("VALIDATION PASSED")
        print("=" * 60)

        return len(self.errors) == 0


def load_data(filepath):
    """Load camera data from CSV."""
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        print(f"ERROR: Could not load {filepath}")
        print(f" {e}")
        sys.exit(1)


def validate_structure(df, report):
    """Validate dataset structure."""
    print("\nChecking dataset structure...")

    # Check required columns
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        report.add_error(f"Missing required columns: {', '.join(missing_columns)}")
    else:
        report.add_pass("All required columns present")

    # Check for extra columns
    extra_columns = [col for col in df.columns if col not in REQUIRED_COLUMNS]
    if extra_columns:
        report.add_warning(f"Extra columns found: {', '.join(extra_columns)}")

    # Check row count
    if len(df) == 0:
        report.add_error("Dataset is empty (0 rows)")
    else:
        report.add_pass(f"Dataset contains {len(df)} cameras")


def validate_camera_ids(df, report):
    """Validate camera ID field."""
    print("Checking camera IDs...")

    if 'camera_id' not in df.columns:
        return

    # Check for missing IDs
    missing_ids = df['camera_id'].isna().sum()
    if missing_ids > 0:
        report.add_error(f"{missing_ids} cameras have missing camera_id")
    else:
        report.add_pass("No missing camera IDs")

    # Check for duplicates
    duplicates = df['camera_id'].duplicated().sum()
    if duplicates > 0:
        duplicate_ids = df[df['camera_id'].duplicated(keep=False)]['camera_id'].unique()
        report.add_error(f"{duplicates} duplicate camera IDs: {', '.join(duplicate_ids)}")
    else:
        report.add_pass("No duplicate camera IDs")

    # Check ID format (should be CAM-XXX)
    invalid_format = []
    for cam_id in df['camera_id'].dropna():
        if not isinstance(cam_id, str):
            invalid_format.append(str(cam_id))
        elif not cam_id.startswith('CAM-'):
            invalid_format.append(cam_id)
        elif not cam_id[4:].isdigit() or len(cam_id) != 7:
            invalid_format.append(cam_id)

    if invalid_format:
        report.add_warning(f"Camera IDs with non-standard format: {', '.join(invalid_format[:5])}")
    else:
        report.add_pass("All camera IDs follow CAM-XXX format")


def validate_coordinates(df, report):
    """Validate latitude and longitude."""
    print("Checking coordinates...")

    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        return

    # Check for missing coordinates
    missing_lat = df['latitude'].isna().sum()
    missing_lon = df['longitude'].isna().sum()

    if missing_lat > 0:
        report.add_error(f"{missing_lat} cameras have missing latitude")
    else:
        report.add_pass("No missing latitude values")

    if missing_lon > 0:
        report.add_error(f"{missing_lon} cameras have missing longitude")
    else:
        report.add_pass("No missing longitude values")

    # Check coordinate bounds (NYC)
    invalid_lat = df[
        (df['latitude'].notna()) & 
        ((df['latitude'] < NYC_BOUNDS['lat_min']) | (df['latitude'] > NYC_BOUNDS['lat_max']))
    ]
    invalid_lon = df[
        (df['longitude'].notna()) & 
        ((df['longitude'] < NYC_BOUNDS['lon_min']) | (df['longitude'] > NYC_BOUNDS['lon_max']))
    ]

    if len(invalid_lat) > 0:
        cameras = invalid_lat['camera_id'].tolist()
        report.add_error(f"{len(invalid_lat)} cameras outside NYC latitude bounds: {', '.join(cameras)}")
    else:
        report.add_pass("All latitudes within NYC bounds")

    if len(invalid_lon) > 0:
        cameras = invalid_lon['camera_id'].tolist()
        report.add_error(f"{len(invalid_lon)} cameras outside NYC longitude bounds: {', '.join(cameras)}")
    else:
        report.add_pass("All longitudes within NYC bounds")

    # Check coordinate precision
    low_precision = []
    for idx, row in df.iterrows():
        if pd.notna(row['latitude']):
            lat_str = str(row['latitude'])
            if '.' in lat_str:
                decimals = len(lat_str.split('.')[1])
                if decimals < 4:
                    low_precision.append(row['camera_id'])

    if low_precision:
        report.add_warning(f"{len(low_precision)} cameras have low coordinate precision (<4 decimals)")


def validate_status(df, report):
    """Validate status field."""
    print("Checking status values...")

    if 'status' not in df.columns:
        return

    # Check for missing status
    missing_status = df['status'].isna().sum()
    if missing_status > 0:
        report.add_error(f"{missing_status} cameras have missing status")
    else:
        report.add_pass("No missing status values")

    # Check for invalid status values
    invalid_status = df[~df['status'].isin(VALID_STATUSES + [pd.NA, None])]
    if len(invalid_status) > 0:
        unique_invalid = invalid_status['status'].unique()
        report.add_error(f"Invalid status values found: {', '.join(map(str, unique_invalid))}")
        report.add_error(f"Valid values are: {', '.join(VALID_STATUSES)}")
    else:
        report.add_pass(f"All status values valid ({', '.join(VALID_STATUSES)})")


def validate_dates(df, report):
    """Validate installation_date field."""
    print("Checking installation dates...")

    if 'installation_date' not in df.columns:
        return

    # Check for missing dates
    missing_dates = df['installation_date'].isna().sum()
    if missing_dates > 0:
        report.add_error(f"{missing_dates} cameras have missing installation_date")
    else:
        report.add_pass("No missing installation dates")

    # Try to parse dates
    invalid_dates = []
    future_dates = []
    today = datetime.now().date()

    for idx, row in df.iterrows():
        if pd.notna(row['installation_date']):
            try:
                date_obj = pd.to_datetime(row['installation_date']).date()
                # Check if date is in the future
                if date_obj > today:
                    future_dates.append(row['camera_id'])
            except:
                invalid_dates.append(row['camera_id'])

    if invalid_dates:
        report.add_error(f"{len(invalid_dates)} cameras have invalid date format: {', '.join(invalid_dates)}")
    else:
        report.add_pass("All dates in valid format (YYYY-MM-DD)")

    if future_dates:
        report.add_warning(f"{len(future_dates)} cameras have future installation dates: {', '.join(future_dates)}")


def validate_location_names(df, report):
    """Validate location_name field."""
    print("Checking location names...")

    if 'location_name' not in df.columns:
        return

    # Check for missing names
    missing_names = df['location_name'].isna().sum()
    if missing_names > 0:
        report.add_error(f"{missing_names} cameras have missing location_name")
    else:
        report.add_pass("No missing location names")

    # Check for empty strings
    empty_names = (df['location_name'] == '').sum()
    if empty_names > 0:
        report.add_error(f"{empty_names} cameras have empty location_name")

    # Check for very short names
    if 'location_name' in df.columns:
        short_names = df[df['location_name'].str.len() < 5]
        if len(short_names) > 0:
            report.add_warning(f"{len(short_names)} cameras have very short location names (<5 chars)")


def main():
    """Main execution function."""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║ NYC CAMERA DATA VALIDATOR ║")
    print("╚═══════════════════════════════════════════════════════════╝")

    # Load data
    filepath = "data/sample_cameras.csv"
    print(f"\nLoading data from: {filepath}")
    df = load_data(filepath)
    print(f"Loaded {len(df)} cameras\n")

    # Create validation report
    report = ValidationReport()

    # Run validation checks
    validate_structure(df, report)
    validate_camera_ids(df, report)
    validate_coordinates(df, report)
    validate_status(df, report)
    validate_dates(df, report)
    validate_location_names(df, report)

    # Print report
    success = report.print_report()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
