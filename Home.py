import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# ------------------------------
# Define the data
data = {
    "France": 3494224,
    "United States of America": 1707222,
    "Brazil": 1375590,
    "Germany": 960529,
    "United Kingdom": 797711,
    "Japan": 396158,
    "Italy": 358046,
    "Australia": 282558,
    "Netherlands": 258677,
    "Colombia": 246936,
    "Canada": 244398,
    "Spain": 158764,
    "Malta": 96583,
    "Switzerland": 69286,
    "Belgium": 62061,
    "Sweden": 51161,
    "Finland": 25859,
    "Monaco": 22355,
    "Luxembourg": 20199,
    "Taiwan, Province of China": 18536,
    "Portugal": 18084,
    "Norway": 17463,
    "South Korea": 14706,
    "China": 10163,
    "Ecuador": 9998,
    "Chile": 7045,
    "Turkey": 6228,
    "United Arab Emirates": 4637,
    "Argentina": 3811,
    "Denmark": 2965,
    "Bangladesh": 2911,
    "Romania": 2574,
    "Jersey": 1700,
    "New Zealand": 1308,
    "Poland": 1040,
    "Malaysia": 1000,
    "Russian Federation": 700,
    "Hungary": 401,
    "Thailand": 207,
    "Cyprus": 126,
    "Austria": 100,
    "Bermuda": 73,
    "India": 16
}

# Convert to DataFrame
df = pd.DataFrame(data.items(), columns=["Country", "Credits"])

# Geocode countries
geolocator = Nominatim(user_agent="geoapi")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

df["location"] = df["Country"].apply(geocode)
df = df.dropna(subset=["location"])
df["Lat"] = df["location"].apply(lambda loc: loc.latitude)
df["Lon"] = df["location"].apply(lambda loc: loc.longitude)

# Brazil origin
BRAZIL_LAT = -14.2350
BRAZIL_LON = -51.9253

# ------------------------------
# Setup map with Robinson projection
fig = plt.figure(figsize=(18, 10))
projection = ccrs.Robinson()
ax = plt.axes(projection=projection)
ax.set_global()

# Remove outer border
for spine in ax.spines.values():
    spine.set_visible(False)

# Add map features
ax.coastlines(resolution='110m', linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linewidth=0.4)

# Load Natural Earth countries
shapename = 'admin_0_countries'
countries_shp = shpreader.natural_earth(resolution='110m', category='cultural', name=shapename)
destination_names = set(df["Country"])

# Draw countries
for country in shpreader.Reader(countries_shp).records():
    name = country.attributes['NAME_LONG']
    geom = country.geometry

    if name == 'Antarctica' or geom is None or geom.is_empty:
        continue

    try:
        color = '#cc0033' if name in destination_names else '#eeeeee'
        ax.add_geometries([geom], ccrs.PlateCarree(), facecolor=color, edgecolor='gray', linewidth=0.2)
    except:
        continue

# Draw lines
for _, row in df.iterrows():
    ax.plot([BRAZIL_LON, row["Lon"]],
            [BRAZIL_LAT, row["Lat"]],
            color='green',
            linewidth=row["Credits"] / 1_000_000,
            alpha=0.7,
            transform=ccrs.Geodetic())

# Brazil marker
ax.plot(BRAZIL_LON, BRAZIL_LAT,
        marker='o', color='darkgreen', markersize=10,
        transform=ccrs.PlateCarree())

# ------------------------------
# Streamlit output
st.title("Global Retirements of Brazilian NBS Credits")
st.pyplot(fig)
