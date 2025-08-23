import streamlit as st
import pandas as pd
import time

import config.constants as CONSTANTS
from utils.data_loader import SimulationManager
from src.mf_simulator import MFSimulator
from src.dip_factor import DipFactorUtils
from src.nav_metrics import compute_nav_metrics
from mftools_wrapper import MFScheme
from streamlit_components.metrics import show_simulation_metrics
from streamlit_components.dataframe import show_dataframe

def show_dip_factor_section(params):

    st.session_state['selected_scheme_code'] = scheme_code = params['scheme_code']
    st.session_state['selected_scheme_name'] = params['scheme_name']
    frequency = params['frequency']
    df = MFScheme(scheme_code=scheme_code).get_nav_data()
    
    st.subheader(f"NAV Metrics")
    st.caption(f"{frequency.title()}")
    lookback_days = [7, 30, 60, 90, 180, 365]
    metrics_df = (
        pd.DataFrame(
            [compute_nav_metrics(
                df=df, 
                lookback_days=days) 
            for days in lookback_days]
        )
    )
    metrics_df.columns = metrics_df.columns.str.replace('_', ' ').str.title()
    show_dataframe(metrics_df)
    
    dip_factor = (
        DipFactorUtils(
        df=df,
        weights=params['weights'],
        drop_threshold_range=params['drop_threshold_range']
        )
        .from_frequency(
            frequency=frequency
        )
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Dip Factor", value=f"{dip_factor:.2f}")
    with col2:
        default_lumpsum = (
            CONSTANTS.LUMPSUM_PER_WEEK if params['frequency'].lower() == 'weekly'
            else CONSTANTS.LUMPSUM_PER_MONTH
        )
        x = st.number_input("Enter your lumpsum balance", value=CONSTANTS.LUMPSUM_PER_WEEK)
    with col3:
        st.metric(label="Possible Investment", value=f"{dip_factor * x:.2f}")

def show_saved_simulations(width):
    sim_manager = SimulationManager()
    saved_sims = sim_manager.load_saved_simulations()

    df_sims = pd.DataFrame(
        saved_sims,
        columns=['id', 'scheme_name', 'description', 'frequency', 'run_time']
    ).rename(columns={
        'id': 'ID',
        'scheme_name': 'Scheme Name',
        'description': 'Description',
        'frequency': 'Frequency',
        'run_time': 'Run Time'
        })
    
    st.dataframe(df_sims, use_container_width=True)
    selected_sim = st.selectbox("Select a Simulation", saved_sims, format_func=lambda x: x.get('id', 'N/A'))
    
    st.subheader("Parameter Details")
    st.json(selected_sim)


    if st.button("Run Simulation"):
        mf_simulator_obj = MFSimulator(nav_df=None, scheme_code=selected_sim['scheme_code'])
        investment_history, final_metrics = mf_simulator_obj.run_simulation_from_params(selected_sim)
        
        st.subheader("Simulation Results")
        show_simulation_metrics(investment_history, final_metrics, mf_simulator_obj)


    if st.button("Delete Simulation"):
        sim_manager.delete_simulation(selected_sim)
        st.success("Simulation deleted successfully.")
        time.sleep(1)
        st.rerun()

    return selected_sim


def main():
    
    # Load saved simulations
    sim_manager = SimulationManager()
    saved_sims = sim_manager.load_saved_simulations()

    if not saved_sims:
        st.info("No saved simulations found. Please save a simulation first.")
        return
    
    params = show_saved_simulations([0.5, 3, 3, 1, 2])
    if params:
        st.divider()
        show_dip_factor_section(params)
    

if __name__ == "__main__":
    st.title("Saved Simulations")
    main()