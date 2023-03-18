import streamlit as st

st.set_page_config(
    page_title="Northern Ireland Population Analyses",
    page_icon="chart_with_upwards_trend", #page_icon="👋",
    # layout='wide'
)

st.markdown("# Northern Ireland Population Analyses Data Application")

st.markdown(
    """
    This is a data application to support exploratory analyses
    of open datasets relating to births, deaths and other population
    characteristics for Northern Ireland.
    
    **👈 Select an area of interest from the sidebar** to start 
    exploring.
"""
)

st.image('img/bonhoeffer.jpg', use_column_width=True)
st.caption('[Image credit](https://www.insightforliving.ca/read/articles/dietrich-bonhoeffer)')
