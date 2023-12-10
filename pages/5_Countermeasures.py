"""
Countermeasures page.
"""
import base64
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")


@st.cache_data
def load_data(path):
    """
    Load serialised data into dataframe.
    :param path: Location on local filesystem.
    :return: Pandas dataframe.
    """
    dataframe = pd.read_pickle(path)
    return dataframe


@st.cache_data
def convert_df(input_df):
    """
    Conver specified dataframe to CSV.
    :param input_df:
    :return:CSV
    """
    return input_df.to_csv().encode("utf-8")


def display_pdf(file):
    """
    Render a PDF in HTML.
    :param file:
    :return: None.
    """
    # Opening file from file path
    with open(file, "rb") as input_file:
        base64_pdf = base64.b64encode(input_file.read()).decode("utf-8")

    pdf_display = (
        f'<embed src="data:application/pdf;base64,{base64_pdf}" '
        f'width="700" height="1000" type="application/pdf">'
    )

    st.markdown(pdf_display, unsafe_allow_html=True)


def main():
    """
    Driver.
    :return:
    """
    st.title("NI Countermeasures")
    injections_cumulative_df = load_data("data/injections/CumulativeInjectionsUpTo2Dec2023.pkl")

    with st.sidebar:
        st.markdown("### Access underlying data")
        show_raw_data_selected = st.checkbox(
            "Show raw data", value=False, help="Display raw data below the plot."
        )

    tab1, tab2, tab3 = st.tabs(["Rollout", "Clinical Trials", "SEC Filings"])

    with tab1:
        st.markdown(
            """
        ## Injections Administered
        """
        )

        fig_cumulative_injections = make_subplots(specs=[[{"secondary_y": False}]])

        injections = [
            "Primary Dose 1",
            "Primary Dose 2",
            "Primary Dose 3",
            "1st Booster Dose",
            "Spring 2022 Booster",
            "Autumn 2022 Booster",
            "Spring 2023 Booster",
            "Autumn 2023 Booster"
        ]

        for injection in injections:
            fig_cumulative_injections.add_trace(
                go.Scatter(
                    x=injections_cumulative_df["Injection Date"],
                    y=injections_cumulative_df[injection],
                    name=f"{injection} Injection",
                ),
                secondary_y=False,
            )

        layout = go.Layout(
            height=600,
            margin={"l": 50, "r": 50, "b": 100, "t": 100, "pad": 4},
            title={"text": 'Cumulative Injections Administered (December 2020 - December 2023)'},
            xaxis={'title_text': 'Date of administration',
                   'type': 'category',
                   'tickmode': 'linear',
                   'tick0': 1,
                   'dtick': 24},
            yaxis={"title_text": 'Number of Injections'},
        )
        fig_cumulative_injections = go.Figure(
            data=fig_cumulative_injections.data, layout=layout
        )
        st.plotly_chart(fig_cumulative_injections, use_container_width=True, theme=None)

        if show_raw_data_selected:
            st.subheader("Raw data")
            st.write(injections_cumulative_df)

        st.markdown("---")
        st.caption("Data published up to and including 2nd December 2023.")
        st.caption(
            """
        Data sourced from 
        [HSC Vaccination Dashboard](https://covid-19.hscni.net/ni-covid-19-vaccinations-dashboard/).
        """
        )

    with tab2:
        st.markdown("### BioNTech-Pfizer BNT162b2 Clinical Trial")
        st.markdown("#### Deaths during the trial")
        st.markdown(
            "> *During the blinded, controlled period, "
            "15 BNT162b2 and 14 placebo recipients died; during "
            "the open-label period, 3 BNT162b2 "
            "and 2 original placebo recipients who received BNT162b2 "
            "after unblinding died. None "
            "of these deaths were considered related to BNT162b2 by investigators.* "
            "[Ref](https://www.medrxiv.org/content/10.1101/2021.07.28.21261159v1.supplementary-material)"
        )

        trials_deaths_total = load_data(
            "data/injections/pfizer-biontech/CombinedClinicalTrialDeathsTotalOnly.pkl"
        )
        fig2 = go.Figure()

        fig2.add_trace(
            go.Pie(
                labels=trials_deaths_total["Arm"],
                values=trials_deaths_total["Total Deaths"],
                pull=[0, 0.1],
                marker_colors=["salmon", "lightskyblue"],
            )
        )

        fig2.update_layout(
            title="Total Deaths during during "
                  "clinical trial for BioNTech/Pfizer "
                  "BNT162b2 by Trial Arm"
        )

        hovertemp = "<b>Trial Arm: </b> %{label} <br>"
        hovertemp += "<b>Total Deaths: </b> %{value}"

        fig2.update_traces(
            hoverinfo="label+percent",
            textinfo="percent+value",
            textfont_size=14,
            marker={"line": {'color': '#000000', 'width': 1}},
        )
        fig2.update_layout(
            height=400,  # set the height of the figure
            width=600,  # set the width of the figure
            margin={"l": 50, "r": 50, "t": 50, "b": 50},  # set the margins of the figure
        )

        st.plotly_chart(fig2, use_container_width=True, theme=None)

        trials_deaths_breakdown = load_data(
            "data/injections/pfizer-biontech/CombinedClinicalTrialDeathsBreakdown.pkl"
        )

        arms = ["BNT162b2", "Placebo"]
        trials_deaths_breakdown.sort_values("BNT162b2", ascending=False, inplace=True)

        def calculate_color(var):
            return "salmon" if var == "BNT162b2" else "lightskyblue"

        fig = go.Figure()
        for arm in arms:
            fig.add_trace(
                go.Bar(
                    x=trials_deaths_breakdown["Reported Cause of Death"],
                    y=trials_deaths_breakdown[arm],
                    marker_color=calculate_color(arm),
                    name=arm,
                    hovertemplate=f"{arm}",
                )
            )
        fig.update_layout(
            title="Cause(s) of Deaths assigned "
                  "during during clinical "
                  "trial for BioNTech/Pfizer BNT162b2",
            legend_title_text="Arm",
            height=600,
        )
        fig.update_layout(
            height=600,
            width=600,
            margin={"l": 50, "r": 50, "t": 50, "b": 210},  # set the margins of the figure
        )

        fig.update_xaxes(title_text="Cause of Death")
        fig.update_yaxes(title_text="Deaths")
        fig.update_xaxes(tickangle=90)
        st.plotly_chart(fig, use_container_width=True, theme=None)

        st.markdown("#### Trial Report")
        display_pdf(
            "doc/injection/pfizer-biontech/six-month-safety-efficacy-pfizer-mrna.pdf"
        )
        st.markdown(
            """
        
        ##### Appendices
        """
        )
        display_pdf(
            "doc/injection/pfizer-biontech/appendices-to-pfizer-mrna-clinical-trial-document.pdf"
        )

        if show_raw_data_selected:
            st.subheader("Raw data")
            st.write(trials_deaths_total)
            st.write(trials_deaths_breakdown)

        st.markdown("---")
        st.caption(
            "Trial death data sourced from "
            "[Six Month Safety and Efficacy of the BNT162b2 mRNA COVID-19 Vaccine]"
            "(https://www.medrxiv.org/content/10.1101/2021.07.28.21261159v1.supplementary-material)."
        )

    with tab3:
        st.markdown(
            """
        ## Moderna
        """
        )
        st.markdown("#### Product Categorisation")
        st.markdown(
            "> *Currently, mRNA is considered a gene therapy product by "
            "the FDA. Unlike certain gene "
            "therapies that irreversibly alter cell DNA and could act as a source of side effects, "
            "mRNA-based medicines are designed to not irreversibly change "
            "cell DNA; however, side effects "
            "observed in gene therapy could negatively impact the perception of "
            "mRNA medicines despite the "
            "differences in mechanism.* "
            "[Ref](https://www.sec.gov/Archives/edgar/data/1682852/000168285220000017/mrna-20200630.htm)"
        )
        display_pdf("doc/injection/moderna/mrna-20200630.pdf")

        st.markdown(
            """
        ## BioNTech
        """
        )

        display_pdf("doc/injection/pfizer-biontech/biontech-sec-submission-nov-2020.pdf")


if __name__ == "__main__":
    main()
