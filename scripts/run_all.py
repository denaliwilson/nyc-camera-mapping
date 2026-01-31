"""Master script to run the complete analysis pipeline.

This script runs repository analysis scripts in sequence and prints a
concise success/failure summary.
"""

from __future__ import annotations

import subprocess
import sys
from typing import List, Tuple


def run_script(script_path: str, description: str) -> bool:
    """Run a Python script and return True on success.

    Parameters
    ----------
    script_path
        Relative path to the script to run (e.g. "scripts/load_cameras.py").
    description
        Short human-readable description used in console output.
    """
    print("\n" + "=" * 60)
    print(f"Running: {description}")
    print("=" * 60)

    try:
        subprocess.run([sys.executable, script_path], check=True)
        print(f"{description} completed successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"{description} failed")
        return False


def main() -> None:
    print("\nNYC CAMERA ANALYSIS - COMPLETE PIPELINE")
    print("=" * 60)

    scripts: List[Tuple[str, str]] = [
        ("scripts/load_cameras.py", "Data Loading"),
        ("scripts/validate_data.py", "Data Validation"),
        ("scripts/analyze_data.py", "Statistical Analysis"),
        ("scripts/create_basic_map.py", "Basic Map Creation"),
        ("scripts/create_heatmap.py", "Heat Map Creation"),
        ("scripts/create_cluster_map.py", "Cluster Map Creation"),
        ("scripts/calculate_coverage.py", "Coverage Analysis"),
        ("scripts/find_gaps.py", "Gap Detection"),
        ("scripts/nearest_neighbor.py", "Nearest Neighbor Analysis"),
        ("scripts/detect_clusters.py", "Cluster Detection"),
        ("scripts/density_analysis.py", "Density Analysis"),
        ("scripts/export_to_kml.py", "KML Export"),
        ("scripts/export_to_geoJSON.py", "GeoJSON Export"),
        ("scripts/export_styled_kml.py", "Styled KML Export"),
        ("scripts/generate_reports.py", "Report Generation"),
    ]

    results: List[Tuple[str, bool]] = []

    for path, desc in scripts:
        success = run_script(path, desc)
        results.append((desc, success))

    # Summary
    print("\n" + "=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)

    for desc, success in results:
        status = "OK" if success else "FAILED"
        print(f"{status:7} {desc}")

    total = len(results)
    successful = sum(1 for _, s in results if s)

    print(f"\nCompleted: {successful}/{total} tasks")

    if successful == total:
        print("\nALL ANALYSES COMPLETED SUCCESSFULLY")
    else:
        print("\nSome tasks failed. Check output above for details.")


if __name__ == "__main__":
    main()
