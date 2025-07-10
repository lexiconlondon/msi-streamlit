import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader

# Sample data — replace with your own
df = pd.DataFrame({
    'Country': ['United States', 'France', 'Germany'],
    'Lat': [37.0902, 46.2276, 51.1657],
    'Lon': [-95.7129, 2.2137, 10.4515],
    'Credits': [3000000, 2000000, 1000000]
})

# Brazil origin
BRAZIL_LAT = -14.2350
BRAZIL_LON = -51.9253

# Set up map
fig = plt.figure(figsize=(24, 16))
ax = plt.axes(projection=ccrs.Mercator())

ax.set_global()
ax.set_extent([-180, 180, -60, 90], crs=ccrs.PlateCarree())
ax.coastlines(linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linewidth=0.4)

# Load Natural Earth countries shapefile
shapename = 'admin_0_countries'
countries_shp = shpreader.natural_earth(resolution='110m',
                                        category='cultural',
                                        name=shapename)

# Get set of destination country names
destination_names = set(df['Country'])

# Plot countries
for country in shpreader.Reader(countries_shp).records():
    name = country.attributes['NAME_LONG']
    geom = country.geometry

    # If destination country, fill with #cc0033
    if name in destination_names:
        ax.add_geometries([geom], ccrs.PlateCarree(),
                          facecolor='#cc0033', edgecolor='black', linewidth=0.2)
    else:
        ax.add_geometries([geom], ccrs.PlateCarree(),
                          facecolor='#eeeeee', edgecolor='gray', linewidth=0.2)

# Plot lines from Brazil to destinations
for _, row in df.iterrows():
    ax.plot([BRAZIL_LON, row['Lon']],
            [BRAZIL_LAT, row['Lat']],
            color='green',
            linewidth=row['Credits'] / 1e6,
            alpha=0.7,
            transform=ccrs.Geodetic())

# Plot Brazil origin point
ax.plot(BRAZIL_LON, BRAZIL_LAT, marker='o', color='darkgreen', markersize=10, transform=ccrs.PlateCarree())

# Display in Streamlit
st.pyplot(fig)
