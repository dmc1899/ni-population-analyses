import streamlit as st

st.set_page_config(
    page_title="NI Population Analyses",
    page_icon="chart_with_upwards_trend", #page_icon="👋",
    # layout='wide'
)


def add_bg_from_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background-image: url("img/a-book-gcb51cc40a_1920.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )

add_bg_from_url()
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
