import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader

# --- Sample data (replace with your actual data or CSV load) ---
df = pd.DataFrame({
    'Country': ['United States', 'France', 'Germany'],
    'Lat': [37.0902, 46.2276, 51.1657],
    'Lon': [-95.7129, 2.2137, 10.4515],
    'Credits': [3000000, 2000000, 1000000]
})

# Clean the data — remove rows with NaN values
df = df.dropna(subset=['Country', 'Lat', 'Lon', 'Credits'])

# Brazil origin
BRAZIL_LAT = -14.2350
BRAZIL_LON = -51.9253

# --- Set up the map ---
fig = plt.figure(figsize=(24, 16))
projection = ccrs.Mercator(min_latitude=-60, max_latitude=85)
ax = plt.axes(projection=projection)

# Limit map view to exclude Antarctica and extreme poles
ax.set_extent([-180, 180, -60, 85], crs=projection)

# Add map features
ax.coastlines(linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linewidth=0.4)

# Load country shapefile
shapename = 'admin_0_countries'
countries_shp = shpreader.natural_earth(resolution='110m',
                                        category='cultural',
                                        name=shapename)

# Set of destination country names to highlight
destination_names = set(df['Country'])

# Draw countries safely
for country in shpreader.Reader(countries_shp).records():
    name = country.attributes['NAME_LONG']
    geom = country.geometry

    # Skip invalid or unwanted shapes
    if name == 'Antarctica' or geom is None or geom.is_empty:
        continue

    try:
        color = '#cc0033' if name in destination_names else '#eeeeee'
        ax.add_geometries([geom], ccrs.PlateCarree(),
                          facecolor=color, edgecolor='black', linewidth=0.2)
    except Exception as e:
        print(f"Skipping {name} due to geometry error: {e}")

# Draw flow lines from Brazil to destinations
for _, row in df.iterrows():
    try:
        ax.plot([BRAZIL_LON, row['Lon']],
                [BRAZIL_LAT, row['Lat']],
                color='green',
                linewidth=row['Credits'] / 1e6,  # Adjust line thickness
                alpha=0.7,
                transform=ccrs.Geodetic())
    except Exception as e:
        print(f"Skipping line to {row['Country']} due to error: {e}")

# Mark Brazil
ax.plot(BRAZIL_LON, BRAZIL_LAT,
        marker='o', color='darkgreen', markersize=10,
        transform=ccrs.PlateCarree())

# Display in Streamlit
st.title("Brazilian NBS Credit Flows")
st.pyplot(fig)
