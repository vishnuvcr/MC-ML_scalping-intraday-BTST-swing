import anyio, json, os, sys
from pathlib import Path
from mcp import Client

URL = os.environ.get("MCP_URL", "https://vjaiswal-nifty-mcp.hf.space/mcp")
START = os.environ.get("MCP_START", "2024-01-01")
END = os.environ.get("MCP_END", "2026-09-07")
OUT = Path(os.environ.get("MCP_OUT", "raw/nifty100_15m"))
OUT.mkdir(parents=True, exist_ok=True)

async def main():
    async with Client(URL) as client:
        symbols_result = await client.call_tool("list_symbols", {"dataset": "stocks"})
        text = ""
        for block in symbols_result.content:
            if hasattr(block, "text"):
                text += block.text
        try:
            obj = json.loads(text)
        except Exception:
            obj = {"raw": text}
        symbols = []
        if isinstance(obj, dict):
            for key in ("symbols", "data", "results"):
                if isinstance(obj.get(key), list):
                    symbols = [x if isinstance(x, str) else x.get("symbol") for x in obj[key]]
                    break
        symbols = [x for x in symbols if x]
        if not symbols:
            raise RuntimeError(f"Unable to parse stock symbols from list_symbols response: {text[:1000]}")
        Path("research_results/phase9_mcp_symbols.json").parent.mkdir(parents=True, exist_ok=True)
        Path("research_results/phase9_mcp_symbols.json").write_text(json.dumps(symbols, indent=2))
        for symbol in symbols:
            out = OUT / f"{symbol}.csv"
            if out.exists() and out.stat().st_size > 1000:
                continue
            last_err = None
            for interval in ("15minute", "15m", "1minute"):
                try:
                    result = await client.call_tool("get_candles", {
                        "dataset": "stocks",
                        "symbol": symbol,
                        "interval": interval,
                        "start": START,
                        "end": END,
                        "limit": 500000
                    })
                    blob = ""
                    for block in result.content:
                        if hasattr(block, "text"):
                            blob += block.text
                    obj = json.loads(blob)
                    Path("raw/nifty100_15m").mkdir(parents=True, exist_ok=True)
                    out.write_text(json.dumps({"symbol": symbol, "interval": interval, "data": obj}))
                    break
                except Exception as exc:
                    last_err = repr(exc)
            else:
                (OUT / f"{symbol}.error.txt").write_text(last_err or "unknown error")

if __name__ == "__main__":
    anyio.run(main)
