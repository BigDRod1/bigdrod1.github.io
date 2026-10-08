"""Download daily adjusted close prices from Yahoo Finance via yfinance and cache to CSV."""
import yfinance as yf, pandas as pd, time
TICKERS = ["^GSPC","SPY","QQQ","IWM","EFA","EEM","TLT","IEF","LQD","HYG","GLD","VNQ","DBC",
           "XLK","XLF","XLE","XLV","XLY","XLP","XLU","XLI","XLB",
           "AAPL","MSFT","AMZN","JPM","XOM","JNJ","KO","GE","IBM","PG","WMT","CVX","INTC","CSCO","PFE","BAC","C","NVDA","T","DIS","HD","MRK","F","BA","CAT","MMM",
           "BTC-USD"]
out = {}
for t in TICKERS:
    for attempt in range(3):
        try:
            df = yf.download(t, period="max", auto_adjust=True, progress=False, threads=False)
            s = df["Close"].squeeze().dropna()
            if len(s) > 0:
                out[t] = s; break
        except Exception as e:
            print(t, e)
        time.sleep(2)
    print(t, len(out.get(t, [])), out[t].index[0].date() if t in out else None)
px = pd.DataFrame(out)
px.index.name = "Date"
irx = yf.download("^IRX", period="max", auto_adjust=True, progress=False, threads=False)["Close"].squeeze().dropna()
irx.name = "IRX"; irx.index.name = "Date"; irx.to_csv("data/irx_daily.csv")
px.to_csv("data/prices_daily.csv")
print(px.shape, px.index[-1])
