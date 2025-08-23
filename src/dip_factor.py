import pandas as pd
import config.constants as CONSTANTS
from .nav_metrics import compute_nav_metrics

class DipFactorCalculator:
    def __init__(
            self, 
            recent_drops : dict, 
            historical_drops : dict, 
            weights : dict = None, 
            drop_threshold_range : tuple = None
        ):
        """
        DipFactorCalculator computes a normalized "dip factor" from NAV drawdowns.

        Args:
            recent_drops (dict): Recent period drops with keys:
                - 'peak': Drop percentage from recent peak NAV.
                - 'avg': Drop percentage from recent average NAV.
            historical_drops (dict): Historical period drops with same keys.
            weights (dict, optional): Weight configuration with keys:
                - 'recent_vs_historical': Weight of recent vs. historical factor.
                - 'peak_vs_average': Weight of peak drop vs. average drop.
                Defaults to CONSTANTS.WEIGHTS.
            drop_threshold_range (tuple, optional): (min_drop, max_drop) thresholds
                used for normalizing dips into [0.0, 1.0].
                Defaults to CONSTANTS.DROP_THRESHOLD_RANGE.
        """

        self.recent_drops = recent_drops
        self.historical_drops = historical_drops
        self.weights = weights or CONSTANTS.WEIGHTS
        self.drop_threshold_range = drop_threshold_range or CONSTANTS.DROP_THRESHOLD_RANGE

    def _normalize_drop(self, d: float) -> float:
        min_th, max_th = self.drop_threshold_range
        if d > -min_th: 
            return 0.0
        if d <= -max_th: 
            return 1.0
        return (-d - min_th) / (max_th - min_th)

    @staticmethod
    def _weighted_avg(a: float, b: float, w: float) -> float:
        return w * a + (1 - w) * b

    def calculate_dip_factor(self) -> float:
        factor_recent = self._weighted_avg(
            self._normalize_drop(self.recent_drops['peak']),
            self._normalize_drop(self.recent_drops['avg']),
            self.weights['peak_vs_average'],
        )

        factor_historical = self._weighted_avg(
            self._normalize_drop(self.historical_drops['peak']),
            self._normalize_drop(self.historical_drops['avg']),
            self.weights['peak_vs_average'],
        )

        return self._weighted_avg(
            factor_recent,
            factor_historical,
            self.weights['recent_vs_historical'],
        )


class DipFactorUtils:
    def __init__(
        self,
        df: pd.DataFrame,
        weights: dict = None,
        drop_threshold_range: tuple = None,
    ):
        """
        Utility class to compute dip factors over different time horizons.

        This class prepares the inputs (recent and historical drop metrics) required by
        `DipFactorCalculator` and provides higher-level helper methods to compute
        dip factors from raw NAV data.

        Args:
            df (pd.DataFrame): DataFrame containing NAV history (must be compatible
                with `compute_nav_metrics`).
            weights (dict): Dictionary of weights used in dip factor calculation.
                Expected keys:
                    - "recent_vs_historical": relative weight of recent vs historical dips.
                    - "peak_vs_average": relative weight of peak drop vs average drop.
                Defaults to `CONSTANTS.WEIGHTS` if not provided.
            drop_threshold_range (tuple): Tuple defining the thresholds for normalizing
                percentage drops into [0.0, 1.0]. Defaults to `CONSTANTS.DROP_THRESHOLD_RANGE`.
        """
        self.df = df
        self.weights = weights or CONSTANTS.WEIGHTS
        self.drop_threshold_range = drop_threshold_range or CONSTANTS.DROP_THRESHOLD_RANGE

    def compute_raw(
        self,
        recent_days: int,
        historical_days: int,
    ) -> float:
        
        recent = compute_nav_metrics(
            df=self.df, 
            lookback_days=recent_days, 
            as_string=False
        )
        historical = compute_nav_metrics(
            df=self.df, 
            lookback_days=historical_days, 
            as_string=False
        )
        

        x = DipFactorCalculator(
            recent_drops= {
                'peak' : recent['%_vs_high'],
                'avg' : recent['%_vs_avg'],
            },
            historical_drops={
                'peak' : historical['%_vs_high'],
                'avg' : historical['%_vs_avg'],
            },
            weights=self.weights,
            drop_threshold_range=self.drop_threshold_range
        )
        return x.calculate_dip_factor()

    def from_frequency(self, frequency: str = "weekly") -> float:
        frequency = frequency.lower()
        if frequency == "weekly":
            return self.compute_raw(30, 60)
        if frequency == "monthly":
            return self.compute_raw(60, 90)
        return 0
