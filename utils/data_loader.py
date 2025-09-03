import uuid
from config.settings import SAVED_SIMULATIONS_FILE_PATH, FAV_FILE_PATH, BLACKLIST_FILE_PATH, MY_INVESTMENTS_FILE_PATH

from typing import List, Dict, Any
import streamlit as st  # Only needed if using Streamlit secrets
from .gcs_client import GCSClient

class GCSJSONManager(GCSClient):
    """
    Child class of GCSClient with added add_item and remove_item functionality.
    """
    BUCKET_NAME = "mf-storage"  # Hardcoded bucket name

    def __init__(self, file_name: str):
        super().__init__(bucket_name=self.BUCKET_NAME, file_name=file_name)

    def add_item(self, item: Dict[str, Any], unique_key: str = None) -> None:
        """Add a new item, optionally ensuring no duplicates."""
        data = self.load_data()
        if unique_key:
            if not any(d.get(unique_key) == item.get(unique_key) for d in data):
                data.append(item)
        else:
            data.append(item)
        self.save_data(data)

    def remove_item(self, key: str, value: str) -> None:
        """Remove an item by key-value match."""
        data = self.load_data()
        data = [d for d in data if d.get(key) != value]
        self.save_data(data)




class BlacklistManager(GCSJSONManager):
    def __init__(self):
        super().__init__(BLACKLIST_FILE_PATH)

    def add_blacklist(self, scheme_code: str, scheme_name: str) -> None:
        FavouritesManager().remove_favourite(scheme_code)  # avoid duplicates
        self.add_item({"scheme_code": scheme_code, "scheme_name": scheme_name}, unique_key="scheme_code")

    def remove_blacklist(self, scheme_code: str) -> None:
        self.remove_item("scheme_code", scheme_code)


class FavouritesManager(GCSJSONManager):
    def __init__(self):
        super().__init__(FAV_FILE_PATH)

    def add_favourite(self, scheme_code: str, scheme_name: str) -> None:
        BlacklistManager().remove_blacklist(scheme_code)
        self.add_item({"scheme_code": scheme_code, "scheme_name": scheme_name}, unique_key="scheme_code")

    def remove_favourite(self, scheme_code: str) -> None:
        self.remove_item("scheme_code", scheme_code)


class SimulationManager(GCSJSONManager):
    def __init__(self):
        super().__init__(SAVED_SIMULATIONS_FILE_PATH)

    def save_simulation(self, params: Dict):
        params = {k.replace(" ", "_").lower(): v for k, v in params.items()}
        data = self.load_data()
        existing = next((sim for sim in data if sim['id'] == params['id']), None)
        if existing:
            existing.update(params)
        else:
            data.append(params)
        self.save_data(data)

    def delete_simulation(self, sim_id: str):
        self.remove_item("id", sim_id)


class MyInvestmentsManager(GCSJSONManager):
    def __init__(self):
        super().__init__(MY_INVESTMENTS_FILE_PATH)

    def add_investment(self, investment: Dict[str, str]) -> None:
        if 'investment_id' not in investment:
            investment['investment_id'] = str(uuid.uuid4())
        self.add_item(investment, unique_key="investment_id")

    def remove_investment(self, investment_id: str) -> None:
        self.remove_item("investment_id", investment_id)
