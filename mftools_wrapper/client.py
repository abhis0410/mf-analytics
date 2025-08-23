from mftool import Mftool

class MFClient:
    """Wrapper around Mftool with cleaner methods."""

    def __init__(self):
        self.client = Mftool()

    def get_scheme_codes(self):
        return self.client.get_scheme_codes()

    def get_scheme_details(self, scheme_code):
        return self.client.get_scheme_details(scheme_code)

    def get_scheme_quote(self, scheme_code):
        return self.client.get_scheme_quote(scheme_code)

    def get_historical_nav(self, scheme_code):
        return self.client.get_scheme_historical_nav(scheme_code, as_Dataframe=False)["data"]
