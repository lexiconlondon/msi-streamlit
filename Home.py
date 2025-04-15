import pandas as pd
import plotly.express as px

# Sample data
data = pd.DataFrame({
    'country_code': ['USA', 'CAN', 'BRA', 'FRA', 'RUS', 'CHN', 'IND', 'AUS', 'ZAF', 'EGY'],
    'value': [300, 150, 200, 180, 220, 400, 350, 170, 130, 120]
})

# Plotly choropleth with customizations
fig = px.choropleth(
    data_frame=data,
    locations='country_code',
    color='value',
    hover_name='country_code',
    hover_data={'value': True, 'country_code': False},  # show value, hide repeated code
    color_continuous_scale='Viridis',  # Try 'Viridis', 'Cividis', 'Plasma', 'Turbo', etc.
    projection='natural earth',
    title='🌍 Global Data Heat Map'
)

# Customize color bar and layout
fig.update_layout(
    margin={"r":0,"t":40,"l":0,"b":0},
    title_font_size=24,
    title_font_family='Arial Black',
    paper_bgcolor='#f4f4f4',
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='natural earth'
    ),
    coloraxis_colorbar=dict(
        title='Value',
        title_side='right',
        tickformat=',.0f',
        lenmode='fraction',
        len=0.75,
        thickness=15
    )
)

fig.show()
                          
