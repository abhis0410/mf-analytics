import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def main():
    st.set_page_config(page_title="Mutual Fund Tracker", layout="wide")
    st.title("📊 Mutual Fund Tracker")
    st.write("Welcome! Use the sidebar to navigate between:")
    st.markdown("""
    - **All Mutual Funds** — Browse all schemes available in the market  
    - **Single MF** — Dive into details for a specific scheme
    - **MF Details** — View detailed information about a specific mutual fund
    - **Simulate Strategy** — Test different investment strategies
    - **NAV Analysis** — Analyze the NAV trends and metrics
    """)
 


if __name__ == "__main__":
    main()
