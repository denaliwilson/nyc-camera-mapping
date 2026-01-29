import pandas as pd 
import folium 
from folium.plugins import MarkerCluster 

# Load data 
df = pd.read_csv("data/sample_cameras.csv") 
print(f"Loaded {len(df)} cameras") 

# Get color 
def get_color(status): 
    if status == 'Active': return 'green' 
    elif status == 'Maintenance': return 'orange' 
    elif status == 'Offline': return 'red' 
    else: return 'gray' 

# Calculate center 
center_lat = df['latitude'].mean() 
center_lon = df['longitude'].mean() 

# Create map 
m = folium.Map( location=[center_lat, center_lon], zoom_start=11, tiles='OpenStreetMap' ) 

# Create marker cluster 
marker_cluster = MarkerCluster().add_to(m) 

# Add markers to cluster 
for idx, row in df.iterrows(): 
    popup_text = f""" <b>{row['camera_id']}</b><br> {row['location_name']}<br> Status: {row['status']} """ 
    folium.Marker( location=[row['latitude'], row['longitude']], popup=popup_text, tooltip=row['camera_id'], icon=folium.Icon(color=get_color(row['status'])) ).add_to(marker_cluster) 

# Save 
m.save("maps/camera_cluster_map.html") 
print("Cluster map saved to: maps/camera_cluster_map.html") 

print("Try zooming in and out!")