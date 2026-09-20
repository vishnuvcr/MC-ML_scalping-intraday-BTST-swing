#!/usr/bin/env python3
import argparse
import shutil
import subprocess
from pathlib import Path
import pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    root = Path(args.root)
    fixed = root.parent / (root.name + "_fixed")
    if fixed.exists():
        shutil.rmtree(fixed)
    shutil.copytree(root, fixed)

    for p in fixed.rglob("signal_panel.csv"):
        df = pd.read_csv(p)
        if "mc_return" not in df.columns and "mc_ret" in df.columns:
            df["mc_return"] = df["mc_ret"]
        if "mc_return" not in df.columns:
            df["mc_return"] = float("nan")
        df.to_csv(p, index=False)

    cmd = [
        "python", "scripts/aggregate_ganesh_nifty500.py",
        "--root", str(fixed),
        "--out", args.out,
    ]
    raise SystemExit(subprocess.call(cmd))

if __name__ == "__main__":
    main()
