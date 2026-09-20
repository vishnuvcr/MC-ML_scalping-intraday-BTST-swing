import argparse, glob, json, math, os, zlib
from pathlib import Path
import numpy as np
import pandas as pd

SYMBOLS = ['TCS','RELIANCE','HDFCBANK','INFY','ICICIBANK','SBIN','AXISBANK','BHARTIARTL','KOTAKBANK','ITC','LT','HCLTECH','BAJFINANCE','MARUTI','HINDUNILVR','SUNPHARMA','TATASTEEL','ADANIPORTS','NTPC','ONGC']
HF_TRAIN=('2024-04-01','2025-06-30'); HF_VAL=('2025-07-01','2025-12-31'); HF_TEST=('2026-01-01','2026-04-30')
DAY_TRAIN=('2018-01-01','2024-12-31'); DAY_VAL=('2025-01-01','2025-12-31'); DAY_TEST=('2026-01-01','2026-09-18')

def ema(s,n): return s.ewm(span=n,adjust=False,min_periods=n).mean()
def atr(df,n=14):
    pc=df['close'].shift(1)
    tr=pd.concat([df['high']-df['low'],(df['high']-pc).abs(),(df['low']-pc).abs()],axis=1).max(axis=1)
    return tr.ewm(alpha=1/n,adjust=False,min_periods=n).mean()

def parse_intraday(p):
    files=glob.glob(str(Path(p)/'*.csv*'))
    if not files: raise FileNotFoundError(p)
    f=files[0]; df=pd.read_csv(f)
    cols={c.lower():c for c in df.columns}
    dt=cols.get('datetime') or cols.get('timestamp') or cols.get('date')
    rename={cols[x]:x for x in ['open','high','low','close','volume'] if x in cols}
    df=df.rename(columns=rename)
    df['ts']=pd.to_datetime(df[dt],utc=True,errors='coerce') if getattr(pd.to_datetime(df[dt],errors='coerce').dt,'tz',None) is None else pd.to_datetime(df[dt],errors='coerce')
    # Convert naive/offset-aware timestamps to IST
    if df['ts'].dt.tz is None: df['ts']=df['ts'].dt.tz_localize('Asia/Kolkata')
    else: df['ts']=df['ts'].dt.tz_convert('Asia/Kolkata')
    df=df.dropna(subset=['ts','open','high','low','close']).sort_values('ts').drop_duplicates('ts')
    df=df[(df['ts'].dt.time>=pd.Timestamp('09:15').time()) & (df['ts'].dt.time<=pd.Timestamp('15:30').time())]
    return df.set_index('ts')[['open','high','low','close','volume']].astype(float)

def resample_ohlcv(df,rule):
    x=df.resample(rule,origin='start_day',offset='15min',label='left',closed='left').agg({'open':'first','high':'max','low':'min','close':'last','volume':'sum'})
    return x.dropna(subset=['open','high','low','close'])

def parse_daily_json(path):
    obj=json.loads(Path(path).read_text())
    data=obj.get('data',obj.get('results',obj)) if isinstance(obj,dict) else obj
    df=pd.DataFrame(data)
    df['date']=pd.to_datetime(df['date'])
    keep=[c for c in ['date','open','high','low','close','volume'] if c in df.columns]
    return df[keep].set_index('date').sort_index().astype(float)

def mc_gate(history,seed):
    if len(history)<20: return True
    h=np.asarray(history[-30:],dtype=float); rng=np.random.default_rng(seed)
    draws=rng.choice(h,size=(250,len(h)),replace=True)
    positive=np.sum(np.prod(1+draws,axis=1)>1.0)
    return positive>=125

def costs(buy,sell,delivery,friction_bps):
    turnover=buy+sell; brokerage=40.0; exchange=turnover*0.0000307; sebi=turnover*0.000001
    gst=0.18*(brokerage+exchange+sebi); stt=turnover*0.001 if delivery else sell*0.00025
    stamp=buy*(0.00015 if delivery else 0.00003); dp=13.5 if delivery else 0.0
    return brokerage+exchange+sebi+gst+stt+stamp+dp+turnover*friction_bps/10000.0

def classify(d,kind):
    s=d.strftime('%Y-%m-%d')
    if kind in ('scalp','intraday'):
        return 'train' if HF_TRAIN[0]<=s<=HF_TRAIN[1] else 'val' if HF_VAL[0]<=s<=HF_VAL[1] else 'test' if HF_TEST[0]<=s<=HF_TEST[1] else None
    return 'train' if DAY_TRAIN[0]<=s<=DAY_TRAIN[1] else 'val' if DAY_VAL[0]<=s<=DAY_VAL[1] else 'test' if DAY_TEST[0]<=s<=DAY_TEST[1] else None

def run(df,kind,friction,mc,symbol):
    df=df.copy(); df['ema20']=ema(df.close,20); df['ema26']=ema(df.close,26) if kind in ('scalp','intraday') else ema(df.close,21); df['atr']=atr(df)
    equity=100000.0; peak=equity; maxdd=0.0; hist=[]; trades=[]; pos=None
    max_hold=12 if kind=='scalp' else 20 if kind=='intraday' else 1 if kind=='btst' else 8
    delivery=kind in ('btst','swing')
    idx=list(df.index)
    for i in range(27,len(df)-1):
        row=df.iloc[i]
        if pos is not None:
            held=i-pos['entry_i']+1; exit_px=None
            if kind=='btst': exit_px=row.close if held>=1 else None
            else:
                if kind=='swing':
                    if row.low<=pos['stop']: exit_px=row.open if row.open<pos['stop'] else pos['stop']
                else:
                    if pos['dir']==1 and row.low<=pos['stop']: exit_px=row.open if row.open<pos['stop'] else pos['stop']
                    if pos['dir']==-1 and row.high>=pos['stop']: exit_px=row.open if row.open>pos['stop'] else pos['stop']
                if exit_px is None and held>=max_hold: exit_px=row.close
            if exit_px is not None:
                qty=pos['qty']; gross=pos['dir']*(exit_px-pos['entry'])*qty; buy=pos['entry']*qty if pos['dir']==1 else exit_px*qty; sell=exit_px*qty if pos['dir']==1 else pos['entry']*qty
                net=gross-costs(buy,sell,delivery,friction); ret=net/pos['equity_before']; equity+=net; peak=max(peak,equity); maxdd=min(maxdd,equity/peak-1); hist.append(ret)
                trades.append({'symbol':symbol,'entry':str(idx[pos['entry_i']].date()),'exit':str(idx[i].date()),'net':net,'ret':ret,'equity':equity}) ; pos=None
            if equity<1000: break
            continue
        up=bool(df.ema20.iloc[i]>df.ema26.iloc[i] and df.ema20.iloc[i-1]<=df.ema26.iloc[i-1])
        dn=bool(df.ema20.iloc[i]<df.ema26.iloc[i] and df.ema20.iloc[i-1]>=df.ema26.iloc[i-1])
        signal=(up or dn) if kind in ('scalp','intraday') else up
        if not signal: continue
        if mc and not mc_gate(hist,zlib.crc32(f'{symbol}-{kind}'.encode()) & 0xffffffff): continue
        entry=float(df.open.iloc[i+1]); qty=int(math.floor(equity/entry))
        if qty<=0 or not np.isfinite(df.atr.iloc[i]): continue
        direction=1 if up else -1
        stop=entry-1.5*float(df.atr.iloc[i]) if direction==1 else entry+1.5*float(df.atr.iloc[i])
        if kind=='swing': stop=entry-0.75*float(df.atr.iloc[i]); direction=1
        pos={'entry_i':i+1,'entry':entry,'qty':qty,'dir':direction,'stop':stop,'equity_before':equity}
    return trades,maxdd,equity

def stats(trades):
    if not trades: return {'n':0,'return_pct':0.0,'pf':None,'win_rate':None}
    net=np.array([t['net'] for t in trades],float); gp=net[net>0].sum(); gl=-net[net<0].sum()
    return {'n':int(len(net)),'return_pct':float(net.sum()/100000*100),'pf':float(gp/gl) if gl>0 else None,'win_rate':float((net>0).mean())}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--hf-root',default='raw/fno'); ap.add_argument('--daily-root',default='raw/tejhq'); ap.add_argument('--out',default='research_results/phase8'); ap.add_argument('--symbols',default=','.join(SYMBOLS)); args=ap.parse_args(); symbols=args.symbols.split(',')
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True); rows=[]; provenance=[]
    for s in symbols:
        try:
            intra=parse_intraday(Path(args.hf_root)/s); provenance.append({'symbol':s,'hf_rows':len(intra),'hf_start':str(intra.index.min()),'hf_end':str(intra.index.max())})
            for freq,kind in [('5min','scalp'),('15min','intraday')]:
                data=resample_ohlcv(intra,freq)
                for friction in [0,2.5,5,10]:
                    for mc in [False,True]:
                        tr,dd,eq=run(data,kind,friction,mc,s); ss=stats([t for t in tr if HF_TEST[0]<=t['exit']<=HF_TEST[1]])
                        rows.append({'symbol':s,'horizon':kind,'friction_bps':friction,'mc':mc,'test':ss,'maxdd':dd,'final_equity':eq})
            day=parse_daily_json(Path(args.daily_root)/f'{s}.json'); provenance[-1].update({'day_rows':len(day),'day_start':str(day.index.min()),'day_end':str(day.index.max())})
            for kind in ['btst','swing']:
                for friction in [0,2.5,5,10]:
                    for mc in [False,True]:
                        tr,dd,eq=run(day,kind,friction,mc,s); ss=stats([t for t in tr if DAY_TEST[0]<=t['exit']<=DAY_TEST[1]])
                        rows.append({'symbol':s,'horizon':kind,'friction_bps':friction,'mc':mc,'test':ss,'maxdd':dd,'final_equity':eq})
        except Exception as e:
            provenance.append({'symbol':s,'error':repr(e)})
    flat=[]
    for r in rows:
        x=r['test']; flat.append({**{k:v for k,v in r.items() if k!='test'},**x})
    pd.DataFrame(flat).to_csv(out/'per_symbol_results.csv',index=False); Path(out/'provenance.json').write_text(json.dumps(provenance,indent=2))
    summary={}
    frame=pd.DataFrame(flat)
    for (h,fr,mc),g in frame.groupby(['horizon','friction_bps','mc']):
        valid=g[g.n>0]; rets=valid.return_pct.to_numpy(float); summary[f'{h}|{fr}|{mc}']={'symbols':int(len(valid)),'mean_test_return_pct':float(np.mean(rets)) if len(rets) else 0.0,'median_test_return_pct':float(np.median(rets)) if len(rets) else 0.0,'positive_symbols':int((rets>0).sum()),'median_pf':float(np.nanmedian(valid.pf)) if valid.pf.notna().any() else None}
    Path(out/'summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()