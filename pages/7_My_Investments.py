from datetime import datetime, timedelta
import streamlit as st
from utils.data_loader import MyInvestmentsManager
from src.mftools_wrapper import MFScheme
import pandas as pd
from src.streamlit_utils import add_groww_link
from streamlit_components.line_chart_plotter import LineChartPlotter


def investment_details(scheme_code, scheme_name, enhance = True, invest_manager=None):
    if invest_manager is None:
        invest_manager = MyInvestmentsManager()

    all_investments = pd.DataFrame(invest_manager.load_investments())
    df_investment = all_investments[(all_investments['scheme_code'] == scheme_code) & (all_investments['scheme_name'] == scheme_name)]
    df_investment = (
        df_investment
        .drop(columns=['scheme_code', 'scheme_name'])
        .reset_index(drop=True)
    )
    if enhance:
        df_investment.columns = df_investment.columns.str.replace('_', ' ').str.title()

    return df_investment


def show_individual_investments(scheme_number=None, scheme_name=None, invest_manager=None):
    
    if scheme_number is None and scheme_name is None:
        if 'selected_scheme_code' not in st.session_state:  
            st.info("Please select a scheme first.")
            return
        
        scheme_number = st.session_state['selected_scheme_code']
        scheme_name = st.session_state['selected_scheme_name']

    st.write(f"{scheme_name} ({scheme_number})")

    df_investment = investment_details(scheme_number, scheme_name, True, invest_manager=invest_manager)
    if df_investment is None or df_investment.empty:
        st.info("No investments found for this scheme.")
        return
    
    st.dataframe(df_investment, use_container_width=True)
    df_investment.rename(columns={"Date Of Transaction": "Date", "Nav": "NAV"}, inplace=True)
    line_chart_plotter = LineChartPlotter(df_investment)
    line_chart_plotter.plot(
        value_cols=["Amount Invested"]
    )

    return

def show_all_investments(index):
    st.subheader(f"{index}. All Investments")
    index += 1

    invest_manager = MyInvestmentsManager()
    all_investments = pd.DataFrame(invest_manager.load_investments())

    if all_investments.empty:
        st.info("No investments found.")
        return

    all_scheme_number = all_investments['scheme_code'].unique()
    all_scheme_name = all_investments['scheme_name'].unique()

    for i in range(len(all_scheme_name)):
        scheme_number = all_scheme_number[i]
        scheme_name = all_scheme_name[i]
        show_individual_investments(scheme_number=scheme_number, scheme_name=scheme_name, invest_manager=invest_manager)
        st.divider()
    
    pass


def main():
    index = 1
    st.title("📈 My Investments")

    # Show the investment view
    if st.radio("Select Investment View", ("Individual", "All")) == "Individual":
        show_individual_investments()
    else:
        show_all_investments(index)
    
    index += 1


if __name__ == "__main__":
    main()