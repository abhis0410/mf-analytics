import pandas as pd
from datetime import datetime
from .client import MFClient

class MFScheme:
    """
    Represents a single mutual fund scheme and provides methods to access its 
    details and NAV (Net Asset Value) data.

    This class handles:
        - Fetching scheme metadata (fund house, type, category, start date, etc.)
        - Retrieving current and historical NAV data
        - Querying NAV on specific dates
        - Optional data preprocessing (adding day, month, year columns)

    Parameters:
        scheme_code (str): Unique identifier for the mutual fund scheme.
        eager (bool, optional): If True (default), fetch scheme details and NAV data on initialization.

    Public Methods:
        get_details() -> dict
            Returns scheme metadata including current NAV.
        get_nav_data() -> pd.DataFrame
            Returns historical NAV data for the scheme.
        get_nav_on_date(date: datetime.date) -> tuple[datetime.date, float] | None
            Returns NAV on or before the given date.
    """



    def __init__(self, scheme_code, eager=True):
        self.client = MFClient()
        self.scheme_code = scheme_code
        self._details = None
        self._df = None
        if eager:
            self._load_details()
            self._load_nav_data()

    def _load_details(self):
        raw = self.client.get_scheme_details(self.scheme_code)
        quote = self.client.get_scheme_quote(self.scheme_code)
        self._details = {
            **raw,
            "scheme_start_date": raw["scheme_start_date"]["date"],
            "scheme_start_nav": raw["scheme_start_date"]["nav"],
            "current_nav": float(quote["nav"]),
            "current_date": pd.to_datetime(quote["last_updated"], format="%d-%b-%Y"),
        }
        return self._details

    def _load_nav_data(self):
        """Return NAV data (historical + latest) for this scheme."""
        df = pd.DataFrame(self.client.get_historical_nav(self.scheme_code))
        df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
        df["nav"] = df["nav"].astype(float)

        if self._details is None:
            self._load_details()
            
        if df["date"].max() != self._details["current_date"]:
            new_row = pd.Series({
                "date": self._details["current_date"],
                "nav": float(self._details["current_nav"])
            })
            df = pd.concat([new_row.to_frame().T, df], ignore_index=True)

        df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
        df = df.assign(
            day=df["date"].dt.day_name(),
            month=df["date"].dt.month_name(),
            year=df["date"].dt.year
        )

        self._df = df
        return df


    # Public API
    def get_details(self, refresh=False):
        """Retrieve scheme details, with optional refresh.

        Returns:
            dict: Dictionary containing scheme details with the following keys:
                - fund_house (str): Fund house managing the scheme.
                - scheme_type (str): Type of the scheme (e.g., Equity, Debt).
                - scheme_category (str): Category within the scheme type.
                - scheme_code (str): Unique identifier for the scheme.
                - scheme_name (str): Full name of the scheme.
                - scheme_start_date (str): Launch date of the scheme.
                - scheme_start_nav (float): NAV at the launch date.
                - current_nav (float): Most recent NAV.
                - current_date (str): Date corresponding to the most recent NAV.
        """

        if refresh or self._details is None:
            self._load_details()
        return self._details

    def get_nav_data(self, refresh=False):
        """Retrieve NAV data for the scheme, with optional refresh.

        Returns:
            pd.DataFrame: DataFrame containing NAV history with the following columns:
                - date (datetime): Date of the NAV.
                - nav (float): Net Asset Value on the given date.
                - day (str): Day of the week for the date.
                - month (str): Month name for the date.
                - year (int): Year of the date.
        """

        if refresh or self._df is None:
            self._load_nav_data()
        return self._df

    def get_nav_on_date(self, date: pd.Timestamp):
        """Get NAV on or before a specific date.

        Args:
            date (datetime.date | pd.Timestamp): Target date.

        Returns:
            tuple[datetime.date, float] | None: 
                - (date, nav) if data is available (most recent date <= target).
                - None if no NAV data exists before the given date.
        """
        df = self.get_nav_data()
        date = pd.to_datetime(date)
        
        df_filtered = df[df["date"] <= date]
        if df_filtered.empty:
            return None

        # Get the most recent NAV before or on the target date
        row = df_filtered.sort_values("date", ascending=False).iloc[0]
        return row["date"], row["nav"]

