import streamlit as st
import pandas as pd
import json
import matplotlib as plt
import plotly.express as px
import plotly.graph_objects as go



# -- Set page config
apptitle = 'A&R Quickview'

st.set_page_config(page_title= apptitle, page_icon=":chart:")

#####################################################################################################################
### LOADING FILES

@st.cache_data
def load_data():
    LLM_Output = pd.read_csv('Data/LLM_Output_fewshot_GPTSentiment.csv')
    EM_DM = pd.read_csv('Data/EM_DM_wGICS.csv')
    return LLM_Output, EM_DM

# LOAD GeoJSON FILE
with open("Data/world_countries_geojson_simple.json") as response:
    geo = json.load(response)

LLM_Output, EM_DM = load_data()

LLM_aggregate = LLM_Output[(LLM_Output['A&R Company'] == True) & (LLM_Output['EU_TAXO_DNSH_OVERALL'] == 'Yes') & (LLM_Output['A11_fewshot_GPTsentiment'] == 'Negative')].pivot_table(values = "ISSUER_ISIN", index = ["GICS_SUBINDUSTRY", "GICS_SECTOR", "ISSUER_CNTRY_DOMICILE", ], aggfunc = "count").reset_index()

#####################################################################################################################

######################################################################################################

### Add title and header
st.title('Adaptation and Resilient Q&A Initial Results')

st.markdown("""
 * Use the menu at left to select data and set plot parameters
 * Your plots will appear below
""")

with st.expander("See A&R Questions"):

    Questions = """
    1. Does this company contribute to increasing the ability of clients/customers to understand and manage climate-related risks and disasters proactively?
    2. Does this company provide products/services to assist clients/customers prepare for and prevent physical climate risks?
    3. Does this company enhance the ability of clients/customers to respond effectively to physical climate risks and disasters during adverse conditions?
    4. Does this company's products or services support clients/customers in coping and adjusting to adverse climate conditions in real-time?
    5. Does this company contribute to the recovery process from adverse physical climate impacts?
    6. Does this company provide strategies or solutions to help alleviate the adverse impacts of climate events and facilitate a 'build-forward better' approach?
    7. Does this company's product/service contribute to adaptation or resilience against chronic climate-related risks, such as extreme heat, extreme cold, wind gusts, heavy rain, and heavy snowfall?
    8. Does this company's product/service contribute to adaptation or resilience against acute climate-related risks, such as tropical cyclones, coastal flooding, fluvial flooding, river low flow, and wildfires?
    9. Is this company actively involved in developing products or solutions for climate-resilient infrastructure, including challenges related to water management, coastal issues, and urban planning?
    10. Is the primary focus of this company's products/services centered on adjusting to both current and expected effects of climate change?
    11. Does the product/services of this company primarily work on reducing greenhouse gas emissions or preventing their release into the atmosphere?
    """
    st.markdown(Questions)

#####################################################################################################################

#####################################################################################################################

### SELECT DATA
st.sidebar.markdown("## Select GICS Sector and Market")

select_market = st.sidebar.selectbox('What market do you want to analyze?',
                                    ['Both EM and DM', 'EM', 'DM'])

select_gics = st.sidebar.selectbox("Select GICS Sectors",
                                    ['All GICS Sectors', 'Communication Services', 'Consumer Discretionary', 'Industrials',
                                    'Energy', 'Real Estate', 'Information Technology', 'Materials',
                                    'Consumer Staples', 'Utilities', 'Financials', 'Health Care'])

select_company_size = st.sidebar.selectbox('Select Size of Companies',
                                        ['All Sizes', 'Large Cap', 'Mid Cap', 'Small Cap'])

## Geographic Market Selection
if select_market == 'Both EM and DM':
    region = EM_DM
else:
    region = EM_DM[EM_DM['Classification']==select_market]

## GICS Subindustry Selection
if select_company_size == 'All Sizes':
    LLM_Output = LLM_Output
elif select_company_size == 'Large Cap':
    LLM_Output = LLM_Output[LLM_Output['LARGE CAP FLAG'] == 1]
    LLM_aggregate = LLM_Output[(LLM_Output['A&R Company'] == True) & (LLM_Output['EU_TAXO_DNSH_OVERALL'] == 'Yes') & (LLM_Output['A11_fewshot_GPTsentiment'] == 'Negative')].pivot_table(values = "ISSUER_ISIN", index = ["GICS_SUBINDUSTRY", "GICS_SECTOR", "ISSUER_CNTRY_DOMICILE", ], aggfunc = "count").reset_index()
elif select_company_size == 'Mid Cap':
    LLM_Output = LLM_Output[LLM_Output['MID CAP FLAG'] == 1]
    LLM_aggregate = LLM_Output[(LLM_Output['A&R Company'] == True) & (LLM_Output['EU_TAXO_DNSH_OVERALL'] == 'Yes') & (LLM_Output['A11_fewshot_GPTsentiment'] == 'Negative')].pivot_table(values = "ISSUER_ISIN", index = ["GICS_SUBINDUSTRY", "GICS_SECTOR", "ISSUER_CNTRY_DOMICILE", ], aggfunc = "count").reset_index()
elif select_company_size == 'Small Cap':
    LLM_Output = LLM_Output[LLM_Output['SMALL CAP FLAG'] == 1]
    LLM_aggregate = LLM_Output[(LLM_Output['A&R Company'] == True) & (LLM_Output['EU_TAXO_DNSH_OVERALL'] == 'Yes') & (LLM_Output['A11_fewshot_GPTsentiment'] == 'Negative')].pivot_table(values = "ISSUER_ISIN", index = ["GICS_SUBINDUSTRY", "GICS_SECTOR", "ISSUER_CNTRY_DOMICILE", ], aggfunc = "count").reset_index()

## GICS Industry Selection
if select_gics == 'All GICS Sectors':
    region = region
    LLM_aggregate = LLM_aggregate
else:
    region = region[region['GICS_SECTOR']==select_gics]
    LLM_aggregate = LLM_aggregate[LLM_aggregate['GICS_SECTOR']==select_gics]


#####################################################################################################################

### SUMMARY CHART (PART 2 VISUAL 4)

# Histogram of Summary Results
sector_colors = ['#ffffff', '#697ab7', '#00c4b3', '#ffc629', '#00945d', '#76777a', '#c8c8c8', '#cad1ea', '#f18a00', '#e54360', '#5787da']

# Create a figure and add a bar trace with specific colors
fig = go.Figure()
fig.add_trace(go.Bar(
    name='GICS Sectors',
    x=['Industrials', 'Materials', 'Utilities', 'Consumer Discretionary', 'Information Technology', 'Energy', 'Financial', 'Real Estate', 'Consumer Staples', 'Health Care', 'Communication Services'],
    y=[394, 166, 127, 69, 62, 61, 46, 39, 39, 10, 8],
    marker_color=sector_colors,  # Assigning the colors
    error_y=dict(type='data', array=[103, 24, 74, 19, 21, 22, 13, 10, 4, 6, 1])
))

# Update layout to add a title
fig.update_layout(title="Distribution of A&R Companies by GICS Sector",
                  xaxis_title="GICS Sectors",
                  yaxis_title="# of A&R Companies",
                  margin = dict(t=60, l=1, r=1, b=10),
                  font=dict(family="Arial",size=25))

# Show the figure
st.plotly_chart(fig, use_container_width=True)

#####################################################################################################################

### HEAT MAP  (PART 2 VISUAL 5)
dm_map = go.Figure(
        go.Choroplethmapbox(geojson=geo,
                            locations= region.ISO_Alpha_3,
                            featureidkey = "properties.iso_a3",
                            z = region.AR_Company_Count,
                            hoverinfo='z+location',
                            colorscale="bluyl",
                            zauto=True))

dm_map.update_layout(title="Heatmap of A&R Companies",
                    mapbox_style="carto-positron",
                    mapbox_zoom=.2,
                    width=900,
                    height=600)

st.plotly_chart(dm_map, use_container_width=True)

######################################################################################################
# A&R Companies in Each Countries By GICS Sector

AR_treemamp = px.treemap(LLM_aggregate, path=[px.Constant('A&R Companies'), 'GICS_SECTOR', 'GICS_SUBINDUSTRY', 'ISSUER_CNTRY_DOMICILE'], values='ISSUER_ISIN',color='GICS_SECTOR',
                        color_discrete_sequence=['#0626a9'],
                        color_discrete_map={'Energy':'#76777a',
                                            'Materials':'#697ab7',
                                            'Industrials':'#ffffff',
                                            'Consumer Discretionary':'#ffc629',
                                            'Consumer Staples':'#f18a00',
                                            'Health Care':'#e54360',
                                            'Financials':'#c8c8c8',
                                            'Information Technology':'#00945d',
                                            'Communication Services':'#5787da',
                                            'Utilities':'#00c4b3',
                                            'Real Estate':'#cad1ea',
                                            'Covered Bonds': '#6C4675'})
AR_treemamp.update_traces(textinfo='label+percent parent+value', textfont=dict(family="Arial", size=20),
                        marker=dict(line=dict(color='#000000', width=.5)))

AR_treemamp.update_layout(margin = dict(t=1, l=1, r=1, b=1),
                          uniformtext=dict(minsize=20))

st.plotly_chart(AR_treemamp, use_container_width=True)

######################################################################################################
#### Pie Chart of A&R Companies Per Country

AR_Piechart = px.pie(region, 
                     values='AR_Company_Count', 
                     names='ISO_Alpha_3', 
                     title='Distribution of A&R Companies per Country', 
                     width=1000, height= 700)
AR_Piechart.update_traces(textposition='inside', textinfo='percent+label+value')

AR_Piechart.update_layout(uniformtext_minsize=15, uniformtext_mode='hide', font=dict(family="Arial", size=15), margin = dict(t=45, l=1, r=10, b=5))

st.plotly_chart(AR_Piechart, use_container_width=True)

######################################################################################################
#### Sunburst Chart with GICS Sector and GICS Subindustry

AR_Sunburst = px.sunburst(LLM_aggregate,
                          path=['GICS_SECTOR', 'GICS_SUBINDUSTRY'],
                          values='ISSUER_ISIN',
                          title='Sunburst Chart of A&R Companies', 
                          color = 'GICS_SECTOR',
                          height = 1000,
                          color_discrete_map={'Energy':'#76777a',
                                 'Materials':'#697ab7',
                                 'Industrials':'#ffffff',
                                 'Consumer Discretionary':'#ffc629',
                                 'Consumer Staples':'#f18a00',
                                 'Health Care':'#e54360',
                                 'Financials':'#c8c8c8',
                                 'Information Technology':'#00945d',
                                 'Communication Services':'#5787da',
                                 'Utilities':'#00c4b3',
                                 'Real Estate':'#cad1ea',
                                 'Covered Bonds': '#6C4675'})
AR_Sunburst.update_traces(textinfo='label')
AR_Sunburst.update_layout(uniformtext_minsize=15, uniformtext_mode='hide', font=dict(family="Arial", size=15), margin = dict(t=45, l=1, r=10, b=5))

st.plotly_chart(AR_Sunburst, use_container_width=True)

                          