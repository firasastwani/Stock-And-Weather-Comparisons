import pandas as pd
from hw01 import stocks as S

def test_read_and_returns_shape():
    df = S.read_stock_csv("data/nvda_2023_sample.csv")
    r = S.daily_simple_returns(df)
    assert pd.isna(r.iloc[0])
    assert len(r) == len(df)

def test_mas_columns():
    df = S.read_stock_csv("data/nvda_2023_sample.csv")
    mas = S.rolling_moving_averages(df, windows=(3,5))
    assert all(col in mas.columns for col in ["price", "ma_3", "ma_5"])
