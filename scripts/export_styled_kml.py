"""Export styled KML with color-coded cameras"""

import pandas as pd
import simplekml


def load_cameras():
    df = pd.read_csv("data/sample_cameras.csv")
    print(f"Loaded {len(df)} cameras")
    return df


def get_icon_color(status):
    """Get color code for camera status"""
    colors = {
        'Active': 'ff00ff00',         # Green (AABBGGRR format)
        'Maintenance': 'ff00a5ff',    # Orange
        'Inactive': 'ff0000ff'        # Red
    }
    return colors.get(status, 'ffffffff')  # White default


def create_styled_kml(df, output_path):
    """Create KML with styled markers"""
    print("\nCreating styled KML...")

    # Create KML
    kml = simplekml.Kml()
    kml.document.name = "NYC Camera Network (Styled)"

    # Create folders for each status
    active_folder = kml.newfolder(name="Active Cameras")
    maintenance_folder = kml.newfolder(name="Maintenance")
    inactive_folder = kml.newfolder(name="Inactive Cameras")

    # Map status to folder
    folder_map = {
        'Active': active_folder,
        'Maintenance': maintenance_folder,
        'Inactive': inactive_folder,
    }

    # Add cameras
    for idx, row in df.iterrows():
        # Get the right folder
        folder = folder_map.get(row['status'], kml)

        # Create description
        status_emoji = {
            'Active': '',
            'Maintenance': '',
            'Inactive': ''
        }
        emoji = status_emoji.get(row['status'], '')

        description = f"""
            <h2>{emoji} {row['camera_id']}</h2>
            <p><b>Location:</b> {row['location_name']}</p>
            <p><b>Status:</b> {row['status']}</p>
            <p><b>Installed:</b> {row['installation_date']}</p>
            <hr>
            <p style="font-size:0.9em; color:#666;">
            Coordinates: {row['latitude']:.4f}°N, {abs(row['longitude']):.4f}°W
            </p>
        """

        # Create point in folder
        pnt = folder.newpoint(
            name=f"{row['camera_id']} - {row['location_name'][:30]}",
            description=description,
            coords=[(row['longitude'], row['latitude'])]
        )

        # Style the icon
        pnt.style.iconstyle.color = get_icon_color(row['status'])
        pnt.style.iconstyle.scale = 1.2
        pnt.style.iconstyle.icon.href = (
            'http://maps.google.com/mapfiles/kml/shapes/webcam.png'
        )

        # Style the label
        pnt.style.labelstyle.scale = 0.8

    # Save
    kml.save(output_path)
    print(f"Styled KML saved to: {output_path}")

    # Print summary
    print("\nSummary:")
    active_count = len(df[df['status'] == 'Active'])
    maintenance_count = len(df[df['status'] == 'Maintenance'])
    inactive_count = len(df[df['status'] == 'Inactive'])
    print(f" Active: {active_count} cameras")
    print(f" Maintenance: {maintenance_count} cameras")
    print(f" Inactive: {inactive_count} cameras")


def main():
    print("\n" + "=" * 60)
    print("STYLED KML EXPORT")
    print("=" * 60)
    df = load_cameras()
    output_path = "maps/cameras_styled.kml"
    create_styled_kml(df, output_path)
    print("\nDone! Open in Google Earth to see color-coded cameras!")


if __name__ == "__main__":
    main()
