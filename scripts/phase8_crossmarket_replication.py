#!/usr/bin/env python3
import csv, io, json, math, os, random
from pathlib import Path
import statistics
import urllib.request

NSE_SYMBOLS = [
    "TCS","RELIANCE","HDFCBANK","INFY","ICICIBANK","SBIN","AXISBANK","BHARTIARTL",
    "KOTAKBANK","ITC","LT","HCLTECH","BAJFINANCE","MARUTI","HINDUNILVR",
    "SUNPHARMA","TATASTEEL","ADANIPORTS","NTPC","ONGC"
]
BSE_SYMBOLS = [
    "DRREDDY","HDFCBANK","HINDUNILVR","ICICIBANK","INFY","ITC","JSWSTEEL","KPITTECH",
    "LT","M%26M","ONGC","POLYCAB","RELIANCE","SBIN","SUNPHARMA","TCS","TITAN","TRENT","WIPRO"
]
COSTS_BPS = (0.0, 5.0, 10.0)
NSE_REPO = "https://raw.githubusercontent.com/Ram9219/NIFTY-50-Stock-Market-Data-2000---2022-/main/"
BSE_REPO = "https://raw.githubusercontent.com/JashPancholi/BSE_STOCK_DATA/main/"

def download(url, cache_file):
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    if cache_file.exists() and cache_file.stat().st_size:
        return cache_file.read_text()
    req = urllib.request.Request(url, headers={"User-Agent": "MC-research/phase8"})
    with urllib.request.urlopen(req, timeout=60) as r:
        text = r.read().decode("utf-8")
    cache_file.write_text(text)
    return text

def ema(values, n):
    out=[float("nan")]*len(values)
    alpha=2.0/(n+1.0); prev=float("nan")
    for i,v in enumerate(values):
        if not math.isfinite(v): continue
        prev=v if not math.isfinite(prev) else alpha*v+(1-alpha)*prev
        if i >= n-1: out[i]=prev
    return out

def atr(rows, n=14):
    tr=[]
    for i,r in enumerate(rows):
        if i==0: tr.append(r["high"]-r["low"])
        else:
            pc=rows[i-1]["close"]
            tr.append(max(r["high"]-r["low"], abs(r["high"]-pc), abs(r["low"]-pc)))
    return ema(tr,n)

def parse_csv(text):
    reader=csv.DictReader(io.StringIO(text))
    rows=[]
    for r in reader:
        try:
            raw=str(r["Date"]).strip()
            if len(raw)==10 and raw[2]=="-":
                d,m,y=raw.split("-"); dt=f"{y}-{m}-{d}"
            else:
                dt=raw[:10]
            row={"date":dt,
                 "open":float(r["Open"]),
                 "high":float(r["High"]),
                 "low":float(r["Low"]),
                 "close":float(r["Close"])}
            if all(math.isfinite(row[k]) for k in ("open","high","low","close")):
                rows.append(row)
        except Exception:
            continue
    return sorted(rows,key=lambda x:x["date"])

def seeded_rng(seed):
    rng=random.Random(seed)
    return rng

def mc_gate(history, seed):
    if len(history)<20:
        return True
    h=history[-30:]
    rng=seeded_rng(seed)
    positive=0
    for _ in range(250):
        prod=1.0
        for _ in h:
            prod *= 1.0 + rng.choice(h)
        if prod>1.0: positive += 1
    return positive>=125

def cost_model(buy,sell,friction_bps,delivery=True):
    turnover=buy+sell
    brokerage=40.0
    exchange=turnover*0.0000307
    sebi=turnover*0.000001
    gst=0.18*(brokerage+exchange+sebi)
    stt=turnover*0.001 if delivery else sell*0.00025
    stamp=buy*(0.00015 if delivery else 0.00003)
    dp=13.5 if delivery else 0.0
    friction=turnover*friction_bps/10000.0
    return brokerage+exchange+sebi+gst+stt+stamp+dp+friction

def backtest(rows, symbol, horizon, friction_bps, use_mc, test_start, test_end):
    if len(rows)<40: return None
    closes=[r["close"] for r in rows]
    e20=ema(closes,20); e21=ema(closes,21); a=atr(rows,14)
    equity=100000.0; peak=equity; max_dd=0.0
    history=[]; position=None; trades=[]
    for i in range(26,len(rows)-1):
        r=rows[i]
        if position is not None:
            held=i-position["entry_i"]+1
            exit_px=None; reason=None
            if horizon=="btst" and held>=1:
                exit_px=r["close"]; reason="overnight"
            elif horizon=="swing":
                if r["low"]<=position["stop"]:
                    exit_px=r["open"] if r["open"]<position["stop"] else position["stop"]; reason="stop"
                elif held>=8:
                    exit_px=r["close"]; reason="time"
            if exit_px is not None:
                qty=position["qty"]
                gross=(exit_px-position["entry"])*qty
                net=gross-cost_model(position["entry"]*qty, exit_px*qty, friction_bps, True)
                ret=net/position["equity_before"]
                equity += net
                peak=max(peak,equity)
                max_dd=min(max_dd, equity/peak-1.0)
                history.append(ret)
                if test_start<=r["date"]<=test_end:
                    trades.append({"ret":ret,"net":net,"reason":reason})
                position=None
            continue
        if not all(math.isfinite(x) for x in (e20[i],e21[i],a[i])): continue
        up=e20[i]>e21[i] and e20[i-1]<=e21[i-1]
        if not up: continue
        if use_mc and not mc_gate(history, (hash(symbol+horizon)&0xffffffff)):
            continue
        entry=rows[i+1]["open"]
        qty=int(math.floor(equity/entry))
        if qty<=0: continue
        stop=entry-0.75*a[i] if horizon=="swing" else entry
        position={"entry_i":i+1,"entry":entry,"qty":qty,"equity_before":equity,"stop":stop}
    rets=[t["ret"] for t in trades if math.isfinite(t["ret"])]
    wins=[x for x in rets if x>0]; losses=[x for x in rets if x<0]
    gross_profit=sum(wins); gross_loss=-sum(losses)
    mean=statistics.fmean(rets) if rets else float("nan")
    sd=statistics.stdev(rets) if len(rets)>1 else float("nan")
    return {
        "symbol":symbol, "horizon":horizon, "friction_bps":friction_bps, "mc":use_mc,
        "n":len(rets), "return_pct":100.0*sum(rets), "pf":gross_profit/gross_loss if gross_loss>0 else None,
        "win_rate":sum(x>0 for x in rets)/len(rets) if rets else None,
        "trade_sharpe":mean/sd if math.isfinite(sd) and sd>0 else None,
        "maxdd_pct":100.0*max_dd
    }

def finite_median(values):
    v=sorted(x for x in values if x is not None and math.isfinite(x))
    return statistics.median(v) if v else None

def aggregate(rows):
    out={}
    keys=sorted(set((r["source"],r["horizon"],r["friction_bps"],r["mc"]) for r in rows))
    for source,horizon,friction,mc in keys:
        g=[r for r in rows if (r["source"],r["horizon"],r["friction_bps"],r["mc"])==(source,horizon,friction,mc) and r["n"]>0]
        rets=[r["return_pct"] for r in g if math.isfinite(r["return_pct"])]
        out[f"{source}|{horizon}|{friction}|{mc}"]={
            "symbols":len(g),
            "mean_return_pct":statistics.fmean(rets) if rets else None,
            "median_return_pct":finite_median(rets),
            "positive_symbols":sum(r>0 for r in rets),
            "median_pf":finite_median([r["pf"] for r in g]),
            "median_trade_sharpe":finite_median([r["trade_sharpe"] for r in g])
        }
    return out

def main():
    out=Path("research_results/phase8_crossmarket")
    out.mkdir(parents=True,exist_ok=True)
    cache=Path(".cache/phase8_crossmarket")
    results=[]
    provenance=[]
    # NSE historical
    for symbol in NSE_SYMBOLS:
        fname=symbol+".csv"; url=NSE_REPO+fname
        try:
            rows=parse_csv(download(url,cache/"nse"/fname))
            provenance.append({"source":"nse_historical","symbol":symbol,"rows":len(rows),"start":rows[0]["date"],"end":rows[-1]["date"]})
            for horizon in ("btst","swing"):
                for friction in COSTS_BPS:
                    for mc in (False,True):
                        r=backtest(rows,symbol,horizon,friction,mc,"2019-01-01","2022-12-31")
                        if r: r["source"]="nse_historical"; results.append(r)
        except Exception as e:
            provenance.append({"source":"nse_historical","symbol":symbol,"error":repr(e)})
    # BSE cross-market
    for encoded in BSE_SYMBOLS:
        symbol=encoded.replace("%26","&")
        fname=encoded+".csv"
        url=BSE_REPO+fname
        try:
            rows=parse_csv(download(url,cache/"bse"/fname))
            provenance.append({"source":"bse_crossmarket","symbol":symbol,"rows":len(rows),"start":rows[0]["date"],"end":rows[-1]["date"]})
            for horizon in ("btst","swing"):
                for friction in COSTS_BPS:
                    for mc in (False,True):
                        r=backtest(rows,symbol,horizon,friction,mc,"2025-01-01","2025-12-31")
                        if r: r["source"]="bse_crossmarket"; results.append(r)
        except Exception as e:
            provenance.append({"source":"bse_crossmarket","symbol":symbol,"error":repr(e)})
    (out/"per_symbol_results.json").write_text(json.dumps(results,indent=2))
    (out/"provenance.json").write_text(json.dumps(provenance,indent=2))
    (out/"summary.json").write_text(json.dumps(aggregate(results),indent=2))
    print(json.dumps(aggregate(results),indent=2))

if __name__=="__main__":
    main()
