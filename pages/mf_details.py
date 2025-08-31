import streamlit as st
import pandas as pd
from mftools_wrapper import MFScheme
from streamlit_components.line_chart_plotter import LineChartPlotter
from streamlit_components.dataframe import show_dataframe
from streamlit_components.plots import render_nav_chart
from src.nav_metrics import compute_nav_metrics
from streamlit_components.groww_link_manager import GrowwLinkManager
from streamlit_components.buttons import add_both_favourites_and_blacklist_buttons
from config.page_mapping import PAGE_MAPPING


def initial_buttons(scheme_name, scheme_code):
    GrowwLinkManager().add_groww_link(scheme_name=scheme_name)
    add_both_favourites_and_blacklist_buttons(
            scheme_code=scheme_code,
            scheme_name=scheme_name
    )
    if st.button("Run Simulation"):
        st.switch_page(PAGE_MAPPING["SIMULATE_STRATEGY"])



def main():    
    if 'selected_scheme_code' not in st.session_state:
        st.error("Please go to 'All Mutual Funds' and select a scheme first.")
        st.stop()

    scheme_name = st.session_state['selected_scheme_name']
    scheme_code = st.session_state['selected_scheme_code']
    
    st.write(f"{scheme_name} | {scheme_code}")

    mf_scheme_obj = MFScheme(scheme_code=scheme_code)
    df = mf_scheme_obj.get_nav_data()
    initial_buttons(scheme_name, scheme_code)
    
    st.divider()
    # Complete NAV Data
    st.subheader("Complete NAV Data")
    show_dataframe(df)

    st.divider()
    # NAV Plots
    # st.subheader("NAV Plots")
    chart_days = [7, 30, 60, 90, 180, 365]
    tab_labels = [f"Last {days} days" for days in chart_days] + ["Complete NAV Plot"]
    tabs = st.tabs(tab_labels)
    for tab, days in zip(tabs[:-1], chart_days):  # All tabs except last one
        with tab:
            render_nav_chart(
                df=df,
                days=days
            )
    # Last tab for complete NAV plot
    with tabs[-1]:
        st.subheader("Complete NAV Plot")
        line_chart_plotter = LineChartPlotter(df)
        line_chart_plotter.plot(
            value_cols=["Nav"]
        )

    # Drop Metrics
    st.divider()
    st.subheader("Drop Metrics")
    lookback_days = [7, 30, 60, 90, 180, 365]
    metrics_df = (
        pd.DataFrame(
            [compute_nav_metrics(
                df=df, 
                lookback_days=days) 
            for days in lookback_days]
        )
    )
    today_nav = metrics_df["today_nav"][0]
    metrics_df.drop(columns=["today_nav"], inplace=True)
    metrics_df.columns = metrics_df.columns.str.replace('_', ' ').str.title()
    st.markdown(
        f"<p style='text-align:center; color:grey; font-size:20px;'>Today NAV: <b>{today_nav:.2f}</b></p>",
        unsafe_allow_html=True
    )
    show_dataframe(metrics_df)







if __name__ == "__main__":
    main()  