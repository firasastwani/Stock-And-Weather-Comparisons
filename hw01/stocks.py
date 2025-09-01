from __future__ import annotations
import numpy as np
import pandas as pd

PRICE_COL = "Adj Close"

def read_stock_csv(path: str) -> pd.DataFrame:
    """
    Reads a stock CSV file and returns a DataFrame indexed by date.
    HINTS:
    - Use `pd.read_csv(path, parse_dates=['Date'])`.
    - Sort ascending by `Date` and then `set_index('Date')` to get a DatetimeIndex.
    - Expect a price column named `Adj Close` (see `PRICE_COL`). You may keep extra columns.
    - If duplicate dates exist, choose a policy (e.g., keep last). For HW tests, assume no duplicates.
    - Do not forward-fill missing prices here. Leave NaNs as-is.
    """
    # Read CSV with Date column parsed as datetime
    df = pd.read_csv(path, parse_dates=['Date'])
    
    # Sort ascending by Date and set as index
    df = df.sort_values('Date').set_index('Date')
    
    return df

def daily_simple_returns_pct(df: pd.DataFrame, price_col: str = PRICE_COL) -> pd.Series:
    """
    Computes daily simple returns from the price column.
    HINTS:
    - Use the vectorized method on the price Series: `pct_change()`.
    - The first row will be NaN. Keep it. Tests will drop NaNs when needed.
    - Index and dtype should be preserved (float output).
    - Default `price_col` is `Adj Close`.
    """

    # Use the vectorized pct_change() method as suggested in hints
    returns = df[price_col].pct_change()
    
    return returns

    

def daily_simple_returns_formula(df: pd.DataFrame, price_col: str = PRICE_COL) -> pd.Series:
    """
    Computes daily simple returns from the price column using the explicit formula.
    HINTS:
    - Formula: r_t = P_t / P_{t-1} - 1.
    - Use `shift(1)` for P_{t-1}. Prefer `Series.div(Series.shift(1))` to handle alignment.
    - The result should match `pct_change()` exactly aside from float precision.
    - First row will be NaN by definition.
    """

    # Formula: r_t = P_t / P_{t-1} - 1
    price_series = df[price_col]
    returns = price_series.div(price_series.shift(1)) - 1
    
    return returns


def daily_simple_returns(df: pd.DataFrame, price_col: str = PRICE_COL) -> pd.Series:
    """
    Computes daily simple returns from the price column.
    HINTS:
    - Delegate to one of the two functions above.
    - Verify equivalence between the two implementations with a tolerance (e.g., `np.allclose`).
    - Return the chosen Series unchanged (do not round).
    """

    returns_percent = daily_simple_returns_pct(df, price_col)
    returns_formula = daily_simple_returns_formula(df, price_col)

    # Verify equivalence between the two implementations with tolerance
    res = np.allclose(returns_percent, returns_formula, rtol=1e-10)

    return returns_formula

    
def log_returns(df: pd.DataFrame, price_col: str = PRICE_COL) -> pd.Series:
    """
    Computes log returns from the price column.
    OPTIONAL.
    HINTS:
    - Use `np.log(price).diff()`.
    - Relationship: sum of log returns over a range equals log of cumulative gross return.
    - First row will be NaN.
    """
    
    print("Not implemented")
    return pd.Series(dtype=float)

def average_daily_return(returns: pd.Series) -> float:
    """
    Input is a series of daily returns; compute the average daily return.
    HINTS:
    - Drop NaNs, then take the arithmetic mean.
    - Do NOT annualize here. Return the daily mean as a float.
    """

    price_series = returns.dropna()

    return price_series.mean()

def cumulative_return(df: pd.DataFrame, price_col: str = PRICE_COL) -> float:
    """
    Computes the cumulative return over the full period.
    HINTS:
    - Use first and last *valid* prices in the selected column.
    - Formula: (P_last / P_first) - 1.
    - If there are fewer than 1 valid observations, return NaN.
    - Using `Adj Close` makes this split/dividend-adjusted.
    """

    # Get first and last valid (non-NaN) prices
    price_series = df[price_col].dropna()
    
    # Check if we have at least 1 valid observation
    if len(price_series) < 1:
        return float('nan')
    
    P_first = price_series.iloc[0]
    P_last = price_series.iloc[-1]
    
    # Formula: (P_last / P_first) - 1
    return (P_last / P_first) - 1

def annualized_volatility(returns: pd.Series, trading_days: int = 252) -> float:
    """
    Computes the annualized volatility from daily returns.
    OPTIONAL.
    HINTS:
    - Drop NaNs, compute sample std with `ddof=1` on daily returns.
    - Scale by `sqrt(trading_days)` (use 252 by default).
    - If there are fewer than 2 non-NaN returns, return NaN.
    """
    print("Not implemented")
    return float('nan')

def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.015, trading_days: int = 252) -> float:
    """
    Computes the annualized Sharpe ratio.
    OPTIONAL.
    HINTS:
    - Convert annual risk-free rate to daily: `rf_d = (1+rf)^(1/252) - 1`.
    - Excess daily returns = daily returns - rf_d.
    - Daily Sharpe = mean(excess) / std(excess, ddof=1).
    - Annualize by multiplying by `sqrt(252)`.
    - If std is 0 or insufficient data, return NaN.
    """

    print("Not implemented")
    return float('nan')

def rolling_moving_averages(df: pd.DataFrame, windows=(20, 50), price_col: str = PRICE_COL) -> pd.DataFrame:
    """
    Computes rolling moving averages for given window sizes.
    OPTIONAL.
    HINTS:
    - For each window `w` in `windows`, create a new column named `SMA{w}`.
    - Use `Series.rolling(window=w, min_periods=w).mean()` so early rows stay NaN until full window.
    - Right-aligned windows by default; index preserved.
    - Leave existing columns intact; return a new DataFrame with added SMA columns.
    """
    # Create a copy to avoid modifying the original DataFrame
    result_df = df.copy()
    
    result_df['price'] = df[price_col]

    for w in windows:
        result_df[f'ma_{w}'] = df[price_col].rolling(window=w, min_periods=w).mean()
    
    return result_df
