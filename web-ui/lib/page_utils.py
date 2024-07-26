import streamlit as st
import os



def show_footer_caption(footer_caption):
    st.markdown("---")
    st.caption(footer_caption)


def show_header_and_caption(header, caption):
    st.title(f"{header}")
    st.caption(f"👈 {caption}")


def set_page_config(title, icon="chart_with_upwards_trend", layout="wide"):
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout=layout
    )


def add_bg_from_url(url):
    #"https://images.pexels.com/photos/316466/pexels-photo-316466.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
    st.markdown(
        f"""
         <style>
         .stApp {{
             background-image: url({url}); 
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )

def _is_running_on_streamlit_cloud():
    # Streamlit Cloud sets the environment variable 'STREAMLIT_SERVER'
    return os.getenv('USER') == 'appuser'


def initialize_session_state() -> None:
    """
    Given the multi-module repository we are using, the mount point
    on Streamlit cloud for resources is different to that when run
    locally. This function merely changes the local path prefix for
    resources based on a check if the app is running on the cloud.
    """
    if _is_running_on_streamlit_cloud():
        print("this was cloud")
        st.session_state['parent_resource_path'] = 'web-ui/'
    else:
        print("not cloud")
        st.session_state['parent_resource_path'] = './'