import streamlit as st
import pandas as pd

from utils.data_loader import MyInvestmentsManager
from streamlit_components.dataframe import show_dataframe
from mftools_wrapper import MFScheme

def func(invest_manager_obj : MyInvestmentsManager):
    all_investments = pd.DataFrame(invest_manager_obj.load_data())
    df = (
        all_investments
        .groupby(["scheme_code", "scheme_name"])
        .agg({
            "amount_invested": "sum",
            "units_bought" : "sum"
        })
        .reset_index()
    )
    show_dataframe(df)

    # ---------------------------------------------
    st.divider()
    st.subheader("Overall Investment Performance")
    all_metrics = {
        "total_invested" : 0,
        "current_value" : 0,
    }
    for index, row in df.iterrows():
        latest_nav = MFScheme(row['scheme_code']).get_details()['current_nav']
        all_metrics['total_invested'] += row['amount_invested']
        all_metrics['current_value'] += row['units_bought'] * latest_nav

    all_metrics['profit'] = all_metrics['current_value'] - all_metrics['total_invested']
    all_metrics['roi'] = (all_metrics['profit'] / all_metrics['total_invested'] * 100) if all_metrics['total_invested'] != 0 else 0

    
    
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(label="💰 Total Invested", value=f"₹{all_metrics['total_invested']:,.2f}")
    col2.metric(label="📈 Current Value", value=f"₹{all_metrics['current_value']:,.2f}")
    col3.metric(label="💸 Profit", value=f"₹{all_metrics['profit']:,.2f}")
    col4.metric(label="📉 ROI", value=f"{all_metrics['roi']:.2f}%")

def main():
    invest_manager = MyInvestmentsManager()



    func(invest_manager)






if __name__ == '__main__':
    main()

