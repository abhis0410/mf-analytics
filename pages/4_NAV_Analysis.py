import streamlit as st
import pandas as pd
from mftools_wrapper import MFScheme
from streamlit_components.line_chart_plotter import LineChartPlotter
from streamlit_components.dataframe import show_dataframe
from streamlit_components.plots import render_nav_chart

def load_data(scheme_code: str) -> pd.DataFrame:
    mf_scheme = MFScheme(scheme_code)
    return mf_scheme.df


def main():
    st.title("📌 NAV Analysis for DIP Tracking")    
    if 'selected_scheme_code' not in st.session_state:
        st.error("Please go to 'All Mutual Funds' and select a scheme first.")
        st.stop()

    scheme_name = st.session_state['selected_scheme_name']
    scheme_code = st.session_state['selected_scheme_code']
    
    st.write(f"{scheme_name} | {scheme_code}")

    mf_scheme_obj = MFScheme(scheme_code=scheme_code)
    df = mf_scheme_obj.get_nav_data()

    # Complete NAV Data
    st.write("### 1. Complete NAV Data")
    show_dataframe(df)

    # Nav Plots
    chart_days = [7, 30, 60, 90, 180, 365]
    for i, days in enumerate(chart_days):
        render_nav_chart(
            df=df, 
            section_index=i+2, 
            days=days
    )

    # Complete Nav Plot
    st.write(f"### 8. Complete NAV Plot")
    line_chart_plotter = LineChartPlotter(df)
    line_chart_plotter.plot(
        value_cols=["Nav"]
    )


if __name__ == "__main__":
    main()  