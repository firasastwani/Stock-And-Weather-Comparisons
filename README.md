# CSCI 4170/6170 — Fall 2025
## Lab+HW 01 Starter (Weather + Stocks)

This starter provides **uniform printing**, **function signatures for unit testing**, a simple **CLI**, and **public smoke tests**.

Autograding will call functions and the CLI exactly as specified here.

### Quick start
```bash
# Optional -- create a virtual env and install requirements
#     Note: - (you can use the environment installed via Anaconda/pyCharm) 
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run public tests // tests/test_*.py { will be completed at }
pytest -q

# Example CLI runs (JSON output is what the autograder relies on)

# Weather JSON +  { plot capability: coming soon }
python -m hw01.cli weather --input data/weather_small.csv 
python -m hw01.cli weather --input data/weather_small.csv --json
python -m hw01.cli weather --input data/weather_small.csv --start 2022-01-10 --end 2022-01-20
python -m hw01.cli weather --input data/weather_small.csv --plot-out images/weather_tmax_celsius.png

# Stocks JSON + { plot capability: coming soon }
python -m hw01.cli stocks --input data/nvda_2023_sample.csv --ticker NVDA 
python -m hw01.cli stocks --input data/nvda_2023_sample.csv --ticker NVDA --json
python -m hw01.cli stocks --input data/nvda_2023_sample.csv --ticker NVDA --plot-out images/stock_price_ma.png --plot-kind price_ma


```
**Do not** change function names or return types in `hw01/stocks.py`, `hw01/weather.py`, or the JSON schema emitted by the CLI.
You may add helper functions/files.

### Repo layout
```
.

├── data/
│   ├── nvda_2023_sample.csv
|   ├── NVDA.csv
|   ├── rdu-weather-history.csv
│   └── weather_small.csv
├── hw01/
│   ├── __init__.py
│   ├── cli.py
│   ├── formatter.py
│   ├── plotting.py
│   ├── stocks.py
│   └── weather.py
├── tests/
│   ├── test_cli_public.py
│   ├── test_stocks_public.py
│   └── test_weather_public.py
├── requirements.txt
├── images
│   ├── weather_plot.png 
└── README.md
```

### Notes
- The **public tests** are light-weight and focus on *interfaces and shape*. Grading will use **hidden tests** with a larger dataset.
- The CLI supports `--json` for exact, reproducible output. The default console printing uses the provided `formatter.py` to keep everyone consistent.
- You may include plots saved to `images/`, but the auto-grader will not rely on images.

For tests, I had to use PYTHONPATH=. pytest -q to get it to work.

Data Used:

I updated the nvda_2023_sample.csv to include the entire years stock data in order to properly compare against AMD, which is also sliced for just the year 2023.

Comparison:  

Stock Comparison: NVIDIA (NVDA) vs. AMD (2023)

For this comparison, I chose AMD as the benchmark against NVIDIA since the two are direct competitors in the semiconductor industry, and both benefited from the surge in artificial intelligence demand during 2023.

I analyzed closing prices, trading volume, daily returns, and cumulative returns, along with the numerical output from the hw01.cli.

Average Daily Returns:
NVDA: 0.0054
AMD: 0.0038

Cumulative Returns:
NVDA: 2.4610
AMD: 1.3026

These numbers show that NVIDIA not only had higher average daily returns but also delivered nearly double the cumulative return compared to AMD.

Looking at the charts, both companies experienced a significant spike in May 2023 across price, trading volume, and cumulative returns. However, NVIDIA’s surge was nearly twice as large as AMD’s.

After some research, the reason for the difference in this spike was that NVDAs earnings report dramatically exceeded the expectations for that quarter, largely due to explosive demand for their GPUs powering AI applications.

AMD, while benefiting from the same AI demand, did not have the same grasp on the market in terms of AI chips, as a reult, the stock did not rise at the same maginitude that NVDA’s did.

# Stock-And-Weather-Comparisons
