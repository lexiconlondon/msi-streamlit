import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Load your data
df = pd.DataFrame({
    'Country': ['United States', 'France', 'Germany'],
    'Lat': [37.0902, 46.2276, 51.1657],
    'Lon': [-95.7129, 2.2137, 10.4515],
    'Credits': [3000000, 2000000, 1000000]
})

# Brazil coordinates (origin)
BRAZIL_LAT = -14.2350
BRAZIL_LON = -51.9253

# Plotting
fig = plt.figure(figsize=(15, 10))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_global()
ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.add_feature(cfeature.OCEAN, facecolor='aliceblue')

# Plot flow lines
for _, row in df.iterrows():
    ax.plot([BRAZIL_LON, row['Lon']],
            [BRAZIL_LAT, row['Lat']],
            linewidth=row['Credits'] / 1e6,  # Adjust scale for thickness
            color='green',
            alpha=0.7,
            transform=ccrs.Geodetic())

# Plot Brazil (origin) point
ax.plot(BRAZIL_LON, BRAZIL_LAT, marker='o', color='darkgreen', markersize=10, transform=ccrs.PlateCarree())

# Optionally label destinations
for _, row in df.iterrows():
    ax.text(row['Lon'], row['Lat'], row['Country'], fontsize=9, transform=ccrs.PlateCarree())

plt.title("Global Destinations of Brazilian NBS Credits (2024)", fontsize=15)
plt.show()
