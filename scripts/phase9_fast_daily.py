#!/usr/bin/env python3
import argparse, json, math, zlib
from pathlib import Path
import numpy as np, pandas as pd, statsmodels.api as sm

FRICTION=5.0
TRAIN_START="2018-01-01"; TRAIN_END="2023-12-31"
VAL_START="2024-01-01"; VAL_END="2024-12-31"
TEST_START="2025-01-01"; TEST_END="2026-04-08"

def ema(a,n):
    return pd.Series(a).ewm(span=n,adjust=False,min_periods=n).mean().to_numpy()

def atr(a,n=14):
    close=a["close"].to_numpy(float); high=a["high"].to_numpy(float); low=a["low"].to_numpy(float)
    pc=np.roll(close,1); pc[0]=np.nan
    tr=np.maximum.reduce([high-low,np.abs(high-pc),np.abs(low-pc)])
    return pd.Series(tr).ewm(alpha=1/n,adjust=False,min_periods=n).mean().to_numpy()

def mc_gate(hist,seed):
    if len(hist)<20: return True
    h=np.asarray(hist[-30:],float); rng=np.random.default_rng(seed)
    draws=rng.choice(h,size=(250,len(h)),replace=True)
    return int(np.sum(np.prod(1+draws,axis=1)>1.0))>=125

def cost(buy,sell,delivery=True):
    t=buy+sell; brokerage=40.0; exchange=t*0.0000307; sebi=t*0.000001
    gst=0.18*(brokerage+exchange+sebi)
    stt=t*0.001 if delivery else sell*0.00025
    stamp=buy*(0.00015 if delivery else 0.00003); dp=13.5 if delivery else 0.0
    return brokerage+exchange+sebi+gst+stt+stamp+dp+t*FRICTION/10000.0

def bt_daily(g,kind,use_mc,symbol):
    a=g.sort_values("date").reset_index(drop=True)
    c=a.close.to_numpy(float); e20=ema(c,20); e21=ema(c,21); avtr=atr(a,14)
    dates=a.date.astype("datetime64[ns]").to_numpy()
    op=a.open.to_numpy(float); hi=a.high.to_numpy(float); lo=a.low.to_numpy(float)
    eq=100000.; hist=[]; trades=[]; i=26; seed=zlib.crc32((symbol+kind).encode()) & 0xffffffff
    while i < len(a)-1:
        if not (np.isfinite(e20[i]) and np.isfinite(e21[i]) and np.isfinite(avtr[i])):
            i+=1; continue
        if not (e20[i]>e21[i] and e20[i-1]<=e21[i-1]):
            i+=1; continue
        if use_mc and not mc_gate(hist,seed):
            i+=1; continue
        entry_i=i+1; entry=op[entry_i]; qty=int(eq//entry)
        if qty<=0: i+=1; continue
        stop=entry-0.75*avtr[i] if kind=="swing" else None
        exit_i=None; exit_px=None
        if kind=="btst":
            exit_i=entry_i; exit_px=a.close.iloc[entry_i]
        else:
            end=min(len(a)-1,entry_i+8-1)
            for j in range(entry_i,end+1):
                if lo[j]<=stop:
                    exit_i=j; exit_px=op[j] if op[j]<stop else stop; break
                if j==end:
                    exit_i=j; exit_px=a.close.iloc[j]
        gross=(exit_px-entry)*qty; net=gross-cost(entry*qty,exit_px*qty,True); ret=net/eq
        eq += net; hist.append(ret)
        signal_date=str(pd.Timestamp(dates[i]).date()); entry_date=str(pd.Timestamp(dates[entry_i]).date()); exit_date=str(pd.Timestamp(dates[exit_i]).date())
        trades.append({"signal_date":signal_date,"entry_date":entry_date,"date":exit_date,"ret":ret,"net":net})
        i=exit_i+1
    return trades

def summarize(t):
    if not t: return {"n":0,"return_pct":0.0,"pf":None,"win_rate":None}
    n=np.array([x["net"] for x in t],float); w=n[n>0]; l=n[n<0]
    return {"n":int(n.size),"return_pct":float(n.sum()/1000.0),"pf":float(w.sum()/-l.sum()) if l.size else None,"win_rate":float((n>0).mean())}

def features(df):
    z=df.sort_values(["symbol","date"]).copy()
    z["ret1"]=z.groupby("symbol").close.pct_change()
    prev=z.groupby("symbol").close.shift(1)
    z["gap"]=z.open/prev-1
    z["adv20"]=z.groupby("symbol").turnover.transform(lambda s:s.rolling(20,min_periods=20).mean())
    z["adv60"]=z.groupby("symbol").turnover.transform(lambda s:s.rolling(60,min_periods=60).mean())
    z["vol20"]=z.groupby("symbol").ret1.transform(lambda s:s.rolling(20,min_periods=20).std())
    tr=(z.high-z.low).where(prev.isna(),pd.concat([(z.high-z.low),(z.high-prev).abs(),(z.low-prev).abs()],axis=1).max(axis=1))
    z["atr14"]=tr.groupby(z.symbol).transform(lambda s:s.ewm(alpha=1/14,adjust=False,min_periods=14).mean())
    z["atr_pct"]=z.atr14/z.close
    z["ema20"]=z.groupby("symbol").close.transform(lambda s:s.ewm(span=20,adjust=False,min_periods=20).mean())
    z["ema50"]=z.groupby("symbol").close.transform(lambda s:s.ewm(span=50,adjust=False,min_periods=50).mean())
    z["trend"]=z.ema20/z.ema50-1
    z["mom20"]=z.groupby("symbol").close.pct_change(20)
    mv=z.groupby("symbol").volume.transform(lambda s:s.rolling(20,min_periods=20).mean())
    sv=z.groupby("symbol").volume.transform(lambda s:s.rolling(20,min_periods=20).std())
    z["vol_z"]=(z.volume-mv)/sv
    cs=z.groupby("date").agg(breadth=("ret1",lambda s:float((s>0).mean())),median_ret=("ret1","median"),dispersion=("ret1","std")).sort_index()
    cs["market_vol20"]=cs["median_ret"].rolling(20,min_periods=20).std().shift(1)
    cs["market_trend20"]=cs["median_ret"].rolling(20,min_periods=20).sum().shift(1)
    cs["breadth"]=cs["breadth"].shift(1)
    cs["dispersion"]=cs["dispersion"].shift(1)
    z=z.merge(cs[["breadth","dispersion","market_vol20","market_trend20"]],left_on="date",right_index=True,how="left")
    z["date_key"]=z.date.dt.strftime("%Y-%m-%d")
    return z

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--daily-root",required=True); ap.add_argument("--out",default="research_results/phase9_fast_daily")
    ap.add_argument("--bse-root",default="")
    a=ap.parse_args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    files=list(Path(a.daily_root).glob("nse/year=*/nse_*.parquet"))
    frames=[pd.read_parquet(p,columns=["date","symbol","isin","open","high","low","close","volume","turnover","series"]) for p in files]
    nse=pd.concat(frames,ignore_index=True)
    nse["date"]=pd.to_datetime(nse["date"])
    nse=nse[nse["series"].isin(["EQ","BE","BZ"])].sort_values(["symbol","date"]).drop_duplicates(["symbol","date"],keep="last")
    basis=pd.DataFrame()
    if a.bse_root:
        bfiles=list(Path(a.bse_root).glob("bse/year=*/bse_*.parquet"))
        if bfiles:
            bframes=[pd.read_parquet(p,columns=["date","symbol","close","series"]) for p in bfiles]
            bse=pd.concat(bframes,ignore_index=True); bse["date"]=pd.to_datetime(bse["date"])
            bse=bse[bse["series"].isin(["A","B","T"])][["date","symbol","close"]].drop_duplicates(["symbol","date"],keep="last")
            nx=nse[["date","symbol","close"]].rename(columns={"close":"nse_close"})
            basis=nx.merge(bse.rename(columns={"close":"bse_close"}),on=["date","symbol"],how="inner").sort_values(["symbol","date"])
            basis["basis"]=basis["bse_close"]/basis["nse_close"]-1
            basis["basis_lag1"]=basis.groupby("symbol")["basis"].shift(1)
            basis=basis[["date","symbol","basis_lag1"]]
    feat=features(nse)
    if not basis.empty: feat=feat.merge(basis,on=["date","symbol"],how="left")
    feat=feat.set_index(["symbol","date_key"],drop=False)
    rows=[]; feature_rows=[]
    for symbol,g in nse.groupby("symbol",sort=True):
        if len(g)<80: continue
        for kind in ("btst","swing"):
            b=bt_daily(g,kind,False,symbol); m=bt_daily(g,kind,True,symbol)
            bt=[t for t in b if TEST_START<=t["date"]<=TEST_END and TEST_START<=t["signal_date"]<=TEST_END]
            mt=[t for t in m if TEST_START<=t["date"]<=TEST_END and TEST_START<=t["signal_date"]<=TEST_END]
            rows.append({"symbol":symbol,"horizon":kind,"baseline":summarize(bt),"mc":summarize(mt),"delta_return_pct":summarize(mt)["return_pct"]-summarize(bt)["return_pct"]})
            for tag,trades in [(0,bt),(1,mt)]:
                for t in trades:
                    try: f=feat.loc[(symbol,t["signal_date"])]
                    except KeyError: continue
                    rec={**t,"symbol":symbol,"mc":tag}
                    for k in ["adv20","adv60","vol20","atr_pct","trend","mom20","vol_z","gap","breadth","dispersion","market_vol20","market_trend20","basis_lag1"]:
                        rec[k]=f[k]
                    feature_rows.append(rec)
    pd.DataFrame(rows).to_json(out/"full_nse_daily_results.json",orient="records",indent=2)
    f=pd.DataFrame(feature_rows)
    if not f.empty:
        p=f.groupby(["symbol","signal_date","mc"],as_index=False).ret.sum().pivot_table(index=["symbol","signal_date"],columns="mc",values="ret",aggfunc="sum").reset_index().rename(columns={0:"ret_base",1:"ret_mc"})
        fp=f.sort_values("signal_date").groupby(["symbol","signal_date"],as_index=False).first()
        p=p.merge(fp.drop(columns=["ret","mc"],errors="ignore"),on=["symbol","signal_date"],how="left")
        p["mc_accept"]=p["ret_mc"].notna().astype(int)
        factors=[]
        for col in ["adv20","adv60","vol20","atr_pct","trend","mom20","vol_z","gap"]:
            q=p[[col,"ret_base","ret_mc"]].dropna().copy()
            if q.empty: continue
            q["q"]=pd.qcut(q[col],5,labels=False,duplicates="drop")+1
            for k,gq in q.groupby("q"):
                factors.append({"factor":col,"quintile":int(k),"n":len(gq),"mean_base":float(gq.ret_base.mean()),"mean_mc":float(gq.ret_mc.mean()),"mean_delta":float((gq.ret_mc-gq.ret_base).mean()),"mc_better_rate":float((gq.ret_mc>gq.ret_base).mean())})
        pd.DataFrame(factors).to_csv(out/"factor_quintiles.csv",index=False); p.to_csv(out/"trade_factor_panel.csv",index=False)
        X=p[[c for c in ["adv20","vol20","atr_pct","trend","mom20","vol_z","gap"] if c in p]].replace([np.inf,-np.inf],np.nan)
        m=p[["ret_base","ret_mc"]].dropna().copy(); m["delta"]=m.ret_mc-m.ret_base
        common=pd.concat([X,m],axis=1).dropna()
        if len(common)>=50:
            Xs=common[X.columns].copy()
            for col in X.columns:
                s=Xs[col].std(); Xs[col]=(Xs[col]-Xs[col].mean())/(s if np.isfinite(s) and s else 1)
            mod=sm.OLS(common.delta,sm.add_constant(Xs,has_constant="add")).fit(cov_type="HC3")
            Path(out/"conditional_regression.json").write_text(json.dumps({"n":len(common),"r2":float(mod.rsquared),"params":{k:float(v) for k,v in mod.params.items()},"pvalues":{k:float(v) for k,v in mod.pvalues.items()}},indent=2))
    if not f.empty:
        acceptance=f.groupby("symbol")["mc"].mean().rename("mc_accept_rate").reset_index()
        acceptance.to_csv(out/"symbol_mc_acceptance.csv",index=False)
        common=p.dropna(subset=["ret_base","ret_mc"]).copy() if not p.empty else pd.DataFrame()
        if len(common)>=20:
            base_sym=common.groupby("symbol")["ret_base"].mean()
            mc_sym=common.groupby("symbol")["ret_mc"].mean()
            delta=mc_sym.sub(base_sym,fill_value=np.nan).dropna()
            rng=np.random.default_rng(9022026); syms=delta.index.to_numpy(); vals=[]
            for _ in range(2000): vals.append(float(delta.reindex(rng.choice(syms,size=len(syms),replace=True)).mean()))
            Path(out/"paired_mc_delta_bootstrap.json").write_text(json.dumps({"symbol_n":int(len(delta)),"mean_delta":float(delta.mean()),"ci95_low":float(np.quantile(vals,0.025)),"ci95_high":float(np.quantile(vals,0.975))},indent=2))
    Path(out/"provenance.json").write_text(json.dumps({"nse_symbols":int(nse.symbol.nunique()),"nse_rows":int(len(nse)),"nse_start":str(nse.date.min().date()),"nse_end":str(nse.date.max().date()),"test_start":TEST_START,"test_end":TEST_END},indent=2))
if __name__=="__main__": main()
