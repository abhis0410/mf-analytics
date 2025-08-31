import streamlit as st
import pandas as pd
from datetime import datetime
from .line_chart_plotter import LineChartPlotter
from typing import Optional

def render_nav_chart(df: pd.DataFrame, days: int, section_index: Optional[int] = None) -> None:
    """
    Render a NAV line chart for the last `days` days.

    Args:
        df (pd.DataFrame): DataFrame containing at least ['Date', 'NAV'].
        days (int): Number of trailing days to display.
        section_index (int, optional): Section number for ordering in Streamlit layout.
                                       If None, no numbering is shown.
    """
    df = df.copy()
    df.columns = df.columns.str.replace('_', ' ').str.title()

    start_date = max(
        (datetime.today() - pd.DateOffset(days=days)),
        pd.to_datetime(df["Date"]).min()
    ).strftime("%Y-%m-%d")
    
    end_date = datetime.today().strftime("%Y-%m-%d")

    # Show section index only if provided
    title = f"{section_index}. NAV Trend (last {days} days)" if section_index is not None else f"NAV Trend (last {days} days)"
    st.subheader(title)

    LineChartPlotter(df).plot(
        value_cols=["Nav"],
        start_date=start_date,
        end_date=end_date,
    )

