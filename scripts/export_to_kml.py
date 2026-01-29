"""
Export Camera Data to KML Format
=================================

Export camera data to KML format for Google Earth.

Usage:
    python scripts/export_to_kml.py
"""

import pandas as pd
import simplekml


def load_cameras():
    """
    Load camera data from CSV.

    Returns:
    --------
    pandas.DataFrame
        Camera data
    """
    df = pd.read_csv("data/sample_cameras.csv")
    print(f"✅ Loaded {len(df)} cameras")
    return df


def create_kml(df, output_path):
    """
    Create KML file with all cameras.

    Parameters:
    -----------
    df : pandas.DataFrame
        Camera data
    output_path : str
        Where to save the KML file
    """
    print("\n📦 Creating KML file...")

    # Create KML document
    kml = simplekml.Kml()
    kml.document.name = "NYC Transit Camera Network"
    kml.document.description = (
        f"{len(df)} security cameras across NYC transit stations"
    )

    # Add each camera as a point
    for idx, row in df.iterrows():
        # Create description with HTML
        description = f"""
        <h3>Camera Details</h3>
        <table>
        <tr><td><b>Camera ID:</b></td><td>{row['camera_id']}</td></tr>
        <tr><td><b>Location:</b></td><td>{row['location_name']}</td></tr>
        <tr><td><b>Status:</b></td><td>{row['status']}</td></tr>
        <tr><td><b>Installed:</b></td><td>{row['installation_date']}</td></tr>
        </table>
        """

        # Create point (note: KML uses lon, lat order!)
        pnt = kml.newpoint(
            name=row['camera_id'],
            description=description,
            coords=[(row['longitude'], row['latitude'])]
        )

        # Set label to show camera ID
        pnt.style.labelstyle.scale = 0.7

    # Save KML file
    kml.save(output_path)
    print(f"✅ KML saved to: {output_path}")
    print(f"📂 File size: {len(df)} placemarks")


def main():
    """Main execution function."""
    print("\n" + "=" * 60)
    print("📦 KML EXPORT TOOL")
    print("=" * 60)

    # Load data
    df = load_cameras()

    # Create KML
    output_path = "maps/cameras.kml"
    create_kml(df, output_path)

    print("\n" + "=" * 60)
    print("✅ KML EXPORT COMPLETE!")
    print("=" * 60)

    print("\nNext steps:")
    print("1. Download Google Earth Pro (free)")
    print("2. Open cameras.kml in Google Earth")
    print("3. Fly through NYC and see your cameras!")
    print()


if __name__ == "__main__":
    main()
