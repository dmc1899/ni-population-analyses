"""
Landing page for application.
"""
import streamlit as st

st.set_page_config(
    page_title="Pandemic Period Data",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)

st.markdown(
    """# Pandemic Period Insights for Northern Ireland
"""
)
st.caption("👈 Select an area of interest from the sidebar to start exploring.")

st.markdown(
    """
    This [data application](https://acho.io/blogs/what-is-a-data-application) 
    provides exploratory analyses of open datasets for 
    Northern Ireland specifically around the COVID-19 pandemic and pandemic 
    response period.
    
    Analyses includes births, deaths, countermeasures and the interrelationship between them.
"""
)

st.image("img/bonhoeffer.jpg", use_column_width=True)
st.caption(
    "[Image credit](https://www.insightforliving.ca/read/articles/dietrich-bonhoeffer)"
)
