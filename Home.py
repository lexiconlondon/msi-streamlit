import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader

# ------------------------------
# Load data from your input
data = [
    ("France", 3494224, 2.552275, 46.696113),
    ("United States of America", 1707222, -97.482602, 39.538479),
    ("Brazil", 1375590, -49.55945, -12.098687),
    ("Germany", 960529, 9.678348, 50.961733),
    ("United Kingdom", 797711, -2.116346, 54.402739),
    ("Japan", 396158, 138.44217, 36.142538),
    ("Italy", 358046, 11.076907, 44.732482),
    ("Australia", 282558, 134.04972, -24.129522),
    ("Netherlands", 258677, 5.61144, 52.422211),
    ("Colombia", 246936, -73.174347, 3.373111),
    ("Canada", 244398, -101.9107, 60.324287),
    ("Spain", 158764, -3.464718, 40.090953),
    ("Malta", 96583, 14.433005, 35.892886),
    ("Switzerland", 69286, 7.463965, 46.719114),
    ("Belgium", 62061, 4.800448, 50.785392),
    ("Sweden", 51161, 19.01705, 65.85918),
    ("Finland", 25859, 27.276449, 63.252361),
    ("Monaco", 22355, 7.398291, 43.739652),
    ("Luxembourg", 20199, 6.07762, 49.733732),
    ("Portugal", 18084, -8.271754, 39.606675),
    ("Norway", 17463, 9.679975, 61.357092),
    ("South Korea", 14706, 128.129504, 36.384924),
    ("China", 10163, 106.337289, 32.498178),
    ("Ecuador", 9998, -78.188375, -1.259076),
    ("Chile", 7045, -72.318871, -38.151771),
    ("Turkey", 6228, 34.508268, 39.345388),
    ("United Arab Emirates", 4637, 54.547256, 23.466285),
    ("Argentina", 3811, -64.173331, -33.501159),
    ("Denmark", 2965, 9.018163, 55.966965),
    ("Bangladesh", 2911, 89.684963, 24.214956),
    ("Romania", 2574, 24.972624, 45.733237),
    ("Jersey", 1700, -2.090146, 49.220808),
    ("New Zealand", 1308, 172.787, -39.759),
    ("Poland", 1040, 19.490468, 51.990316),
    ("Malaysia", 1000, 113.83708, 2.528667),
    ("Hungary", 401, 19.447867, 47.086841),
    ("Thailand", 207, 101.073198, 15.45974),
    ("Cyprus", 126, 33.084182, 34.913329),
    ("Austria", 100, 14.130515, 47.518859),
    ("Bermuda", 73, -64.763573, 32.296592),
    ("India", 16, 79.358105, 22.686852),
]

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Country", "Credits", "Lon", "Lat"])
df = df.dropna(subset=["Lat", "Lon", "Credits"])

# Brazil origin
BRAZIL_LAT = -12.098687
BRAZIL_LON = -49.55945

# ------------------------------
# Set up map
fig = plt.figure(figsize=(18, 10))
projection = ccrs.Robinson()
ax = plt.axes(projection=projection)
ax.set_global()

# Remove outer border
for spine in ax.spines.values():
    spine.set_visible(False)

# Add base map features
ax.coastlines(resolution='110m', linewidth=0)
ax.add_feature(cfeature.BORDERS, linewidth=0.4)

# Load world country shapes
shapename = 'admin_0_countries'
countries_shp = shpreader.natural_earth(resolution='110m', category='cultural', name=shapename)
destination_names = set(df["Country"])

# Draw countries, shade linked ones
for country in shpreader.Reader(countries_shp).records():
    name = country.attributes['NAME_LONG']
    geom = country.geometry
    if name == "Antarctica" or geom is None or geom.is_empty:
        continue
    try:
        color = "#7188ef" if name in destination_names else "#f4f5fd"
        ax.add_geometries([geom], ccrs.PlateCarree(), facecolor=color, edgecolor="gray", linewidth=0.2)
    except:
        continue

# Plot flow lines
for _, row in df.iterrows():
    ax.plot([BRAZIL_LON, row["Lon"]],
            [BRAZIL_LAT, row["Lat"]],
            color='green',
            linewidth=row["Credits"] / 1_000_000,
            alpha=0.7,
            transform=ccrs.Geodetic())

# Plot Brazil point
ax.plot(BRAZIL_LON, BRAZIL_LAT, marker='o', color='darkgreen', markersize=10, transform=ccrs.PlateCarree())

# ------------------------------
# Streamlit output
st.title("Global Retirements of Brazilian NBS Credits")
st.pyplot(fig)
