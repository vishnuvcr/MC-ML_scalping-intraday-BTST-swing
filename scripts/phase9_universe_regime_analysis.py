#!/usr/bin/env python3
import argparse, json, math, re, statistics, zlib
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm

FRICTION = 5.0
TEST_START = "2025-01-01"
TEST_END = "2026-09-07"

def ema(s,n): return s.ewm(span=n, adjust=False, min_periods=n).mean()
def atr(df,n=14):
    pc=df["close"].shift(1)
    tr=pd.concat([(df["high"]-df["low"]), (df["high"]-pc).abs(), (df["low"]-pc).abs()],axis=1).max(axis=1)
    return tr.ewm(alpha=1/n, adjust=False, min_periods=n).mean()

def cost(buy,sell,delivery=True):
    turnover=buy+sell; brokerage=40.0
    exchange=turnover*0.0000307; sebi=turnover*0.000001
    gst=0.18*(brokerage+exchange+sebi)
    stt=turnover*0.001 if delivery else sell*0.00025
    stamp=buy*(0.00015 if delivery else 0.00003)
    dp=13.5 if delivery else 0.0
    return brokerage+exchange+sebi+gst+stt+stamp+dp+turnover*FRICTION/10000

def mc_gate(hist, seed):
    if len(hist)<20: return True
    h=np.asarray(hist[-30:],dtype=float); rng=np.random.default_rng(seed)
    draws=rng.choice(h,size=(250,len(h)),replace=True)
    pos=np.sum(np.prod(1+draws,axis=1)>1.0)
    return pos>=125

def parse_json_candles(path):
    obj=json.loads(Path(path).read_text())
    data=obj.get("data", obj)
    if isinstance(data,dict):
        for k in ("data","candles","results"):
            if isinstance(data.get(k),list): data=data[k]; break
    rows=[]
    for r in data:
        if isinstance(r,dict):
            rows.append(r)
        elif isinstance(r,(list,tuple)) and len(r)>=6:
            rows.append({"timestamp":r[0],"open":r[1],"high":r[2],"low":r[3],"close":r[4],"volume":r[5]})
    df=pd.DataFrame(rows)
    if df.empty: return df
    cols={c.lower():c for c in df.columns}
    dt=cols.get("timestamp") or cols.get("datetime") or cols.get("date")
    ren={cols[k]:k for k in ("open","high","low","close","volume") if k in cols}
    df=df.rename(columns=ren)
    df["ts"]=pd.to_datetime(df[dt],errors="coerce")
    if df["ts"].dt.tz is None: df["ts"]=df["ts"].dt.tz_localize("Asia/Kolkata")
    else: df["ts"]=df["ts"].dt.tz_convert("Asia/Kolkata")
    df=df.dropna(subset=["ts","open","high","low","close"]).sort_values("ts").drop_duplicates("ts")
    return df.set_index("ts")[["open","high","low","close","volume"]].astype(float)

def parse_nse_daily(files):
    frames=[]
    for p in files:
        d=pd.read_parquet(p)
        if "series" in d.columns: d=d[d.series.isin(["EQ","BE","BZ"])]
        d=d.rename(columns={"date":"date"})
        keep=[c for c in ["date","symbol","isin","open","high","low","close","volume","turnover"] if c in d.columns]
        frames.append(d[keep])
    x=pd.concat(frames,ignore_index=True)
    x["date"]=pd.to_datetime(x["date"])
    return x.sort_values(["symbol","date"]).drop_duplicates(["symbol","date"],keep="last")

def parse_bse(files):
    if not files: return pd.DataFrame()
    frames=[]
    for p in files:
        d=pd.read_parquet(p)
        d["date"]=pd.to_datetime(d["date"])
        keep=[c for c in ["date","symbol","isin","close"] if c in d.columns]
        frames.append(d[keep])
    return pd.concat(frames,ignore_index=True).drop_duplicates(["symbol","date"],keep="last")

def daily_features(nse):
    z=nse.copy()
    z["ret1"]=z.groupby("symbol")["close"].pct_change()
    z["gap"] = z["open"]/z.groupby("symbol")["close"].shift(1)-1
    z["adv20"]=z.groupby("symbol")["turnover"].transform(lambda s:s.rolling(20,min_periods=20).mean())
    z["adv60"]=z.groupby("symbol")["turnover"].transform(lambda s:s.rolling(60,min_periods=60).mean())
    z["vol20"]=z.groupby("symbol")["ret1"].transform(lambda s:s.rolling(20,min_periods=20).std())
    prev_close=z.groupby("symbol")["close"].shift(1)
    tr=pd.concat([(z["high"]-z["low"]),(z["high"]-prev_close).abs(),(z["low"]-prev_close).abs()],axis=1).max(axis=1)
    z["atr14"]=tr.groupby(z["symbol"]).transform(lambda s:s.ewm(alpha=1/14,adjust=False,min_periods=14).mean())
    z["atr_pct"]=z["atr14"]/z["close"]
    z["ema20"]=z.groupby("symbol")["close"].transform(lambda s:ema(s,20))
    z["ema50"]=z.groupby("symbol")["close"].transform(lambda s:ema(s,50))
    z["trend"]=z["ema20"]/z["ema50"]-1
    z["mom20"]=z.groupby("symbol")["close"].pct_change(20)
    z["vol_z"]=(z["volume"]-z.groupby("symbol")["volume"].transform(lambda s:s.rolling(20,min_periods=20).mean()))/z.groupby("symbol")["volume"].transform(lambda s:s.rolling(20,min_periods=20).std())
    z["date_key"]=z["date"].dt.strftime("%Y-%m-%d")
    return z

def market_regimes(nse):
    x=nse.copy()
    x["ret1"]=x.groupby("symbol")["close"].pct_change()
    reg=x.groupby("date").agg(
        breadth=("ret1",lambda s:float((s>0).mean())),
        market_median_ret=("ret1","median"),
        cross_sectional_dispersion=("ret1","std")
    ).reset_index()
    reg["market_vol20"]=reg["market_median_ret"].rolling(20,min_periods=20).std()
    reg["market_trend20"]=reg["market_median_ret"].rolling(20,min_periods=20).sum()
    reg["breadth_regime"]=pd.cut(reg["breadth"],[-np.inf,0.4,0.6,np.inf],labels=["weak","neutral","strong"])
    reg["vol_regime"]=pd.qcut(reg["market_vol20"],3,labels=["low","mid","high"],duplicates="drop")
    reg["trend_regime"]=np.where(reg["market_trend20"]>0,"up","down")
    return reg

def cross_market_basis(nse,bse):
    if bse.empty: return pd.DataFrame(columns=["date","symbol","basis","basis_abs","basis_lag1"])
    n=nse[["date","symbol","close"]].rename(columns={"close":"nse_close"})
    b=bse[["date","symbol","close"]].rename(columns={"close":"bse_close"})
    m=n.merge(b,on=["date","symbol"],how="inner")
    m["basis"]=m["bse_close"]/m["nse_close"]-1
    m["basis_abs"]=m["basis"].abs()
    m=m.sort_values(["symbol","date"])
    m["basis_lag1"]=m.groupby("symbol")["basis"].shift(1)
    return m[["date","symbol","basis","basis_abs","basis_lag1"]]

def backtest_daily(g, kind, mc):
    g=g.sort_values("date").reset_index(drop=True)
    g["e20"]=ema(g.close,20); g["e21"]=ema(g.close,21); g["atr"]=atr(g[["open","high","low","close"]],14)
    eq=100000.; hist=[]; pos=None; trades=[]
    for i in range(26,len(g)-1):
        r=g.iloc[i]
        if pos:
            held=i-pos["ei"]+1; exit_px=None
            if kind=="btst" and held>=1: exit_px=r.close
            elif kind=="swing":
                if r.low<=pos["stop"]: exit_px=r.open if r.open<pos["stop"] else pos["stop"]
                elif held>=8: exit_px=r.close
            if exit_px is not None:
                qty=pos["qty"]; net=(exit_px-pos["entry"])*qty-cost(pos["entry"]*qty,exit_px*qty,True); ret=net/pos["eq"]; eq+=net; hist.append(ret)
                if TEST_START<=pos["signal_date"]<=TEST_END and TEST_START<=str(r.date.date())<=TEST_END: trades.append({"entry_date":pos["signal_date"],"date":str(r.date.date()),"ret":ret,"net":net})
                pos=None
            continue
        if not np.isfinite(r.e20) or not np.isfinite(r.e21) or not np.isfinite(r.atr): continue
        up=r.e20>r.e21 and g.iloc[i-1].e20<=g.iloc[i-1].e21
        if not up: continue
        if mc and not mc_gate(hist,zlib.crc32((g.symbol.iloc[0]+kind).encode()) & 0xffffffff): continue
        entry=float(g.open.iloc[i+1]); qty=int(eq//entry)
        if qty<=0: continue
        stop=entry-0.75*r.atr if kind=="swing" else entry
        pos={"ei":i+1,"entry":entry,"qty":qty,"eq":eq,"entry_date":str(g.date.iloc[i+1].date()),"signal_date":str(g.date.iloc[i].date()),"stop":stop}
    return trades

def backtest_15m(df,symbol,mc):
    if df.empty: return []
    d=df.copy().sort_index()
    d["e20"]=ema(d.close,20); d["e26"]=ema(d.close,26); d["atr"]=atr(d)
    eq=100000.; hist=[]; pos=None; trades=[]
    for i in range(27,len(d)-1):
        r=d.iloc[i]
        if pos:
            held=i-pos["ei"]+1; exit_px=None; reason=None
            if r.low<=pos["stop"]: exit_px=r.open if r.open<pos["stop"] else pos["stop"]; reason="stop"
            elif held>=20: exit_px=r.close; reason="time"
            if exit_px is not None:
                qty=pos["qty"]; direction=pos["dir"]
                gross=direction*(exit_px-pos["entry"])*qty
                buy=pos["entry"]*qty if direction==1 else exit_px*qty
                sell=exit_px*qty if direction==1 else pos["entry"]*qty
                net=gross-cost(buy,sell,False); ret=net/pos["eq"]; eq+=net; hist.append(ret)
                if TEST_START<=str(r.name.date())<=TEST_END: trades.append({"symbol":symbol,"entry_ts":str(d.index[pos["ei"]]),"exit_ts":str(r.name),"ret":ret,"net":net,"direction":direction,"exit_reason":reason})
                pos=None
            continue
        if not np.isfinite(r.e20) or not np.isfinite(r.e26) or not np.isfinite(r.atr): continue
        up=r.e20>r.e26 and d.e20.iloc[i-1]<=d.e26.iloc[i-1]
        dn=r.e20<r.e26 and d.e20.iloc[i-1]>=d.e26.iloc[i-1]
        if not (up or dn): continue
        if mc and not mc_gate(hist,zlib.crc32(symbol.encode()) & 0xffffffff): continue
        entry=float(d.open.iloc[i+1]); qty=int(eq//entry)
        if qty<=0: continue
        direction=1 if up else -1
        stop=entry-1.5*r.atr if direction==1 else entry+1.5*r.atr
        pos={"ei":i+1,"entry":entry,"qty":qty,"eq":eq,"dir":direction,"stop":stop}
    return trades

def summarize(trades):
    if not trades: return {"n":0,"return_pct":0.0,"pf":None,"win_rate":None}
    n=np.array([t["net"] for t in trades],float); wins=n[n>0]; losses=n[n<0]
    return {"n":int(len(n)),"return_pct":float(n.sum()/1000.),"pf":float(wins.sum()/-losses.sum()) if len(losses) else None,"win_rate":float((n>0).mean())}

def standardized_regression(df, y_col, x_cols):
    q=df[[y_col]+x_cols].replace([np.inf,-np.inf],np.nan).dropna().copy()
    if len(q)<50: return {"n":len(q),"status":"insufficient"}
    X=q[x_cols].copy()
    for col in x_cols:
        sd=X[col].std()
        X[col]=(X[col]-X[col].mean())/(sd if sd and np.isfinite(sd) else 1.0)
    X=sm.add_constant(X,has_constant="add")
    y=q[y_col].astype(float)
    model=sm.OLS(y,X).fit(cov_type="HC3")
    return {"n":int(len(q)),"r2":float(model.rsquared),"params":{k:float(v) for k,v in model.params.items()},"pvalues":{k:float(v) for k,v in model.pvalues.items()}}

def quintile_table(df, value_col):
    rows=[]
    df=df.dropna(subset=[value_col,"ret"]).copy()
    if df.empty: return rows
    try: df["q"]=pd.qcut(df[value_col],5,labels=False,duplicates="drop")+1
    except Exception: return rows
    for q,g in df.groupby("q"):
        rows.append({"factor":value_col,"quintile":int(q),"n":len(g),"mean_ret":float(g.ret.mean()),"median_ret":float(g.ret.median()),"mc_better_rate":float((g.ret_mc-g.ret_base>0).mean())})
    return rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--daily-root",required=True); ap.add_argument("--mcp-root",default="")
    ap.add_argument("--bse-root",default=""); ap.add_argument("--out",default="research_results/phase9")
    a=ap.parse_args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    nse=parse_nse_daily(list(Path(a.daily_root).glob("nse/year=*/nse_*.parquet")))
    feat=daily_features(nse)
    regimes=market_regimes(nse)
    bse=parse_bse(list(Path(a.bse_root).glob("bse/year=*/bse_*.parquet"))) if a.bse_root else pd.DataFrame()
    basis=cross_market_basis(nse,bse)
    feat=feat.merge(regimes,on="date",how="left").merge(basis,on=["date","symbol"],how="left")
    nse_test=nse[(nse.date>=TEST_START)&(nse.date<=TEST_END)]
    daily_rows=[]; feature_rows=[]; selected_rows=[]
    for symbol,g in nse.groupby("symbol",sort=True):
        if len(g)<80: continue
        for kind in ("btst","swing"):
            base=backtest_daily(g,kind,False); mc=backtest_daily(g,kind,True)
            sb=summarize([t for t in base if TEST_START<=t["date"]<=TEST_END])
            sm=summarize([t for t in mc if TEST_START<=t["date"]<=TEST_END])
            daily_rows.append({"symbol":symbol,"horizon":kind,"baseline":sb,"mc":sm,"delta_return_pct":sm["return_pct"]-sb["return_pct"]})
            for t in mc:
                d=t["entry_date"]
                fg=feat[(feat.symbol==symbol)&(feat.date_key==d)]
                if len(fg): feature_rows.append({**t,**fg.iloc[0][["adv20","adv60","vol20","atr_pct","trend","mom20","vol_z","gap","breadth","market_vol20","market_trend20","cross_sectional_dispersion","basis","basis_abs","basis_lag1"]].to_dict(),"mc":1})
            for t in base:
                d=t["entry_date"]; fg=feat[(feat.symbol==symbol)&(feat.date_key==d)]
                if len(fg): feature_rows.append({**t,**fg.iloc[0][["adv20","adv60","vol20","atr_pct","trend","mom20","vol_z","gap"]].to_dict(),"mc":0})
    pd.DataFrame(daily_rows).to_json(out/"full_nse_daily_results.json",orient="records",indent=2)
    f=pd.DataFrame(feature_rows)
    if not f.empty:
        pivot=f.groupby(["symbol","entry_date","mc"],as_index=False).agg(ret=("ret","sum"))
        base=pivot[pivot.mc==0].rename(columns={"ret":"ret_base"}).drop(columns="mc")
        mc=pivot[pivot.mc==1].rename(columns={"ret":"ret_mc"}).drop(columns="mc")
        joined=base.merge(mc,on=["symbol","entry_date"],how="outer")
        # Reattach features from all available rows.
        ff=f.sort_values("entry_date").groupby(["symbol","entry_date"],as_index=False).first()
        joined=joined.merge(ff.drop(columns=["ret","mc"],errors="ignore"),on=["symbol","entry_date"],how="left")
        factor_tables=[]
        for col in ["adv20","adv60","vol20","atr_pct","trend","mom20","vol_z","gap","breadth","market_vol20","market_trend20","cross_sectional_dispersion","basis","basis_abs","basis_lag1"]:
            factor_tables += quintile_table(joined,col)
        joined.to_csv(out/"trade_factor_panel.csv",index=False); pd.DataFrame(factor_tables).to_csv(out/"factor_quintiles.csv",index=False)
        regressors=["adv20","vol20","atr_pct","trend","mom20","vol_z","gap","breadth","market_vol20","market_trend20","cross_sectional_dispersion","basis_abs"]
        models={}
        if "ret_mc" in joined.columns:
            tmp=joined.dropna(subset=["ret_base","ret_mc"]).copy(); tmp["mc_delta"]=tmp["ret_mc"]-tmp["ret_base"]
            models["mc_delta_common"]=standardized_regression(tmp,"mc_delta",[x for x in regressors if x in tmp.columns])
        mc_only=f[f["mc"]==1].copy()
        if not mc_only.empty:
            models["mc_trade_return"]=standardized_regression(mc_only,"ret",[x for x in regressors if x in mc_only.columns])
        Path(out/"conditional_regressions.json").write_text(json.dumps(models,indent=2))
    mcp_files=list(Path(a.mcp_root).glob("*.csv"))+list(Path(a.mcp_root).glob("*.json")) if a.mcp_root else []
    intraday_rows=[]
    for p in mcp_files:
        if p.name.endswith(".error.txt"): continue
        try:
            df=parse_json_candles(p) if p.suffix==".json" else pd.read_csv(p)
            if not isinstance(df.index,pd.DatetimeIndex):
                dt="ts" if "ts" in df.columns else "timestamp" if "timestamp" in df.columns else "date"
                df["ts"]=pd.to_datetime(df[dt],errors="coerce")
                if df["ts"].dt.tz is None: df["ts"]=df["ts"].dt.tz_localize("Asia/Kolkata")
                else: df["ts"]=df["ts"].dt.tz_convert("Asia/Kolkata")
                df=df.set_index("ts")
            df=df[["open","high","low","close","volume"]].astype(float)
            symbol=p.stem
            bt=backtest_15m(df,symbol,False); mc=backtest_15m(df,symbol,True)
            intraday_rows.append({"symbol":symbol,"baseline":summarize(bt),"mc":summarize(mc),"delta_return_pct":summarize(mc)["return_pct"]-summarize(bt)["return_pct"]})
        except Exception as exc:
            intraday_rows.append({"symbol":p.stem,"error":repr(exc)})
    pd.DataFrame(intraday_rows).to_csv(out/"nifty100_15m_results.csv",index=False)
    prov={"nse_symbols":int(nse.symbol.nunique()),"nse_rows":int(len(nse)),"daily_test_start":TEST_START,"daily_test_end":TEST_END,"nifty100_files":len(mcp_files),"bse_available":bool(not bse.empty),"bse_matched_rows":int(len(basis))}
    Path(out/"provenance.json").write_text(json.dumps(prov,indent=2))
    print(json.dumps(prov,indent=2))

if __name__=="__main__": main()
