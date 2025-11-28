"""Utility helpers for data access and slicing."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import pandas as pd
import yfinance as yf


def download_price_history(
    tickers: Sequence[str],
    start: Any,
    end: Any,
    *,
    price_field: str = "Adj Close",
    auto_adjust: bool = True,
) -> pd.DataFrame:
    """Download and return a clean price matrix for the requested tickers."""
    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end)
    data = yf.download(
        tickers=tickers,
        start=start_ts,
        end=end_ts,
        auto_adjust=auto_adjust,
        group_by="column",
        progress=False,
    )

    if data.empty:
        raise ValueError("No price data retrieved from yfinance.")

    if isinstance(data.columns, pd.MultiIndex):
        first_level = data.columns.get_level_values(0)
        if price_field in first_level:
            prices = data[price_field].copy()
        elif "Close" in first_level:
            prices = data["Close"].copy()
        else:
            raise KeyError(
                f"Requested price field '{price_field}' not found in download."
            )
    else:
        prices = data.copy()

    return prices.sort_index().dropna(how="all")


def slice_period(
    px: pd.DataFrame, start: Any, end: Any | None = None
) -> pd.DataFrame:
    """Return the subset of rows whose index falls within start/end."""
    start_ts = pd.Timestamp(start)
    if end is None:
        return px.loc[px.index >= start_ts]

    end_ts = pd.Timestamp(end)
    mask = (px.index >= start_ts) & (px.index <= end_ts)
    return px.loc[mask]

