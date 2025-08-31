import streamlit as st
from utils.data_loader import FavouritesManager, BlacklistManager
from config.page_mapping import PAGE_MAPPING

def show_favourites():
    widths = [1, 4.5, 1, 1, 1, 1]

    st.subheader("⭐ My Favourite Schemes")
    favourites_manager_obj = FavouritesManager()
    favs = favourites_manager_obj.load_data()
    st.caption(f"Total favourites: {len(favs)}")
    if not favs:
        st.info("You have no favourites yet. Go to 'All Mutual Funds' to add some.")
        return

    col1, col2, col3, col4, col5, col6 = st.columns(widths)
    col1.markdown("**Scheme Code**")
    col2.markdown("**Scheme Name**")
    col3.markdown("**Remove**")
    col4.markdown("**View Details**")
    col5.markdown("**Add Investment**")
    col6.markdown("**View Investments**")

    for fav in favs:
        col1, col2, col3, col4, col5, col6 = st.columns(widths)

        col1.write(fav["scheme_code"])
        col2.write(fav["scheme_name"])

        if col3.button("❌", key=f"remove_{fav['scheme_code']}"):
            favourites_manager_obj.remove_favourite(fav["scheme_code"])
            st.success(f"Removed {fav['scheme_name']}")
            st.rerun()

        if col4.button("🔍", key=f"view_{fav['scheme_code']}"):
            st.session_state['selected_scheme_name'] = fav['scheme_name']
            st.session_state['selected_scheme_code'] = fav['scheme_code']
            st.switch_page(PAGE_MAPPING["MF_DETAILS"])
        
        
        if col5.button("➕", key=f"add_investments_{fav['scheme_code']}"):
            st.session_state['selected_scheme_name'] = fav['scheme_name']
            st.session_state['selected_scheme_code'] = fav['scheme_code']
            st.switch_page(PAGE_MAPPING["ADD_DELETE_INVESTMENTS"])

        if col6.button("👁️", key=f"view_investment_{fav['scheme_code']}"):
            st.session_state['selected_scheme_name'] = fav['scheme_name']
            st.session_state['selected_scheme_code'] = fav['scheme_code']
            st.switch_page(PAGE_MAPPING["MY_INVESTMENTS"])

    return

def show_blacklist():
    widths = [1.5, 4, 1, 1]
    st.subheader("🚫 My Blacklist Schemes")
    blacklists_manager_obj = BlacklistManager()
    blacklisted = blacklists_manager_obj.load_data()

    st.caption(f"Total Blacklists: {len(blacklisted)}")
    if not blacklisted:
        st.info("You have no blacklisted schemes.")
        return

    col1, col2, col3, col4 = st.columns(widths)
    col1.markdown("**Scheme Code**")
    col2.markdown("**Scheme Name**")
    col3.markdown("**Remove**")
    col4.markdown("**View Details**")

    for scheme in blacklisted:
        col1, col2, col3, col4 = st.columns(widths)
        col1.write(scheme["scheme_code"])
        col2.write(scheme["scheme_name"])

        if col3.button("❌", key=f"remove_{scheme['scheme_code']}"):
            blacklists_manager_obj.remove_blacklist(scheme["scheme_code"])
            st.success(f"Removed {scheme['scheme_name']}")
            st.rerun()

        if col4.button("🔍", key=f"view_{scheme['scheme_code']}"):
            st.session_state['selected_scheme_name'] = scheme['scheme_name']
            st.session_state['selected_scheme_code'] = scheme['scheme_code']
            st.switch_page(PAGE_MAPPING["MF_DETAILS"])

def main():
    st.set_page_config(page_title="Watchlist", page_icon="👀")

    st.divider()
    show_favourites()
    st.divider()
    show_blacklist()
    st.divider()

if __name__ == "__main__":
    main()
