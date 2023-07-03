"""
Monthly births page.
"""
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")


@st.cache_data
def load_data():
    """
    Load the serialised pickle file into a dataframe.
    :return: Pandas dataframe.
    """
    dataframe = pd.read_pickle("data/births/AllBirthsUpToMonth32023.pkl")
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
    all_monthly_births_df = load_data()
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

    fig = px.bar(
        all_monthly_births_df,
        x="Month_of_Birth",
        y=range_2006_to_2023,
        title="NI Total Monthly Births by Month of Birth 2006-2023",
        barmode="group",
        height=600,
    )

    fig.update_xaxes(title_text="Month of Birth")
    fig.update_yaxes(title_text="Number of Births", secondary_y=False)

    fig.update_layout(legend_title_text="Year")

    st.plotly_chart(fig, use_container_width=True, theme=None)

    if show_raw_data_selected:
        st.subheader("Raw data")
        st.write(all_monthly_births_df)

    st.markdown("---")
    st.caption("Data published up to and including March 2023.")
    st.caption(
        "Data sourced from "
        "[NISRA Monthly Births Registered in Northern Ireland]"
        "(https://www.nisra.gov.uk/publications/monthly-births)."
    )


if __name__ == "__main__":
    main()
