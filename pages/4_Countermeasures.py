# ref - https://github.com/jkanner/streamlit-dataview/blob/master/app.py
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import base64

st.set_page_config(layout='wide')

st.title('Countermeasures (2020 - Present)')
#st.caption('Use the sidebar on the left to configure parameters for your analyses.')


@st.cache_data
def load_data(path):
    dataframe = pd.read_pickle(path)
    return dataframe


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def display_pdf(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        # Embedding PDF in HTML
    pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" ' \
                  F'width="700" height="1000" type="application/pdf">'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

#st.info('Plotting cumulative injection distribution')

injections_cumulative_df = load_data('data/injections/CumulativeInjections.pkl')
#csv = convert_df(injections_cumulative_df)

with st.sidebar:

    st.markdown("### Access underlying data")
    show_raw_data_selected = st.checkbox('Show raw data', value=False, help='Display raw data below the plot.')

    # st.download_button(
    #     label="Download as CSV",
    #     data=csv,
    #     file_name='all_weekly_deaths.csv',
    #     mime='text/csv',
    #     help='Download the raw data as a CSV file.'
    # )

tab1, tab2, tab3 = st.tabs(["Rollout", "Clinical Trials", "SEC Filings"])


with tab1:
    st.markdown('''
    ## Injections Administered
    ''')
    # st.header("A cat")
    # st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

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
        height=600,
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

    st.markdown('---')
    st.caption('''
    Injection distribution data sourced from [HSC Vaccination Dashboard](https://covid-19.hscni.net/ni-covid-19-vaccinations-dashboard/).
    ''')

with tab2:
    st.markdown("### BioNTech-Pfizer BNT162b2 Clinical Trial")
    st.markdown("#### Deaths during the trial")
    st.markdown("> *During the blinded, controlled period, 15 BNT162b2 and 14 placebo recipients died; during "
                "the open-label period, 3 BNT162b2 and 2 original placebo recipients who received BNT162b2 "
                "after unblinding died. None of these deaths were considered related to BNT162b2 by investigators.* "
                "[Ref](https://www.medrxiv.org/content/10.1101/2021.07.28.21261159v1.supplementary-material)")

    trials_deaths_total = load_data('data/injections/pfizer-biontech/CombinedClinicalTrialDeathsTotalOnly.pkl')
    fig2 = go.Figure()

    fig2.add_trace(go.Pie(labels=trials_deaths_total['Arm'],
                          values=trials_deaths_total['Total Deaths'],
                          pull=[0, 0.1],
                          marker_colors=['salmon','lightskyblue']))

    fig2.update_layout(title='Total Deaths during during clinical trial for BioNTech/Pfizer BNT162b2 by Trial Arm')

    hovertemp = "<b>Trial Arm: </b> %{label} <br>"
    hovertemp += "<b>Total Deaths: </b> %{value}"

    fig2.update_traces(hoverinfo='label+percent', textinfo='percent+value', textfont_size=14,
                       marker=dict(line=dict(color='#000000', width=1)))
    fig2.update_layout(
        height=400, # set the height of the figure
        width=600, # set the width of the figure
        margin=dict(l=50, r=50, t=50, b=50), # set the margins of the figure
    )

    st.plotly_chart(fig2, use_container_width=True, theme=None)

    trials_deaths_breakdown = load_data('data/injections/pfizer-biontech/CombinedClinicalTrialDeathsBreakdown.pkl')

    arms = ['BNT162b2', 'Placebo']
    trials_deaths_breakdown.sort_values('BNT162b2', ascending=False, inplace=True)

    def calculate_color(var):
        return 'salmon' if var == 'BNT162b2' else 'lightskyblue'

    fig = go.Figure()
    for arm in arms:
        fig.add_trace(go.Bar(x=trials_deaths_breakdown['Reported Cause of Death'], y=trials_deaths_breakdown[arm],
                             marker_color=calculate_color(arm),
                             name=arm,
                             hovertemplate=f"{arm}"))
    fig.update_layout(title='Cause(s) of Deaths assigned during during clinical trial for BioNTech/Pfizer BNT162b2',
                      legend_title_text = "Arm", height=600)
    fig.update_layout(
        height=600,
        width=600,
        margin=dict(l=50, r=50, t=50, b=210), # set the margins of the figure
    )

    fig.update_xaxes(title_text="Cause of Death")
    fig.update_yaxes(title_text="Deaths")
    fig.update_xaxes(tickangle=90)
    st.plotly_chart(fig, use_container_width=True, theme=None)

    st.markdown("#### Trial Report")
    display_pdf('doc/injection/pfizer-biontech/six-month-safety-efficacy-pfizer-mrna.pdf')
    st.markdown('''
    
    ##### Appendices
    ''')
    display_pdf('doc/injection/pfizer-biontech/appendices-to-pfizer-mrna-clinical-trial-document.pdf')

    if show_raw_data_selected:
        st.subheader('Raw data')
        st.write(trials_deaths_total)
        st.write(trials_deaths_breakdown)

    st.markdown('---')
    st.caption('Trial death data sourced from [Six Month Safety and Efficacy of the BNT162b2 mRNA COVID-19 Vaccine]'
               '(https://www.medrxiv.org/content/10.1101/2021.07.28.21261159v1.supplementary-material).')

with tab3:
    st.markdown('''
    ## Moderna
    ''')
    st.markdown("#### Product Categorisation")
    st.markdown("> *Currently, mRNA is considered a gene therapy product by the FDA. Unlike certain gene "
                "therapies that irreversibly alter cell DNA and could act as a source of side effects, "
                "mRNA-based medicines are designed to not irreversibly change cell DNA; however, side effects "
                "observed in gene therapy could negatively impact the perception of mRNA medicines despite the "
                "differences in mechanism.* "
                "[Ref](https://www.sec.gov/Archives/edgar/data/1682852/000168285220000017/mrna-20200630.htm)")
    display_pdf('doc/injection/moderna/mrna-20200630.pdf')

    st.markdown('''
    ## BioNTech
    ''')

    display_pdf('doc/injection/pfizer-biontech/biontech-sec-submission-nov-2020.pdf')
