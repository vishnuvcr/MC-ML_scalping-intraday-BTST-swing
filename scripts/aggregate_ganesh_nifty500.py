#!/usr/bin/env python3
import json
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

def summarize_group(g):
    net = g["net"].to_numpy(float) if "net" in g.columns else np.array([])
    wins = net[net > 0]
    losses = net[net < 0]
    return {
        "n": int(len(net)),
        "return_pct": float(net.sum() / 1000.0) if len(net) else 0.0,
        "pf": float(wins.sum() / -losses.sum()) if len(losses) else None,
        "win_rate": float((net > 0).mean()) if len(net) else None
    }

def add_regimes(panel, daily):
    if daily.empty or panel.empty:
        return panel
    d = daily.groupby("date").agg(
        n=("n", "sum"), pos=("pos", "sum"),
        sum_ret=("sum_ret", "sum"), sum_sq=("sum_sq", "sum")
    ).reset_index()
    d["breadth"] = d["pos"] / d["n"]
    d["mean_ret"] = d["sum_ret"] / d["n"]
    d["dispersion"] = np.sqrt(
        np.maximum(d["sum_sq"] / d["n"] - d["mean_ret"] ** 2, 0)
    )
    d["breadth"] = d["breadth"].shift(1)
    d["dispersion"] = d["dispersion"].shift(1)
    d["date"] = pd.to_datetime(d["date"])
    p = panel.copy()
    p["signal_day"] = pd.to_datetime(p["signal_ts"]).dt.normalize()
    p = p.merge(
        d[["date", "breadth", "dispersion"]],
        left_on="signal_day", right_on="date", how="left"
    ).drop(columns=["date"])
    return p

def regress(panel):
    factors = [
        "adv20", "adv60", "vol20", "atr_pct",
        "trend", "mom20", "vol_z", "gap",
        "market_vol20", "market_trend20", "breadth", "dispersion"
    ]
    factors = [f for f in factors if f in panel.columns]
    z = panel.replace([np.inf, -np.inf], np.nan).dropna(subset=factors).copy()
    if len(z) < 50:
        return {"status": "insufficient", "n": len(z)}

    out = []
    X = z[factors].copy()
    for c in factors:
        s = X[c].std()
        X[c] = (X[c] - X[c].mean()) / (s if np.isfinite(s) and s else 1.0)
    X = sm.add_constant(X, has_constant="add")

    accepted = z["mc_accept"].astype(int)
    try:
        model = sm.GLM(accepted, X, family=sm.families.Binomial()).fit(cov_type="HC3")
        for c in factors:
            out.append({
                "model": "MC_acceptance",
                "factor": c,
                "coef": float(model.params[c]),
                "p": float(model.pvalues[c])
            })
    except Exception as exc:
        return {"error": repr(exc), "n": len(z)}

    accepted_rows = z[z["mc_ret"].notna()].copy()
    if len(accepted_rows) >= 50:
        Xa = accepted_rows[factors].copy()
        for c in factors:
            s = Xa[c].std()
            Xa[c] = (Xa[c] - Xa[c].mean()) / (s if np.isfinite(s) and s else 1.0)
        Xa = sm.add_constant(Xa, has_constant="add")
        model = sm.OLS(accepted_rows["mc_ret"], Xa).fit(cov_type="HC3")
        for c in factors:
            out.append({
                "model": "MC_trade_return",
                "factor": c,
                "coef": float(model.params[c]),
                "p": float(model.pvalues[c])
            })

    pvals = np.array([x["p"] for x in out], dtype=float)
    _, qvals, _, _ = multipletests(pvals, alpha=0.05, method="fdr_bh")
    for row, q in zip(out, qvals):
        row["fdr_p"] = float(q)
        row["fdr_significant"] = bool(q < 0.05)
    return {"n": len(z), "tests": out}

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    root = Path(args.root)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    result_files = list(root.rglob("per_symbol_results.csv"))
    panel_files = list(root.rglob("signal_panel.csv"))
    daily_files = list(root.rglob("daily_cross_section.csv"))

    results = pd.concat([pd.read_csv(p) for p in result_files], ignore_index=True) if result_files else pd.DataFrame()
    panel = pd.concat([pd.read_csv(p) for p in panel_files], ignore_index=True) if panel_files else pd.DataFrame()
    daily = pd.concat([pd.read_csv(p) for p in daily_files], ignore_index=True) if daily_files else pd.DataFrame()

    if not results.empty:
        results = results.drop_duplicates(["symbol", "friction_bps"], keep="last").sort_values(["friction_bps", "symbol"])
        results.to_csv(out / "all_per_symbol_results.csv", index=False)

        summaries = []
        for fr in sorted(results["friction_bps"].unique()):
            g = results[results["friction_bps"] == fr]
            for model in ["baseline", "mc"]:
                ret_col = f"{model}_return_pct"
                pf_col = f"{model}_pf"
                summaries.append({
                    "friction_bps": fr, "model": model,
                    "symbols": len(g),
                    "mean_return_pct": float(g[ret_col].mean()),
                    "median_return_pct": float(g[ret_col].median()),
                    "positive_symbols": int((g[ret_col] > 0).sum()),
                    "median_pf": float(g[pf_col].dropna().median()) if g[pf_col].notna().any() else None,
                    "mean_delta_vs_baseline": (
                        float(g["delta_return_pct"].mean()) if model == "mc" else 0.0
                    )
                })
        pd.DataFrame(summaries).to_csv(out / "universe_summary.csv", index=False)

    if not panel.empty:
        panel = add_regimes(panel, daily)
        panel.to_csv(out / "all_signal_panel_with_regimes.csv", index=False)

        # Factor quintiles, evaluated descriptively on 2026 test observations.
        qrows = []
        factor_cols = [
            "adv20", "adv60", "vol20", "atr_pct",
            "trend", "mom20", "vol_z", "gap",
            "market_vol20", "market_trend20", "breadth", "dispersion"
        ]
        for factor in [x for x in factor_cols if x in panel.columns]:
            q = panel[[factor, "baseline_ret", "mc_ret"]].dropna().copy()
            if q.empty:
                continue
            try:
                q["quintile"] = pd.qcut(q[factor], 5, labels=False, duplicates="drop") + 1
            except Exception:
                continue
            for k, g in q.groupby("quintile"):
                mc = g["mc_ret"].dropna()
                base = g["baseline_ret"].dropna()
                qrows.append({
                    "factor": factor, "quintile": int(k), "n": len(g),
                    "baseline_mean_ret": float(base.mean()) if len(base) else np.nan,
                    "mc_mean_ret": float(mc.mean()) if len(mc) else np.nan,
                    "mc_win_rate": float((mc > 0).mean()) if len(mc) else np.nan,
                    "mc_minus_baseline": float(mc.mean() - base.mean()) if len(mc) and len(base) else np.nan
                })
        pd.DataFrame(qrows).to_csv(out / "factor_quintiles_test.csv", index=False)
        conditional = regress(panel)
        (out / "conditional_regressions.json").write_text(json.dumps(conditional, indent=2))

    concentration = {}
    five = results[results["friction_bps"] == 5.0].copy() if not results.empty else pd.DataFrame()
    if not five.empty:
        winners = five[five["mc_return_pct"] > 0].sort_values("mc_return_pct", ascending=False)
        total_positive = winners["mc_return_pct"].sum()
        concentration = {
            "symbols": int(len(five)),
            "positive_symbols": int((five["mc_return_pct"] > 0).sum()),
            "median_mc_return_pct": float(five["mc_return_pct"].median()),
            "mean_mc_return_pct": float(five["mc_return_pct"].mean()),
            "top10_positive_share": float(winners.head(10)["mc_return_pct"].sum() / total_positive)
            if total_positive != 0 else None
        }
    (out / "concentration.json").write_text(json.dumps(concentration, indent=2))

    provenance = {
        "dataset_1": "ganeshbiyer/Nse_Historical_Data: 2018-2025",
        "dataset_2": "ganeshbiyer/Nse_Historical_Data_2026: 2026",
        "intraday_resolution": "1-minute source resampled to 15-minute",
        "strategy": "LONG-ONLY EMA20/26; ATR14 1.5 stop; 20 bars max; next-bar open",
        "frictions_bps_per_leg": [0, 5, 10],
        "mc": "250 bootstrap paths on latest 30 net returns after 20-trade warm-up; >=125 positive terminal paths",
        "validation": "2025",
        "test": "2026 YTD through the last available Ganesh observation"
    }
    (out / "provenance.json").write_text(json.dumps(provenance, indent=2))

if __name__ == "__main__":
    main()
