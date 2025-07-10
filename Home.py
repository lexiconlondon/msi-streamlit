import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader

# Sample data — replace with your actual values
df = pd.DataFrame({
    'Country': ['United States', 'France', 'Germany'],
    'Lat': [37.0902, 46.2276, 51.1657],
    'Lon': [-95.7129, 2.2137, 10.4515],
    'Credits': [3000000, 2000000, 1000000]
})

# Brazil coordinates (origin)
BRAZIL_LAT = -14.2350
BRAZIL_LON = -51.9253

# Set up taller map with Mercator projection
fig = plt.figure(figsize=(18, 10))

projection = ccrs.Robinson(min_latitude=-60, max_latitude=85)
ax = plt.axes(projection=projection)
ax.set_global()

# Add clean map features
ax.coastlines(linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linewidth=0.4)

# Load country polygons
shapename = 'admin_0_countries'
countries_shp = shpreader.natural_earth(resolution='110m',
                                        category='cultural',
                                        name=shapename)

# List of destination countries to highlight
destination_names = set(df['Country'])

# Draw countries
for country in shpreader.Reader(countries_shp).records():
    name = country.attributes['NAME_LONG']
    geom = country.geometry

    # Shade linked countries
    if name in destination_names:
        ax.add_geometries([geom], ccrs.PlateCarree(),
                          facecolor='#cc0033', edgecolor='black', linewidth=0.2)
    else:
        ax.add_geometries([geom], ccrs.PlateCarree(),
                          facecolor='#eeeeee', edgecolor='gray', linewidth=0.2)

# Draw lines from Brazil to destinations
for _, row in df.iterrows():
    if pd.notna(row['Lat']) and pd.notna(row['Lon']):
        ax.plot([BRAZIL_LON, row['Lon']],
                [BRAZIL_LAT, row['Lat']],
                color='green',
                linewidth=row['Credits'] / 1e6,  # Adjust line width scale
                alpha=0.7,
                transform=ccrs.Geodetic())

# Plot Brazil origin point
ax.plot(BRAZIL_LON, BRAZIL_LAT, marker='o', color='darkgreen', markersize=10, transform=ccrs.PlateCarree())

# Display the map in Streamlit
st.title("Brazilian NBS Credit Flows")
st.pyplot(fig)
