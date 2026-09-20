#!/usr/bin/env python3
import argparse, json, math, zlib
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

FRICTIONS = [0.0, 5.0, 10.0]
VALIDATION_START = pd.Timestamp("2025-01-01", tz="Asia/Kolkata")
VALIDATION_END = pd.Timestamp("2025-12-31 23:59:59", tz="Asia/Kolkata")
TEST_START = pd.Timestamp("2026-01-01", tz="Asia/Kolkata")

def ema(s, n):
    return s.ewm(span=n, adjust=False, min_periods=n).mean()

def atr(df, n=14):
    prev = df["close"].shift(1)
    tr = pd.concat([
        df["high"] - df["low"],
        (df["high"] - prev).abs(),
        (df["low"] - prev).abs()
    ], axis=1).max(axis=1)
    return tr.ewm(alpha=1.0/n, adjust=False, min_periods=n).mean()

def cost_intraday(buy, sell, friction_bps):
    turnover = buy + sell
    brokerage = 40.0
    exchange = turnover * 0.0000307
    sebi = turnover * 0.000001
    gst = 0.18 * (brokerage + exchange + sebi)
    stt = sell * 0.00025
    stamp = buy * 0.00003
    return brokerage + exchange + sebi + gst + stt + stamp + turnover * friction_bps / 10000.0

def mc_gate(history, seed):
    if len(history) < 20:
        return True
    hist = np.asarray(history[-30:], dtype=float)
    rng = np.random.default_rng(seed)
    draws = rng.choice(hist, size=(250, len(hist)), replace=True)
    terminal_positive = np.prod(1.0 + draws, axis=1) > 1.0
    return int(terminal_positive.sum()) >= 125

def normalize_intraday(df):
    cols = {str(c).lower().strip(): c for c in df.columns}
    ts_col = next((cols[c] for c in ("timestamp", "datetime", "date", "time") if c in cols), None)
    if ts_col is None:
        raise ValueError(f"No timestamp column in {list(df.columns)}")
    rename = {}
    for want in ("open", "high", "low", "close", "volume"):
        if want in cols:
            rename[cols[want]] = want
    df = df.rename(columns=rename).copy()
    required = {"open", "high", "low", "close"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing OHLC columns: {sorted(missing)}")
    ts = pd.to_datetime(df[ts_col], errors="coerce")
    if getattr(ts.dt, "tz", None) is None:
        # Ganesh files are expected to be exchange-local. If the first bars look
        # like UTC timestamps, convert them instead.
        first = ts.dropna().dt.hour.head(50)
        if len(first) and (first.between(3, 5).mean() > 0.6):
            ts = ts.dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")
        else:
            ts = ts.dt.tz_localize("Asia/Kolkata")
    else:
        ts = ts.dt.tz_convert("Asia/Kolkata")
    df["ts"] = ts
    keep = ["ts", "open", "high", "low", "close"] + (["volume"] if "volume" in df.columns else [])
    df = df[keep].dropna(subset=["ts", "open", "high", "low", "close"])
    for c in ("open", "high", "low", "close", "volume"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["open", "high", "low", "close"]).sort_values("ts")
    df = df[(df["ts"].dt.time >= pd.Timestamp("09:15").time()) &
            (df["ts"].dt.time <= pd.Timestamp("15:30").time())]
    return df.set_index("ts")

def read_symbol(paths):
    frames = []
    for p in paths:
        if Path(p).exists() and Path(p).stat().st_size > 0:
            frames.append(pd.read_parquet(p))
    if not frames:
        return pd.DataFrame()
    return normalize_intraday(pd.concat(frames, ignore_index=True))

def resample_15m(raw):
    agg = {
        "open": "first", "high": "max", "low": "min",
        "close": "last"
    }
    if "volume" in raw.columns:
        agg["volume"] = "sum"
    out = raw.resample(
        "15min", origin="start_day", offset="15min",
        label="left", closed="left"
    ).agg(agg)
    return out.dropna(subset=["open", "high", "low", "close"])

def daily_features(m15):
    d = m15.resample("1D").agg({
        "open": "first", "high": "max", "low": "min",
        "close": "last", "volume": "sum"
    }).dropna(subset=["close"])
    d["ret1"] = d["close"].pct_change()
    prev = d["close"].shift(1)
    d["gap"] = d["open"] / prev - 1
    traded_value = d["close"] * d["volume"]
    d["adv20"] = traded_value.rolling(20, min_periods=20).mean().shift(1)
    d["adv60"] = traded_value.rolling(60, min_periods=60).mean().shift(1)
    d["vol20"] = d["ret1"].rolling(20, min_periods=20).std().shift(1)
    d["atr_pct"] = (atr(d) / d["close"]).shift(1)
    e20 = ema(d["close"], 20)
    e50 = ema(d["close"], 50)
    d["trend"] = (e20 / e50 - 1).shift(1)
    d["mom20"] = d["close"].pct_change(20).shift(1)
    mean_v = d["volume"].rolling(20, min_periods=20).mean()
    std_v = d["volume"].rolling(20, min_periods=20).std()
    d["vol_z"] = ((d["volume"] - mean_v) / std_v).shift(1)
    return d

def simulate(m15, features, symbol, friction_bps, use_mc, use_global_gate=False):
    d = m15.copy()
    d["e20"] = ema(d["close"], 20)
    d["e26"] = ema(d["close"], 26)
    d["atr14"] = atr(d, 14)

    equity = 100000.0
    peak = equity
    max_dd = 0.0
    history = []
    trades = []
    seed = zlib.crc32(symbol.encode()) & 0xffffffff
    test_started = False

    for i in range(27, len(d) - 1):
        r = d.iloc[i]
        if not (np.isfinite(r["e20"]) and np.isfinite(r["e26"]) and np.isfinite(r["atr14"])):
            continue

        # Frozen Phase-7 intraday rule is LONG ONLY.
        cross_up = bool(r["e20"] > r["e26"] and d["e20"].iloc[i-1] <= d["e26"].iloc[i-1])
        if not cross_up:
            continue

        signal_ts = d.index[i]
        if signal_ts >= TEST_START and not test_started:
            # OOS equity is reset at the test boundary so historical
            # compounding, splits and early-sample path dependence cannot
            # contaminate the 2026 evaluation capital.
            equity = 100000.0
            peak = equity
            max_dd = 0.0
            test_started = True

        feature_row = features.loc[signal_ts.normalize()] if signal_ts.normalize() in features.index else None
        factor = feature_row.to_dict() if feature_row is not None else {}

        if use_global_gate and int(factor.get("global_risk_on", 0) or 0) != 1:
            continue

        accepted = (not use_mc) or mc_gate(history, seed)
        if not accepted:
            continue

        entry_i = i + 1
        entry = float(d["open"].iloc[entry_i])
        qty = int(equity // entry)
        if qty <= 0:
            continue

        stop = entry - 1.5 * float(r["atr14"])
        exit_i = None
        exit_px = None
        reason = None

        last_i = min(len(d) - 1, entry_i + 20 - 1)
        for j in range(entry_i, last_i + 1):
            bar = d.iloc[j]
            if bar["low"] <= stop:
                exit_i = j
                exit_px = float(bar["open"]) if bar["open"] < stop else float(stop)
                reason = "stop"
                break
            if j == last_i:
                exit_i = j
                exit_px = float(bar["close"])
                reason = "time"

        buy_value = entry * qty
        sell_value = exit_px * qty
        gross = (exit_px - entry) * qty
        net = gross - cost_intraday(buy_value, sell_value, friction_bps)
        ret = net / equity
        equity += net
        peak = max(peak, equity)
        max_dd = min(max_dd, equity / peak - 1.0)
        history.append(ret)

        trades.append({
            "symbol": symbol,
            "signal_ts": str(signal_ts),
            "signal_date": str(signal_ts.date()),
            "entry_ts": str(d.index[entry_i]),
            "exit_ts": str(d.index[exit_i]),
            "net": net,
            "ret": ret,
            "exit_reason": reason,
            "global_gate_used": int(use_global_gate),
            **factor
        })

    return trades, max_dd

def summarize(trades, max_dd):
    if not trades:
        return {
            "n": 0, "return_pct": 0.0, "pf": None,
            "win_rate": None, "maxdd_pct": float(max_dd * 100.0)
        }
    n = np.asarray([t["net"] for t in trades], dtype=float)
    wins = n[n > 0]
    losses = n[n < 0]
    return {
        "n": int(len(n)),
        "return_pct": float(n.sum() / 1000.0),
        "pf": float(wins.sum() / -losses.sum()) if len(losses) else None,
        "win_rate": float((n > 0).mean()),
        "maxdd_pct": float(max_dd * 100.0)
    }

def factor_tests(panel):
    if panel.empty:
        return {}, pd.DataFrame()
    factors = [
        "adv20", "adv60", "vol20", "atr_pct",
        "trend", "mom20", "vol_z", "gap"
    ]
    available = [f for f in factors if f in panel.columns]
    test = panel.replace([np.inf, -np.inf], np.nan).dropna(subset=available).copy()
    if len(test) < 50:
        return {"status": "insufficient", "n": len(test)}, pd.DataFrame()

    quintiles = []
    for factor in available:
        q = test[[factor, "baseline_ret", "mc_ret"]].dropna().copy()
        if q.empty:
            continue
        try:
            q["quintile"] = pd.qcut(q[factor], 5, labels=False, duplicates="drop") + 1
        except Exception:
            continue
        for k, g in q.groupby("quintile"):
            mcvals = g["mc_ret"].dropna()
            basevals = g["baseline_ret"].dropna()
            quintiles.append({
                "factor": factor, "quintile": int(k), "n": len(g),
                "baseline_mean_ret": float(basevals.mean()) if len(basevals) else np.nan,
                "mc_mean_ret": float(mcvals.mean()) if len(mcvals) else np.nan,
                "mc_positive_rate": float((mcvals > 0).mean()) if len(mcvals) else np.nan,
                "mc_vs_baseline_mean": float((mcvals.mean() - basevals.mean()))
                    if len(mcvals) and len(basevals) else np.nan
            })

    model_cols = available + ["market_vol20", "market_trend20", "breadth", "dispersion"]
    model_cols = [c for c in model_cols if c in test.columns]
    if len(model_cols) < 2:
        return {"status": "no_regression_factors", "n": len(test)}, pd.DataFrame(quintiles)

    out = []
    X = test[model_cols].copy()
    y = test["mc_return"].notna().astype(int)
    for c in model_cols:
        s = X[c].std()
        X[c] = (X[c] - X[c].mean()) / (s if np.isfinite(s) and s else 1.0)
    X = sm.add_constant(X, has_constant="add")
    try:
        logit = sm.GLM(y, X, family=sm.families.Binomial()).fit(cov_type="HC3")
        for c in model_cols:
            out.append({
                "model": "MC_acceptance",
                "factor": c,
                "coef": float(logit.params[c]),
                "p": float(logit.pvalues[c])
            })
    except Exception as exc:
        return {"error": repr(exc), "n": len(test)}, pd.DataFrame(quintiles)

    accepted = test[test["mc_return"].notna()].dropna(subset=["mc_return"])
    if len(accepted) >= 50:
        Xa = accepted[model_cols].copy()
        for c in model_cols:
            s = Xa[c].std()
            Xa[c] = (Xa[c] - Xa[c].mean()) / (s if np.isfinite(s) and s else 1.0)
        Xa = sm.add_constant(Xa, has_constant="add")
        ols = sm.OLS(accepted["mc_return"], Xa).fit(cov_type="HC3")
        for c in model_cols:
            out.append({
                "model": "MC_trade_return",
                "factor": c,
                "coef": float(ols.params[c]),
                "p": float(ols.pvalues[c])
            })

    pvals = np.asarray([x["p"] for x in out], dtype=float)
    _, qvals, _, _ = multipletests(pvals, alpha=0.05, method="fdr_bh")
    for row, q in zip(out, qvals):
        row["fdr_p"] = float(q)
        row["fdr_significant"] = bool(q < 0.05)

    return {"n": len(test), "tests": out}, pd.DataFrame(quintiles)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols-file", required=True)
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--nifty50", required=True)
    ap.add_argument("--global-markets", default="")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    symbols = [x.strip() for x in Path(args.symbols_file).read_text().splitlines() if x.strip()]

    nifty = pd.read_parquet(args.nifty50)
    nifty = normalize_intraday(nifty)
    nifty15 = resample_15m(nifty)
    nifty_daily = nifty15.resample("1D").agg({
        "open": "first", "high": "max", "low": "min",
        "close": "last", "volume": "sum"
    }).dropna(subset=["close"])
    nifty_daily["market_vol20"] = nifty_daily["close"].pct_change().rolling(20, min_periods=20).std().shift(1)
    me20 = ema(nifty_daily["close"], 20)
    me50 = ema(nifty_daily["close"], 50)
    nifty_daily["market_trend20"] = (me20 / me50 - 1).shift(1)

    global_features = pd.DataFrame()
    if args.global_markets:
        global_features = pd.read_csv(args.global_markets)
        global_features["date"] = pd.to_datetime(global_features["india_date"]).dt.tz_localize("Asia/Kolkata")
        global_features = global_features.drop(columns=["india_date"], errors="ignore").set_index("date").sort_index()

    all_results = []
    panel_rows = []
    daily_rows = []
    failures = []

    for symbol in symbols:
        try:
            files = [
                str(Path(args.data_dir) / "base" / f"{symbol}.parquet"),
                str(Path(args.data_dir) / "y2026" / f"{symbol}.parquet")
            ]
            raw = read_symbol(files)
            if len(raw) < 2000:
                failures.append({"symbol": symbol, "error": "insufficient rows"})
                continue

            m15 = resample_15m(raw)
            features = daily_features(m15)
            if not global_features.empty:
                features = features.join(global_features, how="left")
                features["global_gap_nifty_minus_world"] = (
                    features["ret1"] - features["global_median_ret"]
                )
            else:
                features["global_gap_nifty_minus_world"] = np.nan
                features["global_risk_on"] = 0
            if len(m15) < 100:
                failures.append({"symbol": symbol, "error": "insufficient 15m bars"})
                continue

            # Build baseline, MC and the pre-specified global risk-on gate at each friction level.
            for friction in FRICTIONS:
                base_trades, base_dd = simulate(m15, features, symbol, friction, False, False)
                mc_trades, mc_dd = simulate(m15, features, symbol, friction, True, False)
                base_global_trades, base_global_dd = simulate(m15, features, symbol, friction, False, True)
                mc_global_trades, mc_global_dd = simulate(m15, features, symbol, friction, True, True)

                def select_test(ts):
                    return TEST_START <= pd.Timestamp(ts) <= raw.index.max()

                bt = [t for t in base_trades if select_test(t["signal_ts"])]
                mt = [t for t in mc_trades if select_test(t["signal_ts"])]
                bgt = [t for t in base_global_trades if select_test(t["signal_ts"])]
                mgt = [t for t in mc_global_trades if select_test(t["signal_ts"])]

                # 2025 validation + 2026 test statistics.
                bv = [t for t in base_trades if VALIDATION_START <= pd.Timestamp(t["signal_ts"]) <= VALIDATION_END]
                mv = [t for t in mc_trades if VALIDATION_START <= pd.Timestamp(t["signal_ts"]) <= VALIDATION_END]
                bgv = [t for t in base_global_trades if VALIDATION_START <= pd.Timestamp(t["signal_ts"]) <= VALIDATION_END]
                mgv = [t for t in mc_global_trades if VALIDATION_START <= pd.Timestamp(t["signal_ts"]) <= VALIDATION_END]

                bstats = summarize(bt, base_dd)
                mstats = summarize(mt, mc_dd)
                bgstats = summarize(bgt, base_global_dd)
                mgstats = summarize(mgt, mc_global_dd)
                vbstats = summarize(bv, base_dd)
                vmstats = summarize(mv, mc_dd)
                vbgstats = summarize(bgv, base_global_dd)
                vmgstats = summarize(mgv, mc_global_dd)

                all_results.append({
                    "symbol": symbol, "friction_bps": friction,
                    "baseline_n": bstats["n"], "baseline_return_pct": bstats["return_pct"],
                    "baseline_pf": bstats["pf"], "baseline_win_rate": bstats["win_rate"],
                    "baseline_maxdd_pct": bstats["maxdd_pct"],
                    "mc_n": mstats["n"], "mc_return_pct": mstats["return_pct"],
                    "mc_pf": mstats["pf"], "mc_win_rate": mstats["win_rate"],
                    "mc_maxdd_pct": mstats["maxdd_pct"],
                    "base_global_n": bgstats["n"], "base_global_return_pct": bgstats["return_pct"],
                    "base_global_pf": bgstats["pf"], "base_global_win_rate": bgstats["win_rate"],
                    "base_global_maxdd_pct": bgstats["maxdd_pct"],
                    "mc_global_n": mgstats["n"], "mc_global_return_pct": mgstats["return_pct"],
                    "mc_global_pf": mgstats["pf"], "mc_global_win_rate": mgstats["win_rate"],
                    "mc_global_maxdd_pct": mgstats["maxdd_pct"],
                    "delta_return_pct": mstats["return_pct"] - bstats["return_pct"],
                    "delta_global_vs_mc_pct": mgstats["return_pct"] - mstats["return_pct"],
                    "validation_baseline_return_pct": vbstats["return_pct"],
                    "validation_mc_return_pct": vmstats["return_pct"],
                    "validation_delta_return_pct": vmstats["return_pct"] - vbstats["return_pct"],
                    "validation_base_global_return_pct": vbgstats["return_pct"],
                    "validation_mc_global_return_pct": vmgstats["return_pct"],
                    "validation_global_vs_mc_pct": vmgstats["return_pct"] - vmstats["return_pct"]
                })

                if friction == 5.0:
                    bmap = {t["signal_ts"]: t for t in bt}
                    mmap = {t["signal_ts"]: t for t in mt}
                    bgmap = {t["signal_ts"]: t for t in bgt}
                    mgmap = {t["signal_ts"]: t for t in mgt}
                    for ts, b in bmap.items():
                        row = {
                            "symbol": symbol, "signal_ts": ts,
                            "baseline_ret": b["ret"], "baseline_net": b["net"],
                            "mc_accept": int(ts in mmap),
                            "mc_ret": mmap[ts]["ret"] if ts in mmap else np.nan,
                            "mc_net": mmap[ts]["net"] if ts in mmap else np.nan,
                            "global_gate": int(ts in bgmap),
                            "base_global_ret": bgmap[ts]["ret"] if ts in bgmap else np.nan,
                            "base_global_net": bgmap[ts]["net"] if ts in bgmap else np.nan,
                            "mc_global_accept": int(ts in mgmap),
                            "mc_global_ret": mgmap[ts]["ret"] if ts in mgmap else np.nan,
                            "mc_global_net": mgmap[ts]["net"] if ts in mgmap else np.nan
                        }
                        for k in (
                            "adv20", "adv60", "vol20", "atr_pct",
                            "trend", "mom20", "vol_z", "gap",
                            "global_median_ret", "global_breadth",
                            "global_dispersion", "vix_change", "dxy_ret",
                            "usdinr_ret", "wti_ret", "gold_ret",
                            "global_gap_nifty_minus_world"
                        ):
                            row[k] = b.get(k, np.nan)
                        dkey = pd.Timestamp(ts).normalize()
                        if dkey in nifty_daily.index:
                            row["market_vol20"] = nifty_daily.loc[dkey, "market_vol20"]
                            row["market_trend20"] = nifty_daily.loc[dkey, "market_trend20"]
                        else:
                            row["market_vol20"] = np.nan
                            row["market_trend20"] = np.nan
                        panel_rows.append(row)

            d = features.reset_index()
            d = d.rename(columns={d.columns[0]:"date"})
            d["symbol"] = symbol
            daily_rows.append(d[["date", "symbol", "ret1"]])
        except Exception as exc:
            failures.append({"symbol": symbol, "error": repr(exc)})

    results = pd.DataFrame(all_results)
    results.to_csv(out / "per_symbol_results.csv", index=False)

    panel = pd.DataFrame(panel_rows)
    if not panel.empty:
        panel.to_csv(out / "signal_panel.csv", index=False)
        p = results[results["friction_bps"] == 5.0].copy()
        winners = p[p["mc_return_pct"] > 0].sort_values("mc_return_pct", ascending=False)
        concentration = {
            "symbols": int(len(p)),
            "positive_symbols": int((p["mc_return_pct"] > 0).sum()),
            "median_mc_return_pct": float(p["mc_return_pct"].median()) if len(p) else None,
            "mean_mc_return_pct": float(p["mc_return_pct"].mean()) if len(p) else None,
            "top10_positive_share": (
                float(winners.head(10)["mc_return_pct"].sum() / winners["mc_return_pct"].sum())
                if len(winners) and winners["mc_return_pct"].sum() != 0 else None
            )
        }
        (out / "concentration.json").write_text(json.dumps(concentration, indent=2))

    if daily_rows:
        daily = pd.concat(daily_rows, ignore_index=True)
        cross = daily.groupby("date").agg(
            n=("ret1", "count"),
            pos=("ret1", lambda s: int((s > 0).sum())),
            sum_ret=("ret1", "sum"),
            sum_sq=("ret1", lambda s: float((s ** 2).sum()))
        ).reset_index()
        cross["breadth"] = cross["pos"] / cross["n"]
        cross["mean_ret"] = cross["sum_ret"] / cross["n"]
        cross["dispersion"] = np.sqrt(
            np.maximum(cross["sum_sq"] / cross["n"] - cross["mean_ret"] ** 2, 0)
        )
        cross.to_csv(out / "daily_cross_section.csv", index=False)

    (out / "failures.json").write_text(json.dumps(failures, indent=2))
    (out / "provenance.json").write_text(json.dumps({
        "symbols_requested": len(symbols),
        "test_start": str(TEST_START),
        "validation_start": str(VALIDATION_START),
        "validation_end": str(VALIDATION_END),
        "frictions_bps_per_leg": FRICTIONS,
        "strategy": "Phase-7 frozen LONG-ONLY EMA20/26, ATR14 1.5 stop, 20-bar max hold, next-bar open entry",
        "global_gate": "pre-specified risk-on gate: prior completed global equity breadth >= 62.5% and VIX change <= 0",
        "oos_accounting": "reset test equity to INR 100000 at TEST_START; train/validation path not allowed to set test capital",
        "mc": "250 bootstrap paths of last 30 net trade returns after 20-trade warm-up; >=125 positive paths",
        "sources": [
            "ganeshbiyer/Nse_Historical_Data (2018-2025)",
            "ganeshbiyer/Nse_Historical_Data_2026 (2026)"
        ]
    }, indent=2))

if __name__ == "__main__":
    main()
