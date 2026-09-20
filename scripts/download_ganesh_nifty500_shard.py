#!/usr/bin/env python3
import argparse, json, os, shutil, time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import pandas as pd

BASE = "https://raw.githubusercontent.com/ganeshbiyer/Nse_Historical_Data/main"
Y2026 = "https://raw.githubusercontent.com/ganeshbiyer/Nse_Historical_Data_2026/main"

def fetch(url, out, attempts=4):
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and out.stat().st_size > 0:
        return True
    last = None
    for i in range(attempts):
        try:
            req = Request(url, headers={"User-Agent": "MC-Phase9/1.0"})
            with urlopen(req, timeout=120) as r, out.open("wb") as fh:
                shutil.copyfileobj(r, fh)
            if out.stat().st_size > 0:
                return True
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            last = repr(exc)
            time.sleep(2 ** i)
    if out.exists() and out.stat().st_size == 0:
        out.unlink()
    print("DOWNLOAD_FAILED", url, last)
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols-json", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    symbols = json.loads(args.symbols_json)
    root = Path(args.out)
    base_dir = root / "base"
    y26_dir = root / "y2026"
    ref_dir = root / "reference"
    base_dir.mkdir(parents=True, exist_ok=True)
    y26_dir.mkdir(parents=True, exist_ok=True)
    ref_dir.mkdir(parents=True, exist_ok=True)

    failures = []
    for symbol in symbols:
        ok = fetch(f"{BASE}/{symbol}.parquet", base_dir / f"{symbol}.parquet")
        y26 = fetch(f"{Y2026}/{symbol}.parquet", y26_dir / f"{symbol}.parquet")
        if not ok and not y26:
            failures.append({"symbol": symbol, "error": "missing from both Ganesh repos"})

    base_idx = ref_dir / "NIFTY50-base.parquet"
    y26_idx = ref_dir / "NIFTY50-2026.parquet"
    fetch(f"{BASE}/NIFTY50-INDEX.parquet", base_idx)
    fetch(f"{Y2026}/NIFTY50-INDEX.parquet", y26_idx)

    parts = []
    for p in (base_idx, y26_idx):
        if p.exists() and p.stat().st_size > 0:
            parts.append(pd.read_parquet(p))
    if parts:
        pd.concat(parts, ignore_index=True).to_parquet(ref_dir / "NIFTY50-INDEX.parquet", index=False)

    (root / "download_failures.json").write_text(json.dumps(failures, indent=2))

if __name__ == "__main__":
    main()
