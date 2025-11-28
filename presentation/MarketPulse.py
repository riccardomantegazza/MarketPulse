import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from librarian.core import (
    annualized_volatility,
    drawdown_series,
    log_returns,
    max_drawdown,
    rolling_average_pairwise_corr,
)
from librarian.models import MarketEvent
from librarian.utils import download_price_history, slice_period

#%%
tickers = ['XLK', 'XLV', 'XLF', 'XLE', 'XLP', 'XLI', 'XLC', 'XLB', 'XLU', 'XLRE', 'XLY']
start_date = pd.Timestamp('2015-01-01')
end_date = pd.Timestamp('2025-01-01')

# Event Windows
covid_event = MarketEvent('COVID', pd.Timestamp('2020-01-10'), pd.Timestamp('2023-05-05'))
war_event = MarketEvent('Guerra Ucraina', pd.Timestamp('2022-02-24'), pd.Timestamp.today().normalize())

covid_start, covid_end = covid_event.start, covid_event.end
war_start, war_end = war_event.start, war_event.end
event_windows = [covid_event, war_event]

px = download_price_history(tickers=tickers, start=start_date, end=end_date)

returns = log_returns(px)
vol_ann = annualized_volatility(returns)
dd_series = drawdown_series(px)
dd_max = max_drawdown(px)
msi_full = rolling_average_pairwise_corr(returns, window=63)

assert dd_series.columns.equals(returns.columns)
assert vol_ann.index.equals(returns.columns)

risk_snapshot = pd.DataFrame({
    "annualized_vol": vol_ann,
    "max_drawdown": dd_max,
})

risk_snapshot.sort_values("annualized_vol", ascending=False).head()

msi_full.sort_index(ascending=False).head().to_frame("market_shift_index")

dd_series.head()

returns.head()

plt.figure(figsize=(12, 6))
plt.plot(msi_full, label="Market Shift Index", linewidth=2, color='blue')
plt.axvspan(covid_start, covid_end, alpha=0.2, color='red', label="COVID")
plt.axvspan(war_start, war_end, alpha=0.2, color='orange', label="Guerra Ucraina")
plt.title("Market Shift Index - Media Correlazioni tra Settori (rolling 63 giorni)")
plt.xlabel("Data")
plt.ylabel("Media Correlazioni")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 7))
dd_series.plot(alpha=0.7, linewidth=1.5)
plt.title("Drawdown Storico per Settore", fontsize=14, fontweight='bold')
plt.xlabel("Data", fontsize=12)
plt.ylabel("Drawdown (%)", fontsize=12)
plt.legend(ncol=3, fontsize=9, loc='lower right', framealpha=0.9)
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
dd_max.sort_values().plot(kind='bar', color='blue', alpha=0.7)
plt.title("Max Drawdown per Settore (Periodo Totale)", fontsize=14, fontweight='bold')
plt.xlabel("Settore", fontsize=12)
plt.ylabel("Max Drawdown (%)", fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()

prices_covid = slice_period(px, covid_start, covid_end)
returns_covid = returns.loc[covid_start:covid_end].copy()
msi_covid = rolling_average_pairwise_corr(returns_covid, window=63)
dd_covid = max_drawdown(prices_covid)
vol_covid = annualized_volatility(returns_covid)

corr_covid = returns_covid.corr()
fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(corr_covid.values, cmap='viridis', vmin=0, vmax=1, aspect='auto')
cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Correlation Coefficient', rotation=270, labelpad=20)
ax.set_xticks(range(len(corr_covid.columns)))
ax.set_xticklabels(corr_covid.columns, rotation=45, ha='right')
ax.set_yticks(range(len(corr_covid.index)))
ax.set_yticklabels(corr_covid.index)
ax.set_title("Correlation Heatmap - COVID Period", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
vol_covid_sorted = vol_covid.sort_values(ascending=False).head()
ax.barh(vol_covid_sorted.index, vol_covid_sorted.values, color='steelblue', alpha=0.7)
ax.set_xlabel('Annualized Volatility', fontsize=12)
ax.set_title('Top 5 Sectors by Volatility - COVID Period', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
dd_covid_sorted = dd_covid.sort_values().head()
ax.barh(dd_covid_sorted.index, dd_covid_sorted.values, color='crimson', alpha=0.7)
ax.set_xlabel('Max Drawdown (%)', fontsize=12)
ax.set_title('Top 5 Sectors by Max Drawdown - COVID Period', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(msi_covid.index, msi_covid.values, linewidth=2, color='blue', label='Market Shift Index')
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Average Correlation', fontsize=12)
ax.set_title('Market Shift Index - COVID Period', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

prices_war = slice_period(px, war_start, war_end)
returns_war = log_returns(prices_war)
msi_war = rolling_average_pairwise_corr(returns_war, window=63)
dd_war = max_drawdown(prices_war)
vol_war = annualized_volatility(returns_war)

corr_war = returns_war.corr()
fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(corr_war.values, cmap='viridis', vmin=0, vmax=1, aspect='auto')
cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Correlation Coefficient', rotation=270, labelpad=20)
ax.set_xticks(range(len(corr_war.columns)))
ax.set_xticklabels(corr_war.columns, rotation=45, ha='right')
ax.set_yticks(range(len(corr_war.index)))
ax.set_yticklabels(corr_war.index)
ax.set_title("Correlation Heatmap - War Period", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
vol_war_sorted = vol_war.sort_values(ascending=False).head()
ax.barh(vol_war_sorted.index, vol_war_sorted.values, color='steelblue', alpha=0.7)
ax.set_xlabel('Annualized Volatility', fontsize=12)
ax.set_title('Top 5 Sectors by Volatility - War Period', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
dd_war_sorted = dd_war.sort_values().head()
ax.barh(dd_war_sorted.index, dd_war_sorted.values, color='crimson', alpha=0.7)
ax.set_xlabel('Max Drawdown (%)', fontsize=12)
ax.set_title('Top 5 Sectors by Max Drawdown - War Period', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(msi_war.index, msi_war.values, linewidth=2, color='orange', label='Market Shift Index')
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Average Correlation', fontsize=12)
ax.set_title('Market Shift Index - War Period', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

