#!/usr/bin/env python3
import argparse, json, math, zlib
from collections import defaultdict
from pathlib import Path
import numpy as np, pandas as pd, pyarrow.parquet as pq
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

FRICTION_BPS=5.0
TEST_START=pd.Timestamp('2026-01-01',tz='Asia/Kolkata')
TEST_END=pd.Timestamp('2026-01-21 23:59',tz='Asia/Kolkata')

def ema(s,n): return s.ewm(span=n,adjust=False,min_periods=n).mean()
def atr(df,n=14):
    pc=df.close.shift(1)
    tr=pd.concat([df.high-df.low,(df.high-pc).abs(),(df.low-pc).abs()],axis=1).max(axis=1)
    return tr.ewm(alpha=1/n,adjust=False,min_periods=n).mean()
def cost(buy,sell):
    t=buy+sell; brokerage=40.0; exchange=t*0.0000307; sebi=t*0.000001
    gst=0.18*(brokerage+exchange+sebi); stt=sell*0.00025; stamp=buy*0.00003
    return brokerage+exchange+sebi+gst+stt+stamp+t*FRICTION_BPS/10000.0
def mc_gate(hist,seed):
    if len(hist)<20: return True
    h=np.asarray(hist[-30:],float); rng=np.random.default_rng(seed)
    draws=rng.choice(h,size=(250,len(h)),replace=True)
    return int((np.prod(1+draws,axis=1)>1).sum())>=125
def resample15(df):
    return df.resample('15min',origin='start_day',offset='15min',label='left',closed='left').agg({'open':'first','high':'max','low':'min','close':'last','volume':'sum'}).dropna(subset=['open','high','low','close'])
def daily_features(m15):
    d=m15.resample('1D').agg({'open':'first','high':'max','low':'min','close':'last','volume':'sum'}).dropna(subset=['close'])
    d['ret1']=d.close.pct_change(); prev=d.close.shift(1); d['gap']=d.open/prev-1
    d['adv20']=(d.close*d.volume).rolling(20,min_periods=20).mean().shift(1)
    d['adv60']=(d.close*d.volume).rolling(60,min_periods=60).mean().shift(1)
    d['vol20']=d.ret1.rolling(20,min_periods=20).std().shift(1)
    d['atr_pct']=(atr(d)/d.close).shift(1)
    e20=ema(d.close,20); e50=ema(d.close,50); d['trend']=(e20/e50-1).shift(1)
    d['mom20']=d.close.pct_change(20).shift(1)
    vm=d.volume.rolling(20,min_periods=20).mean(); vs=d.volume.rolling(20,min_periods=20).std(); d['vol_z']=((d.volume-vm)/vs).shift(1)
    return d
def simulate(m15,feat,symbol,use_mc):
    d=m15.copy(); d['e20']=ema(d.close,20); d['e26']=ema(d.close,26); d['atr']=atr(d)
    eq=100000.; hist=[]; pos=None; trades=[]; seed=zlib.crc32(symbol.encode()) & 0xffffffff
    for i in range(27,len(d)-1):
        r=d.iloc[i]
        if pos is not None:
            held=i-pos['entry_i']+1; exit_px=None; reason=None
            if pos['dir']==1 and r.low<=pos['stop']: exit_px=r.open if r.open<pos['stop'] else pos['stop']; reason='stop'
            elif pos['dir']==-1 and r.high>=pos['stop']: exit_px=r.open if r.open>pos['stop'] else pos['stop']; reason='stop'
            elif held>=20: exit_px=r.close; reason='time'
            if exit_px is not None:
                qty=pos['qty']; gross=pos['dir']*(exit_px-pos['entry'])*qty
                buy=pos['entry']*qty if pos['dir']==1 else exit_px*qty; sell=exit_px*qty if pos['dir']==1 else pos['entry']*qty
                net=gross-cost(buy,sell); ret=net/pos['eq']; eq+=net; hist.append(ret)
                rec=dict(pos['rec']); rec.update({'exit_ts':str(d.index[i]),'net':net,'ret':ret,'exit_reason':reason}); trades.append(rec); pos=None
            continue
        if not (np.isfinite(r.e20) and np.isfinite(r.e26) and np.isfinite(r.atr)): continue
        up=bool(r.e20>r.e26 and d.e20.iloc[i-1]<=d.e26.iloc[i-1]); dn=bool(r.e20<r.e26 and d.e20.iloc[i-1]>=d.e26.iloc[i-1])
        if not (up or dn): continue
        signal_ts=d.index[i]
        factor=feat.loc[signal_ts.normalize()].to_dict() if signal_ts.normalize() in feat.index else {}
        accepted=(not use_mc) or mc_gate(hist,seed)
        entry_i=i+1; entry=float(d.open.iloc[entry_i]); qty=int(eq//entry)
        if qty<=0: continue
        direction=1 if up else -1; stop=entry-1.5*r.atr if direction==1 else entry+1.5*r.atr
        if accepted: pos={'entry_i':entry_i,'entry':entry,'qty':qty,'eq':eq,'dir':direction,'stop':stop,'rec':{'symbol':symbol,'signal_ts':str(signal_ts),'signal_date':str(signal_ts.date()),**factor}}
    return trades
def iter_symbol_groups(path):
    pf=pq.ParquetFile(path); carry=None
    cols=['symbol','timestamp','open','high','low','close','volume']
    for batch in pf.iter_batches(batch_size=250000,columns=cols):
        df=batch.to_pandas()
        if carry is not None: df=pd.concat([carry,df],ignore_index=True); carry=None
        if df.empty: continue
        last=df.symbol.iloc[-1]; tail=df[df.symbol.eq(last)].copy(); head=df.iloc[:-len(tail)] if len(tail) else df
        for sym,g in head.groupby('symbol',sort=False): yield sym,g.drop(columns='symbol')
        carry=tail
    if carry is not None and not carry.empty: yield carry.symbol.iloc[0],carry.drop(columns='symbol')
def prep_raw(g):
    ts=pd.to_datetime(g.timestamp,utc=True,errors='coerce').dt.tz_convert('Asia/Kolkata')
    g=g.assign(ts=ts).dropna(subset=['ts','open','high','low','close']).copy()
    g=g[(g.ts.dt.time>=pd.Timestamp('09:15').time())&(g.ts.dt.time<=pd.Timestamp('15:30').time())].set_index('ts')
    return g[['open','high','low','close','volume']].astype(float)
def stats(trades):
    n=np.array([t['net'] for t in trades],float) if trades else np.array([]); w=n[n>0]; l=n[n<0]
    return {'n':int(len(n)),'return_pct':float(n.sum()/1000.0),'pf':float(w.sum()/-l.sum()) if len(l) else None,'win_rate':float((n>0).mean()) if len(n) else None}
def fdr_regression(df):
    factors=[c for c in ['adv20','adv60','vol20','atr_pct','trend','mom20','vol_z','gap','market_vol20','market_trend20','breadth','dispersion'] if c in df.columns]
    if len(df)<50 or not factors: return {}
    z=df.replace([np.inf,-np.inf],np.nan).dropna(subset=factors).copy(); out=[]
    if len(z)<50: return {}
    X=z[factors].copy()
    for c in factors: s=X[c].std(); X[c]=(X[c]-X[c].mean())/(s if np.isfinite(s) and s else 1.0)
    X=sm.add_constant(X,has_constant='add')
    try:
        m=sm.GLM(z.mc_accept.astype(float),X,family=sm.families.Binomial()).fit(cov_type='HC3')
        for c in factors: out.append({'model':'mc_accept','factor':c,'coef':float(m.params[c]),'p':float(m.pvalues[c])})
    except Exception as e: return {'error':repr(e)}
    a=z[z.mc_accept==1].dropna(subset=['mc_ret'])
    if len(a)>=50:
        Xa=a[factors].copy()
        for c in factors: s=Xa[c].std(); Xa[c]=(Xa[c]-Xa[c].mean())/(s if np.isfinite(s) and s else 1.0)
        try:
            m=sm.OLS(a.mc_ret,sm.add_constant(Xa,has_constant='add')).fit(cov_type='HC3')
            for c in factors: out.append({'model':'mc_return','factor':c,'coef':float(m.params[c]),'p':float(m.pvalues[c])})
        except Exception as e: pass
    p=np.array([x['p'] for x in out]); _,q,_,_=multipletests(p,alpha=0.05,method='fdr_bh')
    for x,v in zip(out,q): x['fdr_p']=float(v); x['fdr_significant']=bool(v<0.05)
    return {'n':len(z),'tests':out}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',default='research_results/phase9_full_nse_intraday'); ap.add_argument('--repo-id',default='rahulkrraj/indian-stock-market-minute-data')
    a=ap.parse_args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True); work=Path('.cache/phase9_fullminute'); work.mkdir(parents=True,exist_ok=True)
    from huggingface_hub import hf_hub_download
    summary=[]; panel=[]; breadth=defaultdict(lambda:[0,0,0.0,0.0]); market={}
    for idx in range(8):
        path=hf_hub_download(repo_id=a.repo_id,filename=f'minute/train-{idx:05d}.parquet',repo_type='dataset',local_dir=str(work))
        for symbol,g in iter_symbol_groups(path):
            raw=prep_raw(g)
            if len(raw)<2000: continue
            m15=resample15(raw); feat=daily_features(m15)
            rr=feat.ret1.dropna()
            for dt,v in rr.items():
                key=str(dt.date()); st=breadth[key]; st[0]+=1; st[1]+=int(v>0); st[2]+=float(v); st[3]+=float(v*v)
            if symbol=='NIFTY_50':
                for dt,r in feat.iterrows(): market[str(dt.date())]={'market_vol20':r.get('vol20'),'market_trend20':r.get('trend')}
            bt=simulate(m15,feat,symbol,False); mc=simulate(m15,feat,symbol,True)
            bt=[t for t in bt if TEST_START<=pd.Timestamp(t['signal_ts'])<=TEST_END]; mc=[t for t in mc if TEST_START<=pd.Timestamp(t['signal_ts'])<=TEST_END]
            summary.append({'symbol':symbol,'baseline':stats(bt),'mc':stats(mc)})
            b={t['signal_ts']:t for t in bt}; mm={t['signal_ts']:t for t in mc}
            for ts,t in b.items():
                r=dict(t); r['baseline_ret']=t['ret']; r['baseline_net']=t['net']; r['mc_accept']=int(ts in mm); r['mc_ret']=mm[ts]['ret'] if ts in mm else np.nan; r['mc_net']=mm[ts]['net'] if ts in mm else np.nan; panel.append(r)
        try: Path(path).unlink()
        except Exception: pass
    p=pd.DataFrame(panel)
    if not p.empty:
        p['signal_date']=pd.to_datetime(p.signal_date); p['breadth']=p.signal_date.map(lambda d:(breadth.get(str(d.date())) or [0,0,np.nan,np.nan])[1]/max((breadth.get(str(d.date())) or [0])[0],1)); p['dispersion']=p.signal_date.map(lambda d:(lambda st: math.sqrt(max(st[3]/st[0]-(st[2]/st[0])**2,0)) if st and st[0] else np.nan)(breadth.get(str(d.date()))); p['market_vol20']=p.signal_date.map(lambda d:(market.get(str(d.date())) or {}).get('market_vol20')); p['market_trend20']=p.signal_date.map(lambda d:(market.get(str(d.date())) or {}).get('market_trend20'))
        p.to_csv(out/'signal_panel.csv',index=False);
        qs=[]
        for c in ['adv20','adv60','vol20','atr_pct','trend','mom20','vol_z','gap','market_vol20','market_trend20','breadth','dispersion']:
            if c not in p.columns: continue
            q=p[[c,'mc_accept','baseline_ret','mc_ret']].dropna().copy()
            if q.empty: continue
            q['quintile']=pd.qcut(q[c],5,labels=False,duplicates='drop')+1
            for k,g in q.groupby('quintile'): qs.append({'factor':c,'quintile':int(k),'n':len(g),'mc_accept_rate':float(g.mc_accept.mean()),'baseline_mean_ret':float(g.baseline_ret.mean()),'mc_mean_ret':float(g.mc_ret.dropna().mean()) if g.mc_ret.notna().any() else np.nan,'mc_win_rate':float((g.mc_ret.dropna()>0).mean()) if g.mc_ret.notna().any() else np.nan})
        pd.DataFrame(qs).to_csv(out/'factor_quintiles_descriptive.csv',index=False); Path(out/'conditional_regressions.json').write_text(json.dumps(fdr_regression(p),indent=2))
    per=[]
    for s in summary: per.append({'symbol':s['symbol'],'baseline_return_pct':s['baseline']['return_pct'],'baseline_pf':s['baseline']['pf'],'baseline_n':s['baseline']['n'],'mc_return_pct':s['mc']['return_pct'],'mc_pf':s['mc']['pf'],'mc_n':s['mc']['n'],'delta_return_pct':s['mc']['return_pct']-s['baseline']['return_pct']})
    pf=pd.DataFrame(per); pf.to_csv(out/'per_symbol_intraday_results.csv',index=False)
    concentration={}
    if not pf.empty:
        winners=pf[pf.mc_return_pct>0].sort_values('mc_return_pct',ascending=False); concentration={'symbols':int(len(pf)),'positive_symbols':int((pf.mc_return_pct>0).sum()),'median_return_pct':float(pf.mc_return_pct.median()),'mean_return_pct':float(pf.mc_return_pct.mean()),'top10_return_share':float(winners.head(10).mc_return_pct.sum()/winners.mc_return_pct.sum()) if winners.mc_return_pct.sum()!=0 else None}
    Path(out/'concentration.json').write_text(json.dumps(concentration,indent=2)); Path(out/'provenance.json').write_text(json.dumps({'repo_id':a.repo_id,'minute_coverage':'2022-01-03 to 2026-01-21','train':'2022-01-03 to 2024-12-31','validation':'2025','test':'2026-01-01 to 2026-01-21','friction_bps_per_leg':FRICTION_BPS,'shards':8},indent=2))
if __name__=='__main__': main()