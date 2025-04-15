import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🌍 Global Data Heat Map")

# Sample data
data = pd.DataFrame({
    'country_code': ['USA', 'CAN', 'BRA', 'FRA', 'RUS', 'CHN', 'IND', 'AUS', 'ZAF', 'EGY'],
    'value': [300, 150, 200, 180, 220, 400, 350, 170, 130, 120]
})

fig = px.choropleth(
    data_frame=data,
    locations='country_code',
    color='value',
    hover_name='country_code',
    color_continuous_scale='Viridis',
    projection='natural earth',
    title='World Heat Map by Country Code'
)

st.plotly_chart(fig, use_container_width=True)
