import streamlit as st

st.set_page_config(
    page_title="NI Population Analyses",
    page_icon="chart_with_upwards_trend", #page_icon="👋",
    #layout='wide'
)


def add_bg_from_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background-image: url("https://images.pexels.com/photos/316466/pexels-photo-316466.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )

#add_bg_from_url()
st.markdown('''# Covidera Demographics for Northern Ireland
''')
st.caption('👈 Select an area of interest from the sidebar to start exploring.')

st.markdown(
    '''
    This [data application](https://acho.io/blogs/what-is-a-data-application) provides exploratory analyses of 
    open demographic datasets for Northern Ireland specifically in and around the COVID-19 pandemic and pandemic 
    response period (AKA the Covidera).
    
    Analyses includes births, deaths, countermeasures and the interrelationship between them.
'''
)

st.image('img/bonhoeffer.jpg', use_column_width=True)
st.caption('[Image credit](https://www.insightforliving.ca/read/articles/dietrich-bonhoeffer)')
