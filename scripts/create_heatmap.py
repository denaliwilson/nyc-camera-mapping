import pandas as pd 
import folium 
from folium.plugins import HeatMap 

# Load data 
df = pd.read_csv("data/sample_cameras.csv") 
print(f"Loaded {len(df)} cameras") 

# Calculate center 
center_lat = df['latitude'].mean() 
center_lon = df['longitude'].mean() 

# Create map with dark theme 
m = folium.Map( location=[center_lat, center_lon], zoom_start=11, tiles='CartoDB dark_matter' ) 

# Prepare heat data - list of [lat, lon] pairs 
heat_data = [] 
for idx, row in df.iterrows(): heat_data.append([row['latitude'], row['longitude']]) 

# Add heat layer 
HeatMap( heat_data, radius=25, blur=35, gradient={ 0.0: 'blue', 0.3: 'cyan', 0.5: 'lime', 0.7: 'yellow', 1.0: 'red' } ).add_to(m) 

# Save 
m.save("maps/camera_heatmap.html") 
print("Heat map saved to: maps/camera_heatmap.html")