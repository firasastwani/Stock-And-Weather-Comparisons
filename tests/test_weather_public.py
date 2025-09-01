from hw01 import weather as W

def test_weather_summary_keys():
    df = W.read_weather_csv("data/weather_small.csv")
    summary = W.min_max_summary(df)
    for k in ["mean_temperaturemin", "median_temperaturemin", "mean_temperaturemax", "median_temperaturemax"]:
        assert k in summary

def test_slice_means_has_cols():
    df = W.read_weather_csv("data/weather_small.csv")
    s = W.slice_and_means(df, start="2022-01-10", end="2022-01-20")
    assert "temperaturemax" in s.index and "precipitation" in s.index
