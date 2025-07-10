import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Sample data (replace with your real values)
df = pd.DataFrame({
    'Country': ['United States', 'France', 'Germany'],
    'Lat': [37.0902, 46.2276, 51.1657],
    'Lon': [-95.7129, 2.2137, 10.4515],
    'Credits': [3000000, 2000000, 1000000]
})

# Brazil coordinates
BRAZIL_LAT = -14.2350
BRAZIL_LON = -51.9253

# Setup map
fig = plt.figure(figsize=(15, 10))
ax = plt.axes(projection=ccrs.PlateCarree())

# Add map features
ax.set_global()
ax.stock_img()  # Adds a visible background
ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.add_feature(cfeature.OCEAN, facecolor='aliceblue')

# Plot lines
for _, row in df.iterrows():
    ax.plot([BRAZIL_LON, row['Lon']],
            [BRAZIL_LAT, row['Lat']],
            color='green',
            linewidth=row['Credits'] / 1e6,  # Scale line width
            alpha=0.7,
            transform=ccrs.Geodetic())

# Plot Brazil point
ax.plot(BRAZIL_LON, BRAZIL_LAT, marker='o', color='darkgreen', markersize=8, transform=ccrs.PlateCarree())

# Add destination labels
for _, row in df.iterrows():
    ax.text(row['Lon'], row['Lat'], row['Country'], fontsize=9, transform=ccrs.PlateCarree())

plt.title("Global Destinations of Brazilian NBS Credits", fontsize=15)
plt.show()
