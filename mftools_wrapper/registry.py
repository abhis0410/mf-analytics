import pandas as pd
from .client import MFClient

class MFRegistry:
    """Manages all mutual fund schemes metadata."""

    def __init__(self):
        self.client = MFClient()
        self.scheme_codes = self._load_scheme_codes()

    def _load_scheme_codes(self):
        scheme_codes = self.client.get_scheme_codes()
        return (
            pd.DataFrame.from_dict(scheme_codes, orient="index", columns=["Name"])
            .reset_index()
            .rename(columns={"index": "scheme_code", "Name": "scheme_name"})
            .iloc[1:]
        )

    def get_scheme_codes(self):
        return self.scheme_codes
