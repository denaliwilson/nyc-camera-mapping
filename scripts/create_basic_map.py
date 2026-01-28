import pandas as pd 
import folium 

# Load camera data
df = pd.read_csv("data/sample_cameras.csv")
print(f"Loaded {len(df)} cameras")

# Get color based on status
def get_color(status):
    if status == 'Active':
        return 'green'
    elif status == 'Maintenance':
        return 'orange'
    elif status == 'Offline':
        return 'red'
    else:
        return 'gray'

# Calculate center of map
center_lat = df['latitude'].mean()
center_lon = df['longitude'].mean()

# Create map
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=11,
    tiles='OpenStreetMap'
)

# Add each camera as a marker
for idx, row in df.iterrows():
    popup_text = f""" <b>{row['camera_id']}</b><br> {row['location_name']}<br> Status: {row['status']}<br> Installed: {row['installation_date']} """
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup_text,
        tooltip=row['camera_id'],
        icon=folium.Icon(color=get_color(row['status']))
    ).add_to(m)

# Save map
m.save("maps/camera_map_basic.html")
print("Map saved to: maps/camera_map_basic.html") 
print("Open this file in your browser!")