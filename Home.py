import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry
import io

# Sample data
data = pd.DataFrame({
    'country_code': ['BWA','MNG','POL','CYP','GNB','GMB','ZAF','BHS','IND','ATG','GUY','NER','GUM','','TLS','BRB','MDV','IDN','ERI','TCD','BGD','VUT','','SSD','KAZ','PHL','MAR','CUB','MUS','HKG','DMA','DJI','BFA','SOM','','NCL','','MTQ','CZE','IRQ','MYS','SEN','PNG','DOM','SYR','HTI','ABW','SAU','','SRB','YEM','LBY','CHN','KWT','MKD','','BEN','CPV','','ISR','','TTO','THA','TWN','GIB','TKM','MRT','BHR','DZA','QAT','SGP','IRN','OMN','TUN','BIH','UZB','AUS','WSM','JPN','','AZE','BGR','EGY','MLT','','LKA','MLI','MDG','ARG','DEU','VNM','GNQ','COG','MNE','MAC','USA','ITA','','EST','','MEX','MDA','','KOR','ARE','RUS','TGO','NGA','GRC','PYF','ROU','SUR','IRL','NLD','MMR','GHA','','TZA','GTM','BLR','GAB','LBN','PRK','BOL','LUX','SVK','PAK','HND','RWA','','SVN','HUN','BLZ','KHM','FJI','AUT','CHL','SLV','GIN','ARM','GEO','ZWE','BDI','LVA','HRV','ECU','BEL','AFG','GBR','LAO','NIC','LTU','KGZ','','CMR','SDN','AGO','BTN','','','PAN','PER','DNK','VEN','CAN','','NZL','ESP','ZMB','GRL','','KEN','TJK','SWZ','URY','PRT','MOZ','COL','FIN','','ALB','','CHE','SLE','','UGA','','BRA','MWI','','CRI','FRA','','NAM','','','NOR','ISL','','PRY','','CAF','ETH','NPL','SWE','ALA'],
'value':[811.77,751.5,730.76,707.91,700,700,697.54,695.82,689.04,674.38,671.96,657.87,654.78,649.6,649.37,648.79,648.38,643.93,640.14,635.53,630.33,621.23,613.38,607.67,605.21,605.13,601.9,601.29,600.59,594.1,585.73,585.64,582.17,580.58,577.09,575.33,571.74,569.66,566.47,565.11,561.46,558.57,556.82,556.8,555.24,555.11,552.73,548.76,537.54,532.54,523.78,523.38,523.32,521.61,512.53,512.41,504.57,503.68,499.56,498.54,495.36,490.17,490.12,490.08,490,490,489.66,488.1,487.68,487.09,484.47,483.26,479.3,478.01,476.27,475.97,471.58,471.24,467.96,465.67,461.99,451.03,447.56,443.33,442.81,435.63,429.36,418.32,416.64,414.82,411.06,410.62,409.13,404.38,401.67,400.67,400.51,400.13,397.18,393.12,389.14,384.28,384.08,381.24,381.06,380.18,378.99,369.63,368.19,367.48,361.78,356.31,353.4,339.9,339.48,337.39,337.22,336.88,329.22,327.24,325.09,314.51,314.39,313.3,312.84,311.52,300.41,296.2,293.99,293.49,287.92,278.32,275.96,273.68,267.38,254.63,247.03,247.01,244.61,243.91,239.53,239,238.77,228.5,219.62,209.7,207.74,206.18,200.32,196.32,184,182.11,178.39,170.98,169.5,168.08,166.17,163.4,151.84,149.1,146.31,141.99,132.81,129.48,127.53,124.66,122.21,117.7,110.03,109.88,105.57,105.09,103.42,103.11,99.72,95.09,94.63,90.03,89.7,83.52,78.96,75.33,69.56,69.09,66.56,65.96,63.07,62.03,56.22,52.08,46.09,42.97,40.61,39.41,36.87,35.38,28.99,28.17,26.77,25.24,24.44,24,24,24,22.14,18.09]
})

# Remove empty country codes
data = data[data['country_code'] != '']

# Get full list of ISO-3 country codes from pycountry
all_iso3 = [country.alpha_3 for country in pycountry.countries]

# Build complete country list with NaN where no value is available
full_data = pd.DataFrame({'country_code': all_iso3})
merged = full_data.merge(data, on='country_code', how='left')

# Define value range
min_val = data['value'].min()
max_val = data['value'].max()

# Define 4 custom color stops
custom_scale = [
    [0.0, "#aebaf0"],
    [0.33, "#7188ef"],
    [0.66, "#a81476"],
    [1.0,"#000"]
]

# Create the choropleth
fig = px.choropleth(
    data_frame=merged,
    locations='country_code',
    color='value',
    hover_name='country_code',
    color_continuous_scale=custom_scale,
    range_color=(min_val, max_val),
    projection='natural earth',
    title='World Heat Map with Custom Color Stops'
)

# Hide country borders and Antarctica
fig.update_geos(
    showcountries=False,
    showcoastlines=False,
    lataxis_range=[-60, 90],  # Hide Antarctica
    showframe=False,
    showland=True,
    landcolor="#ccc"  # Color for countries with no data
)

# Layout cleanup
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    coloraxis_colorbar=dict(title='Value')
)

fig.update_traces(
    marker_line_width=0,           # Remove visible borders
    marker_line_color='rgba(0,0,0,0)'  # Force transparent borders
)

# Show the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Export to SVG and provide download button
buffer = io.BytesIO()
fig.write_image(buffer, format='svg')
st.download_button(
    label="⬇️ Download as SVG",
    data=buffer.getvalue(),
    file_name="world_heatmap.svg",
    mime="image/svg+xml"
)
