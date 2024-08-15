"""
About page.
"""
from lib.page_utils import *


def main():
    """
    Driver.
    :return: None.
    """
    # _debug("Before assignment")
    # _initialize_session_state()

    print(st.session_state['parent_resource_path'])
    st.markdown(
        """# About
    """
    )

    st.markdown(
        """
        This [data application](https://acho.io/blogs/what-is-a-data-application) 
        enables exploratory analyses of population and demographic datasets pertaining 
        to the  COVID-19 pandemic response period in Northern Ireland (NI).
        
        Analyses include births, deaths, disabilities, countermeasures and their interrelationships.
        
        If you identify any miscalculations or other errata, please <a href="mailto:dmc1899@gmail.com">let us know</a>  and we will remediate appropriately. 
    """, unsafe_allow_html=True
    )


if __name__ == "__main__":
    initialize_session_state()
    main()
