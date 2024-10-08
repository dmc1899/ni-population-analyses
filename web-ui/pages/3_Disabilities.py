"""
Disabilities page.
"""

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from lib.page_utils import *

st.set_page_config(layout="wide")


@st.cache_data
def load_data():
    """
    Load serialised data into dataframe.
    :return: Pandas dataframe.
    """
    dataframe = pd.read_pickle(
        f"{st.session_state['parent_resource_path']}resources/data/disabilities/MonthlyDisabilityRegistrationsNov2022.pkl"
    )
    return dataframe


@st.cache_data
def convert_df(input_df):
    """
    Conver a dataframe to CSV.
    :param input_df:Dataframe to convert.
    :return: CSV
    """
    return input_df.to_csv().encode("utf-8")


def main():
    """
    Driver.
    :return: None
    """
    st.title("NI Personal Independence Payment Claims")

    disability_claims_df = load_data()
    csv = convert_df(disability_claims_df)

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

    fig = make_subplots(specs=[[{"secondary_y": False}]])

    fig.add_trace(
        go.Scatter(
            x=disability_claims_df["Year Month"],
            y=disability_claims_df["Total New Claims Registered"],
            name="Total New Claims",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=disability_claims_df["Year Month"],
            y=disability_claims_df["Total New Claims 12-month Rolling Average"],
            name="12-month Rolling Average",
            line={"dash": 'dash'},
            visible="legendonly",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=disability_claims_df["Year Month"],
            y=disability_claims_df["Total New Claims 6-month Rolling Average"],
            name="6-month Rolling Average",
            line={"dash": 'dash'},
            visible="legendonly",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=disability_claims_df["Year Month"],
            y=disability_claims_df["Total New Claims 3-month Rolling Average"],
            name="3-month Rolling Average",
            line={"dash": 'dash'},
            visible="legendonly",
        ),
        secondary_y=False,
    )

    # fig.update_layout(
    #     title_text="New Personal Independence Claims by Month (2016-2022)", height=650
    # )

    # fig.update_xaxes(
    #     {'title_text': 'Month', 'type': 'category', 'tickmode': 'linear', 'tick0': 1, 'dtick': 2}
    #
    # )

    fig.update_yaxes(title_text="Claims", secondary_y=False)

    layout = go.Layout(
        height=650,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
        title=dict(text="New Personal Independence Claims by Month (2016-2022)"),
        xaxis=dict(title_text="Month", type='category', tickmode = 'linear', tick0 = 1, dtick = 2,tickangle=50),
        yaxis=dict(title_text="Claims"),
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": -0.4,
            "xanchor": "left",
            "x": 0.01,
        },
        plot_bgcolor='rgba(0,0,0,0)',  # Makes the plot area background transparent
        # paper_bgcolor='rgba(0,0,0,0)', # Makes the entire figure background transparent
        font={
            "color": "black"            # Sets the text color of all the components
        }
    )
    fig = go.Figure(data=fig.data, layout=layout)
    # st.plotly_chart(fig_cum_sum_deaths_fig, use_container_width=True, theme=None)
    st.plotly_chart(fig, use_container_width=True, theme=None)

    if show_raw_data_selected:
        st.subheader("Raw data")
        st.write(disability_claims_df)

    st.markdown("---")
    st.caption("Data published up to and including November 2022.")
    st.caption(
        """
    Data sourced from [Department for Communities Personal Independence 
    Payment Statistics](https://www.communities-ni.gov.uk/articles/personal-independence-payment-statistics).
    """
    )


if __name__ == "__main__":
    initialize_session_state()
    main()
