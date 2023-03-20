# ref - https://github.com/jkanner/streamlit-dataview/blob/master/app.py
import math
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import streamlit
import streamlit as st
from plotly.subplots import make_subplots

st.set_page_config(layout='wide')

# Title the app
st.title('Cause of Death (2018 - Present)')
#st.caption('Use the sidebar on the left to configure parameters for your analyses.')

st.markdown('''
Cause of death statistics datasets sourced from [NISRA Register General Quarterly Tables](https://www.nisra.gov.uk/statistics/registrar-general-quarterly-report/registrar-general-quarterly-tables).
''')

st.markdown('''
## Cause of Death as a Percentage over Time
''')


@st.cache_data
def load_data():
    dataframe = pd.read_pickle('data/deaths/DeathsByCauseUpToQ42022.pkl')
    return dataframe



@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


analysis_end_month_for_births = 12
age_breakdown_df = load_data()
csv = convert_df(age_breakdown_df)


age_groups = ['<1', '1-14', '15-34', '35-44', '45-54', '55-64', '65-74', '75-79', '80-84', '85-89', '>90']

for age_group in age_groups:

    df_subset = age_breakdown_df[age_breakdown_df['Age_Group'] == age_group]
    fig = px.bar(df_subset,
                 x='Period',
                 y='Percentage_of_Period_Age_Deaths',
                 title='NI Cause of Death as a Percentage Over Time (2018 - 2022)',
                 barmode='stack',
                 facet_col='Age_Group',
                 facet_col_wrap=1,
                 color='Cause_of_Death',
                 text_auto=True,
                 category_orders={"Period": ['2018-Q1','2018-Q2','2018-Q3','2018-Q4','2019-Q1','2019-Q2', \
                                             '2019-Q3','2019-Q4', '2020-Q1', '2020-Q2', '2020-Q3', '2020-Q4', \
                                             '2021-Q1', '2021-Q2', '2021-Q3', '2021-Q4', '2022-Q1', '2022-Q2', \
                                             '2022-Q3','2022-Q4']},
                 height=600)

    # Set x-axis title
    fig.update_xaxes(title_text="Period", showgrid=True)

    # Set y-axis titles
    fig.update_yaxes(title_text="% of Deaths", secondary_y=False)

    #fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-1.0,
        xanchor="left",
        x=0.01
    ))
    # Set Legend Name
    fig.update_layout(legend_title_text='Cause of Death')

    st.plotly_chart(fig, use_container_width=True, theme=None)
