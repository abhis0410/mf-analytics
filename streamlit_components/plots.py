import streamlit as st
import pandas as pd
from datetime import datetime
from .line_chart_plotter import LineChartPlotter

def render_nav_chart(df: pd.DataFrame, section_index: int, days: int) -> None:
    """
    Render a NAV line chart for the last `days` days.

    Args:
        df (pd.DataFrame): DataFrame containing at least ['Date', 'NAV'].
        section_index (int): Section number for ordering in Streamlit layout.
        days (int): Number of trailing days to display.
    """
    df = df.copy()
    df.columns = df.columns.str.replace('_', ' ').str.title()

    start_date = max(
        (datetime.today() - pd.DateOffset(days=days)),
        pd.to_datetime(df["Date"]).min()
    ).strftime("%Y-%m-%d")
    
    end_date = datetime.today().strftime("%Y-%m-%d")

    st.subheader(f"{section_index}. NAV Trend (last {days} days)")
    LineChartPlotter(df).plot(
        value_cols=["Nav"],
        start_date=start_date,
        end_date=end_date,
    )
