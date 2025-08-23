import json, os, uuid
from typing import List, Dict
from config.settings import SAVED_SIMULATIONS_FILE_PATH, FAV_FILE_PATH, BLACKLIST_FILE_PATH, MY_INVESTMENTS_FILE_PATH


class BlacklistManager:
    def __init__(self):
        self.file_path = BLACKLIST_FILE_PATH
    
    def load_blacklists(self) -> List[Dict[str, str]]:
        """Load blacklists from JSON file."""
        if os.path.exists(BLACKLIST_FILE_PATH):
            with open(BLACKLIST_FILE_PATH, "r") as f:
                try:
                    return json.load(f) 
                except json.JSONDecodeError:
                    return []
        return []

    def save_blacklists(self, blacks: List[Dict[str, str]]) -> None:
        """Save blacklists list to JSON file."""
        os.makedirs(os.path.dirname(BLACKLIST_FILE_PATH), exist_ok=True)
        with open(BLACKLIST_FILE_PATH, "w") as f:
            json.dump(blacks, f, indent=4)

    def add_blacklist(self, scheme_code: str, scheme_name: str) -> None:
        """Add a scheme to blacklists (no duplicates)."""
        FavouritesManager().remove_favourite(scheme_code)

        blacks = self.load_blacklists()
        if not any(f["scheme_code"] == scheme_code for f in blacks):
            blacks.append({"scheme_code": scheme_code, "scheme_name": scheme_name})
            self.save_blacklists(blacks)

    def remove_blacklist(self,scheme_code: str) -> None:
        """Remove a scheme from blacklists by scheme_code."""
        blacks = self.load_blacklists()
        blacks = [f for f in blacks if f["scheme_code"] != scheme_code]
        self.save_blacklists(blacks)

class FavouritesManager:
    def __init__(self):
        self.file_path = FAV_FILE_PATH

    def load_favourites(self) -> List[Dict[str, str]]:
        """Load favourites from JSON file."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def save_favourites(self, favs: List[Dict[str, str]]) -> None:
        """Save favourites list to JSON file."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w") as f:
            json.dump(favs, f, indent=4)

    def add_favourite(self, scheme_code: str, scheme_name: str) -> None:
        """Add a scheme to favourites (no duplicates)."""
        BlacklistManager().remove_blacklist(scheme_code)
        favs = self.load_favourites()
        if not any(f["scheme_code"] == scheme_code for f in favs):
            favs.append({"scheme_code": scheme_code, "scheme_name": scheme_name})
            self.save_favourites(favs)

    def remove_favourite(self, scheme_code: str) -> None:
        """Remove a scheme from favourites by scheme_code."""
        favs = self.load_favourites()
        favs = [f for f in favs if f["scheme_code"] != scheme_code]
        self.save_favourites(favs)

class SimulationManager:
    def __init__(self):
        self.file_path = SAVED_SIMULATIONS_FILE_PATH

    def load_saved_simulations(self) -> List[Dict]:
        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, "r") as f:
            return json.load(f)

    def save_simulation(self, params: Dict):
        saved_simulations = self.load_saved_simulations()

        params = {k.replace(" ", "_").lower(): v for k, v in params.items()}

        saved_sim = next((sim for sim in saved_simulations if sim['id'] == params['id']), None)
        if saved_sim:
            saved_sim.update(params)
        else:
            saved_simulations.append(params)

        with open(self.file_path, "w") as f:
            json.dump(saved_simulations, f, indent=4)

    def delete_simulation(self, params: Dict):
        saved_simulations = self.load_saved_simulations()
        saved_simulations.remove(params)

        with open(self.file_path, "w") as f:
            json.dump(saved_simulations, f)

class MyInvestmentsManager:
    def __init__(self):
        self.file_path = MY_INVESTMENTS_FILE_PATH

    def load_investments(self) -> List[Dict[str, str]]:
        """Load investments from JSON file."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def save_investments(self, investments: List[Dict[str, str]]) -> None:
        """Save investments list to JSON file."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w") as f:
            json.dump(investments, f, indent=4)

    def add_investment(self, investment: Dict[str, str]) -> None:
        """Add a new investment."""
        investments = self.load_investments()
        if 'investment_id' not in investment.keys():
            investment['investment_id'] = str(uuid.uuid4())
        investments.append(investment)
        self.save_investments(investments)

    def remove_investment(self, investment_id: str) -> None:
        """Remove an investment from investments by investment_id."""
        investments = self.load_investments()
        investments = [f for f in investments if f["investment_id"] != investment_id]
        self.save_investments(investments)