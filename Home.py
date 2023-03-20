import streamlit as st

st.set_page_config(
    page_title="NI Population Analyses",
    page_icon="chart_with_upwards_trend", #page_icon="👋",
    # layout='wide'
)

st.markdown('''# NI Demographic Data Application
''')

st.markdown(
    '''
    This is an online application to support exploratory analyses
    of open datasets relating to births, deaths and other population
    demographics for Northern Ireland specifically around the pandemic period.
    
    **👈 Select an area of interest from the sidebar** to start 
    exploring.
'''
)

st.image('img/bonhoeffer.jpg', use_column_width=True)
st.caption('[Image credit](https://www.insightforliving.ca/read/articles/dietrich-bonhoeffer)')
