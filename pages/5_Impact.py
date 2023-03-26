# ref - https://github.com/jkanner/streamlit-dataview/blob/master/app.py
# another ref - https://medium.com/codex/plotly-hands-on-how-to-create-a-multiple-y-axis-combo-chart-with-plotly-go-e2ffd323d3c5
import math

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

st.set_page_config(layout='wide')

st.title('Injections & Deaths Exploratory Analysis')
st.caption('👈 Use the sidebar to configure parameters for your analysis.')


@st.cache_data
def load_data():
    dataframe = pd.read_pickle('data/AllDeathsInjections.pkl')
    return dataframe


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


all_deaths_and_injections_df = load_data()
csv = convert_df(all_deaths_and_injections_df)

label_five_year_average_2015_to_2019 = '2015 - 2019'
label_five_year_average_2016_to_2020 = '2016 - 2020'
label_five_year_average_2017_to_2021 = '2017 - 2021'
label_five_year_average_2016_to_2019_and_2021 = '2016 - 2019 and 2021'

label_total_cumulative = 'All Doses'
label_individual_cumulative = 'Per Dose'

# Default UI settings
mean_value_selected = label_five_year_average_2015_to_2019

with st.sidebar:

    st.markdown("### Configure average and injection plots")

    mean_value_selected = st.radio(
        "Five-year Average:",
        (label_five_year_average_2015_to_2019,
         label_five_year_average_2016_to_2020,
         label_five_year_average_2017_to_2021,
         label_five_year_average_2016_to_2019_and_2021),
        index=0, help='Institutions such as NISRA or ONS use different 5-year averages for comparison. ' \
                      'Select the average to include the plot. The selected average will be plotted as a'
                      'recurring series. For example, for 55 weeks plotted on the x-axis, the average deaths'
                      'for Week 1 - Week 52 and then Week 1 - Week 3 are plotted contiguously.')

    injection_value_selected = st.radio(
        "Cumulative Injection:",
        (label_total_cumulative,
         label_individual_cumulative),
        index=0, help='Plot the cumulative total of all injections or the cumulative total of each injection.')

    show_age_group_indicators_selected = st.checkbox('Show cohort injection offers', value= False,
                                                     help='Mark on the graph where cohorts were first offered an injection.')

    st.markdown("### Access underlying data")
    show_raw_data_selected = st.checkbox('Show raw data', value= False, help='Display raw data below the plot.')

    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name='all_deaths_and_injections_deaths.csv',
        mime='text/csv',
        help='Download the raw data as a CSV file.'
    )

if injection_value_selected == label_total_cumulative:
    show_total_cumulative_injections = True
else:
    show_total_cumulative_injections = False

if mean_value_selected == label_five_year_average_2015_to_2019:
    mean_value_to_plot = '2015_to_2019_Mean'
elif mean_value_selected == label_five_year_average_2016_to_2020:
    mean_value_to_plot = '2016_to_2020_Mean'
elif mean_value_selected == label_five_year_average_2017_to_2021:
    mean_value_to_plot = '2017_to_2021_Mean'
elif mean_value_selected == label_five_year_average_2016_to_2019_and_2021:
    mean_value_to_plot = '2016_to_2019_and_2021_Mean'

st.markdown(f'''
### Injection distribution and Weekly Deaths (March 2020 - Present)
''')

fig3 = make_subplots(specs=[[{"secondary_y":True}]])

fig3.add_trace(
    go.Bar(x=all_deaths_and_injections_df['Registration Year Week'],
           y=all_deaths_and_injections_df['Deaths'],
           name="Weekly Deaths",
           opacity=0.49),
    secondary_y=False, #marker.color='red' || name="Weekly Deaths", marker_color='gray', opacity=0.7)
)

fig3.add_trace(
    go.Scatter(x=all_deaths_and_injections_df['Registration Year Week'],
               y=all_deaths_and_injections_df[mean_value_to_plot],
               name=f'{mean_value_selected} <br>Weekly Death</br> Average <br>(Recurring)</br>', line=dict(color='red',width=2)),
    secondary_y=False,
)

if show_total_cumulative_injections:
    fig3.add_trace(
        go.Scatter(x=all_deaths_and_injections_df['Registration Year Week'],
                   y=all_deaths_and_injections_df['Cumulative Injections'],
                   name="Cumulative Total Injections",line=dict(color='orange',dash='dash') ), #line=dict(color='firebrick', width=2, dash='dash')
        secondary_y=True,
    )
else:
    fig3.add_trace(
        go.Scatter(x=all_deaths_and_injections_df['Registration Year Week'],
                   y=all_deaths_and_injections_df['Primary Dose 1'],
                   name="Cumulative Primary Dose 1",  line=dict(dash='dash')), #color='yellow', width=2,
        secondary_y=True,
    )

    fig3.add_trace(
        go.Scatter(x=all_deaths_and_injections_df['Registration Year Week'],
                   y=all_deaths_and_injections_df['Primary Dose 2'],
                   name="Cumulative Primary Dose 2",  line=dict(dash='dash')), #color='yellow', width=2,
        secondary_y=True,
    )

    fig3.add_trace(
        go.Scatter(x=all_deaths_and_injections_df['Registration Year Week'],
                   y=all_deaths_and_injections_df['1st Booster Dose'],
                   name="Cumulative 1st Booster Dose",  line=dict(dash='dash')), #color='yellow', width=2,
        secondary_y=True,
    )

    fig3.add_trace(
        go.Scatter(x=all_deaths_and_injections_df['Registration Year Week'],
                   y=all_deaths_and_injections_df['Spring 2022 Booster'],
                   name="Cumulative Spring 2022 Booster Dose",  line=dict(dash='dash')), #color='yellow', width=2,  visible='legendonly',
        secondary_y=True,
    )


if show_age_group_indicators_selected:
    fig3.add_vline(x='2021W01', line_width=1, line_color='gray')
    fig3.add_annotation(
        x='2021W01',
        y=200,
        xref="x",
        yref="y",
        text="50+ yr Olds <br>Offered </br>Primary <br>Dose</br>",
        showarrow=True,
        font=dict(
            family="Arial",
            size=11,
            color="#020202"
        ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=-70,
        ay=25,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ddd9d8 ",
        opacity=0.7
    )

    fig3.add_vline(x='2021W13', line_width=1, line_color='gray')
    fig3.add_annotation(
        x='2021W13',
        y=600,
        xref="x",
        yref="y",
        text="18-49 yr Olds <br>Offered</br>Primary <br>Dose</br>",
        showarrow=True,
        font=dict(
            family="Arial",
            size=11,
            color="#020202"
        ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=-120,
        ay=40,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ddd9d8 ",
        opacity=0.7
    )

    fig3.add_vline(x='2021W31', line_width=1, line_color='gray')
    fig3.add_annotation(
        x='2021W31',
        y=530,
        xref="x",
        yref="y",
        text="16-17 yr Olds <br>Offered</br>Primary <br>Dose</br>",
        showarrow=True,
        font=dict(
            family="Arial",
            size=11,
            color="#020202"
        ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=70,
        ay=-9,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ddd9d8 ",
        opacity=0.7
    )

    fig3.add_vline(x='2021W35', line_width=1, line_color='gray')
    fig3.add_annotation(
        x='2021W35',
        y=200,
        xref="x",
        yref="y",
        text="12-15 yr Olds <br>Offered </br>Primary <br>Dose</br>",
        showarrow=True,
        font=dict(
            family="Arial",
            size=11,
            color="#020202"
        ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=70,
        ay=-25,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ddd9d8 ",
        opacity=0.7
    )

fig3.update_yaxes(range=[0, 610], secondary_y=False)

if injection_value_selected == label_total_cumulative:
    fig3.update_yaxes(range=[0, 4100000], secondary_y=True)
else:
    fig3.update_yaxes(range=[0, 1700000], secondary_y=True)


fig3.update_layout(title='Cumulative Injections and Weekly Deaths (2020-2023 YTD)',
                   height=600
                   )
fig3.update_xaxes(title_text="Week of Year")
fig3.update_yaxes(title_text="Injections", secondary_y=True)
fig3.update_yaxes(title_text="Deaths", secondary_y=False)
st.plotly_chart(fig3, use_container_width=True)

if show_raw_data_selected:
    st.subheader('Raw data')
    st.write(all_deaths_and_injections_df)


#st.caption('...')
