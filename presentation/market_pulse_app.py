"""Run from the project root with: streamlit run presentation/market_pulse_app.py"""

from __future__ import annotations

import sys
from pathlib import Path

from datetime import date

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from librarian.core import (
    annualized_volatility,
    drawdown_series,
    log_returns,
    rolling_average_pairwise_corr,
)
from librarian.utils import download_price_history


DEFAULT_TICKERS = [
    "XLK",
    "XLV",
    "XLF",
    "XLE",
    "XLP",
    "XLI",
    "XLC",
    "XLB",
    "XLU",
    "XLRE",
    "XLY",
]


def _load_data(
    tickers: list[str],
    start: date,
    end: date,
) -> pd.DataFrame:
    return download_price_history(
        tickers=tickers,
        start=start,
        end=end,
    )


def main() -> None:
    st.set_page_config(
        page_title="Market Pulse",
        layout="wide",
    )

    st.title("Market Pulse – Sector Analytics Dashboard")
    st.write(
        "Explore sector ETFs, their volatility, drawdowns and the Market Shift Index "
        "(average pairwise correlation of returns)."
    )


    with st.sidebar:
        st.header("Configuration")

        tickers = st.multiselect(
            "Tickers",
            options=DEFAULT_TICKERS,
            default=DEFAULT_TICKERS,
            help="Select which ETFs to include in the analysis.",
        )

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start date",
                value=date(2015, 1, 1),
            )
        with col2:
            end_date = st.date_input(
                "End date",
                value=date.today(),
            )

        window = st.number_input(
            "MSI rolling window (sessions)",
            min_value=10,
            max_value=252,
            value=63,
            step=1,
            help="Lookback window used for the Market Shift Index calculation.",
        )

        st.caption(
            "Tip: narrow the date range or number of tickers if the app feels slow — "
            "data is downloaded live from Yahoo Finance."
        )

    if not tickers:
        st.warning("Please select at least one ticker in the sidebar.")
        st.stop()

    if start_date >= end_date:
        st.error("Start date must be strictly before end date.")
        st.stop()


    with st.spinner("Downloading price history from Yahoo Finance..."):
        try:
            px = _load_data(list(tickers), start_date, end_date)
        except Exception as exc:  # noqa: BLE001
            st.error(f"Error while downloading data: {exc}")
            st.stop()

    if px.empty:
        st.error("No price data returned for the chosen configuration.")
        st.stop()

    rets = log_returns(px)


    st.subheader("Key Metrics")
    vols = annualized_volatility(rets)
    max_dd = drawdown_series(px).min()

    metrics_cols = st.columns(3)
    with metrics_cols[0]:
        st.metric(
            "Number of assets",
            f"{px.shape[1]}",
        )
    with metrics_cols[1]:
        st.metric(
            "Sample length (sessions)",
            f"{px.shape[0]}",
        )
    with metrics_cols[2]:
        st.metric(
            "Median annualised volatility",
            f"{vols.median():.1%}",
        )

    with st.expander("Per-asset annualised volatility", expanded=False):
        st.dataframe(vols.sort_values(ascending=False).to_frame("volatility"))


    price_col, dd_col = st.columns(2)

    with price_col:
        st.markdown("#### Normalised price index")
        px_norm = px / px.iloc[0]
        fig, ax = plt.subplots(figsize=(8, 4))
        px_norm.plot(ax=ax)
        ax.set_ylabel("Index (start = 1.0)")
        ax.grid(True, alpha=0.3)
        st.pyplot(fig, clear_figure=True)

    with dd_col:
        st.markdown("#### Drawdown")
        dd = drawdown_series(px)
        fig_dd, ax_dd = plt.subplots(figsize=(8, 4))
        dd.plot(ax=ax_dd)
        ax_dd.set_ylabel("Drawdown")
        ax_dd.grid(True, alpha=0.3)
        st.pyplot(fig_dd, clear_figure=True)


    st.subheader("Market Shift Index (average pairwise correlation)")

    try:
        msi = rolling_average_pairwise_corr(rets, window=int(window))
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    fig_msi, ax_msi = plt.subplots(figsize=(10, 4))
    msi.plot(ax=ax_msi, color="tab:orange")
    ax_msi.set_ylabel("Average pairwise correlation")
    ax_msi.axhline(0, color="black", linewidth=0.5)
    ax_msi.grid(True, alpha=0.3)
    st.pyplot(fig_msi, clear_figure=True)


if __name__ == "__main__":
    main()


