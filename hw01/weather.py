from __future__ import annotations
import pandas as pd

def read_weather_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "date" not in df.columns:
        raise ValueError("Expected a 'date' column in weather CSV.")
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date").set_index("date")

def min_max_summary(df: pd.DataFrame) -> dict:
    """
    Compute the mean and median of temperaturemin and temperaturemax.

    HINTS:
    - Use df["temperaturemin"] and df["temperaturemax"].
    - Drop NaNs before computing statistics.
    - Return a dict with keys "mean_temperaturemin", "median_temperaturemin", etc.
    """
    fn = "[min_max_summary]"

    tempmin = df['temperaturemin'].dropna()
    tempmax = df['temperaturemax'].dropna()

    #["mean_temperaturemin", "median_temperaturemin", "mean_temperaturemax", "median_temperaturemax"]

    summary = {
        
      'mean_temperaturemin': tempmin.mean().round(4),
      'median_temperaturemin':tempmin.median(),
      'mean_temperaturemax': tempmax.mean().round(4),
      'median_temperaturemax': tempmax.median()
    }

    return summary


def add_celsius_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a new column with the max temperature converted from °F to °C.

    HINTS:
    - Make a copy of the DataFrame first.
    - Formula reminder: °C = (°F − 32) × 5/9.
    - Return the modified DataFrame.
    """
    fn = "[add_celsius_column]"

    df_copy = df.copy()
    df_copy['temperaturemax_celsius'] = (df_copy['temperaturemax'] - 32) * 5 / 9    

    return df_copy

def slice_and_means(df: pd.DataFrame, start: str, end: str, cols=("temperaturemax", "precipitation")) -> pd.Series:
    """
    Select a date range and compute the mean of chosen columns.

    HINTS:
    - Use .loc[start:end, cols] to slice the rows and columns.
    - Then compute the mean on that subset.
    - Return a pandas Series of mean values.
    """
    fn = "[slice_and_means]"


    df_range = df.loc[start: end , ['temperaturemax', 'precipitation']]

    range_means = df_range.mean()

    return range_means

def seasonal_summaries(df: pd.DataFrame) -> dict:
    """
    NOTE: Homework-only. For the lab, leave a placeholder.

    Goal:
    - For each season in each "season_year", compute the mean and median of `temperaturemin` and `temperaturemax`, and record the date range covered by that slice.

    Preconditions:
    - `df.index` is a `DatetimeIndex`.
    - `df` includes columns `temperaturemin` and `temperaturemax`.

    Dictionary refresher (nested dicts):
    - Literal: `d = {}` for empty; `d = {'a': 1}` for one key.
    - Access: `d[key]`; safe access: `d.get(key, default)`.
    - Insert/update: `d[key] = value`.
    - Build nested dicts safely with `setdefault`:
      `out.setdefault(year, {})[season] = payload`
    - Iterate in order: `for y in sorted(out): ...`.
    - Types here: outer keys = int years, inner keys = str season names, leaves = floats/strings per spec.

    HINTS (step-by-step):
    1) Derive `months = df.index.month`.
    2) Create a `season` Series aligned to the index using month rules:
       - Spring = 3–5, Summer = 6–8, Fall = 9–11, Winter = 12, 1, 2.
    3) Define `season_year` so Winter is labeled by the January year:
       - `season_year = df.index.year + (months == 12).astype(int)`.
    4) Build a helper frame `meta = pd.DataFrame({'season_year': season_year, 'season': season}, index=df.index)`.
    5) Group and compute per-slice stats:
       - Loop: `for (yr, sn), grp in meta.groupby(['season_year','season'], sort=True):`
         * `sub = df.loc[grp.index]`
         * `tmin = sub['temperaturemin'].dropna()` and `tmax = sub['temperaturemax'].dropna()`
         * Compute `mean` and `median` for both; cast to `float`.
         * `date_min = sub.index.min().strftime('%Y-%m-%d')`, `date_max = sub.index.max().strftime('%Y-%m-%d')`.
         * Use `out.setdefault(int(yr), {})[sn] = { ... }` to build the nested dict.
    6) Skip empty slices; if a series is empty, set its stats to `float('nan')`.
    7) Do not mutate `df`. Return the nested dict.

    Output shape:
    {
      2022: {
        'Winter': { 'date_min': 'YYYY-MM-DD', 'date_max': 'YYYY-MM-DD',
                    'mean_temperaturemin': float, 'median_temperaturemin': float,
                    'mean_temperaturemax': float, 'median_temperaturemax': float },
        'Spring': {...}, 'Summer': {...}, 'Fall': {...}
      },
      2023: { ... }
    }
    """
    fn = "[seasonal_summaries]"
    
    # Get the year from the data (assuming single year)
    year = df.index.year[0]
    
    # Initialize output dictionary for this year
    out = {int(year): {}}
    
    # season date ranges for the year
    seasons = {
        'Winter': (f'{year}-12-01', f'{year+1}-02-28'),
        'Spring': (f'{year}-03-01', f'{year}-05-31'),
        'Summer': (f'{year}-06-01', f'{year}-08-31'),
        'Fall': (f'{year}-09-01', f'{year}-11-30')
    }
    
    # Process each season
    for season_name, (start_date, end_date) in seasons.items():
        
        if season_name == 'Winter':
            winter_data = df[
                ((df.index.year == year) & (df.index.month == 12)) |
                ((df.index.year == year + 1) & (df.index.month.isin([1, 2])))
            ]
            sub = winter_data
        else:
            # Other seasons are within the same year
            sub = df.loc[start_date:end_date]
        
        # Skip if no data for this season
        if len(sub) == 0:
            continue
            
        tmin = sub['temperaturemin'].dropna()
        tmax = sub['temperaturemax'].dropna()
        
        mean_tmin = float(tmin.mean())
        median_tmin = float(tmin.median())
     
            
        mean_tmax = float(tmax.mean())
        median_tmax = float(tmax.median())
  
        
        date_min = sub.index.min().strftime('%Y-%m-%d')
        date_max = sub.index.max().strftime('%Y-%m-%d')
        
        payload = {
            'date_min': date_min,
            'date_max': date_max,
            'mean_temperaturemin': mean_tmin,
            'median_temperaturemin': median_tmin,
            'mean_temperaturemax': mean_tmax,
            'median_temperaturemax': median_tmax
        }
        
        # Add to output dictionary
        out[int(year)][season_name] = payload
    
    return out
