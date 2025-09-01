from __future__ import annotations
import argparse, sys

try:
    from . import stocks as S, weather as W, plotting as P
    from .formatter import print_header, print_kv, print_series, to_json_payload
except ImportError:
    import stocks as S, weather as W, plotting as P
    from formatter import print_header, print_kv, print_series, to_json_payload

def _stocks_cmd(args: argparse.Namespace) -> int:
    df = S.read_stock_csv(args.input)
    rets = S.daily_simple_returns(df, price_col=args.price_col)
    metrics = {
        "avg_daily_return": S.average_daily_return(rets),
        "cumulative_return": S.cumulative_return(df, price_col=args.price_col),
        "additional_metric": None,  # placeholder; students will implement
    }
    payload = {
        "ticker": args.ticker or "UNKNOWN",
        "n_rows": int(df.shape[0]),
        "metrics": metrics,
        "first_5_returns": rets.head(5).tolist(),
    }
    # optional plot
    if args.plot_out:
        if args.plot_kind == "price_ma":
            P.plot_stock_price_ma(df, windows=tuple(args.windows), price_col=args.price_col, outfile=args.plot_out)
        elif args.plot_kind == "returns_hist":
            P.plot_returns_hist(rets, bins=args.bins, outfile=args.plot_out)

    if args.json:
        print(to_json_payload(payload))
        return 0
    print_header(f"Stock Analysis — {payload['ticker']}")
    for k, v in metrics.items():
        print_kv(k, v)
    print_series("first_5_returns", rets, head=5)
    return 0

def _weather_cmd(args: argparse.Namespace) -> int:
    df = W.read_weather_csv(args.input)
    summary = W.min_max_summary(df)
    if not summary:
        summary = {}
    sliced_means = W.slice_and_means(df, start=args.start, end=args.end)
    if sliced_means is None or (hasattr(sliced_means, 'empty') and sliced_means.empty):
        sliced_means = None
    df2 = W.add_celsius_column(df)
    if df2 is None:
        df2 = df
    seasons = W.seasonal_summaries(df)
    if not seasons:
        seasons = {}

    payload = {
        "n_rows": int(df.shape[0]),
        "summary": summary,
        "sliced_means": sliced_means,
        "has_celsius": "temperaturemax_celsius" in df2.columns,
        "seasonal_summaries": seasons,
    }
    # plotting: save if requested; show if requested
    did_plot = False
    if args.plot_out:
        P.plot_weather_tmax_and_celsius(df2, outfile=args.plot_out)
        did_plot = True
    if args.show:
        # If we didn't save (no figure created yet), create the plot first.
        if not did_plot:
            P.plot_weather_tmax_and_celsius(df2, outfile=None)
        # Show the current figure(s)
        try:
            import matplotlib.pyplot as plt
            plt.show()
        except Exception as e:
            print(f"[warn] Unable to show plot window: {e}")

    if args.json:
        print(to_json_payload(payload))
        return 0
    print_header("Weather Analysis")
    if summary:
        for k, v in summary.items():
            print_kv(k, v, places=4 if "min" in k else 2)
    if sliced_means is not None:
        print_series("sliced_means", sliced_means)
    if seasons:
        print_series("seasonal_summaries", seasons)
    return 0

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="hw01", description="CSCI 4170/6170 F25 Lab+HW 01 CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("stocks", help="Analyze a stock CSV")
    sp.add_argument("--input", required=True, help="Path to stock CSV")
    sp.add_argument("--ticker", required=False, help="Ticker symbol (for labeling only)")
    sp.add_argument("--price-col", default="Adj Close", help="Price column to use (default: Adj Close)")
    sp.add_argument("--risk-free", type=float, default=0.015, help="Annual risk-free rate (e.g., 0.015 for 1.5%)")
    sp.add_argument("--json", action="store_true", help="Emit JSON for autograder")
    # plotting
    sp.add_argument("--plot-out", help="Path to save plot (PNG). If omitted, no plot is saved.")
    sp.add_argument("--plot-kind", choices=["price_ma", "returns_hist"], default="price_ma")
    sp.add_argument("--windows", nargs="+", type=int, default=[20, 50], help="MA windows (price_ma only)")
    sp.add_argument("--bins", type=int, default=30, help="Bins for returns_hist")
    sp.set_defaults(func=_stocks_cmd)

    wp = sub.add_parser("weather", help="Analyze a weather CSV")
    wp.add_argument("--input", required=True, help="Path to weather CSV")
    wp.add_argument("--start", default="2022-01-10", help="Slice start date")
    wp.add_argument("--end", default="2022-01-20", help="Slice end date")
    wp.add_argument("--json", action="store_true", help="Emit JSON for autograder")
    # plotting
    wp.add_argument("--plot-out", help="Path to save plot (PNG). If omitted, no plot is saved.")
    # normal behaviour: --show turns the window on (default = off)
    wp.add_argument("--show", action="store_true", help="Display the weather plot in a window")
    wp.set_defaults(func=_weather_cmd)

    return p

def main(argv=None) -> int:
    argv_stocksv = [
        "stocks",
        "--input",  "data/NVDA.csv",
        "--ticker", "NVDA",
    ]
    argv_weatherv = [
        "weather",
        "--input", "data/weather_small.csv",
        "--start", "2022-01-10",
        "--end", "2022-01-20",
        "--plot-out", "images/weather.png",
    ]

    argv = sys.argv[1:] if argv is None else argv
    # If no args are supplied (e.g., running via PyCharm green arrow),
    # fall back to a safe default demo command so it "just works".
    # python -m hw01.cli stocks --input data/NVDA.csv --ticker NVDA
    # python -m hw01.cli weather --input data/rdu-weather-history.csv --plot-out images/weather.png

    if not argv:
        arg_s   = argv_stocksv
        argv_w  = argv_weatherv
        argv = argv_w

        print("[dev] No args supplied; using defaults:", " ".join(argv))
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
