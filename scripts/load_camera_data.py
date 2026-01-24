# scripts/load_camera_data.py
import pandas as pd 

def load_camera_data(filepath):
    """Load camera location data from CSV file."""
    try:
        df = pd.read_csv(filepath)
        print(f"✅ Loaded {len(df)} camera locations")
        print(f"\nColumns: {', '.join(df.columns)}")
        # Validate coordinates are in NYC range
        nyc_lat_min, nyc_lat_max = 40.4774, 40.9176
        nyc_lon_min, nyc_lon_max = -74.2591, -73.7004
        valid_coords = df[
            (df['latitude'] >= nyc_lat_min) &
            (df['latitude'] <= nyc_lat_max) &
            (df['longitude'] >= nyc_lon_min) &
            (df['longitude'] <= nyc_lon_max)
        ]
        print(f"\n✅ {len(valid_coords)} cameras have valid NYC coordinates")
        if len(valid_coords) < len(df):
            invalid = len(df) - len(valid_coords)
            print(f"⚠️ {invalid} cameras have coordinates outside NYC")
        return df
    except FileNotFoundError:
        print(f"❌ Error: Could not find file {filepath}")
        return None
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

if __name__ == "__main__":
    # Test the function
    cameras = load_camera_data("data/sample_cameras.csv")
    if cameras is not None:
        print("\n📊 Sample Data:")
        print(cameras.head())