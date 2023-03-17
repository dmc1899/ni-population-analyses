import streamlit as st

st.set_page_config(
    page_title="Northern Ireland Population Analyses",
    page_icon="👋",
)

st.markdown("# Northern Ireland Population Analyses Data Application")

# st.sidebar.success("Select an area of interest above")

st.markdown(
    """
    This is a data application to support exploratory analyses
    of open datasets relating to births, deaths and other population
    characteristics for Northern Ireland.
    
    **👈 Select an area of interest from the sidebar** to start 
    exploring.
"""
)


### Want to learn more?
# - Check out [streamlit.io](https://streamlit.io)
# - Jump into our [documentation](https://docs.streamlit.io)
# - Ask a question in our [community
# forums](https://discuss.streamlit.io)
# ### See more complex demos
# - Use a neural net to [analyze the Udacity Self-driving Car Image
# Dataset](https://github.com/streamlit/demo-self-driving)
# - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
# # ref - https://github.com/jkanner/streamlit-dataview/blob/master/app.py
# import math
#
# import pandas as pd
# import plotly.graph_objects as go
# import streamlit
# import streamlit as st
# from plotly.subplots import make_subplots
#
# st.set_page_config(layout='wide')
#
# # Title the app
# st.title('Northern Ireland Population Analyses')
# st.caption('Use the sidebar on the left to configure parameters for your analyses.')
#
# st.markdown('''
# ## Weekly death registrations for 2023 YTD
# Weekly death statistics dataset sourced from [NISRA Weekly death registrations in Northern Ireland](https://www.nisra.gov.uk/statistics/death-statistics/weekly-death-registrations-northern-ireland).
# ''')
#
#
# @st.cache_data
# def load_data():
#     dataframe = pd.read_pickle('data/AllDeathsUpTo2023Week9.pkl')
#     return dataframe
#
#
# @st.cache_data
# def convert_df(df):
#     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to_csv().encode('utf-8')
#
#
# def get_deaths_for(df, week, column):
#     return df.loc[df['Registration_Week'] == week, column].values[0]
#
#
# def is_higher_or_lower(value):
#     if value < 0:
#         return "lower than"
#     elif value > 0:
#         return "higher than"
#     else:
#         return "(the same as)"
#
#
# def calculate_percentage_change(first_value, second_value):
#     real_difference = (second_value - first_value)
#
#     if first_value != 0:
#         percentage = math.floor((real_difference / first_value) * 100)
#     else:
#         percentage = 0
#     return percentage
#
#
# all_weekly_deaths_df = load_data()
# csv = convert_df(all_weekly_deaths_df)
#
# label_five_year_average_2015_to_2019 = '2015 - 2019'
# label_five_year_average_2016_to_2020 = '2016 - 2020'
# label_five_year_average_2017_to_2021 = '2017 - 2021'
# label_five_year_average_2016_to_2019_and_2021 = '2016 - 2019 and 2021'
#
# # Default UI settings
# analysis_end_week_selected = 9
# mean_value_selected = label_five_year_average_2015_to_2019
#
# with st.sidebar:
#
#     st.markdown("### Configure week and average")
#
#     analysis_end_week_selected = st.number_input('2023 Registration Week:', min_value=1, max_value=9, step=1, value=9,
#                                                  help='The week in the current year up to which points are plotted.')
#
#     mean_value_selected = st.radio(
#         "Five-year Average:",
#         (label_five_year_average_2015_to_2019, label_five_year_average_2016_to_2020,
#          label_five_year_average_2017_to_2021, label_five_year_average_2016_to_2019_and_2021),
#         index=0, help='Institutions such as NISRA or ONS use different 5-year averages for comparison. '\
#                       'Select the average to include the plot.')
#
#     st.markdown("### Access underlying data")
#     show_raw_data_selected = st.checkbox('Show raw data', value= False, help='Display raw data below the plot.')
#
#     st.download_button(
#         label="Download as CSV",
#         data=csv,
#         file_name='all_weekly_deaths.csv',
#         mime='text/csv',
#         help='Download the raw data as a CSV file.'
#     )
#
# if mean_value_selected == label_five_year_average_2015_to_2019:
#     mean_value_to_plot = '2015_to_2019_Mean'
# elif mean_value_selected == label_five_year_average_2016_to_2020:
#     mean_value_to_plot = '2016_to_2020_Mean'
# elif mean_value_selected == label_five_year_average_2017_to_2021:
#     mean_value_to_plot = '2017_to_2021_Mean'
# elif mean_value_selected == label_five_year_average_2016_to_2019_and_2021:
#     mean_value_to_plot = '2016_to_2019_and_2021_Mean'
#
# st.markdown(f'''
# ### Analysis for Registration Week {analysis_end_week_selected} 2023
# ''')
#
# comparison_years = ['2022', '2021', '2020', mean_value_to_plot]
# this_week_2023 = get_deaths_for(all_weekly_deaths_df, analysis_end_week_selected, '2023')
#
# # Initialize a dictionary to store the results
# results = {}
#
# # Loop through each year and calculate the percentage change compared to this_week_2023
# for year in comparison_years:
#     weekly_deaths = get_deaths_for(all_weekly_deaths_df, analysis_end_week_selected, year)
#     percentage_change = calculate_percentage_change(weekly_deaths, this_week_2023)
#     results[f'this_week_{year}_vs_2023'] = percentage_change
#
# #streamlit.write(results)
#
# # Store the results in a list of tuples for easier iteration
# result_tuples = [
#     ('2022', results['this_week_2022_vs_2023']),
#     ('2021', results['this_week_2021_vs_2023']),
#     ('2020', results['this_week_2020_vs_2023']),
#     (f'{mean_value_to_plot}', results[f'this_week_{mean_value_to_plot}_vs_2023'])
# ]
#
# st.markdown(f'Registration Week **{analysis_end_week_selected} in 2023** had **{this_week_2023}** registered deaths which is:')
#
# # Iterate through the results and print them out
# for year, percentage_change in result_tuples:
#     percentage_change_abs = abs(percentage_change)
#     comparison = is_higher_or_lower(percentage_change)
#     colour = 'red' if 'higher' in comparison else 'black'
#     st.markdown(f'- :{colour}[{percentage_change_abs}% {comparison} week {analysis_end_week_selected} in {year}]')
#
#
# fig_deaths_trends = make_subplots(specs=[[{'secondary_y': False}]])
#
# years = [mean_value_to_plot, '2020', '2021', '2022', '2023']
#
# for year in years:
#     fig_deaths_trends.add_trace(
#         go.Scatter(x=all_weekly_deaths_df['Registration_Week'],
#                    y=all_weekly_deaths_df[year].loc[0:(analysis_end_week_selected - 1)] if year == '2023' else all_weekly_deaths_df[year],
#                    name=f'{year} Weekly Deaths',
#                    line_color='red' if 'Mean' in year else None,
#                    line_dash='dot' if 'Mean' in year else None),
#         secondary_y=False,
#     )
#
#
# layout = go.Layout(
#     height=600,
#     margin=dict(l=50, r=50, b=50, t=50, pad=4),
#     title=dict(text=f'Weekly Deaths 2020-2023 (up to Week {analysis_end_week_selected}) by Date of Registration versus {mean_value_selected} 5yr average'),
#     xaxis=dict(title_text='Registration Week', type='category', tickmode='linear', tick0=1, dtick=1),
#     yaxis=dict(title_text='Deaths'),
#     legend=dict(
#         orientation="h",
#         yanchor="bottom",
#         y=-0.4,
#         xanchor="left",
#         x=0.01
#     ),
#     # annotations=[dict(
#     #     x='8.1',
#     #     y=324,
#     #     xref='x',
#     #     yref='y',
#     #     text='Week Ending 3rd March 2023',
#     #     showarrow=True,
#     #     font=dict(family='Arial', size=11, color='#020202'),
#     #     align='left',
#     #     arrowhead=2,
#     #     arrowsize=1,
#     #     arrowwidth=2,
#     #     arrowcolor='#636363',
#     #     ax=70,
#     #     ay=-250,
#     #     bordercolor='#c7c7c7',
#     #     borderwidth=2,
#     #     borderpad=4,
#     #     bgcolor='#ddd9d8 ',
#     #     opacity=0.8
#     # )]
# )
# fig_deaths_trends = go.Figure(data=fig_deaths_trends.data, layout=layout)
#
# # fig_deaths_trends.update_layout(legend=dict(
# #     orientation="h",
# #     yanchor="bottom",
# #     y=-0.,
# #     xanchor="left",
# #     x=0.01
# # ))
#
# st.plotly_chart(fig_deaths_trends, use_container_width=True, theme=None)
#
# if show_raw_data_selected:
#     st.subheader('Raw data')
#     st.write(all_weekly_deaths_df)
#
#
# all_weekly_deaths_df_copy = all_weekly_deaths_df.copy()
# all_weekly_deaths_df_copy['week_name'] = all_weekly_deaths_df_copy.index
#
# import matplotlib.pyplot as plt
# from matplotlib.ticker import AutoMinorLocator, MultipleLocator
#
# fig, axs = plt.subplots(1, 1, constrained_layout=True, figsize=(10,4))
#
# #fig.suptitle('NI Excess Weekly Deaths 2020-2023 against 2015-2019 Mean', color='black')
#
# years_to_compare = ['2023']
# index=0
#
# for year in years_to_compare:
#
#     axs.set_title(f'Weekly Deaths 2023 (up to Week {analysis_end_week_selected}) by Date of Registration versus {mean_value_selected} 5yr average', fontsize=10, verticalalignment='top', color='black', pad=18.0)
#
#     x = all_weekly_deaths_df_copy['Registration_Week'].loc[0:(analysis_end_week_selected - 1)] if year == "2023" else all_weekly_deaths_df_copy['Registration_Week']
#     y1 = all_weekly_deaths_df_copy[mean_value_to_plot].loc[0:(analysis_end_week_selected - 1)] if year == "2023" else all_weekly_deaths_df_copy[mean_value_to_plot]
#
#     y2 = all_weekly_deaths_df_copy[f'{year}'].loc[0:(analysis_end_week_selected - 1)] if year == "2023" else all_weekly_deaths_df_copy[f'{year}']
#
#     axs.set_xlim(1, 52)
#     axs.set_ylim(200, 550)
#
#     axs.grid(linestyle="--", linewidth=0.25, color='.5', zorder=-10)
#
#     axs.plot(x, y1, color='red', lw=0.5, label=mean_value_selected, linestyle="--")
#     axs.plot(x, y2, color='dimgrey', lw=0.5, label=f'{year}')
#
#     axs.fill_between(x, y1, y2, where=y2 >= y1, facecolor='lightcoral', interpolate=True)
#     axs.fill_between(x, y1, y2, where=y2 <= y1, facecolor='palegreen', interpolate=True)
#
#     axs.set_xlabel("Registration Week", fontsize=9)
#     axs.set_ylabel("Deaths", fontsize=9)
#
#     axs.xaxis.set_major_locator(MultipleLocator(1))
#
#     axs.tick_params(which='major', width=1.0, length=10, labelsize=8)
#     axs.tick_params(which='minor', width=1.0, length=5, labelsize=8, labelcolor='0.25')
#
#     axs.legend(loc="upper right", fontsize=9)
#
#     index+=1
#
# st.pyplot(fig)
# # with st.echo(code_location='below'):
# #     total_points = st.slider('Number of points in spiral', 1, 5000, 2000)
# #     num_turns = st.slider('Number of turns in spiral', 1, 100, 9)
# #
# #     Point = namedtuple('Point', 'x y')
# #     data = []
# #
# #     points_per_turn = total_points / num_turns
# #
# #     for curr_point_num in range(total_points):
# #         curr_turn, i = divmod(curr_point_num, points_per_turn)
# #         angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
# #         radius = curr_point_num / total_points
# #         x = radius * math.cos(angle)
# #         y = radius * math.sin(angle)
# #         data.append(Point(x, y))
# #
# #     st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
# #         .mark_circle(color='#0068c9', opacity=0.5)
# #         .encode(x='x:Q', y='y:Q'))