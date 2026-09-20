#!/usr/bin/env python3
import argparse, json, math, zlib
from collections import defaultdict
from pathlib import Path
import numpy as np, pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

FRICTION_BPS=5.0; TEST_START='2025-01-01'; TEST_END='2026-04-08'

def ema(s,n): return s.ewm(span=n,adjust=False,min_periods=n).mean()
def atr(df,n=14):
    pc=df.close.shift(1); tr=pd.concat([df.high-df.low,(df.high-pc).abs(),(df.low-pc).abs()],axis=1).max(axis=1)
    return tr.ewm(alpha=1/n,adjust=False,min_periods=n).mean()
def cost(buy,sell):
    t=buy+sell; brokerage=40.0; exchange=t*0.0000307; sebi=t*0.000001; gst=0.18*(brokerage+exchange+sebi); stt=t*0.001; stamp=buy*0.00015; dp=13.5
    return brokerage+exchange+sebi+gst+stt+stamp+dp+t*FRICTION_BPS/10000.0
def mc_gate(hist,seed):
    if len(hist)<20: return True
    h=np.asarray(hist[-30:],float); rng=np.random.default_rng(seed); draws=rng.choice(h,size=(250,len(h)),replace=True)
    return int((np.prod(1+draws,axis=1)>1).sum())>=125
def features(g):
    g=g.sort_values('date').copy(); g['ret1']=g.close.pct_change(); prev=g.close.shift(1); g['gap']=g.open/prev-1
    g['adv20']=(g.close*g.volume).rolling(20,min_periods=20).mean().shift(1); g['adv60']=(g.close*g.volume).rolling(60,min_periods=60).mean().shift(1)
    g['vol20']=g.ret1.rolling(20,min_periods=20).std().shift(1); g['atr_pct']=(atr(g)/g.close).shift(1)
    e20=ema(g.close,20); e50=ema(g.close,50); g['trend']=(e20/e50-1).shift(1); g['mom20']=g.close.pct_change(20).shift(1)
    vm=g.volume.rolling(20,min_periods=20).mean(); vs=g.volume.rolling(20,min_periods=20).std(); g['vol_z']=((g.volume-vm)/vs).shift(1)
    return g
def backtest(g,kind,use_mc,symbol,factor_cols):
    a=g.sort_values('date').reset_index(drop=True); c=a.close.to_numpy(float); e20=ema(a.close,20); e21=ema(a.close,21); avtr=atr(a,14)
    eq=100000.; hist=[]; pos=None; trades=[]; seed=zlib.crc32((symbol+kind).encode()) & 0xffffffff
    for i in range(26,len(a)-1):
        r=a.iloc[i]
        if pos:
            held=i-pos['ei']+1; ex=None
            if kind=='btst' and held>=1: ex=r.close
            elif kind=='swing':
                if r.low<=pos['stop']: ex=r.open if r.open<pos['stop'] else pos['stop']
                elif held>=8: ex=r.close
            if ex is not None:
                qty=pos['qty']; net=(ex-pos['entry'])*qty-cost(pos['entry']*qty,ex*qty); ret=net/pos['eq']; eq+=net; hist.append(ret)
                if TEST_START<=pos['signal_date']<=TEST_END and TEST_START<=str(r.date.date())<=TEST_END:
                    rec=dict(pos['factor']); rec.update({'symbol':symbol,'signal_date':pos['signal_date'],'ret':ret,'net':net}); trades.append(rec)
                pos=None
            continue
        if not (np.isfinite(e20[i]) and np.isfinite(e21[i]) and np.isfinite(avtr[i])): continue
        up=bool(e20[i]>e21[i] and e20[i-1]<=e21[i-1]);
        if not up: continue
        signal_date=str(a.date.iloc[i].date()); f={k:a.iloc[i][k] if k in a.columns else np.nan for k in factor_cols}
        if use_mc and not mc_gate(hist,seed): continue
        entry=float(a.open.iloc[i+1]); qty=int(eq//entry);
        if qty<=0: continue
        stop=entry-0.75*avtr[i] if kind=='swing' else None
        pos={'ei':i+1,'entry':entry,'qty':qty,'eq':eq,'signal_date':signal_date,'stop':stop,'factor':f}
    return trades
def load(root,exchange):
    fs=list(Path(root).glob(f'{exchange}/year=*/{exchange}_*.parquet')); frames=[]
    for p in fs: frames.append(pd.read_parquet(p,columns=['date','symbol','isin','series','open','high','low','close','volume','turnover']))
    x=pd.concat(frames,ignore_index=True); x['date']=pd.to_datetime(x.date);
    if 'series' in x: x=x[x.series.isin(['EQ','BE','BZ'])]
    return x.sort_values(['symbol','date']).drop_duplicates(['symbol','date'],keep='last')
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',required=True); ap.add_argument('--out',default='research_results/phase9_crossmarket_daily'); a=ap.parse_args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    n=load(a.root,'nse'); b=load(a.root,'bse')
    n['ret1']=n.groupby('symbol').close.pct_change();
    reg=n.groupby('date').ret1.agg(breadth=lambda s:float((s>0).mean()),dispersion='std',median_ret='median').reset_index();
    pvt=n[['date','symbol','close']].rename(columns={'close':'nse_close'}).merge(b[['date','symbol','close']].rename(columns={'close':'bse_close'}),on=['date','symbol'],how='inner');
    pvt['basis']=pvt.bse_close/pvt.nse_close-1; pvt=pvt.sort_values(['symbol','date']); pvt['basis_lag1']=pvt.groupby('symbol').basis.shift(1); pvt['basis_abs_lag1']=pvt.groupby('symbol').basis.abs().shift(1);
    factors=['adv20','adv60','vol20','atr_pct','trend','mom20','vol_z','gap','breadth','dispersion','basis_lag1','basis_abs_lag1']; summary=[]; panel=[]
    for symbol,g in n.groupby('symbol',sort=True):
        if len(g)<80: continue
        f=features(g).merge(reg,on='date',how='left').merge(pvt[['date','symbol','basis_lag1','basis_abs_lag1']],on=['date','symbol'],how='left')
        for kind in ['btst','swing']:
            base=backtest(f,kind,False,symbol,factors); mc=backtest(f,kind,True,symbol,factors);
            summary.append({'symbol':symbol,'horizon':kind,'baseline_return_pct':100*sum(t['net'] for t in base)/100000,'baseline_n':len(base),'mc_return_pct':100*sum(t['net'] for t in mc)/100000,'mc_n':len(mc),'delta_return_pct':100*(sum(t['net'] for t in mc)-sum(t['net'] for t in base))/100000});
            bm={(t['signal_date']):t for t in base}; mm={(t['signal_date']):t for t in mc}
            for d,t in bm.items():
                rec={k:t.get(k) for k in factors}; rec.update({'symbol':symbol,'horizon':kind,'signal_date':d,'baseline_ret':t['ret'],'mc_accept':int(d in mm),'mc_ret':mm[d]['ret'] if d in mm else np.nan}); panel.append(rec)
    pf=pd.DataFrame(summary); pf.to_csv(out/'per_symbol_results.csv',index=False); p=pd.DataFrame(panel); p.to_csv(out/'trade_factor_panel.csv',index=False)
    qs=[]
    for c in factors:
        if c not in p: continue
        q=p[[c,'mc_accept','baseline_ret','mc_ret']].dropna().copy();
        if q.empty: continue
        q['quintile']=pd.qcut(q[c],5,labels=False,duplicates='drop')+1
        for k,g in q.groupby('quintile'): qs.append({'factor':c,'quintile':int(k),'n':len(g),'mc_accept_rate':float(g.mc_accept.mean()),'baseline_mean_ret':float(g.baseline_ret.mean()),'mc_mean_ret':float(g.mc_ret.dropna().mean()) if g.mc_ret.notna().any() else np.nan,'mc_win_rate':float((g.mc_ret.dropna()>0).mean()) if g.mc_ret.notna().any() else np.nan})
    pd.DataFrame(qs).to_csv(out/'factor_quintiles.csv',index=False)
    tests=[]; Xcols=[c for c in factors if c in p.columns]; z=p.dropna(subset=Xcols).copy()
    if len(z)>=50:
        X=z[Xcols].copy();
        for c in Xcols: s=X[c].std(); X[c]=(X[c]-X[c].mean())/(s if np.isfinite(s) and s else 1)
        X=sm.add_constant(X,has_constant='add')
        try:
            m=sm.GLM(z.mc_accept.astype(float),X,family=sm.families.Binomial()).fit(cov_type='HC3')
            for c in Xcols: tests.append({'model':'mc_accept','factor':c,'coef':float(m.params[c]),'p':float(m.pvalues[c])})
        except Exception as e: pass
        a2=z[z.mc_accept==1].dropna(subset=['mc_ret']);
        if len(a2)>=50:
            Xa=a2[Xcols].copy();
            for c in Xcols: s=Xa[c].std(); Xa[c]=(Xa[c]-Xa[c].mean())/(s if np.isfinite(s) and s else 1)
            try:
                m=sm.OLS(a2.mc_ret,sm.add_constant(Xa,has_constant='add')).fit(cov_type='HC3')
                for c in Xcols: tests.append({'model':'mc_return','factor':c,'coef':float(m.params[c]),'p':float(m.pvalues[c])})
            except Exception as e: pass
    if tests:
        _,q,_,_=multipletests([t['p'] for t in tests],alpha=0.05,method='fdr_bh')
        for t,v in zip(tests,q): t['fdr_p']=float(v); t['fdr_significant']=bool(v<0.05)
    Path(out/'conditional_regressions.json').write_text(json.dumps({'tests':tests,'n_rows':len(p)},indent=2));
    Path(out/'provenance.json').write_text(json.dumps({'nse_symbols':int(n.symbol.nunique()),'nse_start':str(n.date.min().date()),'nse_end':str(n.date.max().date()),'bse_symbols':int(b.symbol.nunique()),'bse_start':str(b.date.min().date()),'bse_end':str(b.date.max().date()),'test_start':TEST_START,'test_end':TEST_END,'friction_bps_per_leg':FRICTION_BPS},indent=2))
if __name__=='__main__': main()