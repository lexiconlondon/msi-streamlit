import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader

# ------------------------------
# Sample data — replace with actual values
df = pd.DataFrame({
    'Country': ['United States', 'France', 'Germany'],
    'Lat': [37.0902, 46.2276, 51.1657],
    'Lon': [-95.7129, 2.2137, 10.4515],
    'Credits': [3000000, 2000000, 1000000]
})

df = df.dropna(subset=['Country', 'Lat', 'Lon', 'Credits'])

BRAZIL_LAT = -14.2350
BRAZIL_LON = -51.9253

# ------------------------------
# Use Robinson projection
fig = plt.figure(figsize=(18, 10))
projection = ccrs.Robinson()
ax = plt.axes(projection=projection)

ax.set_global()

# Remove outer border
for spine in ax.spines.values():
    spine.set_visible(False)

# Add clean map features
# ax.coastlines(resolution='110m', linewidth=0.5)
# ax.add_feature(cfeature.BORDERS, linewidth=0.4)

# ------------------------------
# Load country polygons
shapename = 'admin_0_countries'
countries_shp = shpreader.natural_earth(resolution='110m', category='cultural', name=shapename)
destination_names = set(df['Country'])

for country in shpreader.Reader(countries_shp).records():
    name = country.attributes['NAME_LONG']
    geom = country.geometry

    # Skip Antarctica and empty shapes
    if name == 'Antarctica' or geom is None or geom.is_empty:
        continue

    try:
        color = '#cc0033' if name in destination_names else '#eeeeee'
        ax.add_geometries([geom], ccrs.PlateCarree(),
                          facecolor=color, edgecolor='gray', linewidth=0.2)
    except Exception as e:
        print(f"Skipping {name}: {e}")

# ------------------------------
# Plot flow lines
for _, row in df.iterrows():
    ax.plot([BRAZIL_LON, row['Lon']],
            [BRAZIL_LAT, row['Lat']],
            color='green',
            linewidth=row['Credits'] / 1e6,
            alpha=0.7,
            transform=ccrs.Geodetic())

# Plot Brazil
ax.plot(BRAZIL_LON, BRAZIL_LAT,
        marker='o', color='darkgreen', markersize=10,
        transform=ccrs.PlateCarree())

# ------------------------------
# Show in Streamlit
st.title("Brazilian NBS Credit Flows (Robinson Projection)")
st.pyplot(fig)
