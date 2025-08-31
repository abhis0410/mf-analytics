import json, os, uuid
from typing import List, Dict, Any
from config.settings import SAVED_SIMULATIONS_FILE_PATH, FAV_FILE_PATH, BLACKLIST_FILE_PATH, MY_INVESTMENTS_FILE_PATH


class BaseJSONManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self):
        """Load data from JSON file."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def load_data(self, refresh: bool = False) -> List[Dict[str, Any]]:
        """Load data from JSON file."""
        if refresh:
            self.data = self._load_data()
        return self.data

    def save_data(self, data: List[Dict[str, Any]]) -> None:
        """Save data to JSON file."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def add_item(self, item: Dict[str, Any], unique_key: str = None) -> None:
        """Add a new item, optionally ensuring no duplicates."""
        data = self.load_data(refresh=True)
        if unique_key:
            if not any(d[unique_key] == item[unique_key] for d in data):
                data.append(item)
        else:
            data.append(item)
        self.save_data(data)

    def remove_item(self, key: str, value: str) -> None:
        """Remove an item by key-value match."""
        data = self.load_data(refresh=True)
        data = [d for d in data if d.get(key) != value]
        self.save_data(data)



class BlacklistManager(BaseJSONManager):
    def __init__(self):
        super().__init__(BLACKLIST_FILE_PATH)

    def add_blacklist(self, scheme_code: str, scheme_name: str) -> None:
        FavouritesManager().remove_favourite(scheme_code)  # avoid duplicates
        self.add_item({"scheme_code": scheme_code, "scheme_name": scheme_name}, unique_key="scheme_code")

    def remove_blacklist(self, scheme_code: str) -> None:
        self.remove_item("scheme_code", scheme_code)


class FavouritesManager(BaseJSONManager):
    def __init__(self):
        super().__init__(FAV_FILE_PATH)

    def add_favourite(self, scheme_code: str, scheme_name: str) -> None:
        BlacklistManager().remove_blacklist(scheme_code)
        self.add_item({"scheme_code": scheme_code, "scheme_name": scheme_name}, unique_key="scheme_code")

    def remove_favourite(self, scheme_code: str) -> None:
        self.remove_item("scheme_code", scheme_code)


class SimulationManager(BaseJSONManager):
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


class MyInvestmentsManager(BaseJSONManager):
    def __init__(self):
        super().__init__(MY_INVESTMENTS_FILE_PATH)

    def add_investment(self, investment: Dict[str, str]) -> None:
        if 'investment_id' not in investment:
            investment['investment_id'] = str(uuid.uuid4())
        self.add_item(investment, unique_key="investment_id")

    def remove_investment(self, investment_id: str) -> None:
        self.remove_item("investment_id", investment_id)
