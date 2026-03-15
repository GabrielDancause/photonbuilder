import yfinance as yf
import json
from datetime import datetime

tickers = ["SCHD", "MSTY", "VYM", "ULTY", "JEPQ"]
results = {}

for t_sym in tickers:
    t = yf.Ticker(t_sym)

    # get info with error handling
    try:
        info = t.info
    except Exception:
        info = {}

    try:
        divs = t.dividends
        hist_divs = {}
        if not divs.empty:
            for dt, val in divs.items():
                y = dt.year
                if y not in hist_divs:
                    hist_divs[y] = 0.0
                hist_divs[y] += val
    except Exception:
        hist_divs = {}

    # keep last 5 full years (2020 to 2024 roughly, plus 2025)
    hist_filtered = {}
    for y in sorted(hist_divs.keys(), reverse=True):
        if y < 2026 and len(hist_filtered) < 5:
            hist_filtered[y] = hist_divs[y]

    yield_val = info.get("trailingAnnualDividendYield") or info.get("dividendYield") or info.get("yield")
    if yield_val is not None:
        yield_val = yield_val * 100

    results[t_sym] = {
        "yield": yield_val,
        "price": info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose"),
        "pe": info.get("trailingPE"),
        "aum": info.get("totalAssets"),
        "history": hist_filtered
    }

with open("real_data.json", "w") as f:
    json.dump(results, f, indent=2)

print(json.dumps(results, indent=2))
