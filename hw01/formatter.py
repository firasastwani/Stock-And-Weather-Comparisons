from __future__ import annotations
from dataclasses import dataclass, asdict
import json
import pandas as pd
from typing import Any, Mapping

DEC_PLACES_DEFAULT = 4
DEC_PLACES_VOL = 6

def print_header(title: str) -> None:
    print(f"=== {title} ===")


def print_kv(name: str, value: float, places: int = DEC_PLACES_DEFAULT) -> None:
    """
    Print a key/value pair, showing numbers with fixed decimal places.
    If *value* is None, NaN, or not a real number, print "N/A" instead
    of raising a formatting error.
    """
    if value is None:
        sval = "N/A"
    else:
        try:
            import math
            if isinstance(value, (int, float)) and math.isfinite(value):
                fmt = f"{{:.{places}f}}"
                sval = fmt.format(value)
            else:
                sval = "N/A"
        except Exception:
            sval = "N/A"
    print(f"{name}: {sval}")


def _is_nested_mapping(obj: Mapping[str, Any]) -> bool:
    """True if every value in `obj` is itself a Mapping (dict-of-dicts)."""
    return bool(obj) and all(isinstance(v, Mapping) for v in obj.values())

def print_series(
    name: str,
    s: Any,
    places: int = DEC_PLACES_DEFAULT,
    head: int | None = None,
) -> None:
    """
    Pretty-print a pandas Series OR various Mapping shapes.

    Supported inputs:
    • pd.Series               – tabular print (old behaviour)
    • Mapping → scalar        – auto-Series, then tabular
    • Mapping → Mapping       – hierarchical pretty print (seasons example)
    Anything else falls back to str(s).
    """
    print(f"[{name}]")

    # ----- 1. special case: nested dict (=dict-of-dict) -----
    if isinstance(s, Mapping) and _is_nested_mapping(s):
        fmt_num = f"{{:.{places}f}}".format
        for top_key in sorted(s.keys()):
            print(top_key)  # e.g. 2022
            inner: Mapping[str, Any] = s[top_key]
            for inner_key in sorted(inner.keys()):
                leaf: Mapping[str, Any] = inner[inner_key]
                date_min = leaf.get("date_min", "")
                date_max = leaf.get("date_max", "")
                rng = (
                    f" ({date_min} → {date_max})"
                    if date_min and date_max
                    else ""
                )
                print(f"  {inner_key}{rng}")  # e.g. "  Winter (…)"
                for k, v in leaf.items():
                    if k in {"date_min", "date_max"}:
                        continue  # already shown
                    try:
                        sval = fmt_num(float(v))
                    except Exception:
                        sval = str(v)
                    print(f"    {k:<22}= {sval}")
        return

    # ----- 2. Everything else: fall back to old logic -----
    if isinstance(s, Mapping):
        s = pd.Series(s)
    elif not isinstance(s, pd.Series):
        try:
            s = pd.Series(s)
        except Exception:
            print(str(s))
            return

    if head is not None:
        s = s.head(head)

    fmt_num = f"{{:.{places}f}}".format
    df = s.reset_index()

    if df.shape[1] == 2:
        idx_name, val_name = df.columns[0], df.columns[1]
        print(f"{idx_name:<12} {val_name}")
        for _, row in df.iterrows():
            idx = str(row[idx_name])
            val = row[val_name]
            try:
                sval = fmt_num(float(val))
            except Exception:
                sval = str(val)
            print(f"{idx:<12} {sval}")
    else:
        print(s.to_string())


def to_json_payload(payload: Mapping[str, Any]) -> str:
    def _sanitize(obj):
        if isinstance(obj, pd.Series):
            return obj.to_dict()
        if isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient="list")
        if hasattr(obj, "item"):
            try:
                return obj.item()
            except Exception:
                pass
        return obj

    clean = {k: _sanitize(v) for k, v in payload.items()}
    return json.dumps(clean, sort_keys=True, ensure_ascii=False)


@dataclass
class StockMetrics:
    avg_daily_return: float
    cumulative_return: float
    annualized_volatility: float
    sharpe_ratio: float

    def as_dict(self) -> dict[str, float]:
        return asdict(self)
