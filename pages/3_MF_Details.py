import streamlit as st
import pandas as pd
from datetime import datetime
import config.constants as CONSTANTS

from mftools_wrapper import MFScheme
from streamlit_components.groww_link_manager import GrowwLinkManager
from streamlit_components.buttons import add_both_favourites_and_blacklist_buttons
from streamlit_components.dataframe import show_dataframe
from streamlit_components.plots import render_nav_chart
from config.page_mapping import PAGE_MAPPING

from src.nav_metrics import compute_nav_metrics

# from src.mftools_wrapper import MFScheme
# from src.ui_helpers import show_dataframe
# from archive.helpers import get_dip_factor, compute_for_last_days
# from src.streamlit_utils import add_groww_link, show_nav_plot_for_last_days

# from src.streamlit_utils import add_both_favourites_and_blacklist_buttons



def main():
    """Streamlit app to display single MF scheme details."""
    
    # Validate navigation
    if 'selected_scheme_code' not in st.session_state:
        st.error("Please go to 'All Mutual Funds' and select a scheme first.")
        st.stop()
    st.subheader(f"Historical NAV")

    scheme_code = st.session_state['selected_scheme_code']
    scheme_name = st.session_state['selected_scheme_name']
    st.write(f"{scheme_name} | {scheme_code}")
    
    GrowwLinkManager().add_groww_link(scheme_name=scheme_name)

    mf_scheme_obj = MFScheme(scheme_code=scheme_code)
    nav_df = mf_scheme_obj.get_nav_data()
    
    add_both_favourites_and_blacklist_buttons(
            scheme_code=scheme_code,
            scheme_name=scheme_name
    )
    
    if st.button("Run Simulation"):
        st.switch_page(PAGE_MAPPING["SIMULATE_STRATEGY"])


    st.divider()

    # Full NAV Dataframe
    st.write("### 1. Full NAV Data")
    show_dataframe(nav_df)
    
    # 60 Days Nav plot
    render_nav_chart(
        df=nav_df,
        section_index=2,
        days=60
    )
    if st.button("View Complete NAV Analysis"):
        st.switch_page(PAGE_MAPPING["NAV_ANALYSIS"])


    # Compute NAV metrics
    st.write("### 3. NAV Metrics")
    lookback_days = [7, 30, 60, 90, 180, 365]
    metrics_df = (
        pd.DataFrame(
            [compute_nav_metrics(
                df=nav_df, 
                lookback_days=days) 
            for days in lookback_days]
        )
    )
    metrics_df.columns = metrics_df.columns.str.replace('_', ' ').str.title()
    show_dataframe(metrics_df)



if __name__ == "__main__":
    st.title("📌 Single MF Details")
    
    main()
