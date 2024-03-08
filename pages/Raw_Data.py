import streamlit as st
import pandas as pd

# -- Set page config
apptitle = 'A&R Quickview'
st.set_page_config(page_title=apptitle, page_icon=":chart:")

#####################################################################################################################
### LOADING FILES

@st.cache_data
def load_data():
    LLM_Output = pd.read_csv('Data/LLM_Output_fewshot_GPTSentiment.csv')
    EM_DM_df = pd.read_csv('Data/EM_DM_wGICS.csv')
    return LLM_Output, EM_DM_df

LLM_Output, EM_DM_df = load_data()

#st.dataframe(LLM_Output, use_container_width=True)
st.dataframe(EM_DM_df, use_container_width=True)