import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Sample data
df = pd.DataFrame({
    'Country': ['United States', 'France', 'Germany'],
    'Lat': [37.0902, 46.2276, 51.1657],
    'Lon': [-95.7129, 2.2137, 10.4515],
    'Credits': [3000000, 2000000, 1000000]
})

# Brazil coordinates
BRAZIL_LAT = -14.2350
BRAZIL_LON = -51.9253

# Streamlit header
st.title("Brazilian NBS Credit Retirements (Flow Map)")

# Plot
fig = plt.figure(figsize=(12, 8))
ax = plt.axes(projection=ccrs.PlateCarree())

ax.set_global()
ax.set_extent([-180, 180, -60, 90], crs=ccrs.PlateCarree())  # Removes Antarctica

ax.coastlines(linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linewidth=0.4)
ax.add_feature(cfeature.LAND, facecolor='#eeeeee')  # Light gray land

# Plot lines from Brazil to destinations
for _, row in df.iterrows():
    ax.plot([BRAZIL_LON, row['Lon']],
            [BRAZIL_LAT, row['Lat']],
            color='green',
            linewidth=row['Credits'] / 1e6,
            alpha=0.7,
            transform=ccrs.Geodetic())
    ax.text(row['Lon'], row['Lat'], row['Country'], fontsize=8, transform=ccrs.PlateCarree())

# Plot Brazil point
ax.plot(BRAZIL_LON, BRAZIL_LAT, marker='o', color='darkgreen', markersize=10, transform=ccrs.PlateCarree())

# Show in Streamlit
st.pyplot(fig)
