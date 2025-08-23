import streamlit as st
import pandas as pd

from mftools_wrapper import MFRegistry
from utils.data_loader import FavouritesManager, BlacklistManager
from streamlit_components.selectbox import categorized_selectbox
from streamlit_components.metrics import display_scheme_details
from streamlit_components.groww_link_manager import GrowwLinkManager
from streamlit_components.buttons import add_both_favourites_and_blacklist_buttons

from config.page_mapping import PAGE_MAPPING




def main():
    """Streamlit app to display all mutual funds.""" 
    
    mf_registry_obj = MFRegistry()
    all_scheme_codes = (
        pd.DataFrame(mf_registry_obj.get_scheme_codes())
    )
    
    favourites_manager_obj = FavouritesManager()
    favourites_df = pd.DataFrame(favourites_manager_obj.load_favourites())
    favourites = favourites_df['scheme_name'].tolist() if not favourites_df.empty else []


    blacklist_manager_obj = BlacklistManager()
    blacklists_df = pd.DataFrame(blacklist_manager_obj.load_blacklists())
    blacklists = blacklists_df['scheme_name'].tolist() if not blacklists_df.empty else []


    selected_scheme_name= categorized_selectbox(
        label="Select a Mutual Fund Scheme:",
        options=all_scheme_codes['scheme_name'].tolist(),
        highlight=favourites,
        deprioritize=blacklists
    )
    # st.info(f"Selected scheme: {selected_scheme_name}")

    if selected_scheme_name:
        scheme_code = all_scheme_codes[all_scheme_codes['scheme_name'] == selected_scheme_name]['scheme_code'].values[0]
        
        st.session_state['selected_scheme_name'] = selected_scheme_name
        st.session_state['selected_scheme_code'] = scheme_code
        
        display_scheme_details(scheme_code)
        
        GrowwLinkManager().add_groww_link(scheme_name=selected_scheme_name)
        

        if st.button("View Details"):
            st.switch_page(PAGE_MAPPING["MF_DETAILS"])
        
        add_both_favourites_and_blacklist_buttons(
            scheme_code=scheme_code,
            scheme_name=selected_scheme_name
        )



if __name__ == "__main__":
    st.set_page_config(page_title="All Mutual Funds", layout="wide")
    st.title("📈 All Mutual Funds")
    
    main()
