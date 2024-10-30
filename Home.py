oimport streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

config = {
  'toImageButtonOptions': {
    'format': 'svg', # one of png, svg, jpeg, webp
    'filename': 'custom_image',
    'height': 500,
    'width': 900,
    'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
  }
}

# Load the Inter font
font_path = 'Inter-Regular.ttf'  # Update path if different
inter_font = fm.FontProperties(fname=font_path)

# Define the new data based on the provided table
data = {
    "Sector": [
        "Oil and Gas", "Utilities", "Industrials", "Aviation", "Marine Transportation",
        "Land Transportation", "Consumer Goods", "Consumer Staples (Food/Household Goods etc.)", "Real Estate"
    ],
    "Very Unlikely": [70, 37, 59, 56, 48, 48, 29, 0, 34],
    "Somewhat Unlikely": [23, 41, 32, 29, 38, 39, 49, 0, 47],
    "Somewhat Likely": [5, 19, 6, 11, 8, 11, 16, 0, 14],
    "Very Likely": [2, 3, 3, 5, 6, 3, 7, 0, 6]
}

# Create DataFrame
sector_df = pd.DataFrame(data)
sector_df.set_index("Sector", inplace=True)

# Define color palette for each sector
color_discrete_sequence = [
    '#ffc62d', '#f08900', '#000000', '#C12D8F', '#118a5e', '#00c4b3', '#aebaf0', '#7188ef', '#0f477b'
]

# Set y-axis positions for plotting, reversing order to have Oil and Gas at the top
y_positions = [i * 2.5 for i in range(len(sector_df.index))][::-1]  # Reverse order for top-down

# Create the bubble chart
fig, ax = plt.subplots(figsize=(14, 10))

for i, (sector, y_pos) in enumerate(zip(sector_df.index, y_positions)):
    for j, category in enumerate(sector_df.columns):
        ax.scatter(j, y_pos,
                   s=sector_df.loc[sector, category] * 10,  # Scale for bubble size
                   color=color_discrete_sequence[i % len(color_discrete_sequence)],  # Color for each sector
                   alpha=0.6,
                   edgecolor='black',
                   marker='o')  # Circular marker

        # Add percentage text next to each bubble
        percentage_text = f"{sector_df.loc[sector, category]}%"
        ax.text(j + 0.15, y_pos, percentage_text, ha='left', va='center', color='black', fontsize=10)

# Customize plot appearance
ax.set_yticks(y_positions)
ax.set_yticklabels(sector_df.index)
ax.set_xticks(range(len(sector_df.columns)))
ax.set_xticklabels(sector_df.columns, rotation=45, ha='center')
ax.spines[:].set_visible(False)  # Hide all spines
ax.grid(False)  # Turn off grid
ax.set_xlabel("")
ax.set_ylabel("")

# Display the chart in Streamlit

st.plotly_chart(fig,config=config)
                          
