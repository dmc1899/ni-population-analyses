# ref - https://github.com/jkanner/streamlit-dataview/blob/master/app.py
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

st.set_page_config(layout='wide')

# Title the app
st.title('Injection Distribution (2020 - Present)')
#st.caption('Use the sidebar on the left to configure parameters for your analyses.')


st.markdown('''
## Cumulative Injections Administered
''')


@st.cache_data
def load_data():
    dataframe = pd.read_pickle('data/injections/CumulativeInjections.pkl')
    return dataframe


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


#st.info('Plotting cumulative injection distribution')

injections_cumulative_df = load_data()
csv = convert_df(injections_cumulative_df)

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


fig_cumulative_injections = make_subplots(specs=[[{"secondary_y": False}]])

injections = ['Primary Dose 1', 'Primary Dose 2', 'Primary Dose 3', '1st Booster Dose', 'Spring 2022 Booster']

for injection in injections:
    fig_cumulative_injections.add_trace(
        go.Scatter(x = injections_cumulative_df['Injection Date'],
                   y=injections_cumulative_df[injection],
                   name=f'{injection} Injection'),
        secondary_y=False
    )

layout = go.Layout(
    height=800,
    margin=dict(l=50, r=50, b=100, t=100, pad=4),
    title=dict(text="Cumulative Injections Administered"),
    xaxis=dict(title_text="Date", type='category', tickmode = 'linear', tick0 = 1, dtick = 24),
    yaxis=dict(title_text="Injections"),
)
fig_cumulative_injections = go.Figure(data=fig_cumulative_injections.data, layout=layout)
st.plotly_chart(fig_cumulative_injections, use_container_width=True, theme=None)


if show_raw_data_selected:
    st.subheader('Raw data')
    st.write(injections_cumulative_df)

st.caption('''
Injection distribution data sourced from [HSC Vaccination Dashboard](https://covid-19.hscni.net/ni-covid-19-vaccinations-dashboard/).
''')
