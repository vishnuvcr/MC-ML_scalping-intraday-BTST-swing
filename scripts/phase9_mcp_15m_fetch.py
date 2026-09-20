import anyio, json, os
from pathlib import Path
from mcp import Client
import pandas as pd

URL=os.environ.get("MCP_URL","https://vjaiswal-nifty-mcp.hf.space/mcp")
START=os.environ.get("MCP_START","2024-01-01")
END=os.environ.get("MCP_END","2026-04-08")
OUT=Path(os.environ.get("MCP_OUT","raw/nifty100_15m")); OUT.mkdir(parents=True,exist_ok=True)

def texts(result):
    return [b.text for b in result.content if hasattr(b,"text")]

def parse_objs(texts_list):
    objs=[]
    for text in texts_list:
        text=text.strip()
        if not text: continue
        try:
            objs.append(json.loads(text)); continue
        except Exception: pass
        for line in text.splitlines():
            line=line.strip()
            if not line or not line.startswith("{"): continue
            try: objs.append(json.loads(line))
            except Exception: pass
    return objs

def extract(objs):
    rows=[]
    for obj in objs:
        data=obj
        if isinstance(data,dict):
            for key in ("data","candles","results","items"):
                if isinstance(data.get(key),list): data=data[key]; break
        if isinstance(data,list):
            for r in data:
                if isinstance(r,dict): rows.append(r)
                elif isinstance(r,(list,tuple)) and len(r)>=6: rows.append({"timestamp":r[0],"open":r[1],"high":r[2],"low":r[3],"close":r[4],"volume":r[5]})
    df=pd.DataFrame(rows)
    if df.empty: return df
    cols={c.lower():c for c in df.columns}
    dt=cols.get("timestamp") or cols.get("datetime") or cols.get("date")
    df=df.rename(columns={cols[k]:k for k in ("open","high","low","close","volume") if k in cols})
    df["ts"]=pd.to_datetime(df[dt],errors="coerce")
    if df["ts"].dt.tz is None: df["ts"]=df["ts"].dt.tz_localize("Asia/Kolkata")
    else: df["ts"]=df["ts"].dt.tz_convert("Asia/Kolkata")
    return df.dropna(subset=["ts","open","high","low","close"]).sort_values("ts").drop_duplicates("ts").set_index("ts")[["open","high","low","close","volume"]].astype(float)

async def main():
    async with Client(URL) as client:
        r=await client.call_tool("list_symbols",{"dataset":"stocks"})
        symbols=sorted({o["symbol"] for o in parse_objs(texts(r)) if isinstance(o,dict) and o.get("symbol")})
        if not symbols: raise RuntimeError("No symbols parsed from list_symbols")
        Path("research_results").mkdir(exist_ok=True)
        Path("research_results/phase9_mcp_symbols.json").write_text(json.dumps(symbols,indent=2))
        errors=[]
        for idx,symbol in enumerate(symbols,1):
            out=OUT/f"{symbol}.csv"
            if out.exists() and out.stat().st_size>1000: continue
            df=None; used=None; last_err=None
            for interval in ("15minute","5minute","1minute"):
                try:
                    rr=await client.call_tool("get_candles",{"dataset":"stocks","symbol":symbol,"interval":interval,"start":START,"end":END,"limit":500000})
                    df=extract(parse_objs(texts(rr)))
                    if not df.empty: used=interval; break
                except Exception as exc: last_err=repr(exc)
            if df is None or df.empty: errors.append({"symbol":symbol,"error":last_err or "empty"}); continue
            if used!="15minute": df=df.resample("15min",origin="start_day",offset="15min",label="left",closed="left").agg({"open":"first","high":"max","low":"min","close":"last","volume":"sum"}).dropna(subset=["open","high","low","close"])
            df.to_csv(out,index_label="timestamp")
            if idx%10==0: print(f"fetched {idx}/{len(symbols)}")
        Path("research_results/phase9_mcp_errors.json").write_text(json.dumps(errors,indent=2))
        if len(errors)==len(symbols): raise RuntimeError("All NIFTY100 symbols failed")

if __name__=="__main__": anyio.run(main)