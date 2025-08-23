import pandas as pd
import streamlit as st

def show_dataframe(df: pd.DataFrame, transpose = False):
    """Display a styled DataFrame in Streamlit."""
    df = df.copy()
    df.columns = [col.replace("_", " ").title() for col in df.columns]

    if transpose:
        df = df.T
    st.dataframe(df)
    st.caption(f"Total Values: {len(df)}")
