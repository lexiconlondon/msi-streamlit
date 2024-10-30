import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define the data
data = {
    "Country": ["Canada", "Russia", "France", "UK", "India", "Germany", "Japan", "China", "US"],
    "Very Unlikely": [5, 64, 3, 5, 52, 4, 3, 46, 26],
    "Somewhat Unlikely": [19, 24, 19, 30, 29, 18, 19, 23, 35],
    "Somewhat Likely": [50, 6, 55, 47, 13, 42, 47, 21, 30],
    "Very Likely": [23, 2, 20, 15, 3, 34, 29, 8, 6]
}

# Create DataFrame
likelihood_df = pd.DataFrame(data)
likelihood_df.set_index("Country", inplace=True)

# Define color palette for each country (in reverse order)
color_discrete_sequence = [
    '#0f477b', '#7188ef', '#aebaf0', '#00c4b3', '#118a5e', '#C12D8F', '#000000', '#f08900', '#ffc62d'
]

# Set y-axis positions for plotting with "US" at the top
y_positions = [i * 2.5 for i in range(len(likelihood_df.index))][::-1]  # Reverse order for top-down

# Create the bubble chart in Matplotlib
fig, ax = plt.subplots(figsize=(14, 10))

for i, (country, y_pos) in enumerate(zip(likelihood_df.index, y_positions)):
    for j, category in enumerate(likelihood_df.columns):
        ax.scatter(j, y_pos,
                   s=likelihood_df.loc[country, category] * 10,  # Scale for bubble size
                   color=color_discrete_sequence[i % len(color_discrete_sequence)],  # Reversed color order
                   alpha=0.6,
                   edgecolor='black',
                   marker='o')  # Circular marker

        # Add percentage text next to each bubble
        percentage_text = f"{likelihood_df.loc[country, category]}%"
        ax.text(j + 0.15, y_pos, percentage_text, ha='left', va='center', color='black', fontsize=10)

# Customize plot appearance
ax.set_yticks(y_positions)
ax.set_yticklabels(likelihood_df.index)
ax.set_xticks(range(len(likelihood_df.columns)))
ax.set_xticklabels(likelihood_df.columns, rotation=45, ha='center')
ax.spines[:].set_visible(False)  # Hide all spines
ax.grid(False)  # Turn off grid
ax.set_xlabel("")
ax.set_ylabel("")

# Display the chart in Streamlit
st.pyplot(fig)

                          
