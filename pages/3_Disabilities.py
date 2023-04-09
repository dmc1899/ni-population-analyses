# ref - https://github.com/jkanner/streamlit-dataview/blob/master/app.py
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

st.set_page_config(layout='wide')

# Title the app
st.title('Personal Independence Payment Claims (2016 - Present)')
#st.caption('Use the sidebar on the left to configure parameters for your analyses.')



st.markdown('''
## New Personal Independence Payment Claims
''')


@st.cache_data
def load_data():
    dataframe = pd.read_pickle('data/disabilities/MonthlyDisabilityRegistrationsNov2022.pkl')
    return dataframe


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


disability_claims_df = load_data()
csv = convert_df(disability_claims_df)

with st.sidebar:

    st.markdown("### Access underlying data")
    show_raw_data_selected = st.checkbox('Show raw data',
                                         value=False,
                                         help='Display raw data below the plot.')

    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name='all_weekly_deaths.csv',
        mime='text/csv',
        help='Download the raw data as a CSV file.'
    )

fig = make_subplots(specs=[[{"secondary_y": False}]])

fig.add_trace(
    go.Scatter(x=disability_claims_df['Year Month'],
               y=disability_claims_df['Total New Claims Registered'],
               name="Total New Claims"),
    secondary_y=False)


fig.add_trace(
    go.Scatter(x=disability_claims_df['Year Month'],
               y=disability_claims_df['Total New Claims 12-month Rolling Average'],
               name="12-month Rolling Average", line=dict(dash='dash'),visible='legendonly'),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=disability_claims_df['Year Month'],
               y=disability_claims_df['Total New Claims 6-month Rolling Average'],
               name="6-month Rolling Average", line=dict(dash='dash'),visible='legendonly'),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=disability_claims_df['Year Month'],
               y=disability_claims_df['Total New Claims 3-month Rolling Average'],
               name="3-month Rolling Average", line=dict(dash='dash'),visible='legendonly'),
    secondary_y=False,
)

fig.update_layout(
    title_text="New Personal Independence Claims by Month (2016-2022)",
    height=650
)

fig.update_xaxes(dict(title_text='Month', type='category', tickmode='linear', tick0=1, dtick=2))

fig.update_yaxes(title_text="Claims", secondary_y=False)

st.plotly_chart(fig, use_container_width=True, theme=None)

if show_raw_data_selected:
    st.subheader('Raw data')
    st.write(disability_claims_df)

st.markdown('---')
st.caption('''
Disability claim statistics datasets sourced from [Department for Communities Personal Independence Payment Statistics](https://www.communities-ni.gov.uk/articles/personal-independence-payment-statistics).
''')
