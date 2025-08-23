import pandas as pd


def compute_nav_metrics(
    df: pd.DataFrame,
    lookback_days: int,
    as_string: bool = True
) -> dict:
    """
    Calculate NAV performance metrics over a specified lookback period ending at the most recent date.

    The function evaluates the latest NAV against the high, low, and average NAV within
    the lookback window, and returns both raw values and relative percentage comparisons.

    Args:
        df: DataFrame containing columns ['date', 'nav'].
        lookback_days: Number of trailing days from the latest date to include in the window.
        as_string: If True, percentage differences are returned as formatted strings with symbols;
                   otherwise as numeric floats.

    Returns:
        dict: Dictionary containing NAV performance metrics.
            - as_of_date: Latest NAV date.
            - start_date: First date in the lookback window.
            - lookback_days: Lookback window size in days.
            - today_nav: NAV on the latest date.
            - high_nav: Maximum NAV within the window.
            - avg_nav: Average NAV within the window.
            - low_nav: Minimum NAV within the window.
            - %_vs_high: Today vs high NAV percentage difference.
            - %_vs_avg: Today vs average NAV percentage difference.
            - %_vs_low: Today vs low NAV percentage difference.
    """
    if 'date' not in df.columns or 'nav' not in df.columns:
        raise ValueError("DataFrame must contain 'date' and 'nav' columns")

    df = (
        df[["date", "nav"]]
        .copy()
        .sort_values("date")
    )

    end_date = df["date"].max()
    window = df[df["date"] >= end_date - pd.Timedelta(days=lookback_days)]


    latest_nav = window.loc[window["date"] == end_date, "nav"].iloc[0]
    high_nav, low_nav, avg_nav = window["nav"].max(), window["nav"].min(), window["nav"].mean()

    percentage = (
        (lambda current, reference: (
            f"{round((current - reference) / reference * 100, 3)}% "
            f"{'↑' if current > reference else ('↓' if current < reference else '→')}"
        ))
        if as_string else
        (lambda current, reference: round((current - reference) / reference * 100, 3))
    )

    return {
        "as_of_date": end_date,
        "start_date": window["date"].min(),
        "lookback_days": lookback_days,
        "today_nav": latest_nav,
        "high_nav": high_nav,
        "avg_nav": avg_nav,
        "low_nav": low_nav,
        "%_vs_high": percentage(latest_nav, high_nav),
        "%_vs_avg": percentage(latest_nav, avg_nav),
        "%_vs_low": percentage(latest_nav, low_nav),
    }





