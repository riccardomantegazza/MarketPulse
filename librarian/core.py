
from __future__ import annotations

import numpy as np
import pandas as pd

__all__ = [
    "log_returns",
    "annualized_volatility",
    "drawdown_series",
    "max_drawdown",
    "rolling_average_pairwise_corr",
]


def log_returns(px: pd.DataFrame) -> pd.DataFrame:
    px_sorted = px.sort_index()
    rets = np.log(px_sorted / px_sorted.shift(1))
    return rets.dropna(how="all")


def annualized_volatility(
    rets: pd.DataFrame, periods_per_year: int = 252
) -> pd.Series:
    return rets.std(skipna=True) * np.sqrt(periods_per_year)


def drawdown_series(px: pd.DataFrame) -> pd.DataFrame:
    cummax = px.cummax()
    return px / cummax - 1.0


def max_drawdown(px: pd.DataFrame) -> pd.Series:
    return drawdown_series(px).min()


def rolling_average_pairwise_corr(
    rets: pd.DataFrame, window: int = 63
) -> pd.Series:
    if window < 2:
        raise ValueError("window must be at least 2 sessions")

    rets = rets.sort_index()
    values = rets.to_numpy()
    dates = rets.index
    metrics: list[float] = []
    metric_dates: list[pd.Timestamp] = []

    for i in range(window, len(rets) + 1):
        sub = values[i - window : i]
        valid_cols = ~np.all(np.isnan(sub), axis=0)
        sub = sub[:, valid_cols]
        if sub.shape[1] < 2:
            metrics.append(np.nan)
            metric_dates.append(dates[i - 1])
            continue

        valid_rows = ~np.all(np.isnan(sub), axis=1)
        sub = sub[valid_rows]
        if sub.shape[0] < 2:
            metrics.append(np.nan)
            metric_dates.append(dates[i - 1])
            continue

        corr = np.corrcoef(sub, rowvar=False)
        n = corr.shape[0]
        off_diag = corr[np.triu_indices(n, k=1)]
        metrics.append(np.nanmean(off_diag))
        metric_dates.append(dates[i - 1])

    return pd.Series(metrics, index=pd.DatetimeIndex(metric_dates), name="market_shift_index")