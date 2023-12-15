"""
Weekly deaths page.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

st.set_page_config(layout="wide")

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def mutate_safely(function):
    """
    There are a limited number of pandas transformations that mutate the dataframe
    in place.  These are limited to modifying a column of data (insert, delete or update);
    assigning to the index or column attributes and modifying the values directly in the dataframe.

    The purpose of this function is to perform the mutating functions idempotently by mutating
    local deep copies of dataframes and returning new copies back to the caller.

    We use Python decorators to adopt this pattern without polluting our core functions. We
    decorate any function with @mutate_safely and write a function that mutates the given
    dataframe directly without returning it.
    """
    def mutate(df, **params):
        df = df.copy()
        function(df, **params)
        return df

    return mutate


@mutate_safely
def rename_index_with_labels(df, labels):
    df.rename(index=labels, inplace=True)
    return


def subset_columns(df, columns):
    return df[columns]


def subset_rows(df, start, end):
    return df[start:end]


def style_dataframe(df, axis=1):
    return df.style.background_gradient(axis=axis)


def generate_sequence_labels(prefix, label_range):
    return {i: f"{prefix} {i + 1}" for i in range(label_range)}


@st.cache_data
def load_data():
    """
    Load the input data from the local filesystem.
    :return: Pandas dataframe
    """
    dataframe = pd.read_pickle("data/deaths/AllDeathsUpTo2023Week49.pkl")
    return dataframe


@st.cache_data
def convert_df_to_csv(input_df):
    """
    Convert a dataframe to CSV format.
    :param input_df:
    :return: CSV
    """
    return input_df.to_csv().encode("utf-8")


def get_deaths_for(input_df, week, year):
    """
    Extract the number of deaths from the given
    dataframe for the given week number
    and column name.
    :param input_df: Dataframe containing the death figures.
    :param week: The week number.
    :param year: The year.
    :return:
    """
    return input_df.loc[input_df["Registration_Week"] == week, year].values[0]


def is_higher_or_lower(value):
    """
    Returns a string from a numerical comparison.
    :param value: The value to evaluate.
    :return: String indicating comparison result.
    """
    if value < 0:
        return "lower"
    if value > 0:
        return "higher"
    return "(the same as)"


def calculate_percentage_change(first_value, second_value):
    """
    Calculate the percentage change between two values.
    :param first_value: Starting value.
    :param second_value: Ending value.
    :return: Increase from Starting to Ending value.
    """
    real_difference = second_value - first_value

    if first_value != 0:
        percentage = round((real_difference / first_value) * 100, 1)
    else:
        percentage = 0
    return percentage


ALL_YEAR_COLUMNS = [
    "2015",
    "2016",
    "2017",
    "2018",
    "2019",
    "2020",
    "2021",
    "2022",
    "2023",
]

LABEL_FIVE_YEAR_AVERAGE_2015_TO_2019 = "2015-2019"
LABEL_FIVE_YEAR_AVERAGE_2016_TO_2020 = "2016-2020"
LABEL_FIVE_YEAR_AVERAGE_2017_TO_2021 = "2017-2021"
LABEL_FIVE_YEAR_AVERAGE_2018_TO_2022 = "2018-2022"
LABEL_FIVE_YEAR_AVERAGE_2016_TO_2019_AND_2021 = "2016-2019 and 2021"

label_key_mapping = {
    LABEL_FIVE_YEAR_AVERAGE_2015_TO_2019: "2015_to_2019_Mean",
    LABEL_FIVE_YEAR_AVERAGE_2016_TO_2020: "2016_to_2020_Mean",
    LABEL_FIVE_YEAR_AVERAGE_2017_TO_2021: "2017_to_2021_Mean",
    LABEL_FIVE_YEAR_AVERAGE_2018_TO_2022: "2018_to_2022_Mean",
    LABEL_FIVE_YEAR_AVERAGE_2016_TO_2019_AND_2021: "2016_to_2019_and_2021_Mean",
}


def main():
    """
    Driver.
    :return:
    """
    st.title("NI Weekly Deaths")
    st.caption("👈 Use the sidebar to configure parameters for your analysis.")

    all_weekly_deaths_df = load_data()
    csv = convert_df_to_csv(all_weekly_deaths_df)

    with st.sidebar:
        st.markdown("### Configure week and average")

        analysis_end_week_selected = st.number_input(
            "2023 Registration Week:",
            min_value=1,
            max_value=49,
            step=1,
            value=49,
            help="The registration week in the current year to analyse.",
        )

        mean_value_selected = st.radio(
            "Five-year average:",
            (
                LABEL_FIVE_YEAR_AVERAGE_2015_TO_2019,
                LABEL_FIVE_YEAR_AVERAGE_2016_TO_2020,
                LABEL_FIVE_YEAR_AVERAGE_2017_TO_2021,
                LABEL_FIVE_YEAR_AVERAGE_2018_TO_2022,
                LABEL_FIVE_YEAR_AVERAGE_2016_TO_2019_AND_2021,
            ),
            index=0,
            help="Institutions such as NISRA or ONS use different 5-year averages for comparison. "
            "Select the average to include the plot.",
        )

        st.markdown("### Access underlying data")
        show_raw_data_selected = st.checkbox(
            "Show raw data", value=False, help="Display raw data below the plot."
        )

        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="all_weekly_deaths.csv",
            mime="text/csv",
            help="Download the raw data as a CSV file.",
        )

    mean_value_to_plot = label_key_mapping.get(mean_value_selected, "2015_to_2019_Mean")
    mean_value_selected = mean_value_selected + " 5yr average"

    comparison_years = ["2022", "2021", "2020", mean_value_to_plot]
    this_week_2023 = get_deaths_for(
        all_weekly_deaths_df, analysis_end_week_selected, "2023"
    )

    st.metric(
        f"Week {analysis_end_week_selected} 2023",
        f"{this_week_2023} Deaths",
        "",
        delta_color="inverse",
        help=f"There were {this_week_2023} deaths registered "
        f"during registration week {analysis_end_week_selected} of 2023.",
    )

    st.markdown("---")
    st.markdown("#### Prior Year Comparisons")
    col2, col3, col4, col5 = st.columns(4)

    metric_results = {}
    for comparison_year in comparison_years:
        weekly_deaths = get_deaths_for(
            all_weekly_deaths_df, analysis_end_week_selected, comparison_year
        )
        percentage_change = calculate_percentage_change(weekly_deaths, this_week_2023)
        percentage_change_abs = abs(percentage_change)
        comparison_outcome = is_higher_or_lower(percentage_change)

        if "higher" in comparison_outcome:
            display_colour = "red"
        elif "lower" in comparison_outcome:
            display_colour = "green"
        else:
            display_colour = "black"

        if "Mean" in comparison_year:
            formatted_year = mean_value_selected
            metric_title = f"Week {analysis_end_week_selected} {mean_value_selected}"
        else:
            formatted_year = comparison_year
            metric_title = f"Week {analysis_end_week_selected} {comparison_year}"

        metric_summary_text = (
            f":{display_colour}[Week {analysis_end_week_selected} is "
            f"{percentage_change_abs}% {comparison_outcome} in 2023 than "
            f"in {formatted_year}.]"
        )

        metric_results[f"this_week_{comparison_year}_vs_2023"] = (
            metric_title,
            weekly_deaths,
            percentage_change,
            metric_summary_text,
        )

    comparison_years = ["2022", "2021", "2020", f"{mean_value_to_plot}"]

    for comparison_year in comparison_years:
        computed_key_value = f"this_week_{comparison_year}_vs_2023"
        metric_title = metric_results[f"this_week_{comparison_year}_vs_2023"][0]
        weekly_deaths = metric_results[f"this_week_{comparison_year}_vs_2023"][1]
        percentage_change = metric_results[f"this_week_{comparison_year}_vs_2023"][2]

        col = None
        help_text = (
            f"There were {weekly_deaths} deaths registered "
            f"during registration week {analysis_end_week_selected} "
            f"of {comparison_year}."
        )

        if comparison_year == f"{mean_value_to_plot}":
            col = col5
            average_comparison_key = f"this_week_{mean_value_to_plot}_vs_2023"
        elif comparison_year == "2022":
            col = col2
        elif comparison_year == "2021":
            col = col3
        elif comparison_year == "2020":
            col = col4

        col.metric(
            metric_title,
            weekly_deaths,
            f"{percentage_change}%",
            delta_color="inverse",
            help=help_text,
        )
        col.markdown(metric_results[f"{computed_key_value}"][3])

    plot_years = [mean_value_to_plot, "2020", "2021", "2022", "2023"]

    fig_deaths_trends = make_subplots(specs=[[{"secondary_y": False}]])

    for comparison_year in plot_years:
        fig_deaths_trends.add_trace(
            go.Scatter(
                x=all_weekly_deaths_df["Registration_Week"],
                y=all_weekly_deaths_df[comparison_year].loc[
                    0 : (analysis_end_week_selected - 1)
                ]
                if comparison_year == "2023"
                else all_weekly_deaths_df[comparison_year],
                name=f"{comparison_year} Weekly Deaths",
                line_color="red" if "Mean" in comparison_year else None,
                line_dash="dot" if "Mean" in comparison_year else None,
            ),
            secondary_y=False,
        )

    layout = go.Layout(
        height=600,
        margin={"l": 50, "r": 50, "b": 50, "t": 50, "pad": 4},
        title={
            "text": f"Weekly Deaths 2020-2023 (up to Week {analysis_end_week_selected}) "
            f"by Date of Registration versus {mean_value_selected}"
        },
        xaxis={
            "title_text": "Registration Week",
            "type": "category",
            "tickmode": "linear",
            "tick0": 1,
            "dtick": 1,
        },
        yaxis={"title_text": "Deaths"},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": -0.4,
            "xanchor": "left",
            "x": 0.01,
        },
    )

    fig_deaths_trends = go.Figure(data=fig_deaths_trends.data, layout=layout)

    st.markdown("---")
    st.plotly_chart(fig_deaths_trends, use_container_width=True, theme=None)

    all_weekly_deaths_df_copy = all_weekly_deaths_df.copy()
    all_weekly_deaths_df_copy["week_name"] = all_weekly_deaths_df_copy.index

    fig, axs = plt.subplots(1, 1, constrained_layout=True, figsize=(10, 4))

    for comparison_year in ["2023"]:
        axs.set_title(
            f"Weekly Deaths 2023 (up to Week {analysis_end_week_selected}) by "
            f"Date of Registration versus {mean_value_selected}",
            fontsize=10,
            verticalalignment="top",
            color="black",
            pad=18.0,
        )

        x_plot_point = (
            all_weekly_deaths_df_copy["Registration_Week"].loc[
                0 : (analysis_end_week_selected - 1)
            ]
            if comparison_year == "2023"
            else all_weekly_deaths_df_copy["Registration_Week"]
        )

        y1_plot_point = (
            all_weekly_deaths_df_copy[mean_value_to_plot].loc[
                0 : (analysis_end_week_selected - 1)
            ]
            if comparison_year == "2023"
            else all_weekly_deaths_df_copy[mean_value_to_plot]
        )

        y2_plot_point = (
            all_weekly_deaths_df_copy[f"{comparison_year}"].loc[
                0 : (analysis_end_week_selected - 1)
            ]
            if comparison_year == "2023"
            else all_weekly_deaths_df_copy[f"{comparison_year}"]
        )

        axs.set_xlim(1, 52)
        axs.set_ylim(200, 550)

        axs.grid(linestyle="--", linewidth=0.25, color=".5", zorder=-10)

        axs.plot(
            x_plot_point,
            y1_plot_point,
            color="red",
            lw=0.5,
            label=mean_value_selected,
            linestyle="--",
        )
        axs.plot(
            x_plot_point,
            y2_plot_point,
            color="dimgrey",
            lw=0.5,
            label=f"{comparison_year}",
        )

        axs.fill_between(
            x_plot_point.astype(int),
            y1_plot_point.astype(float),
            y2_plot_point.astype(int),
            where=y2_plot_point >= y1_plot_point,
            facecolor="lightcoral",
            interpolate=True,
        )
        axs.fill_between(
            x_plot_point.astype(int),
            y1_plot_point.astype(float),
            y2_plot_point.astype(int),
            where=y2_plot_point <= y1_plot_point,
            facecolor="palegreen",
            interpolate=True,
        )

        axs.set_xlabel("Registration Week", fontsize=9)
        axs.set_ylabel("Deaths", fontsize=9)

        axs.xaxis.set_major_locator(MultipleLocator(1))

        axs.tick_params(which="major", width=1.0, length=10, labelsize=8)
        axs.tick_params(
            which="minor", width=1.0, length=5, labelsize=8, labelcolor="0.25"
        )

        axs.legend(loc="upper right", fontsize=9)

    st.markdown("---")
    st.pyplot(fig)

    st.markdown("---")
    st.markdown(
        f"#### Weekly Deaths Heatmap Comparison 2015 - 2023 (up to Week {analysis_end_week_selected})"
    )

    all_weekly_deaths_styled_df = (
        all_weekly_deaths_df.fillna(np.NZERO)
        .pipe(subset_columns, columns=ALL_YEAR_COLUMNS)
        .pipe(subset_rows, start=0, end=(analysis_end_week_selected))
        .pipe(rename_index_with_labels, labels=generate_sequence_labels("Week", 53))
        .pipe(style_dataframe, axis=1)
    )

    st.dataframe(
        all_weekly_deaths_styled_df,
        use_container_width=False,
        height=(36 * analysis_end_week_selected),
    )  # 1228 is length for 34, 1190 is for 33 - 38 per week.

    if show_raw_data_selected:
        st.subheader("Raw data")
        st.write(all_weekly_deaths_df)

    st.markdown("---")
    st.caption("Data published up to and including 8th December 2023.")
    st.caption(
        "Data sourced from [NISRA Weekly death registrations in "
        "Northern Ireland](https://www.nisra.gov.uk/statistics/death-statistics/"
        "weekly-death-registrations-northern-ireland)."
    )


if __name__ == "__main__":
    main()
