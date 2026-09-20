#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

PRIMARY = {
    "sp500": "^GSPC",
    "nasdaq100": "^NDX",
    "dax": "^GDAXI",
    "nikkei": "^N225",
    "hangseng": "^HSI",
}
SECONDARY = {
    "ftse100": "^FTSE",
    "kospi": "^KS11",
    "cac40": "^FCHI",
    "vix": "^VIX",
    "usdinr": "USDINR=X",
    "brent": "BZ=F",
    "gold": "GC=F",
}
TARGETS = {
    "nifty50": "^NSEI",
    "sensex": "^BSESN",
}

TRAIN_START = "2006-01-01"
TRAIN_END = "2023-12-31"
VAL_START = "2024-01-01"
VAL_END = "2025-12-31"
TEST_START = "2026-01-01"


def normalize_download(frame: pd.DataFrame) -> pd.DataFrame:
    if isinstance(frame.columns, pd.MultiIndex):
        frame = frame.copy()
        frame.columns = frame.columns.get_level_values(0)
    cols = {str(c).strip().lower(): c for c in frame.columns}
    date_col = cols.get("date")
    close_col = cols.get("close")
    if date_col is not None:
        idx = pd.to_datetime(frame[date_col], errors="coerce")
    else:
        idx = pd.to_datetime(frame.index, errors="coerce")
    if close_col is None:
        raise ValueError("No Close column found")
    close = pd.to_numeric(frame[close_col], errors="coerce")
    out = pd.DataFrame({"close": close.to_numpy()}, index=idx)
    out = out[~out.index.isna()].sort_index()
    out = out[~out.index.duplicated(keep="last")]
    out["close"] = pd.to_numeric(out["close"], errors="coerce")
    out = out.dropna(subset=["close"])
    if getattr(out.index, "tz", None) is not None:
        out.index = out.index.tz_localize(None)
    return out


def download_or_cache(cache_dir: Path, refresh: bool) -> dict:
    try:
        import yfinance as yf
    except Exception as exc:
        raise RuntimeError("yfinance is required for download mode") from exc

    cache_dir.mkdir(parents=True, exist_ok=True)
    all_symbols = {**PRIMARY, **SECONDARY, **TARGETS}
    out = {}
    for name, ticker in all_symbols.items():
        path = cache_dir / f"{name}.csv"
        if path.exists() and not refresh:
            out[name] = str(path)
            continue
        try:
            raw = yf.download(
                ticker,
                start="2000-01-01",
                end=(pd.Timestamp.utcnow() + pd.Timedelta(days=2)).strftime("%Y-%m-%d"),
                auto_adjust=False,
                progress=False,
                actions=False,
                threads=False,
            )
            if raw is None or raw.empty:
                raise RuntimeError("empty response")
            norm = normalize_download(raw)
            if len(norm) < 100:
                raise RuntimeError(f"only {len(norm)} rows")
            norm.to_csv(path, index_label="date")
            out[name] = str(path)
        except Exception as exc:
            print(f"DOWNLOAD_FAIL {name} {ticker}: {exc}")
    return out


def load_cached(paths: dict) -> dict:
    data = {}
    for name, path in paths.items():
        p = Path(path)
        d = pd.read_csv(p, parse_dates=["date"]).set_index("date")
        d["close"] = pd.to_numeric(d["close"], errors="coerce")
        d = d.dropna(subset=["close"]).sort_index()
        data[name] = d
    return data


def returns(data: dict) -> pd.DataFrame:
    cols = {}
    for name, d in data.items():
        cols[name] = d["close"].pct_change()
    return pd.DataFrame(cols).sort_index()


def make_consensus(global_ret: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in PRIMARY if c in global_ret.columns]
    if len(cols) < len(PRIMARY):
        raise RuntimeError(f"Missing primary global series: expected {list(PRIMARY)}, got {cols}")
    r = global_ret[cols].copy()
    score = np.sign(r).sum(axis=1)
    out = pd.DataFrame(
        {
            "consensus_score": score,
            "global_positive": score >= 3,
            "global_negative": score <= -3,
            **{f"{c}_ret": r[c] for c in cols},
        }
    )
    out.index.name = "date"
    return out.dropna(subset=[f"{c}_ret" for c in cols])


def summarize_target(target_ret: pd.Series, consensus: pd.DataFrame, start: str, end: str) -> dict:
    x = consensus.join(target_ret.rename("target_ret"), how="inner").loc[start:end].copy()

    def stats(s):
        s = s.dropna()
        if len(s) == 0:
            return {"n": 0}
        return {
            "n": int(len(s)),
            "mean_pct": float(100 * s.mean()),
            "median_pct": float(100 * s.median()),
            "win_rate": float((s > 0).mean()),
            "sd_pct": float(100 * s.std(ddof=1)) if len(s) > 1 else None,
        }

    all_s = stats(x["target_ret"])
    hi_s = stats(x.loc[x["global_positive"], "target_ret"])
    lo_s = stats(x.loc[x["global_negative"], "target_ret"])
    diff = None if hi_s["n"] == 0 or lo_s["n"] == 0 else hi_s["mean_pct"] - lo_s["mean_pct"]
    return {
        "all": all_s,
        "consensus_ge_3": hi_s,
        "consensus_le_minus_3": lo_s,
        "high_minus_low_mean_pct_points": diff,
    }


def pilot(data: dict, out_dir: Path) -> dict:
    g = returns({k: data[k] for k in PRIMARY if k in data})
    c = make_consensus(g)
    reports = {}
    for target_name in ("nifty50", "sensex"):
        if target_name in data:
            target_ret = data[target_name]["close"].pct_change()
            reports[target_name] = {
                "train": summarize_target(target_ret, c, TRAIN_START, TRAIN_END),
                "validation": summarize_target(target_ret, c, VAL_START, VAL_END),
                "test": summarize_target(target_ret, c, TEST_START, "2099-12-31"),
            }
    c.reset_index().to_csv(out_dir / "global_consensus_daily.csv", index=False)
    return reports


def phase9_diagnostic(panel_path: Path, consensus: pd.DataFrame, out_dir: Path) -> dict:
    p = pd.read_csv(panel_path)
    date_col = "signal_ts" if "signal_ts" in p.columns else "signal_date"
    if date_col not in p.columns:
        raise ValueError("Phase 9 panel has no signal_ts or signal_date")
    dt = pd.to_datetime(p[date_col], errors="coerce", utc=True).dt.tz_convert(None).dt.normalize()
    p["signal_day"] = dt
    c = consensus.copy()
    c.index = pd.to_datetime(c.index).normalize()
    p = p.merge(c.reset_index(), left_on="signal_day", right_on="date", how="left")
    if "baseline_ret" not in p.columns:
        raise ValueError("Phase 9 panel does not contain baseline_ret")
    test = p[p["signal_day"] >= TEST_START].copy()

    def stats(s):
        s = pd.to_numeric(s, errors="coerce").dropna()
        if len(s) == 0:
            return {"n": 0}
        return {
            "n": int(len(s)),
            "mean_ret_pct": float(100 * s.mean()),
            "median_ret_pct": float(100 * s.median()),
            "win_rate": float((s > 0).mean()),
            "sum_ret_pct": float(100 * s.sum()),
        }

    result = {
        "diagnostic_only": True,
        "reason": "The source Phase 9 panel is not authoritative until the corrected Phase 9 workflow artifact is observed.",
        "all_baseline": stats(test["baseline_ret"]),
        "global_ge_3_baseline": stats(test.loc[test["consensus_score"] >= 3, "baseline_ret"]),
        "global_lt_3_baseline": stats(test.loc[test["consensus_score"] < 3, "baseline_ret"]),
    }
    if "mc_ret" in test.columns:
        result["all_mc_accepted"] = stats(test["mc_ret"])
        result["global_ge_3_mc_accepted"] = stats(test.loc[test["consensus_score"] >= 3, "mc_ret"])
    test.to_csv(out_dir / "phase9_global_joined_diagnostic.csv", index=False)
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--global-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--download", action="store_true")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--phase9-panel", default="")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = Path(args.global_dir)
    paths = download_or_cache(cache_dir, refresh=args.refresh) if args.download else {
        p.stem: str(p) for p in cache_dir.glob("*.csv")
    }
    required = [x for x in PRIMARY if x not in paths]
    if required:
        raise RuntimeError(f"Primary global series missing: {required}")
    data = load_cached(paths)
    reports = pilot(data, out_dir)
    consensus = make_consensus(returns({k: data[k] for k in PRIMARY}))
    result = {
        "pilot": reports,
        "primary_series": PRIMARY,
        "secondary_series": SECONDARY,
        "targets": TARGETS,
        "train": [TRAIN_START, TRAIN_END],
        "validation": [VAL_START, VAL_END],
        "test": [TEST_START, "latest"],
        "candidate_rule": "prior-session five-market sign consensus >= +3 for LONG participation",
        "latest_primary_common_date": str(consensus.index.max().date()) if len(consensus) else None,
    }
    if args.phase9_panel:
        result["phase9_diagnostic"] = phase9_diagnostic(Path(args.phase9_panel), consensus, out_dir)
    (out_dir / "phase10_summary.json").write_text(json.dumps(result, indent=2, default=str))
    (out_dir / "provenance.json").write_text(
        json.dumps(
            {
                "source": "Yahoo Finance via yfinance for workflow execution",
                "raw_data_policy": "runner cache only; no raw market files committed",
                "rule": result["candidate_rule"],
                "primary_cost_gate_bps_per_leg": [5, 10],
                "data_end": result["latest_primary_common_date"],
            },
            indent=2,
        )
    )
    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
