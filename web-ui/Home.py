"""
Landing page for application.
"""
import os
import streamlit as st
from lib.page_utils import *

st.set_page_config(
    page_title="Pandemic Period Data",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)


def _debug(msg: str):
    print("============================================================")
    print(msg)
    print("============================================================")
    print(os.getenv("STREAMLIT_SERVER"))
    print("============================================================")





def main():
    """
    Driver.
    :return: None.
    """
    # _debug("Before assignment")
    # _initialize_session_state()

    print(st.session_state['parent_resource_path'])
    st.markdown(
        """# NI Pandemic Period Insights
    """
    )
    st.caption("👈 Select an area of interest from the sidebar to start exploring.")

    st.markdown(
        """
        This [data application](https://acho.io/blogs/what-is-a-data-application) 
        supports exploratory analyses of population and demographic datasets pertaining 
        to the  COVID-19 pandemic response period in Northern Ireland (NI).
        
        Analyses include births, deaths, disabilities, countermeasures and their interrelationships.
    """
    )

    st.image(f"{st.session_state['parent_resource_path']}resources/img/bonhoeffer.jpg", use_column_width=True)
    st.caption(
        "[Image credit](https://www.insightforliving.ca/read/articles/dietrich-bonhoeffer)"
    )


if __name__ == "__main__":
    initialize_session_state()
    main()
