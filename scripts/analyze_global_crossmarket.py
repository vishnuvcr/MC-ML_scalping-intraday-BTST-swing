#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd

FACTORS = [
    "global_median_ret", "global_breadth", "global_dispersion",
    "vix_change", "dxy_ret", "usdinr_ret", "wti_ret", "gold_ret",
    "global_gap_nifty_minus_world",
]

def summary(df, ret_col, pf_col, n_col):
    x = df[ret_col].dropna()
    return {
        "n_symbols": int(len(df)),
        "mean_return_pct": float(x.mean()) if len(x) else None,
        "median_return_pct": float(x.median()) if len(x) else None,
        "positive_symbols": int((x > 0).sum()) if len(x) else 0,
        "median_pf": float(df[pf_col].dropna().median()) if df[pf_col].notna().any() else None,
        "median_trades": float(df[n_col].median()) if n_col in df else None,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True)
    ap.add_argument("--panel", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    results = pd.read_csv(args.results)
    panel = pd.read_csv(args.panel)

    report = {}
    for fr in [5.0, 10.0]:
        g = results[results.friction_bps == fr]
        report[f"friction_{fr:g}"] = {
            "baseline": summary(g, "baseline_return_pct", "baseline_pf", "baseline_n"),
            "mc": summary(g, "mc_return_pct", "mc_pf", "mc_n"),
            "base_global": summary(g, "base_global_return_pct", "base_global_pf", "base_global_n"),
            "mc_global": summary(g, "mc_global_return_pct", "mc_global_pf", "mc_global_n"),
        }

    qrows = []
    for factor in [f for f in FACTORS if f in panel.columns]:
        q = panel[[factor, "baseline_ret", "mc_ret", "base_global_ret", "mc_global_ret"]].dropna(subset=[factor]).copy()
        if len(q) < 50:
            continue
        q["quintile"] = pd.qcut(q[factor], 5, labels=False, duplicates="drop") + 1
        for k, g in q.groupby("quintile"):
            b, m, bg, mg = [g[c].dropna() for c in ["baseline_ret","mc_ret","base_global_ret","mc_global_ret"]]
            qrows.append({
                "factor": factor, "quintile": int(k), "n": int(len(g)),
                "baseline_mean": float(b.mean()) if len(b) else np.nan,
                "mc_mean": float(m.mean()) if len(m) else np.nan,
                "base_global_mean": float(bg.mean()) if len(bg) else np.nan,
                "mc_global_mean": float(mg.mean()) if len(mg) else np.nan,
            })
    pd.DataFrame(qrows).to_csv(out / "global_factor_quintiles.csv", index=False)

    if "global_gate" in panel.columns:
        r = panel.global_gate == 1
        gate = {
            "signals": int(len(panel)),
            "risk_on_rate": float(r.mean()),
            "baseline_mean_all": float(panel.baseline_ret.mean()),
            "baseline_mean_risk_on": float(panel.loc[r, "baseline_ret"].mean()) if r.any() else None,
            "baseline_mean_risk_off": float(panel.loc[~r, "baseline_ret"].mean()) if (~r).any() else None,
            "mc_global_accept_rate": float(panel.mc_global_accept.mean()) if "mc_global_accept" in panel else None,
            "mc_mean_accepted": float(panel.mc_ret.dropna().mean()) if panel.mc_ret.notna().any() else None,
            "mc_global_mean_accepted": float(panel.mc_global_ret.dropna().mean()) if panel.mc_global_ret.notna().any() else None,
        }
        report["gate"] = gate
        (out / "global_gate_summary.json").write_text(json.dumps(gate, indent=2))

    if "global_median_ret" in panel.columns:
        lead = panel.dropna(subset=["global_median_ret"]).copy()
        lead["global_positive"] = (lead.global_median_ret > 0).astype(int)
        g = lead.groupby("global_positive").baseline_ret.agg(["count","mean","median"]).reset_index()
        g.to_csv(out / "global_lead_lag_by_sign.csv", index=False)
        if len(g) == 2:
            report["lead_lag"] = {
                "positive_global_mean": float(g.loc[g.global_positive == 1, "mean"].iloc[0]),
                "negative_global_mean": float(g.loc[g.global_positive == 0, "mean"].iloc[0]),
                "difference": float(g.loc[g.global_positive == 1, "mean"].iloc[0] - g.loc[g.global_positive == 0, "mean"].iloc[0])
            }

    (out / "global_crossmarket_summary.json").write_text(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
