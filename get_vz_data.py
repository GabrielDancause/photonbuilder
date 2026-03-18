import yfinance as yf
import json

vz = yf.Ticker("VZ")
info = vz.info
financials = vz.financials
balance_sheet = vz.balance_sheet
cashflow = vz.cashflow

data = {
    "price": info.get("currentPrice"),
    "sharesOut": info.get("sharesOutstanding"),
    "freeCashFlow": cashflow.loc["Free Cash Flow"].iloc[0] if "Free Cash Flow" in cashflow.index else None,
    "cash": balance_sheet.loc["Cash And Cash Equivalents"].iloc[0] if "Cash And Cash Equivalents" in balance_sheet.index else 0,
    "shortTermInvestments": balance_sheet.loc["Other Short Term Investments"].iloc[0] if "Other Short Term Investments" in balance_sheet.index else 0,
    "totalDebt": balance_sheet.loc["Total Debt"].iloc[0] if "Total Debt" in balance_sheet.index else 0,
}

if not data["freeCashFlow"]:
    try:
        data["freeCashFlow"] = cashflow.loc["Operating Cash Flow"].iloc[0] - cashflow.loc["Capital Expenditure"].iloc[0]
    except:
        pass

print(json.dumps(data, indent=2))
