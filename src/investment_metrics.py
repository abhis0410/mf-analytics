from src.mf_simulator import MFSimulator
from datetime import datetime
from mftools_wrapper import MFScheme
import pandas as pd

def merge_investment_with_nav(investment_df, scheme_code):
    """
    Merges the user's investment data with the historical NAV data of a mutual fund scheme.

    This function:
    - Takes the investment transactions for a given scheme.
    - Fetches the scheme's NAV history starting from 30 days before the first investment date.
    - Merges both datasets on the date, ensuring days without investments show zero amount invested.

    Args:
        investment_df (pd.DataFrame): DataFrame with columns ['nav_date', 'total_invested'] for user investments.
        scheme_code (str): The unique identifier for the mutual fund scheme.

    Returns:
        pd.DataFrame: Merged DataFrame with columns ['date', 'nav', 'amount_invested'].
                      'amount_invested' will be 0 for dates with no investments.
    """
    investment_df = (
        investment_df[['nav_date', 'amount_invested']]
        .rename(columns={'nav_date': 'date'})
        .assign(date=lambda df: pd.to_datetime(df['date'], format='%Y-%m-%d'))
    )

    start_date = investment_df['date'].min() - pd.Timedelta(days=30)

    mf_scheme_obj = MFScheme(scheme_code)
    nav_df = (
        mf_scheme_obj.get_nav_data()
        [['date', 'nav']]
        .loc[lambda df: (df['date'] >= start_date)]
    )

    merged_df = (
        nav_df
        .merge(investment_df, on='date', how='left')
        .assign(amount_invested=lambda df: df['amount_invested'].fillna(0))
    )
    return merged_df


def get_investment_metrics(
    scheme_code: str,
    investment_df: pd.DataFrame
) -> dict:
    """
    Calculate investment metrics for a given mutual fund scheme.

    Args:
        scheme_code (str): Unique identifier for the mutual fund scheme.
        investment_df (pd.DataFrame): DataFrame with columns ['nav_date', 'amount_invested', 'units_bought'].

    Returns:
        dict: Dictionary containing:
            - total_invested: Total invested amount
            - current_value: Latest value of holdings
            - profit: Absolute profit/loss
            - roi: Return on Investment (%)
            - xirr: Annualized return using XIRR
            - units_bought: Total units purchased
            - current_nav: Latest NAV
            - average_nav: Average purchase NAV
    """
    mf_scheme = MFScheme(scheme_code)
    details = mf_scheme.get_details()

    latest_date = pd.to_datetime(details["current_date"])
    latest_nav = details["current_nav"]

    # Basic investment stats
    total_invested = investment_df["amount_invested"].sum()
    total_units = investment_df["units_bought"].sum()
    final_value = latest_nav * total_units

    # Vectorized cashflows
    cashflows = tuple(
        zip(pd.to_datetime(investment_df["nav_date"]), investment_df["amount_invested"])
    ) + ((latest_date, -final_value),)

    xirr = MFSimulator.calculate_xirr(cashflows)

    return {
        "total_invested": total_invested,
        "final_value": final_value,
        "profit": final_value - total_invested,
        "roi": (final_value - total_invested) / total_invested * 100 if total_invested else 0,
        "xirr": xirr,
        "total_units": total_units,
        "latest_nav": latest_nav,
        "average_nav": total_invested / total_units if total_units else 0,
    }
