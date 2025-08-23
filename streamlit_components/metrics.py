import streamlit as st  
from streamlit_components.line_chart_plotter import LineChartPlotter
from streamlit_components.dataframe import show_dataframe
from mftools_wrapper import MFScheme
from src.mf_simulator import MFSimulator
import pandas as pd


def show_simulation_metrics(
        investment_history: pd.DataFrame, 
        final_metrics: dict,
        simulator_obj: MFSimulator):
    # Showing Final Metrics 
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(label="💰 Total Invested", value=f"₹{final_metrics['total_invested']:,.2f}")
    col2.metric(label="📈 Current Value", value=f"₹{final_metrics['final_value']:,.2f}")
    col3.metric(label="💸 Profit", value=f"₹{final_metrics['profit']:,.2f}")
    col4.metric(label="📉 ROI", value=f"{final_metrics['roi']:.2f}%")

    col1.metric(label="📊 XIRR", value=f"{final_metrics['xirr']:.2f}%")
    col2.metric(label="📦 Total Units", value=f"{final_metrics['total_units']:,.2f}")
    col3.metric(label="📅 Latest NAV", value=f"₹{final_metrics['latest_nav']:,.2f}")

    # Detailed Simulation Data
    st.subheader("Detailed Simulation Data")
    show_dataframe(investment_history)

    # Plots
    line_chart_plotter = LineChartPlotter(investment_history)

    st.subheader("Investment Strategy Simulation")
    line_chart_plotter.plot(
        value_cols=["total_investment"]
    )

    st.subheader("Corresponding NAV Chart")
    line_chart_plotter.plot(
        value_cols=["nav"]
    )

    st.subheader("Daily Nav Chart")
    start_date = pd.to_datetime(investment_history['date'].min())
    end_date = pd.to_datetime(investment_history['date'].max())
    LineChartPlotter(simulator_obj.nav_df).plot(
        value_cols=['nav'],
        start_date=start_date,
        end_date=end_date
    )

def display_scheme_details(scheme_code):
    scheme_obj = MFScheme(scheme_code)
    scheme_details = scheme_obj.get_details()
    scheme_details_df = pd.DataFrame([scheme_details])

    st.write(f"### Scheme Details ")
    show_dataframe(
        df=scheme_details_df,
        transpose=True
    )