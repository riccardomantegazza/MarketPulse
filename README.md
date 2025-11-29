# Market Pulse Project

This project explores the behavior of financial markets by analyzing the performance 
and risk profiles of different stock market sectors. Using historical stock price 
data, the project focuses on uncovering volatility patterns, correlation structures, 
and market dynamics under normal conditions and during periods of stress, such as 
the COVID crisis.

The analysis is based on real market data retrieved through the `yfinance` library,
which interfaces with the Yahoo Finance API. The project includes a full preprocessing
pipeline for financial time series and implements key quantitative risk measures 
such as log-returns, annualized volatility, drawdown, maximum drawdown, and rolling 
pairwise correlations.

The final goal of the project is to provide a clear and data-driven view of how 
different market sectors behave, interact with each other, and respond to market shifts,
supported by quantitative indicators and visual analytics.


```
PythonProject/
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies 
├── librarian/
│   ├── __init__.py      # Public API   
│   ├── core.py          # Financial funcions: returns, volatility, drawdown
│   ├── models.py        # Market Event Class
│   └── utils.py         # Utility helpers for data access and slicing
└──  presentation/
    ├── test_market_pulse_project.ipynb    # Code explanation
    ├── MarketPulse.py       # Main code
    └── market_pulse_app.pyb  # Main application script
```

## Getting Started

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the automated tests:
   ```bash
   pytest
   ```
3. Open the notebook inside `presentation/` to generate the figures.

## Package Overview

* `librarian.core`: quantitative analytics (returns, volatility, drawdowns, MSI).
* `librarian.models`: domain dataclasses such as `MarketEvent`.
* `librarian.utils`: helpers for downloading data and slicing time ranges.

Import the functionality you need:

```python
from librarian import (
    MarketEvent,
    annualized_volatility,
    download_price_history,
    log_returns,
)
```

