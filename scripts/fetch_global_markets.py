#!/usr/bin/env python3
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import yfinance as yf

EQUITY_TICKERS = {
    "sp500": "^GSPC",
    "nasdaq100": "^NDX",
    "ftse100": "^FTSE",
    "dax": "^GDAXI",
    "nikkei225": "^N225",
    "hangseng": "^HSI",
    "kospi": "^KS11",
    "shanghai": "000001.SS",
}
MACRO_TICKERS = {
    "vix": "^VIX",
    "dxy": "DX-Y.NYB",
    "usdinr": "INR=X",
    "wti": "CL=F",
    "gold": "GC=F",
}

def read_india_dates(path):
    d = pd.read_parquet(path)
    cols = {str(c).lower().strip(): c for c in d.columns}
    ts_col = next((cols[c] for c in ("timestamp", "datetime", "date", "time") if c in cols), None)
    if ts_col is None:
        raise ValueError("No timestamp column in NIFTY50 reference")
    ts = pd.to_datetime(d[ts_col], errors="coerce")
    if getattr(ts.dt, "tz", None) is None:
        ts = ts.dt.tz_localize("Asia/Kolkata")
    else:
        ts = ts.dt.tz_convert("Asia/Kolkata")
    dates = pd.Series(ts.dt.normalize().dropna().drop_duplicates().sort_values(), name="india_date")
    return pd.DataFrame({"india_date": dates})

def download_close(ticker, start, end):
    raw = yf.download(
        ticker, start=start, end=end, interval="1d",
        auto_adjust=False, progress=False, threads=False, group_by="column"
    )
    if raw is None or raw.empty:
        raise ValueError(f"No data returned for {ticker}")
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = [c[0] for c in raw.columns]
    close = pd.to_numeric(raw["Close"], errors="coerce").dropna()
    close.index = pd.to_datetime(close.index).tz_localize(None).astype("datetime64[ns]")
    return close

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nifty50", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--start", default="2017-01-01")
    ap.add_argument("--end", default="2026-12-31")
    args = ap.parse_args()

    india = read_india_dates(args.nifty50)
    series = {}
    for name, ticker in {**EQUITY_TICKERS, **MACRO_TICKERS}.items():
        series[name] = download_close(ticker, pd.Timestamp(args.start), pd.Timestamp(args.end))
        print(name, ticker, "rows=", len(series[name]))

    idx = sorted(set().union(*[set(s.index) for s in series.values()]))
    global_daily = pd.DataFrame(index=pd.DatetimeIndex(idx))
    for name, s in series.items():
        global_daily[name] = s.reindex(global_daily.index)
        global_daily[name + "_ret"] = global_daily[name].pct_change()

    equity_ret_cols = [f"{k}_ret" for k in EQUITY_TICKERS]
    global_daily["global_median_ret"] = global_daily[equity_ret_cols].median(axis=1, skipna=True)
    global_daily["global_breadth"] = global_daily[equity_ret_cols].gt(0).mean(axis=1)
    global_daily["global_dispersion"] = global_daily[equity_ret_cols].std(axis=1)
    global_daily["vix_change"] = global_daily["vix"].pct_change()

    features = global_daily.reset_index(names="source_date")
    features["source_date"] = pd.to_datetime(features["source_date"]).astype("datetime64[ns]")
    left = india.copy()
    left["india_date_naive"] = pd.to_datetime(left["india_date"]).dt.tz_localize(None).astype("datetime64[ns]")

    cols = [
        "global_median_ret", "global_breadth", "global_dispersion",
        "vix_change", "dxy_ret", "usdinr_ret", "wti_ret", "gold_ret",
        "sp500_ret", "nasdaq100_ret", "ftse100_ret", "dax_ret",
        "nikkei225_ret", "hangseng_ret", "kospi_ret", "shanghai_ret",
    ]
    f = features[["source_date"] + cols].sort_values("source_date")
    aligned = pd.merge_asof(
        left.sort_values("india_date_naive"),
        f,
        left_on="india_date_naive",
        right_on="source_date",
        direction="backward",
        allow_exact_matches=False,
    )
    aligned["global_risk_on"] = (
        (aligned["global_breadth"] >= 0.625) &
        (aligned["vix_change"] <= 0)
    ).fillna(False).astype(int)
    aligned["india_date"] = pd.to_datetime(aligned["india_date"]).dt.strftime("%Y-%m-%d")
    keep = ["india_date", "source_date"] + cols + ["global_risk_on"]
    out = aligned[keep].copy()
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_path, index=False)
    print("wrote", out_path, "rows=", len(out), "risk_on_rate=", float(out.global_risk_on.mean()))

if __name__ == "__main__":
    main()
