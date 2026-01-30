"""Analyze camera density across grid cells"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


def load_cameras():
	"""Load camera CSV into a DataFrame."""
	df = pd.read_csv("data/sample_cameras.csv")
	return df


def calculate_density(df):
	"""Calculate 2D kernel density estimation.

	Returns lon_mesh, lat_mesh, density array for plotting.
	"""
	print("\n📊 Calculating density distribution...")

	# Extract coordinates
	x = df['longitude'].values
	y = df['latitude'].values

	# Calculate 2D kernel density
	xy = np.vstack([x, y])
	kde = gaussian_kde(xy)

	# Create grid
	lon_min, lon_max = x.min(), x.max()
	lat_min, lat_max = y.min(), y.max()
	lon_grid = np.linspace(lon_min, lon_max, 100)
	lat_grid = np.linspace(lat_min, lat_max, 100)
	lon_mesh, lat_mesh = np.meshgrid(lon_grid, lat_grid)
	grid_coords = np.vstack([lon_mesh.ravel(), lat_mesh.ravel()])

	# Evaluate density
	density = kde(grid_coords).reshape(lon_mesh.shape)

	return lon_mesh, lat_mesh, density


def visualize_density(df, lon_mesh, lat_mesh, density, output_path):
	"""Create density heatmap and save to file."""
	print("\n🎨 Creating density heatmap...")

	fig, ax = plt.subplots(figsize=(15, 12))

	# Plot density
	im = ax.contourf(
		lon_mesh,
		lat_mesh,
		density,
		levels=20,
		cmap='YlOrRd',
		alpha=0.7,
	)

	# Plot camera locations
	ax.scatter(
		df['longitude'],
		df['latitude'],
		c='blue',
		s=50,
		marker='o',
		edgecolors='white',
		linewidth=1.5,
		label='Cameras',
		zorder=5,
	)

	# Add colorbar
	cbar = plt.colorbar(im, ax=ax)
	cbar.set_label('Camera Density', fontsize=12)

	ax.set_title('Camera Density Distribution', fontsize=16, fontweight='bold')
	ax.set_xlabel('Longitude', fontsize=12)
	ax.set_ylabel('Latitude', fontsize=12)
	ax.legend()
	ax.grid(True, alpha=0.3)

	plt.tight_layout()
	plt.savefig(output_path, dpi=300, bbox_inches='tight')
	print(f"✅ Saved to: {output_path}")
	plt.close()


def main():
	print("\n" + "=" * 60)
	print("📊 DENSITY ANALYSIS")
	print("=" * 60)

	df = load_cameras()
	lon_mesh, lat_mesh, density = calculate_density(df)
	visualize_density(df, lon_mesh, lat_mesh, density, "maps/camera_density.png")

	print("\n✅ DENSITY ANALYSIS COMPLETE!")


if __name__ == "__main__":
	main()
