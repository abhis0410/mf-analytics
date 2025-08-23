import os
import json
from googlesearch import search
import streamlit as st


class GrowwLinkManager:
    def __init__(self, cache_file="data/groww_links.json"):
        self.cache_file = cache_file
        self._cache = self._load_cache()   # private cache

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self._cache, f, ensure_ascii=False, indent=2)

    def _find_groww_link(self, scheme_name: str) -> str:
        # First check cache
        if scheme_name in self._cache:
            return self._cache[scheme_name]

        # Otherwise search via Google
        query = f'site:groww.in/mutual-funds "{scheme_name}"'
        try:
            for url in search(query, num_results=5):
                if "groww.in/mutual-funds" in url:
                    self._cache[scheme_name] = url
                    self._save_cache()
                    return url
        except Exception as e:
            st.write(f"Search error: {e}")

        # Cache the miss as None
        self._cache[scheme_name] = None
        self._save_cache()
        return None

    def add_groww_link(self, scheme_name: str):
        """Public method — adds a Groww link to the Streamlit UI."""
        try:
            link = self._find_groww_link(scheme_name)
            if link:
                st.markdown(f"[Groww Link]({link})")
            else:
                st.write("No Groww link found.")
        except Exception as e:
            st.write(f"Error finding Groww link: {e}")
