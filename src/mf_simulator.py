from datetime import timedelta
from pyxirr import xirr
import pandas as pd
import config.constants as CONSTANTS
# from archive.helpers import get_dip_factor
import streamlit as st
from mftools_wrapper import MFScheme
from src.dip_factor import DipFactorUtils


class MFSimulator:
    def __init__(
            self, 
            nav_df: pd.DataFrame = None, 
            scheme_code: str = None
    ):
        """
        This supports two initialization modes:
        1. Directly from a pre-loaded NAV DataFrame.
        2. By providing a scheme code, from which NAV data is internally fetched
        using the `MFScheme` class.


        Args:
            nav_df (pd.DataFrame, optional): Pre-loaded DataFrame containing NAV history.
                Must include a "Date" column. If provided, this data will be used directly.
            scheme_code (str, optional): Unique scheme code used to fetch NAV history
                through `MFScheme`. Ignored if `nav_df` is provided.

        Raises:
            ValueError: If neither `nav_df` nor `scheme_code` is provided.
        """
        if nav_df is None and scheme_code is None:
            raise ValueError("Either nav_df or scheme_code must be provided")

        if nav_df is None:
            nav_df = MFScheme(scheme_code).get_nav_data()

        self.nav_df = nav_df.sort_values("date").reset_index(drop=True)
    
    
    def _add_metrics(self, detail_dict: dict) -> dict:
        add_ons = {
            "profit": detail_dict['final_value'] - detail_dict['total_invested'],
            "roi": ((detail_dict['final_value'] - detail_dict['total_invested']) / 
                    detail_dict['total_invested'] * 100) if detail_dict['total_invested'] != 0 else 0,
            "average_nav" : detail_dict['total_invested'] / detail_dict['total_units'] if detail_dict['total_units'] != 0 else 0
        }
        return {**detail_dict, **add_ons}

    def run_simulation_from_params(self, params: dict):
        if params['frequency'] == "Weekly":
            required_keys = ["weights", 
                             "drop_threshold_range", 
                             "lumpsum", 
                             "carry_forward",
                             "sip_amount", 
                             "weeks", 
                             "weekday"]
            filtered_params = {k: v for k, v in params.items() if k in required_keys}

            return self.simulate_weekly(**filtered_params)
        
        else:
            required_keys = ["weights", 
                             "drop_threshold_range", 
                             "lumpsum", 
                             "carry_forward",
                             "sip_amount", 
                             "months", 
                             "date_of_investment"]

            filtered_params = {k: v for k, v in params.items() if k in required_keys}
            
            return self.simulate_monthly(**filtered_params)



    def simulate_weekly(
            self,
            weights: dict = None,
            drop_threshold_range: tuple = None,
            lumpsum: int = None,
            carry_forward: bool = None,
            sip_amount: int = None,
            weeks: int = None,
            weekday: int = None,
        ):
        """
        Runs simulation weekly
        """

        weights = weights or CONSTANTS.WEIGHTS
        drop_threshold_range = drop_threshold_range or CONSTANTS.DROP_THRESHOLD_RANGE
        lumpsum = lumpsum if lumpsum is not None else CONSTANTS.LUMPSUM_PER_WEEK
        carry_forward = carry_forward if carry_forward is not None else CONSTANTS.CARRY_FORWARD_WEEKLY
        sip_amount = sip_amount or CONSTANTS.SIP_AMOUNT_WEEKLY
        weeks = weeks or CONSTANTS.WEEKS
        weekday = weekday or CONSTANTS.WEEKDAY
        
        end_date = self.nav_df["date"].max()
        start_date = end_date - timedelta(weeks=weeks)
        df = self.nav_df.reset_index(drop=True)

        # Initialise variables
        lumpsum_remain_each_week = lumpsum
        total_units = 0.0
        total_invested = 0.0
        investment_history = []
        
        cashflows = []

        for curr_date in pd.date_range(start_date, end_date):
            if curr_date.weekday() != weekday:
                continue
            
            
            row = df[df["date"] == curr_date]
            if row['nav'].values.size == 0: continue
            nav_curr_date = row['nav'].values[0]
            past_df = df[df["date"] <= curr_date]

            curr_date = curr_date.date()
            curr_day_str = CONSTANTS.WEEKDAY_MAPPING[curr_date.weekday()]

            dip_factor = (
                DipFactorUtils(
                    df=past_df,
                    weights=weights,
                    drop_threshold_range=drop_threshold_range
                )
                .from_frequency(
                    frequency="Weekly"
                )
            )

            dip_buy = dip_factor * lumpsum_remain_each_week
            amount_to_invest = dip_buy + sip_amount

            if amount_to_invest > 0:
                total_units += (amount_to_invest / nav_curr_date)
                total_invested += amount_to_invest
                cashflows.append((curr_date, -amount_to_invest))

                investment_history.append({
                    "date": curr_date,
                    "weekday": curr_day_str,
                    "nav": nav_curr_date,
                    "dip_factor": dip_factor,
                    "dip_buy": dip_buy,
                    "sip": sip_amount,
                    "total_investment": amount_to_invest,
                    "units": (amount_to_invest / nav_curr_date) if nav_curr_date else 0
                })
            if carry_forward : 
                lumpsum_remain_each_week += (lumpsum - dip_buy)

        latest_nav = df['nav'].iloc[-1]
        final_value = total_units * latest_nav
        cashflows.append((df["date"].iloc[-1], final_value))
        investment_history = pd.DataFrame(investment_history)
        
        xirr_value = self.calculate_xirr(cashflows)
        final_metrics = {
            "total_invested": total_invested,
            "final_value": final_value,
            "xirr": xirr_value,
            "total_units": total_units,
            "latest_nav": latest_nav
        }
        final_metrics = self._add_metrics(final_metrics)

        return investment_history, final_metrics

    def simulate_monthly(
            self,
            weights: dict = None,
            drop_threshold_range: tuple = None,
            lumpsum: int = None,
            carry_forward: bool = None,
            sip_amount: int = None,
            months: int = None,
            date_of_investment: int = None
        ):

        """
        Simulates monthly investment performance based on NAV history and dip factors.

        This method allows simulation of investment strategies (lumpsum or SIP) over a
        specified number of months, taking into account historical NAV drops, dip factor
        weights, and user-defined investment preferences. The simulation can also handle
        carry-forward of uninvested amounts if specified.

        Args:
            weights (dict, optional): Dictionary of weights used in dip factor calculation.
                Expected keys:
                    - "recent_vs_historical": relative weight of recent vs historical dips.
                    - "peak_vs_average": relative weight of peak drop vs average drop.
                
            drop_threshold_range (tuple, optional): Tuple defining thresholds for normalizing percentage drops into [0.0, 1.0].
            
            lumpsum (int, optional): One-time investment amount to deploy each month.
            carry_forward (bool, optional): Whether uninvested lumpsum/SIP amounts should
                be carried forward to the next month.
            sip_amount (int, optional): Monthly SIP amount to invest.
            months (int, optional): Number of months to simulate.
            date_of_investment (int, optional): Day of the month when investments are executed.

        Returns:
            pd.DataFrame: DataFrame containing simulated investment details per month,
            including invested amount, units bought, and cumulative NAV metrics.
        """ 

        weights = weights or CONSTANTS.WEIGHTS
        drop_threshold_range = drop_threshold_range or CONSTANTS.DROP_THRESHOLD_RANGE
        lumpsum = lumpsum if lumpsum is not None else CONSTANTS.LUMPSUM_PER_MONTH
        carry_forward = carry_forward if carry_forward is not None else CONSTANTS.CARRY_FORWARD_MONTHLY
        sip_amount = sip_amount or CONSTANTS.SIP_AMOUNT_MONTHLY
        months = months or CONSTANTS.MONTHS
        date_of_investment = date_of_investment or CONSTANTS.DATE_OF_INVESTMENT
        
        end_date = self.nav_df["date"].max()
        start_date = end_date - pd.DateOffset(months=months)
        df = self.nav_df.reset_index(drop=True)

        # Initialise variables
        lumpsum_remain_each_month = lumpsum
        total_units = 0.0
        total_invested = 0.0
        investment_history = []
        cashflows = []

        for curr_date in pd.date_range(start_date, end_date, freq='D'):
            # Invest only on specified date_of_investment
            if curr_date.day != date_of_investment:
                continue
            row = df[df["date"] <= curr_date].nlargest(1, "date")
            if row.empty:
                continue
            
            nav_curr_date = row.iloc[0]['nav']
            curr_date = row.iloc[0]['date']
            curr_day_str = CONSTANTS.WEEKDAY_MAPPING[curr_date.weekday()]
            past_df = df[df["date"] <= curr_date]
            dip_factor = (
                DipFactorUtils(
                    df=past_df,
                    weights=weights,
                    drop_threshold_range=drop_threshold_range
                )
                .from_frequency(
                    frequency="Monthly"
                )
            )

            dip_buy = dip_factor * lumpsum_remain_each_month
            amount_to_invest = dip_buy + sip_amount
            
            if amount_to_invest > 0:
                total_units += (amount_to_invest / nav_curr_date)
                total_invested += amount_to_invest
                cashflows.append((curr_date, -amount_to_invest))

                investment_history.append({
                    "date": curr_date,
                    "weekday": curr_day_str,
                    "nav": nav_curr_date,
                    "dip_factor": dip_factor,
                    "dip_buy": dip_buy,
                    "sip": sip_amount,
                    "total_investment": amount_to_invest,
                    "units": (amount_to_invest / nav_curr_date) if nav_curr_date else 0
                })
            
            if carry_forward:
                lumpsum_remain_each_month += (lumpsum - dip_buy)

        latest_nav = df['nav'].iloc[-1]
        final_value = total_units * latest_nav
        cashflows.append((df["date"].iloc[-1], final_value))
        
        investment_history = pd.DataFrame(investment_history)
        xirr_value = self.calculate_xirr(cashflows) 
        final_metrics = {
            "total_invested": total_invested,
            "final_value": final_value,
            "xirr": xirr_value,
            "total_units": total_units,
            "latest_nav": latest_nav
        }
        final_metrics = self._add_metrics(final_metrics)

        return investment_history, final_metrics


    @staticmethod
    def calculate_xirr(cashflows):
        """Calculate XIRR from self.cashflows (list of (date, amount) tuples)."""
        if not cashflows:
            return 0.0
        try:
            return xirr(cashflows) * 100
        except Exception:
            print("Error calculating XIRR.")
            return 0.0
