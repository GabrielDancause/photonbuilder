#!/usr/bin/env python3
"""Merge prospect data into IV JSON files."""
import json
import os
import re
from pathlib import Path

REPO = Path(os.path.expanduser("~/Desktop/photonbuilder"))
IV_DIR = REPO / "src" / "data" / "iv"
PROSPECT_DIR = REPO / "src" / "data" / "prospect"

# Build prospect index by ticker
prospect_by_ticker = {}
for f in PROSPECT_DIR.glob("*.json"):
    with open(f) as fh:
        data = json.load(fh)
    ticker = data.get("ticker", "").upper()
    if ticker:
        prospect_by_ticker.setdefault(ticker, []).append(data)

def pick_best_prospect(prospects):
    """Prefer base prospect (no model suffix) over consensus/gemini/opus variants."""
    # Score each prospect - lower is better
    def score(p):
        slug = p.get("slug", "")
        if slug.endswith("-economic-prospect"):
            return 0  # base - best
        if "-consensus" in slug:
            return 1
        if "-gemini" in slug:
            return 2
        if "-opus" in slug:
            return 3
        return 4
    prospects.sort(key=score)
    return prospects[0]

updated = 0
no_match = 0
no_match_tickers = []

for iv_file in sorted(IV_DIR.glob("*.json")):
    with open(iv_file) as fh:
        iv_data = json.load(fh)

    ticker = iv_data.get("ticker", "").upper()
    if not ticker:
        no_match += 1
        continue

    prospects = prospect_by_ticker.get(ticker, [])
    if not prospects:
        no_match += 1
        no_match_tickers.append(f"{ticker} ({iv_file.name})")
        continue

    prospect = pick_best_prospect(prospects)

    # Merge prospect fields into IV
    iv_data["prospectScore"] = prospect.get("overallScore")
    iv_data["prospectVerdict"] = prospect.get("verdict")
    iv_data["prospectVerdictDetail"] = prospect.get("verdictDetail")
    iv_data["prospectPillars"] = prospect.get("pillars")
    iv_data["prospectKeyRisks"] = prospect.get("keyRisks")
    iv_data["prospectKeyCatalysts"] = prospect.get("keyCatalysts")
    iv_data["prospectMethodology"] = prospect.get("methodology")

    # Update title
    company = iv_data.get("companyName", ticker)
    iv_data["title"] = f"{company} ({ticker}) — Intrinsic Value & Prospect Score"

    # Update description
    score = prospect.get("overallScore", "N/A")
    verdict = prospect.get("verdict", "")
    old_desc = iv_data.get("description", "")
    iv_data["description"] = f"{old_desc} Economic Prospect Score: {score}/100 — {verdict}."

    with open(iv_file, "w") as fh:
        json.dump(iv_data, fh, indent=2, ensure_ascii=False)

    updated += 1

print(f"✅ Updated: {updated} IV files with prospect data")
print(f"❌ No match: {no_match} IV files had no matching prospect")
if no_match_tickers:
    print(f"   Missing tickers: {', '.join(no_match_tickers[:20])}")
    if len(no_match_tickers) > 20:
        print(f"   ... and {len(no_match_tickers) - 20} more")
