# Funzione per il calcolo dei rendimenti logaritmici giornalieri
def log_returns(px: pd.DataFrame) -> pd.DataFrame:
    px = px.sort_index()
    rets = np.log(px / px.shift(1))
    return rets.dropna(how='all')

# Funzione per calcolo della volatilità annulizzata(252)
def annualized_volatility(rets: pd.DataFrame, periods_per_year = 252) -> pd.Series:
    return rets.std(skipna=True) * np.sqrt(periods_per_year)

# Funzione per il Drawdown dei prezzi
def drawdown_series(px: pd.DataFrame) -> pd.DataFrame:
    cummax = px.cummax()
    dd = px / cummax - 1.0
    return dd

# Funzione per il Max Drawdown del prezzo
def max_drawdown(px: pd.DataFrame) -> pd.Series:
    return drawdown_series(px).min()