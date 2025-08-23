from datetime import datetime, timedelta
import streamlit as st
from utils.data_loader import MyInvestmentsManager
from src.mftools_wrapper import MFScheme
import pandas as pd
from src.streamlit_utils import add_groww_link
from src.ui_helpers import show_dataframe

def show_delete_investment_tab():
    invest_manager = MyInvestmentsManager()
    all_investments = pd.DataFrame(invest_manager.load_investments())
    st.subheader("Delete Investment")
    if all_investments.empty:
        st.write("No investments found.")
        return

    show_dataframe(all_investments)

    investment_to_delete = st.selectbox("Select Investment to Delete", options=all_investments["investment_id"])
    if st.button("Delete Investment"):
        invest_manager.remove_investment(investment_to_delete)
        st.success("Investment deleted successfully!")


def show_add_investement_tab():
    st.subheader(f"Add New Investment")

    if 'selected_scheme_code' not in st.session_state:
        st.info("Please select a scheme first.")

    st.write(f"{st.session_state['selected_scheme_name']} | {st.session_state['selected_scheme_code']}")
    add_groww_link(st.session_state['selected_scheme_name'])

    mf_scheme = MFScheme(st.session_state['selected_scheme_code'])
    default_date = datetime.now().date() - timedelta(days=1)

    amount_invested = st.number_input("Amount Invested", min_value=0.0)
    date_of_transaction = st.date_input("Date of Transaction", value=default_date)
    nav_date = st.date_input("NAV Date", value=default_date)

    nav_actual_date, nav = mf_scheme.get_nav_on_date(nav_date, must_find=True)
    units_bought = round(amount_invested / nav if nav > 0 else 0.0 , 3)

    if nav_date != nav_actual_date:
        st.warning(f"Selected NAV date {nav_date} does not match actual NAV date {nav_actual_date}. Using actual NAV date for calculations.")

    col1, col2 = st.columns(2)
    col1.metric(label=f"📅 NAV as on {nav_actual_date}", value=f"₹{nav:,.4f}")
    col2.metric(label="Units Bought", value=units_bought)
    
    investment_params = {
        "scheme_code": st.session_state['selected_scheme_code'],
        "scheme_name": st.session_state['selected_scheme_name'],

        "amount_invested": amount_invested,
        "nav": nav,
        "nav_date": nav_actual_date.strftime("%Y-%m-%d"),
        "date_of_transaction": date_of_transaction.strftime("%Y-%m-%d"),
    }

    if st.button("Add Investment"):
        # Code to add the investment goes here
        x = MyInvestmentsManager()
        x.add_investment(investment_params)
        st.success("Investment added successfully!")


def main():
    st.set_page_config(page_title="Add or Delete Investment", layout="wide")
    st.title("📈 Add Investment Detail")


    add_or_delete = st.radio("Choose an action:", ["Add Investment", "Delete Investment"], index=0)
    st.divider()
    if add_or_delete == "Delete Investment":
        show_delete_investment_tab()
    
    else:
        show_add_investement_tab()


if __name__ == "__main__":
    main()