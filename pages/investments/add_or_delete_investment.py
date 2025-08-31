import time
import streamlit as st
from utils.data_loader import MyInvestmentsManager
from mftools_wrapper import MFScheme
import pandas as pd
from streamlit_components.groww_link_manager import GrowwLinkManager
from streamlit_components.dataframe import show_dataframe

def show_delete_investment_tab():
    invest_manager = MyInvestmentsManager()
    all_investments = pd.DataFrame(invest_manager.load_data())
    st.subheader("Delete Investment")
    if all_investments.empty:
        st.write("No investments found.")
        return

    show_dataframe(all_investments)

    investment_to_delete = st.selectbox("Select Investment to Delete", options=all_investments["investment_id"])
    if st.button("Delete Investment"):
        invest_manager.remove_investment(investment_to_delete)
        st.success("Investment deleted successfully!")
        time.sleep(1)
        st.rerun()


def show_add_investment_tab():
    st.subheader(f"Add New Investment")

    if 'selected_scheme_code' not in st.session_state:
        st.info("Please select a scheme first.")
        return

    scheme_name = st.session_state['selected_scheme_name']
    scheme_code = st.session_state['selected_scheme_code']
    
    st.write(f"{scheme_name} | {scheme_code}")
    GrowwLinkManager().add_groww_link(scheme_name=scheme_name)

    mf_scheme_obj = MFScheme(scheme_code=scheme_code)
    default_date = mf_scheme_obj.get_details()["current_date"]

    col1, col2 = st.columns(2)
    with col1:
        amount_invested = st.number_input("Amount Invested",None, None, 0, 500)
        broker_tax = st.number_input("Brokerage Tax (%) /100", 0.0, 5.0, 0.5, 0.5) / 100
    with col2:
        date_of_transaction = st.date_input("Date of Transaction", value=default_date)
        nav_date = st.date_input("NAV Date", value=default_date)

    nav_actual_date, nav = mf_scheme_obj.get_nav_on_date(nav_date)
    actual_invested = amount_invested * (100-broker_tax)/100
    units_bought = round(actual_invested / nav if nav > 0 else 0.0 , 3)

    if nav_date != nav_actual_date:
        st.warning(f"Selected NAV date {nav_date} does not match actual NAV date {nav_actual_date}. Using actual NAV date for calculations.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="💰 Amount Invested", value=f"₹{amount_invested:,}")
    col2.metric(label="📉 Actual Invested", value=f"₹{actual_invested:,.4f}")
    col3.metric(label=f"📅 NAV as on {nav_actual_date}", value=f"₹{nav:,.4f}")
    col4.metric(label="Units Bought", value=units_bought)
    
    investment_params = {
        "scheme_code": scheme_code,
        "scheme_name": scheme_name,
        "amount_invested": amount_invested,
        "units_bought": units_bought,
        "nav": nav,
        "nav_date": nav_actual_date.strftime("%Y-%m-%d"),
        "date_of_transaction": date_of_transaction.strftime("%Y-%m-%d"),
    }

    if st.button("Add Investment"):
        x = MyInvestmentsManager()
        x.add_investment(investment_params)
        st.success("Investment added successfully!")


def main():
    add_or_delete = st.radio("Choose an action:", ["Add Investment", "Delete Investment"], index=0)
    st.divider()
    if add_or_delete == "Delete Investment":
        show_delete_investment_tab()
    else:
        show_add_investment_tab()


if __name__ == "__main__":
    main()