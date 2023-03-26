# ref - https://github.com/jkanner/streamlit-dataview/blob/master/app.py
import math

import pandas as pd
import plotly.graph_objects as go
import streamlit
import streamlit as st
from plotly.subplots import make_subplots

st.set_page_config(layout='wide')

# Title the app
st.title('Monthly Birth Statistics (2006 - Present)')
st.caption('👈 Use the sidebar to configure parameters for your analysis.')


st.markdown('''
## Absolute lowest registered monthly births
''')


@st.cache_data
def load_data():
    dataframe = pd.read_pickle('data/births/AllBirthsUpToDec2022.pkl')
    return dataframe



@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


analysis_end_month_for_births = 12
all_monthly_births_df = load_data()
csv = convert_df(all_monthly_births_df)

range_2006_to_2022 = ['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022']

no_index_df = all_monthly_births_df.reset_index(drop=True)
#no_index_df[0:analysis_end_month_for_births].style.highlight_min(range_2006_to_2022,color='red', axis=None)
st.dataframe(no_index_df[0:analysis_end_month_for_births].style.highlight_min(range_2006_to_2022,color='red', axis=None), use_container_width=True,height=458)


st.markdown('''
## Absolute highest registered monthly births
''')

st.dataframe(all_monthly_births_df[0:analysis_end_month_for_births].style.highlight_max(range_2006_to_2022, color='green', axis=None), use_container_width=True,height=458)

st.markdown('''
## Heatmap of highest and lowest monthly births for all months
''')

st.dataframe(all_monthly_births_df[0:analysis_end_month_for_births].style.background_gradient(axis=None), use_container_width=True,height=458)

st.markdown('''
## Heatmap of highest and lowest monthly births per month 
''')

with st.sidebar:

    st.markdown("### Access underlying data")
    show_raw_data_selected = st.checkbox('Show raw data', value = False, help='Display raw data below the plot.')

    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name='all_weekly_deaths.csv',
        mime='text/csv',
        help='Download the raw data as a CSV file.'
    )

st.dataframe(all_monthly_births_df[0:analysis_end_month_for_births].style.background_gradient(axis=1), use_container_width=True,height=458)

import plotly.express as px

fig = px.bar(all_monthly_births_df,
             x='Month_of_Birth',
             y=range_2006_to_2022,
             title='NI Total Monthly Births 2006-2022',
             barmode='group',
             #             facet_col='Month_of_Birth',
             height=600)

# Set x-axis title
fig.update_xaxes(title_text="Month of Birth")

# Set y-axis titles
fig.update_yaxes(title_text="Number of Births", secondary_y=False)

# Set Legend Name
fig.update_layout(legend_title_text='Year')

st.plotly_chart(fig, use_container_width=True, theme=None)

if show_raw_data_selected:
    st.subheader('Raw data')
    st.write(all_monthly_births_df)

st.caption('Monthly birth statistics dataset sourced from [NISRA Monthly Births Registered in Northern Ireland]'
           '(https://www.nisra.gov.uk/publications/monthly-births).')

