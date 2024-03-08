import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud

# -- Set page config
apptitle = 'A&R Products and Services'

st.set_page_config(page_title=apptitle, page_icon=":chart:")

#####################################################################################################################
### LOADING FILES

@st.cache_data
def load_data():
    PandS_Category = pd.read_csv('Data/AR_PandS_EU_export.csv')
    return PandS_Category

PandS_Category= load_data()

#####################################################################################################################

### SELECT DATA
st.sidebar.markdown("## Select Market")

select_market = st.sidebar.selectbox('What market do you want to analyze?',
                                    ['Both EM and DM', 'EM', 'DM'])

select_company_size = st.sidebar.selectbox('Select Size of Companies',
                                        ['All Sizes', 'Large Cap', 'Mid Cap', 'Small Cap'])

if select_market == 'Both EM and DM':
    PandS_Category_selected = PandS_Category
else:
    PandS_Category_selected = PandS_Category[PandS_Category['Market_Classification']==select_market]

## GICS Subindustry Selection
if select_company_size == 'All Sizes':
    PandS_Category_selected = PandS_Category_selected
elif select_company_size == 'Large Cap':
    PandS_Category_selected = PandS_Category_selected[PandS_Category_selected['LARGE CAP FLAG'] == 1]
elif select_company_size == 'Mid Cap':
    PandS_Category_selected = PandS_Category_selected[PandS_Category_selected['MID CAP FLAG'] == 1]
elif select_company_size == 'Small Cap':
    PandS_Category_selected = PandS_Category_selected[PandS_Category_selected['SMALL CAP FLAG'] == 1]


######################################################################################################
### Heat Map of UNEP Activities (PART 1 VISUAL 1)

Heat_Map = PandS_Category_selected.pivot_table(index='GICS_SECTOR', columns='UNEP_Technology_Division', values='ISSUER_NAME', aggfunc='count')#.fillna(0)

fig = px.imshow(Heat_Map, aspect="auto",
                labels=dict(x="AR Product & Service Category", y="GICS Sector", color="Count of Product & Services"),
                color_continuous_scale='greens', zmin=0, width=1200, height=600
)
fig.update_xaxes(side="top", tickangle=45).update_yaxes(showgrid=False)
fig.update_layout(plot_bgcolor='#FFFFFF')

# Display the figure in Streamlit
st.plotly_chart(fig)

######################################################################################################
### Sankey Chart for UNEP (PART 1 VISUAL 2)

# Assuming PandS_Category_selected is your DataFrame that includes all the data

st.subheader('Products and services that align with UNEP TNA Taxonomy')

# Create columns for metrics display
UNEP_Companies, UNEP_PandS_num = st.columns(2)

# Selection box for UNEP Sector
select_UNEP = st.selectbox('Drill down into specific UNEP Sector',
                            ["all", "agriculture & livestock", "water", "forestry & land", "marine, fisheries and coastal zones", "health", "climate change forecast and monitoring"])

# Filter the DataFrame based on the selection
if select_UNEP == 'all':
    UNEP_TNA = PandS_Category_selected[PandS_Category_selected['UNEP_Taxonomy_Aligned']== True]
else:
    UNEP_TNA = PandS_Category_selected[(PandS_Category_selected['UNEP_Technology_Division'] == select_UNEP) & (PandS_Category_selected['UNEP_Taxonomy_Aligned']== True)]

# Update metrics based on the filtered DataFrame
UNEP_Companies.metric('Number of companies with services that align with UNEP', value=UNEP_TNA['ISSUER_NAME'].nunique(), delta=f'Out of 825 companies')
UNEP_PandS_num.metric(label="Number of products and services that align with UNEP", value=UNEP_TNA['Products_and_Services'].nunique(), delta=f"Out of 3,926 products and services")

# Define sankey diagram paths and labels based on the selection
if select_UNEP == 'all':
    sankey_path = ['Market_Classification','GICS_SECTOR', 'UNEP_Technology_Division']
    sankey_label = {'Market_Classification': 'Economic Marker', \
                    'GICS_SECTOR' : 'GICS Sector', \
                    'Technology_Division' : 'UNEP Technology Division'}
else:
    sankey_path = ['Market_Classification', 'GICS_SECTOR', 'UNEP_Technology_Division', 'UNEP_CTC_Technology_Section']
    sankey_label = {'Market_Classification': 'Economic Marker', \
                    'GICS_SECTOR' : 'GICS Sector', \
                    'Technology_Division' : 'UNEP Technology Division', \
                    'CTC_Technology_Section' : f'UNEP {select_UNEP} Section'}

# Create the sankey diagram
UNEP_Chart = px.parallel_categories(UNEP_TNA,
                                    dimensions=sankey_path,
                                    width=1200, height=600,
                                    labels=sankey_label)

UNEP_Chart.update_layout(margin=dict(l=50, r=200, t=50, b=50, pad=4))

# Display the chart
st.plotly_chart(UNEP_Chart, use_container_width=False)

######################################################################################################
### Sankey Chart for EU Taxonomy (NOT VALIDATED) (PART 1 VISUAL 2)

# Assuming PandS_Category_selected is your DataFrame that includes all the data

st.subheader('Products and services that could align with the EU Taxonomy, this dataset has not be fully vetted for substanstial contribution')

# Create columns for metrics display
EU_Companies, EU_PandS_num = st.columns(2)

# Selection box for UNEP Sector
select_EU_Sector = st.selectbox('Drill down into specific EU Sector',
                            ["all", "arts, entertainment and recreation", 
                             "construction and real estate",
                             "education", 
                             "energy", 
                             "environmental protection and restoration activities", 
                             "financial and insurance activities", 
                             "forestry",
                             "human health and social work activities", 
                             "information and communication",
                             "manufacturing",
                             "professional, scientific and technical activities", "transport", "water supply, sewerage, waste management and remediation"])

# Filter the DataFrame based on the selection
if select_EU_Sector == 'all':
    EU_Taxonomy = PandS_Category_selected[PandS_Category_selected['EU_Taxonomy_Aligned']== True]
else:
    EU_Taxonomy = PandS_Category_selected[(PandS_Category_selected['EU_Taxonomy_Sector'] == select_EU_Sector) & (PandS_Category_selected['EU_Taxonomy_Aligned']== True)]

# Update metrics based on the filtered DataFrame
EU_Companies.metric('Number of companies with services that align with UNEP', value=EU_Taxonomy['ISSUER_NAME'].nunique(), delta=f'Out of 825 companies')
EU_PandS_num.metric(label="Number of products and services that align with UNEP", value=EU_Taxonomy['Products_and_Services'].nunique(), delta=f"Out of 3,926 products and services")

# Define sankey diagram paths and labels based on the selection
if select_EU_Sector == 'all':
    sankey_path = ['Market_Classification','GICS_SECTOR', 'EU_Taxonomy_Sector']
    sankey_label = {'Market_Classification': 'Market Classification (EM or DM)', \
                    'GICS_SECTOR' : 'GICS Sector', \
                    'EU_Taxonomy_Sector' : 'EU Sector'}
else:
    sankey_path = ['Market_Classification', 'GICS_SECTOR', 'EU_Taxonomy_Sector', 'EU_Taxonomy_Activity']
    sankey_label = {'Market_Classification': 'Market Classification (EM or DM)', \
                    'GICS_SECTOR' : 'GICS Sector', \
                    'EU_Taxonomy_Sector' : 'EU Sector', \
                    'EU_Taxonomy_Activity' : f'EU {select_EU_Sector} Activity'}

# Create the sankey diagram
EU_Chart = px.parallel_categories(EU_Taxonomy,
                                    dimensions=sankey_path,
                                    width=1200, height=600,
                                    labels=sankey_label)

EU_Chart.update_layout(margin=dict(l=50, r=200, t=50, b=50, pad=4))

# Display the chart
st.plotly_chart(EU_Chart, use_container_width=False)


######################################################################################################
### Word Cloud of PandS Categories (PART 1 VISUAL 3)

# Convert float values to strings in the 'Category' column
PandS_Category_selected['Category'] = PandS_Category_selected['Category'].astype(str)

# Create and generate a word cloud image:
cat_wordcloud = WordCloud(max_words=500).generate(' '.join(PandS_Category_selected['Category']))

# Use Plotly Express to display the image
wordcloud_fig = px.imshow(cat_wordcloud)
wordcloud_fig.update_layout(title='Word Cloud of Categories')
wordcloud_fig.update_xaxes(showticklabels=False)  # Hide x-axis ticks
wordcloud_fig.update_yaxes(showticklabels=False)  # Hide y-axis ticks

# Display the Plotly figure in Streamlit
st.plotly_chart(wordcloud_fig, use_container_width=False)


# Function to reset the cache
def reset_cache():
    st.cache_clear()
    st.experimental_rerun()

# Add a button to reset the cache
if st.button('Reset Cache'):
    reset_cache()