import json, subprocess, sys, os, pathlib

def run_cmd(args):
    result = subprocess.run([sys.executable, "-m", "hw01.cli"] + args, capture_output=True, text=True, cwd=os.getcwd())
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()

def test_cli_stocks_json():
    out = run_cmd(["stocks", "--input", "data/nvda_2023_sample.csv", "--ticker", "NVDA", "--json"])
    payload = json.loads(out)
    assert payload["ticker"] == "NVDA"
    assert "metrics" in payload and "avg_daily_return" in payload["metrics"]

def test_cli_weather_json():
    out = run_cmd(["weather", "--input", "data/weather_small.csv", "--start", "2022-01-10", "--end", "2022-01-20", "--json"])
    payload = json.loads(out)
    assert payload["has_celsius"] is True
    assert "summary" in payload and "sliced_means" in payload

def test_cli_stocks_plot_file(tmp_path):
    png = tmp_path / "stock_price_ma.png"
    run_cmd(["stocks", "--input", "data/nvda_2023_sample.csv", "--ticker", "NVDA", "--plot-out", str(png), "--plot-kind", "price_ma"])
    assert png.exists() and png.stat().st_size > 0

def test_cli_weather_plot_file(tmp_path):
    png = tmp_path / "weather.png"
    run_cmd(["weather", "--input", "data/weather_small.csv", "--plot-out", str(png)])
    assert png.exists() and png.stat().st_size > 0
