#!/usr/bin/env python3
import argparse, json, math, re, zlib
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

FRICTIONS=(0.0,5.0,10.0)
TRAIN_END=pd.Timestamp("2023-12-31")
VAL_START=pd.Timestamp("2024-01-01")
VAL_END=pd.Timestamp("2025-12-31")
TEST1_START=pd.Timestamp("2026-01-01")
TEST1_END=pd.Timestamp("2026-04-30 23:59")
TEST2_START=pd.Timestamp("2026-05-01")
TEST2_END=pd.Timestamp("2026-12-31 23:59")

def symnorm(s):
    return re.sub(r"-EQ$","",str(s).upper())

def is_index(s):
    return any(x in symnorm(s) for x in ("NIFTY","BANKNIFTY","FINNIFTY","MIDCPNIFTY"))

def files(root):
    return {symnorm(p.stem):p for p in Path(root).glob("*.parquet")}

def read_parquet(path):
    df=pd.read_parquet(path)
    lower={str(c).lower():c for c in df.columns}
    if isinstance(df.index,pd.DatetimeIndex):
        ts=pd.Series(df.index,index=df.index)
    else:
        col=next((lower[x] for x in ("datetime","timestamp","date","time") if x in lower),None)
        if col is None:
            raise ValueError(f"no timestamp column: {path}")
        raw=df[col]
        if pd.api.types.is_numeric_dtype(raw):
            m=float(pd.to_numeric(raw,errors="coerce").dropna().median())
            unit="ms" if m>1e12 else "s" if m>1e9 else "D"
            ts=pd.to_datetime(raw,unit=unit,errors="coerce")
        else:
            ts=pd.to_datetime(raw,errors="coerce")
    ts=pd.Series(ts,index=df.index)
    if ts.dt.tz is None:
        ts=ts.dt.tz_localize("Asia/Kolkata")
    else:
        ts=ts.dt.tz_convert("Asia/Kolkata")
    def pick(*names):
        for n in names:
            if n in lower: return lower[n]
        return None
    ren={}
    for target,names in {
        "open":("open","open_price"),"high":("high","high_price"),
        "low":("low","low_price"),"close":("close","close_price"),
        "volume":("volume","vol","total_volume")
    }.items():
        c=pick(*names)
        if c is not None: ren[c]=target
    if not all(x in ren.values() for x in ("open","high","low","close")):
        raise ValueError(f"missing OHLC: {path} cols={list(df.columns)}")
    x=df.rename(columns=ren).copy()
    x["ts"]=ts.values
    keep=[c for c in ("ts","open","high","low","close","volume") if c in x.columns]
    x=x[keep].dropna(subset=["ts","open","high","low","close"])
    x=x[(x.ts.dt.time>=pd.Timestamp("09:15").time())&(x.ts.dt.time<=pd.Timestamp("15:30").time())]
    return x.sort_values("ts").drop_duplicates("ts").set_index("ts").astype(float)

def load_combined(old_path,new_path):
    parts=[]
    for p in (old_path,new_path):
        if p and Path(p).exists():
            parts.append(read_parquet(p))
    if not parts: return pd.DataFrame()
    x=pd.concat(parts).sort_index()
    return x[~x.index.duplicated(keep="last")]

def ema(s,n): return s.ewm(span=n,adjust=False,min_periods=n).mean()

def atr(df,n=14):
    pc=df.close.shift(1)
    tr=pd.concat([df.high-df.low,(df.high-pc).abs(),(df.low-pc).abs()],axis=1).max(axis=1)
    return tr.ewm(alpha=1/n,adjust=False,min_periods=n).mean()

def resample15(df):
    return df.resample("15min",origin="start_day",offset="15min",label="left",closed="left").agg({
        "open":"first","high":"max","low":"min","close":"last","volume":"sum"
    }).dropna(subset=["open","high","low","close"])

def costs(buy,sell,friction):
    t=buy+sell; brokerage=40.0; exchange=t*0.0000307; sebi=t*0.000001
    gst=0.18*(brokerage+exchange+sebi); stt=sell*0.00025; stamp=buy*0.00003
    return brokerage+exchange+sebi+gst+stt+stamp+t*friction/10000.0

def mc_gate(history,seed):
    if len(history)<20: return True
    h=np.asarray(history[-30:],float)
    rng=np.random.default_rng(seed)
    draws=rng.choice(h,size=(250,len(h)),replace=True)
    return int((np.prod(1+draws,axis=1)>1).sum())>=125

def daily_features(m15,market):
    d=m15.resample("1D").agg({
        "open":"first","high":"max","low":"min","close":"last","volume":"sum"
    }).dropna(subset=["close"])
    prev=d.close.shift(1)
    d["ret1"]=d.close.pct_change()
    d["gap"]=d.open/prev-1
    d["adv20"]=(d.close*d.volume).rolling(20,min_periods=20).mean().shift(1)
    d["adv60"]=(d.close*d.volume).rolling(60,min_periods=60).mean().shift(1)
    d["vol20"]=d.ret1.rolling(20,min_periods=20).std().shift(1)
    d["atr_pct"]=(atr(d)/d.close).shift(1)
    d["trend"]=(ema(d.close,20)/ema(d.close,50)-1).shift(1)
    d["mom20"]=d.close.pct_change(20).shift(1)
    vm=d.volume.rolling(20,min_periods=20).mean()
    vs=d.volume.rolling(20,min_periods=20).std()
    d["vol_z"]=((d.volume-vm)/vs).shift(1)
    if market is not None and not market.empty:
        m=market.reindex(d.index).ffill()
        var=m.ret1.rolling(60,min_periods=40).var()
        d["beta60"]=d.ret1.rolling(60,min_periods=40).cov(m.ret1)/var
        d["resid_vol60"]=(d.ret1-d.beta60*m.ret1).rolling(60,min_periods=40).std()
        d["nifty_trend"]=m.trend.shift(1)
        d["nifty_vol20"]=m.vol20.shift(1)
        d["nifty_dd60"]=m.dd60.shift(1)
    return d

def market_daily(old,new):
    parts=[]
    for p in (old,new):
        if p and Path(p).exists(): parts.append(read_parquet(p))
    if not parts: return pd.DataFrame()
    x=pd.concat(parts).sort_index(); x=x[~x.index.duplicated(keep="last")]
    d=x.resample("1D").agg({"open":"first","high":"max","low":"min","close":"last","volume":"sum"}).dropna(subset=["close"])
    if d.index.tz is not None: d.index=d.index.tz_localize(None)
    d["ret1"]=d.close.pct_change()
    d["trend"]=ema(d.close,20)/ema(d.close,50)-1
    d["vol20"]=d.ret1.rolling(20,min_periods=20).std()
    d["dd60"]=d.close/d.close.rolling(60,min_periods=20).max()-1
    return d

def period(ts):
    d=pd.Timestamp(ts)
    if d.tzinfo is not None: d=d.tz_localize(None)
    d=d.normalize()
    if d<=TRAIN_END: return "train"
    if VAL_START<=d<=VAL_END: return "validation"
    if TEST1_START<=d<=TEST1_END: return "test_primary"
    if TEST2_START<=d<=TEST2_END: return "holdout"
    return None

def simulate(m15,feat,symbol,friction,use_mc):
    d=m15.copy()
    d["e20"]=ema(d.close,20); d["e26"]=ema(d.close,26); d["atr"]=atr(d)
    equity=100000.0; hist=[]; peak=equity; maxdd=0.0; pos=None; trades=[]; signals=[]
    seed=zlib.crc32(f"{symbol}-{friction}".encode())&0xffffffff
    for i in range(27,len(d)-1):
        row=d.iloc[i]; ts=d.index[i]
        if pos is not None:
            held=i-pos["entry_i"]+1
            exit_px=None; reason=None
            if pos["direction"]==1 and row.low<=pos["stop"]:
                exit_px=row.open if row.open<pos["stop"] else pos["stop"]; reason="stop"
            elif pos["direction"]==-1 and row.high>=pos["stop"]:
                exit_px=row.open if row.open>pos["stop"] else pos["stop"]; reason="stop"
            elif held>=20:
                exit_px=row.close; reason="time"
            if exit_px is not None:
                qty=pos["qty"]; gross=pos["direction"]*(exit_px-pos["entry"])*qty
                buy=pos["entry"]*qty if pos["direction"]==1 else exit_px*qty
                sell=exit_px*qty if pos["direction"]==1 else pos["entry"]*qty
                net=gross-costs(buy,sell,friction); ret=net/pos["equity"]
                equity+=net; peak=max(peak,equity); maxdd=min(maxdd,equity/peak-1)
                hist.append(ret)
                rec=pos["record"].copy(); rec.update({"exit_ts":str(ts),"net":net,"ret":ret,"exit_reason":reason})
                trades.append(rec); pos=None
            continue
        if not (np.isfinite(row.e20) and np.isfinite(row.e26) and np.isfinite(row.atr)): continue
        up=bool(row.e20>row.e26 and d.e20.iloc[i-1]<=d.e26.iloc[i-1])
        dn=bool(row.e20<row.e26 and d.e20.iloc[i-1]>=d.e26.iloc[i-1])
        if not (up or dn): continue
        f=feat.loc[ts.normalize()] if ts.normalize() in feat.index else pd.Series(dtype=float)
        factor=f.to_dict() if not isinstance(f,pd.DataFrame) else {}
        mins=(ts.hour*60+ts.minute)-555
        tod=int(max(0,mins)//60)
        accepted=(not use_mc) or mc_gate(hist,seed)
        signal={
            "symbol":symbol,"signal_ts":str(ts),"signal_date":str(ts.date()),
            "direction":1 if up else -1,"tod_bucket":tod,"mc_accept":int(accepted),**factor
        }
        signals.append(signal)
        if not accepted: continue
        entry_i=i+1; entry=float(d.open.iloc[entry_i]); qty=int(equity//entry)
        if qty<=0: continue
        direction=1 if up else -1
        stop=entry-1.5*float(row.atr) if direction==1 else entry+1.5*float(row.atr)
        pos={"entry_i":entry_i,"entry":entry,"qty":qty,"equity":equity,
             "direction":direction,"stop":stop,"record":signal.copy()}
    return signals,trades,maxdd


def load_tej(root):
    frames=[]
    for p in list(Path(root).glob("nse/year=*/nse_*.parquet"))+list(Path(root).glob("bse/year=*/bse_*.parquet")):
        side="nse" if "/nse/" in str(p).replace("\\","/") else "bse"
        x=pd.read_parquet(p)
        lo={str(z).lower():z for z in x.columns}
        dc=lo.get("date") or lo.get("datetime") or lo.get("timestamp")
        sc=lo.get("symbol"); cc=lo.get("close"); ic=lo.get("isin")
        if not dc or not sc or not cc: continue
        q=x[[dc,sc,cc]+([ic] if ic else [])].copy()
        q=q.rename(columns={dc:"date",sc:"symbol",cc:"close"})
        if ic: q=q.rename(columns={ic:"isin"})
        q["date"]=pd.to_datetime(q["date"],errors="coerce").dt.normalize()
        q["symbol"]=q["symbol"].astype(str).str.upper()
        q["close"]=pd.to_numeric(q["close"],errors="coerce")
        q["side"]=side
        frames.append(q.dropna(subset=["date","close"]))
    if not frames: return pd.DataFrame()
    return pd.concat(frames,ignore_index=True)

def lagged_basis(tej):
    if tej.empty: return pd.DataFrame()
    n=tej[tej.side=="nse"].copy(); b=tej[tej.side=="bse"].copy()
    key="symbol"
    n["join_key"]=n[key].astype(str).str.upper(); b["join_key"]=b[key].astype(str).str.upper()
    m=n[["date","join_key","symbol","close"]].rename(columns={"symbol":"nse_symbol","close":"nse_close"})
    z=b[["date","join_key","close"]].rename(columns={"close":"bse_close"})
    m=m.merge(z,on=["date","join_key"],how="inner").sort_values(["join_key","date"])
    m["basis"]=m.bse_close/m.nse_close-1
    m["basis_lag1"]=m.groupby("join_key").basis.shift(1)
    m["basis_abs_lag1"]=m.basis_lag1.abs()
    return m[["date","join_key","basis_lag1","basis_abs_lag1"]]

def stats(trades):
    if not trades: return {"n":0,"return_pct":0.0,"pf":None,"win_rate":None}
    x=np.asarray([t["net"] for t in trades],float); w=x[x>0]; l=x[x<0]
    return {"n":int(len(x)),"return_pct":float(x.sum()/100000*100),
            "pf":float(w.sum()/-l.sum()) if len(l) else None,
            "win_rate":float((x>0).mean())}

def factor_regression(panel):
    factors=[c for c in [
        "adv20","adv60","vol20","atr_pct","trend","mom20","vol_z","gap",
        "beta60","resid_vol60","nifty_trend","nifty_vol20","nifty_dd60",
        "breadth_prev","dispersion_prev","tod_bucket"
    ] if c in panel.columns]
    z=panel.replace([np.inf,-np.inf],np.nan).dropna(subset=factors).copy()
    if len(z)<100: return {"n":int(len(z)),"tests":[]}
    tests=[]
    def fit(y,name,sub):
        if len(sub)<100: return
        X=sub[factors].copy()
        for c in factors:
            s=X[c].std(); X[c]=(X[c]-X[c].mean())/(s if np.isfinite(s) and s else 1)
        X=sm.add_constant(X,has_constant="add")
        m=sm.OLS(sub[y].astype(float),X).fit(cov_type="cluster",cov_kwds={"groups":sub.symbol})
        for c in factors:
            tests.append({"model":name,"factor":c,"coef":float(m.params[c]),"p":float(m.pvalues[c])})
    fit("mc_accept","mc_accept",z)
    if "mc_ret" in z:
        fit("mc_ret","mc_ret",z[z.mc_ret.notna()])
    if "mc_uplift" in z:
        fit("mc_uplift","mc_uplift",z[z.mc_uplift.notna()])
    if tests:
        _,q,_,_=multipletests([t["p"] for t in tests],alpha=0.05,method="fdr_bh")
        for t,v in zip(tests,q):
            t["fdr_p"]=float(v); t["fdr_significant"]=bool(v<0.05)
    return {"n":int(len(z)),"tests":tests}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--old-root",required=True); ap.add_argument("--new-root",required=True)
    ap.add_argument("--out",default="research_results/phase9_ganesh_nifty500")
    a=ap.parse_args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    old=files(a.old_root); new=files(a.new_root)
    common=sorted((set(old)&set(new))-{x for x in old if is_index(x)})
    nifty=market_daily(old.get("NIFTY50-INDEX"),new.get("NIFTY50-INDEX"))
    summary=[]; panel_rows=[]; daily_parts=[]; errors=[]; provenance=[]
    for symbol in common:
        try:
            raw=load_combined(old.get(symbol),new.get(symbol))
            if raw.empty: continue
            m15=resample15(raw[["open","high","low","close","volume"]].astype(float))
            if len(m15)<100: continue
            feat=daily_features(m15,nifty)
            dr=feat[["ret1"]].dropna().reset_index().rename(columns={"index":"date"})
            dr["symbol"]=symbol; daily_parts.append(dr[["date","symbol","ret1"]])
            all_b, all_m=None,None
            for friction in FRICTIONS:
                bs,bt,_=simulate(m15,feat,symbol,friction,False)
                ms,mt,_=simulate(m15,feat,symbol,friction,True)
                for tag,trades in (("baseline",bt),("mc",mt)):
                    for p in ("train","validation","test_primary","holdout"):
                        s=stats([t for t in trades if period(t["signal_ts"])==p])
                        summary.append({"symbol":symbol,"friction_bps":friction,"mc":int(tag=="mc"),"period":p,**s})
                if friction==5.0:
                    bmap={t["signal_ts"]:t for t in bt}; mmap={t["signal_ts"]:t for t in mt}
                    for sig in bs:
                        b=bmap.get(sig["signal_ts"])
                        if b is None: continue
                        m=mmap.get(sig["signal_ts"])
                        r=sig.copy()
                        r["period"]=period(sig["signal_ts"])
                        r["baseline_ret"]=b["ret"]; r["baseline_net"]=b["net"]
                        r["mc_ret"]=m["ret"] if m else np.nan
                        r["mc_net"]=m["net"] if m else np.nan
                        r["mc_uplift"]=(m["ret"]-b["ret"]) if m else np.nan
                        panel_rows.append(r)
            provenance.append({"symbol":symbol,"rows_1m":int(len(raw)),
                               "start":str(raw.index.min()),"end":str(raw.index.max())})
        except Exception as e:
            errors.append({"symbol":symbol,"error":repr(e)})
    panel=pd.DataFrame(panel_rows)
    if not panel.empty:
        panel["signal_date"]=pd.to_datetime(panel["signal_date"]).dt.normalize()
    if args.tej_root and not panel.empty:
        tej=load_tej(args.tej_root)
        basis=lagged_basis(tej)
        if not basis.empty:
            panel['basis_key']=panel['symbol'].astype(str).str.upper()
            panel=panel.merge(basis,left_on=['signal_date','basis_key'],right_on=['date','join_key'],how='left')
            panel=panel.drop(columns=['date','join_key','basis_key'],errors='ignore')
    if daily_parts:
        daily=pd.concat(daily_parts,ignore_index=True)
        daily["date"]=pd.to_datetime(daily["date"])
        if getattr(daily["date"].dt,"tz",None) is not None: daily["date"]=daily["date"].dt.tz_localize(None)
        daily["date"]=daily["date"].dt.normalize()
        cs=daily.groupby("date").agg(
            breadth=("ret1",lambda s:float((s>0).mean())),
            dispersion=("ret1","std")
        ).sort_index().shift(1).rename(columns={"breadth":"breadth_prev","dispersion":"dispersion_prev"})
        if not panel.empty:
            panel["signal_date"]=pd.to_datetime(panel.signal_date).dt.normalize()
            panel=panel.merge(cs,left_on="signal_date",right_index=True,how="left")
    if not panel.empty:
        panel.to_parquet(out/"trade_factor_panel.parquet",index=False)
        qrows=[]
        for c in [x for x in [
            "adv20","adv60","vol20","atr_pct","trend","mom20","vol_z","gap",
            "beta60","resid_vol60","nifty_trend","nifty_vol20","nifty_dd60",
            "breadth_prev","dispersion_prev","tod_bucket"
        ] if x in panel.columns]:
            val=panel[panel.period=="validation"][["symbol",c,"mc_accept","baseline_ret","mc_ret"]].dropna()
            both=panel[panel.period.isin(["test_primary","holdout"])][["symbol",c,"mc_accept","baseline_ret","mc_ret"]].dropna()
            if len(val)<50 or both.empty: continue
            try:
                qs=np.unique(val[c].quantile([0,.2,.4,.6,.8,1]).to_numpy())
                if len(qs)<6: continue
                val=val.assign(q=pd.cut(val[c],bins=qs,labels=False,include_lowest=True)+1)
                both=both.assign(q=pd.cut(both[c],bins=qs,labels=False,include_lowest=True)+1)
                for sample,g in val.groupby("q"):
                    qrows.append({"factor":c,"sample":"validation","quintile":int(sample),"n":len(g),
                                   "mc_accept_rate":float(g.mc_accept.mean()),
                                   "baseline_mean_ret":float(g.baseline_ret.mean()),
                                   "mc_mean_ret":float(g.mc_ret.mean()) if g.mc_ret.notna().any() else np.nan})
                for sample,g in both.groupby("q"):
                    qrows.append({"factor":c,"sample":"test_and_holdout","quintile":int(sample),"n":len(g),
                                   "mc_accept_rate":float(g.mc_accept.mean()),
                                   "baseline_mean_ret":float(g.baseline_ret.mean()),
                                   "mc_mean_ret":float(g.mc_ret.mean()) if g.mc_ret.notna().any() else np.nan})
            except Exception:
                pass
        pd.DataFrame(qrows).to_csv(out/"factor_quintiles_validation_test.csv",index=False)
        regs={}
        for p in ("validation","test_primary","holdout"):
            regs[p]=factor_regression(panel[panel.period==p].copy())
        Path(out/"conditional_regressions.json").write_text(json.dumps(regs,indent=2))
    frame=pd.DataFrame(summary); frame.to_csv(out/"per_symbol_results.csv",index=False)
    if not frame.empty:
        smry={}
        for key,g in frame.groupby(["friction_bps","mc","period"]):
            v=g[g.n>0]; x=v.return_pct.to_numpy(float)
            smry["|".join(map(str,key))]={
                "symbols":int(len(v)),
                "mean_return_pct":float(x.mean()) if len(x) else 0.0,
                "median_return_pct":float(np.median(x)) if len(x) else 0.0,
                "positive_symbols":int((x>0).sum()),
                "median_pf":float(np.nanmedian(v.pf)) if v.pf.notna().any() else None
            }
        Path(out/"summary.json").write_text(json.dumps(smry,indent=2))
    Path(out/"provenance.json").write_text(json.dumps({
        "common_nifty500_symbols":len(common),
        "old_files":len(old),"new_files":len(new),
        "train":"2018-01-01 to 2023-12-31",
        "validation":"2024-01-01 to 2025-12-31",
        "primary_test":"2026-01-01 to 2026-04-30",
        "secondary_holdout":"2026-05-01 to dataset maximum",
        "frictions_bps_per_leg":list(FRICTIONS)
    },indent=2))
    Path(out/"errors.json").write_text(json.dumps(errors,indent=2))
    print(json.dumps({"common_symbols":len(common),"summary_rows":len(frame),"factor_rows":len(panel),"errors":len(errors)},indent=2))

if __name__=="__main__":
    main()
