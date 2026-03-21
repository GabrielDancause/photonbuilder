#!/usr/bin/env python3
"""
Add internal links between related pages to boost hidden gems.
Injects a "Related Tools" section before the closing </div> or FAQ section.

Strategy:
- Link FROM high-traffic pages TO hidden gems with great engagement
- Group by topic relevance (dividends, ETFs, valuation, etc.)

Usage:
  python3 scripts/seo-internal-links.py              # dry run
  python3 scripts/seo-internal-links.py --apply       # apply
"""

import os
import re
import sys
from pathlib import Path

BASE = Path(os.path.expanduser("~/Desktop/photonbuilder"))
WM = BASE / "src" / "pages" / "sites" / "westmount"

# Topic clusters: which pages should link to which
# Format: { source_page: [target_pages_with_anchor_text] }
LINK_MAP = {
    # Dividend cluster
    "dividend-aristocrats": [
        ("dividend-reinvestment-calculator", "Dividend Reinvestment Calculator", "See how reinvesting dividends compounds your returns over time."),
        ("what-is-a-dividend", "What Is a Dividend?", "New to dividends? Start with the fundamentals."),
        ("buyback-leaders", "Stock Buyback Leaders", "Compare buyback yields alongside dividend yields."),
    ],
    "what-is-a-dividend": [
        ("dividend-reinvestment-calculator", "Dividend Reinvestment Calculator", "Calculate how reinvesting dividends grows your portfolio."),
        ("dividend-aristocrats", "Dividend Aristocrats List", "See all 67 stocks with 25+ years of consecutive dividend increases."),
    ],
    # Valuation cluster
    "sp500-pe-ratio-history": [
        ("intrinsic-value-dashboard", "Intrinsic Value Dashboard", "See fair value estimates for individual S&P 500 stocks."),
        ("sp500-historical-returns-by-year", "S&P 500 Historical Returns", "Annual returns from 1928 to present."),
        ("market-concentration", "Market Concentration", "How concentrated is the S&P 500 in its top holdings?"),
    ],
    "market-concentration": [
        ("magnificent-seven-stocks-2026", "Magnificent 7 Stocks", "Deep dive into the seven stocks driving concentration."),
        ("sp500-pe-ratio-history", "S&P 500 P/E Ratio History", "Is the market overvalued? Historical context."),
        ("intrinsic-value-dashboard", "Intrinsic Value Dashboard", "Fair value estimates for the largest S&P 500 companies."),
    ],
    # Short interest cluster
    "short-interest": [
        ("most-shorted-stocks", "Most Shorted Stocks", "Detailed analysis of the most shorted stocks right now."),
        ("short-squeeze-candidates", "Short Squeeze Candidates", "Stocks with the highest short squeeze potential."),
        ("buyback-leaders", "Buyback Leaders", "Companies buying back their own shares — the opposite of shorting."),
    ],
    "most-shorted-stocks": [
        ("short-interest", "Short Interest Rankings", "Full short interest data for all tracked stocks."),
        ("short-squeeze-candidates", "Short Squeeze Candidates", "Which heavily shorted stocks could squeeze?"),
        ("beta-volatility", "Beta & Volatility Rankings", "Which stocks move the most? Volatility data."),
    ],
    "short-squeeze-candidates": [
        ("short-interest", "Short Interest Rankings", "Complete short interest data."),
        ("most-shorted-stocks", "Most Shorted Stocks", "The most heavily shorted stocks right now."),
    ],
    # ETF cluster
    "etf-expense-ratios": [
        ("best-growth-etfs-2026", "Best Growth ETFs", "Compare top growth ETFs by performance and fees."),
        ("best-bond-etfs-2026", "Best Bond ETFs", "Find the right bond ETF for your portfolio."),
        ("portfolio-rebalancer", "Portfolio Rebalancer", "Free tool to rebalance your ETF portfolio."),
    ],
    "best-growth-etfs-2026": [
        ("etf-expense-ratios", "ETF Expense Ratios", "Compare expense ratios across 86 popular ETFs."),
        ("portfolio-rebalancer", "Portfolio Rebalancer", "Rebalance your portfolio with our free calculator."),
        ("dividend-reinvestment-calculator", "DRIP Calculator", "Calculate dividend reinvestment returns."),
    ],
    # Tools cluster (cross-link calculators)
    "portfolio-rebalancer": [
        ("dividend-reinvestment-calculator", "DRIP Calculator", "Calculate how reinvesting dividends grows your wealth."),
        ("etf-expense-ratios", "ETF Expense Ratios", "Make sure you're not overpaying in fees."),
        ("stock-comparison-tool", "Stock Comparison Tool", "Compare any two stocks side by side."),
    ],
    "dividend-reinvestment-calculator": [
        ("portfolio-rebalancer", "Portfolio Rebalancer", "Keep your portfolio allocation on target."),
        ("dividend-aristocrats", "Dividend Aristocrats", "67 stocks with 25+ years of dividend growth."),
        ("what-is-a-dividend", "What Is a Dividend?", "Understanding the basics of dividend investing."),
    ],
    # Insider/buyback cluster
    "buyback-leaders": [
        ("insider-trading", "Insider Trading Tracker", "Track insider buying and selling activity."),
        ("institutional-ownership", "Institutional Ownership", "See which stocks institutions are loading up on."),
        ("dividend-aristocrats", "Dividend Aristocrats", "Companies returning cash via dividends instead."),
    ],
    "insider-trading": [
        ("buyback-leaders", "Buyback Leaders", "Companies buying back their own stock."),
        ("insider-buying-tracker-2026", "Insider Buying Tracker", "Recent insider purchases this month."),
        ("institutional-ownership", "Institutional Ownership", "Where are the big funds investing?"),
    ],
}

RELATED_SECTION_HTML = """
  <div class="related-tools" style="margin-top:3rem;padding-top:2rem;border-top:1px solid var(--border-color);">
    <h2 style="font-size:1.2rem;margin-bottom:1rem;">📌 Related Tools & Research</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1rem;">
{cards}
    </div>
  </div>
"""

CARD_HTML = """      <a href="/{slug}/" style="display:block;background:var(--card-bg);border:1px solid var(--border-color);border-radius:10px;padding:1.25rem;text-decoration:none;color:inherit;transition:border-color 0.2s;">
        <strong style="color:var(--text-primary);font-size:0.95rem;">{title}</strong>
        <p style="color:var(--text-secondary);font-size:0.83rem;margin:0.4rem 0 0;line-height:1.4;">{desc}</p>
      </a>"""


def add_links(source_slug: str, links: list, dry_run: bool) -> bool:
    """Add related tools section to a page."""
    astro_file = WM / f"{source_slug}.astro"
    if not astro_file.exists():
        print(f"  ⚠️  {source_slug}.astro not found")
        return False

    content = astro_file.read_text()

    # Skip if already has related tools
    if "related-tools" in content:
        print(f"  ⏭️  {source_slug} — already has related links")
        return False

    # Verify target pages exist
    valid_links = []
    for slug, title, desc in links:
        target = WM / f"{slug}.astro"
        if target.exists():
            valid_links.append((slug, title, desc))
        else:
            print(f"  ⚠️  Target {slug}.astro not found, skipping link")

    if not valid_links:
        return False

    # Build the HTML
    cards = "\n".join(CARD_HTML.format(slug=s, title=t, desc=d) for s, t, d in valid_links)
    section = RELATED_SECTION_HTML.format(cards=cards)

    # Insert before the last </SiteLayout> or before closing FAQ
    # Find the best insertion point
    if "</SiteLayout>" in content:
        content = content.replace("</SiteLayout>", f"{section}\n</SiteLayout>")
    else:
        # Fallback: append before last closing tag
        content += section

    if not dry_run:
        astro_file.write_text(content)

    print(f"  ✅ {source_slug} → linked to {len(valid_links)} pages")
    return True


def main():
    dry_run = "--apply" not in sys.argv
    
    if dry_run:
        print("🔍 DRY RUN — use --apply to write changes\n")
    
    applied = 0
    for source, links in LINK_MAP.items():
        if add_links(source, links, dry_run):
            applied += 1

    print(f"\n📊 {'Would link' if dry_run else 'Linked'}: {applied} pages")
    

if __name__ == "__main__":
    main()
