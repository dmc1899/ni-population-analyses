"""
Monthly births page.
"""
import os

import pandas as pd
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator
from lib.page_utils import *

st.set_page_config(layout="wide")

LATEST_MONTHLY_DATAPOINT_POSITION = 50  # March 2023 = 39


@st.cache_data
def load_data(data_file):
    """
    Load the serialised pickle file into a dataframe.
    :return: Pandas dataframe.
    """
    dataframe = pd.read_pickle(data_file)
    return dataframe


@st.cache_data
def convert_df(input_df):
    """
    Conver the specified dataframe to CSV.
    :param input_df: Dataframe to convert.
    :return: CSV
    """
    return input_df.to_csv().encode("utf-8")


def main():
    """
    Driver.
    :return:
    """
    st.title("NI Monthly Births")
    print(os.getcwd())
    monthly_delta_births_df = load_data(
        f"{st.session_state['parent_resource_path']}resources/data/births/MeanBirthDifference2020to20204_2.pkl"
        # "resources/data/births/MeanBirthDifference2020to20204_2.pkl"
    )[0:LATEST_MONTHLY_DATAPOINT_POSITION]

    # Create the figure and axes objects, specify the size and the dots per inches
    fig, axes = plt.subplots(figsize=(8, 4), dpi=220)

    # Plot bars
    bar1 = axes.bar(
        monthly_delta_births_df["Month_Year_of_Birth"],
        monthly_delta_births_df["% Change from Period Mean Births"],
        width=0.6,
    )
    axes.grid(which="major", axis="x", color="#DAD8D7", alpha=0.5, zorder=1)
    axes.grid(which="major", axis="y", color="#DAD8D7", alpha=0.5, zorder=1)

    # Reformat x-axis label and tick labels
    axes.set_xlabel("Month", fontsize=8, labelpad=10)  # No need for an axis label
    axes.xaxis.set_label_position("bottom")
    axes.xaxis.set_major_locator(MaxNLocator(integer=True))
    axes.xaxis.set_tick_params(
        pad=2, labelbottom=True, bottom=True, labelsize=5, labelrotation=90
    )
    axes.set_xticks(
        monthly_delta_births_df["Month_Year_of_Birth"]
    )  # Map integers numbers from the series to labels list

    axes.set_ylabel("% Change from 2015-2019 Mean", fontsize=6, labelpad=10)
    axes.yaxis.set_label_position("left")
    axes.yaxis.set_major_formatter(lambda s, i: f"{s:,.1f}%")
    axes.yaxis.set_major_locator(MaxNLocator(integer=True))
    axes.yaxis.set_tick_params(
        pad=2, labeltop=False, labelbottom=True, bottom=False, labelsize=5
    )

    # Add label on top of each bar
    axes.bar_label(
        bar1,
        labels=[
            f"{e:,.1f}%"
            for e in monthly_delta_births_df["% Change from Period Mean Births"]
        ],
        padding=3,
        color="black",
        fontsize=4,
    )

    # Remove the spines
    axes.spines[["top", "left", "bottom", "right"]].set_visible(False)

    # Make the left spine thicker
    axes.spines["right"].set_linewidth(1.1)

    # Add in title and subtitle
    axes.text(
        x=0.22,
        y=0.98,
        s="Percentage change in Monthly Births 2020-2024 v " "2015-2019 Mean",
        transform=fig.transFigure,
        ha="left",
        fontsize=10,
        # weight="normal",
        alpha=0.9,
    )
    axes.text(
        x=0.12,
        y=0.92,
        s="Displays the percentage difference in monthly births "
        "versus the 2015-2019 average figure for "
        "the same month.",
        transform=fig.transFigure,
        ha="left",
        fontsize=6,
        alpha=0.8,
    )

    # Adjust the margins around the plot area
    plt.subplots_adjust(
        left=None, bottom=0.2, right=None, top=0.85, wspace=None, hspace=None
    )

    # Set a white background
    fig.patch.set_facecolor("white")

    # Colours - Choose the extreme colours of the colour map
    colours = ["#2196f3", "#bbdefb"]

    # Colormap - Build the colour maps
    cmap = mpl.colors.LinearSegmentedColormap.from_list("colour_map", colours, N=256)
    norm = mpl.colors.Normalize(
        monthly_delta_births_df["% Change from Period Mean Births"].min(),
        monthly_delta_births_df["% Change from Period Mean Births"].max(),
    )
    # linearly normalizes data into the [0.0, 1.0] interval

    # Plot bars
    bar1 = axes.bar(
        monthly_delta_births_df["Month_Year_of_Birth"],
        monthly_delta_births_df["% Change from Period Mean Births"],
        color=cmap(norm(monthly_delta_births_df["% Change from Period Mean Births"])),
        width=0.6,
        zorder=2,
    )

    axes.text(
        "January 2022",
        0.7,
        "Injections first offered to women of "
        "child-bearing age 9 months before this date",
        ha="right",
        va="center",
        size=5,
        zorder=3,
        color="red",
    )
    plt.axvline(x="January 2022", color="red", linewidth=1, mouseover=True)

    st.pyplot(fig)
    st.markdown("---")

    all_monthly_births_df = load_data(f"{st.session_state['parent_resource_path']}resources/data/births/AllBirthsUpToMonth22024.pkl") #"web-ui/resources/data/births/AllBirthsUpToMonth22024.pkl"
    csv = convert_df(all_monthly_births_df)

    range_2006_to_2023 = [
        "2006",
        "2007",
        "2008",
        "2009",
        "2010",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024"
    ]

    with st.sidebar:
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
    #
    # fig = px.bar(
    #     all_monthly_births_df,
    #     x="Month_of_Birth",
    #     y=range_2006_to_2023,
    #     title="NI Total Monthly Births by Month of Birth 2006-2023",
    #     barmode="group",
    #     height=600,
    # )
    #
    # fig.update_xaxes(title_text="Month of Birth")
    # fig.update_yaxes(title_text="Number of Births", secondary_y=False)
    #
    # fig.update_layout(legend_title_text="Year")
    #
    # st.plotly_chart(fig, use_container_width=True, theme=None)

    # fig = go.Figure()
    fig2 = make_subplots(specs=[[{"secondary_y": False}]])

    # Adding a bar trace for each year in the specified range
    for year in range_2006_to_2023:
        fig2.add_trace(go.Bar(
            x=all_monthly_births_df["Month_of_Birth"],
            y=all_monthly_births_df[year],
            name=str(year)
        ))

    # Update the layout of the figure

    new_layout = go.Layout(
        height=600,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
        title=dict(
            text="NI Total Monthly Births by Month of Birth 2006-2024",
            x=0.5,  # Centers the title
            xanchor='center',
            font=dict(
                size=16,  # Adjust the font size as needed
                color='black',  # Set the font color
                family='Arial',  # Set the font family
                weight='normal'  # Make the text non-bold
            )
        ),
        xaxis=dict(title_text="Month of Birth", type='category', tickmode = 'linear', tick0 = 1, dtick = 1, tickangle=0, tickfont=dict(size=14, color='black')),
        yaxis=dict(title_text="Number of Births", tickfont=dict(size=14, color='black'), title_standoff=5),
        plot_bgcolor='rgba(0,0,0,0)',  # Makes the plot area background transparent
        paper_bgcolor='rgba(0,0,0,0)', # Makes the entire figure background transparent
        font={
            "color": "black"            # Sets the text color of all the components
        },
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": -0.4,
            "xanchor": "left",
            "x": 0.01,
        },
    )

    fig2 = go.Figure(data=fig2.data, layout=new_layout)
    st.plotly_chart(fig2, use_container_width=True, theme=None)

    if show_raw_data_selected:
        st.subheader("Raw data")
        st.write(all_monthly_births_df)

    st.markdown("---")
    st.caption("Data published up to and including February 2024.")
    st.caption(
        "Data sourced from "
        "[NISRA Monthly Births Registered in Northern Ireland]"
        "(https://www.nisra.gov.uk/publications/monthly-births)."
    )


if __name__ == "__main__":
    initialize_session_state()
    main()
