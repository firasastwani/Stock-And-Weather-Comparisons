from __future__ import annotations
import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
import pandas as pd

def plot_stock_price_ma(df: pd.DataFrame, windows=(20, 50), price_col: str = "Adj Close", outfile: str = "images/stock_price_ma.png") -> str:
    # single axes; let matplotlib choose colors
    fig, ax = plt.subplots()
    ax.plot(df.index, df[price_col], label="price")
    for w in windows:
        ax.plot(df.index, df[price_col].rolling(window=w, min_periods=1).mean(), label=f"MA{w}")
    ax.set_title("Stock Price with Moving Averages")
    ax.set_xlabel("Date")
    ax.set_ylabel(price_col)
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(outfile, dpi=120)
    plt.close(fig)
    return outfile

def plot_returns_hist(returns: pd.Series, bins: int = 30, outfile: str = "images/stock_returns_hist.png") -> str:
    fig, ax = plt.subplots()
    r = returns.dropna()
    ax.hist(r.values, bins=bins)
    ax.set_title("Daily Returns Histogram")
    ax.set_xlabel("Return")
    ax.set_ylabel("Frequency")
    fig.tight_layout()
    fig.savefig(outfile, dpi=120)
    plt.close(fig)
    return outfile

def plot_weather_tmax_and_celsius(df: pd.DataFrame, outfile: str = "images/weather_tmax_celsius.png") -> str:
    # expects a column 'temperaturemax_celsius'; if missing, create on the fly
    if "temperaturemax_celsius" not in df.columns:
        df = df.copy()
        df["temperaturemax_celsius"] = (df["temperaturemax"] - 32.0) * 5.0 / 9.0
    fig, ax = plt.subplots()
    ax.plot(df.index, df["temperaturemax"], label="tmax (F)")
    ax.plot(df.index, df["temperaturemax_celsius"], label="tmax (C)")
    ax.set_title("Max Temperature (F & C)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature")
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(outfile, dpi=120)
    plt.close(fig)
    return outfile
