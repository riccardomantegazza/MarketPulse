# Installazione Dataset
!pip install yfinance pandas numpy matplotlib

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Classi
tickers = ['XLK', 'XLV', 'XLF', 'XLE', 'XLP', 'XLI', 'XLC', 'XLB', 'XLU', 'XLRE', 'XLY']
start_date = '2015-01-01'
end_date = '2025-01-01'

# Periodi eventi (Pandemia) (Guerra)
covid_start = pd.Timestamp('2020-01-10')
covid_end   = pd.Timestamp('2023-05-05')

war_start   = pd.Timestamp('2022-02-24')
war_end     = pd.Timestamp.today().normalize()  # fino ad oggi


#hello hello