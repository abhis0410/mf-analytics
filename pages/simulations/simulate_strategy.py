import streamlit as st
import pandas as pd
import uuid
import config.constants as CONSTANTS

from streamlit_components.buttons import add_both_favourites_and_blacklist_buttons
from streamlit_components.metrics import show_simulation_metrics

from src.mf_simulator import MFSimulator
from utils.data_loader import SimulationManager
import random, string


def add_save_simulation_button(params):
    desc = st.text_input("Enter a description for the simulation:")
    if st.button("Save Simulation"):
        params['id'] = str(''.join(random.choices(string.ascii_letters + string.digits, k=8)))
        params['run_time'] = pd.Timestamp.now().strftime("%Y-%m-%d %I:%M:%S %p")
        params['description'] = desc or "No description provided"

        x = SimulationManager()
        x.save_simulation(params)
        st.success("Simulation saved successfully!")

def add_weekly_simulation_tab(simulator_obj: MFSimulator):
    st.header("Weekly Simulation")
    days = list(CONSTANTS.WEEKDAY_MAPPING.values())

    # SIP Parameters
    st.subheader("SIP Parameters")

    weeks = st.slider("Number of weeks to simulate", 4, 400, 150)
    selected = st.select_slider("Select Weekday for Investment", options=days, value="Friday")
    weekday = days.index(selected)
    sip_amount = st.slider("Select SIP Amount per week", 0, 10000, 1000, 100)

    # Lumpsum Parameters
    st.subheader("Lumpsum Parameters")

    carry_forward = st.checkbox("Carry Forward Lumpsum amount", value=False)
    lumpsum = st.slider("Select Lumpsum Investment Amount per Week", 0, 50000, 5000, 1000)
    drop_threshold_range = st.slider("Select Drop Thresholds", 0.0, 10.0, (2.0, 8.0), 0.1)
    weights = {
        "recent_vs_historical": st.slider("Weight Max Drop vs Average Drop", 0.0, 1.0, 0.3, 0.05),
        "peak_vs_average": st.slider("Weight 30-day vs 60-day Drop Factor (0 to 1)", 0.0, 1.0, 0.4, 0.05)
    }

    params = {
        'weeks': weeks,
        'weekday': weekday,
        'sip_amount': sip_amount,
        'carry_forward': carry_forward,
        'invest_amount_per_week': lumpsum,
        "drop_threshold_range": drop_threshold_range,
        "weights" : weights
    }
    st.session_state['params'] = params

    if st.button("Run Simulation"):
        investment_history, final_metrics = simulator_obj.simulate_weekly(
            weights=weights,
            drop_threshold_range = drop_threshold_range,
            lumpsum=lumpsum,
            carry_forward=carry_forward,
            sip_amount=sip_amount,
            weeks=weeks,
            weekday=weekday
        )

        st.divider()
        show_simulation_metrics(investment_history, final_metrics, simulator_obj)
        return params

def add_monthly_simulation_tab(simulator_obj: MFSimulator):
    st.header("Monthly Simulation")

    # SIP Parameters
    st.subheader("SIP Parameters")
    months = st.slider("Number of months to simulate", 1, 200, CONSTANTS.MONTHS)
    date_of_investment = st.slider("Date of Investment", 1, 28, CONSTANTS.DATE_OF_INVESTMENT)
    sip_amount = st.slider("Select SIP Amount per month", 0, 100000, CONSTANTS.SIP_AMOUNT_MONTHLY, 100)

    # Lumpsum Parameters
    st.subheader("Lumpsum Parameters")
    carry_forward = st.checkbox("Carry Forward Lumpsum amount", value=False)
    lumpsum = st.slider("Select Lumpsum Investment Amount per Month", 0, 50000, CONSTANTS.LUMPSUM_PER_MONTH, 1000)
    drop_threshold_range = st.slider("Select Drop Thresholds", 0.0, 10.0, (2.0, 8.0), 0.1)
    weights = {
        "recent_vs_historical": st.slider("Weight Max Drop vs Average Drop", 0.0, 1.0, 0.3, 0.05),
        "peak_vs_average": st.slider("Weight 60-day vs 90-day Drop Factor (0 to 1)", 0.0, 1.0, 0.4, 0.05)
    }

    params = {
        'months': months,
        'date_of_investment': date_of_investment,
        'sip_amount': sip_amount,
        'carry_forward': carry_forward,
        'lumpsum': lumpsum,
        'drop_threshold_range': drop_threshold_range,
        'weights' : weights
    }
    st.session_state['params'] = params

    if st.button("Run Simulation"):
        investment_history, final_metrics = simulator_obj.simulate_monthly(
            weights=weights,
            drop_threshold_range = drop_threshold_range,
            lumpsum=lumpsum,
            carry_forward=carry_forward,
            sip_amount=sip_amount,
            months=months,
            date_of_investment=date_of_investment
        )

        st.divider()
        show_simulation_metrics(investment_history, final_metrics, simulator_obj)
        return params
    
    pass

def main():
    if 'selected_scheme_code' not in st.session_state:
        st.error("Please go to 'All Mutual Funds' and select a scheme first.")
        st.stop()

    scheme_code = st.session_state['selected_scheme_code']
    scheme_name = st.session_state['selected_scheme_name']

    st.write(f"{scheme_name} ({scheme_code})")
    add_both_favourites_and_blacklist_buttons(scheme_code, scheme_name)
    
    # write on/off button for simulate monthly, or simulate weekly
    simulation_frequency = st.radio("Select Simulation Frequency", ("Weekly", "Monthly"), index=0)
    st.divider()
    
    params = {
        **st.session_state.get('params', {}),
        "scheme_code": scheme_code,
        "scheme_name": scheme_name,
        "frequency": simulation_frequency
    }

    mf_simulator_obj = MFSimulator(nav_df=None, scheme_code=scheme_code)
    if simulation_frequency == "Weekly":
        add_weekly_simulation_tab(mf_simulator_obj)
    else:
        add_monthly_simulation_tab(mf_simulator_obj)

    st.divider()
    add_save_simulation_button(params)

if __name__ == "__main__":
    main()
