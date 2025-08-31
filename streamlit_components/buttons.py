import streamlit as st
import time
from utils.data_loader import FavouritesManager, BlacklistManager

def add_favourites_button(scheme_code, scheme_name):
    favourite_manager = FavouritesManager()
    favs = favourite_manager.load_data()
    if any(f["scheme_code"] == scheme_code for f in favs):
        if st.button("Remove from Favourites"):
            favourite_manager.remove_favourite(scheme_code)
            st.success(f"Removed {scheme_name}")
            time.sleep(1)
            st.rerun()
    else:
        if st.button("Add to Favourites"):
            favourite_manager.add_favourite(scheme_code, scheme_name)
            st.success(f"Added {scheme_name}")
            time.sleep(1)
            st.rerun()

def add_blacklist_button(scheme_code, scheme_name):
    blacklist_manager = BlacklistManager()
    blacklists = blacklist_manager.load_data()
    if any(b["scheme_code"] == scheme_code for b in blacklists):
        if st.button("Remove from Blacklist"):
            blacklist_manager.remove_blacklist(scheme_code)
            st.success(f"Removed {scheme_name} from Blacklist")
            time.sleep(1)
            st.rerun()
    else:
        if st.button("Add to Blacklist"):
            blacklist_manager.add_blacklist(scheme_code, scheme_name)
            st.success(f"Added {scheme_name} to Blacklist")
            time.sleep(1)
            st.rerun()
            

def add_both_favourites_and_blacklist_buttons(scheme_code, scheme_name):
    col1, col2 = st.columns(2)
    with col1:
        add_favourites_button(scheme_code, scheme_name)
    with col2:
        add_blacklist_button(scheme_code, scheme_name)