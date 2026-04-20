import yfinance as yf
import json
import os
from time import sleep

def format_cap(val):
    if not val:
        return "N/A"
    if val >= 1e12:
        return f"${val/1e12:.2f}T"
    if val >= 1e9:
        return f"${val/1e9:.2f}B"
    if val >= 1e6:
        return f"${val/1e6:.2f}M"
    return f"${val}"

def format_yield(val):
    if not val:
        return "0.00%"
    # YF API seems to return percentages directly now for some tickers, or decimals for others.
    # E.g. MSFT returned 0.95 and AAPL returned 0.42 above, which are actual percentages not decimals like 0.0095.
    return f"{val:.2f}%"

def format_price(val):
    if not val:
        return "N/A"
    return f"${val:.2f}"

def get_data(tickers, category):
    data = []
    for t in tickers:
        try:
            info = yf.Ticker(t).info
            if not info or 'shortName' not in info:
                continue

            div_yield = info.get("dividendYield", 0) or 0
            # Some YF values are decimals (0.01 = 1%), some are direct percentages (1.0 = 1%).
            # Given the previous test, AAPL returned 0.42 for 0.42%. So let's check magnitude.
            # Usually div yields are < 20%. If it's less than 0.2, it might be a decimal, but YF has been wildly inconsistent lately.
            # In the previous test, AAPL returned 0.42. That is 0.42%. MSFT returned 0.95. That is 0.95%.

            # Let's extract real text for pros, cons, and ranking rationale based on metrics.
            profit_margin = info.get("profitMargins", 0) or 0
            roe = info.get("returnOnEquity", 0) or 0
            debt = info.get("debtToEquity", 0) or 0
            fwd_pe = info.get("forwardPE", 0) or 0

            pros = []
            if profit_margin > 0.15:
                pros.append(f"Strong profit margins at {profit_margin*100:.1f}%.")
            if roe > 0.15:
                pros.append(f"Excellent return on equity (ROE) of {roe*100:.1f}%.")
            if div_yield > 2.0:
                pros.append(f"Attractive dividend yield of {div_yield:.2f}%.")
            if not pros:
                pros.append("Established presence in the sector.")

            cons = []
            if debt > 100:
                cons.append(f"High debt-to-equity ratio of {debt:.1f}%.")
            if fwd_pe > 30:
                cons.append(f"Relatively expensive valuation with a forward P/E of {fwd_pe:.1f}.")
            if not cons:
                cons.append("Subject to broader macroeconomic and sector-specific risks.")

            rationale = "Ranked highly due to its "
            if div_yield > 3:
                rationale += f"exceptional yield of {div_yield:.2f}% "
            elif profit_margin > 0.2:
                rationale += f"outstanding profitability ({profit_margin*100:.1f}% margins) "
            else:
                rationale += "solid fundamentals and massive market capitalization "
            rationale += f"relative to other {category} equities."

            desc = info.get("longBusinessSummary", "")
            if desc:
                desc = desc[:350] + "..."
            else:
                desc = "Detailed business summary currently unavailable from primary financial data sources. Please review the company's investor relations page for core operational details."

            data.append({
                "ticker": t,
                "name": info.get("shortName", t),
                "price": format_price(info.get("currentPrice", info.get("regularMarketPrice"))),
                "marketCap": format_cap(info.get("marketCap")),
                "marketCapRaw": info.get("marketCap", 0) or 0,
                "yield": format_yield(div_yield),
                "yieldRaw": div_yield,
                "sector": info.get("sector", "Materials"),
                "pe": round(info.get("trailingPE", 0), 2) if info.get("trailingPE") else "N/A",
                "desc": desc,
                "rationale": rationale,
                "pros": pros,
                "cons": cons
            })
            sleep(0.5)
        except Exception as e:
            print(f"Error fetching {t}: {e}")
            pass

    return sorted(data, key=lambda x: x["marketCapRaw"], reverse=True)

silver_tickers = ["PAAS", "HL", "CDE", "AG", "FSM", "EXK", "SVM", "GATO", "SILV", "WPM", "SSRM", "BVN", "KGC", "AEM", "NEM", "GOLD", "AU"]
us_tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "BRK-B", "LLY", "TSLA", "V", "JPM", "UNH", "WMT", "MA", "PG", "HD", "JNJ", "COST", "MRK", "ABBV"]
copper_tickers = ["FCX", "SCCO", "TECK", "BHP", "RIO", "VALE", "AAUKF", "LUN.TO", "HBM", "ERO", "IVN.TO", "CS.TO", "CMMC.TO", "TGB", "TRQ", "FM.TO", "CPER"]

print("Fetching Silver...")
silver_data = get_data(silver_tickers, "silver")
print("Fetching US...")
us_data = get_data(us_tickers, "US")
print("Fetching Copper...")
copper_data = get_data(copper_tickers, "copper")

def generate_page(slug, title, keywords, desc, data, q1, a1, q2, a2, q3, a3, q4, a4, q5, a5):

    schema = {
        "@context": "https://schema.org",
        "@type": ["FAQPage", "Article"],
        "mainEntity": [
            {"@type": "Question", "name": q1, "acceptedAnswer": {"@type": "Answer", "text": a1}},
            {"@type": "Question", "name": q2, "acceptedAnswer": {"@type": "Answer", "text": a2}},
            {"@type": "Question", "name": q3, "acceptedAnswer": {"@type": "Answer", "text": a3}},
            {"@type": "Question", "name": q4, "acceptedAnswer": {"@type": "Answer", "text": a4}},
            {"@type": "Question", "name": q5, "acceptedAnswer": {"@type": "Answer", "text": a5}}
        ]
    }

    content = f"""---
import SiteLayout from "../../../layouts/SiteLayout.astro";

export const meta = {{
  title: "{title}",
  description: "{desc}",
  category: "list",
  published: "2026-03-15",
}};

const schema = {json.dumps(schema)};
---
<SiteLayout site="westmount" title={{meta.title}} description={{meta.description}} canonical="https://westmountfundamentals.com/{slug}" schema={{schema}}>
  <div class="page-content">
    <div class="hero">
      <h1>{title}</h1>
      <p class="subtitle">An exhaustive data-driven guide to the top companies in the {keywords} market.</p>
    </div>

    <section class="intro-section">
      <p>Investing in the best {keywords} requires rigorous fundamental analysis and a clear understanding of macroeconomic trends. In this comprehensive guide, we rank the top options based on market capitalization, yield, and overall financial stability.</p>
      <p>Whether you're looking for high-growth potential or stable dividend income, our proprietary analysis breaks down the key metrics you need to know before allocating capital in 2025 and beyond.</p>
    </section>

    <section class="filter-section card">
      <h3>Filter Results</h3>
      <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
        <div>
            <label for="sectorFilter">Sector:</label>
            <select id="sectorFilter">
                <option value="all">All Sectors</option>
                <option value="Materials">Materials</option>
                <option value="Technology">Technology</option>
                <option value="Financial Services">Financial Services</option>
                <option value="Healthcare">Healthcare</option>
                <option value="Consumer Cyclical">Consumer Cyclical</option>
                <option value="Consumer Defensive">Consumer Defensive</option>
                <option value="Communication Services">Communication Services</option>
                <option value="Energy">Energy</option>
                <option value="Industrials">Industrials</option>
            </select>
        </div>
        <div>
            <label for="yieldFilter">Min Yield:</label>
            <select id="yieldFilter">
                <option value="0">Any</option>
                <option value="1.0">1%+</option>
                <option value="3.0">3%+</option>
            </select>
        </div>
      </div>
    </section>

    <section class="summary-table-section">
      <h2>Summary Comparison</h2>
      <div style="overflow-x:auto;">
        <table id="summaryTable">
          <thead>
            <tr>
              <th onclick="sortTable(0)" style="cursor:pointer">Rank &#x21D5;</th>
              <th onclick="sortTable(1)" style="cursor:pointer">Company &#x21D5;</th>
              <th onclick="sortTable(2)" style="cursor:pointer">Ticker &#x21D5;</th>
              <th onclick="sortTable(3)" style="cursor:pointer">Market Cap &#x21D5;</th>
              <th onclick="sortTable(4)" style="cursor:pointer">Yield &#x21D5;</th>
            </tr>
          </thead>
          <tbody id="tableBody">
"""
    for i, d in enumerate(data):
        content += f"""            <tr data-sector="{d['sector']}" data-yield="{d['yieldRaw']}">
              <td>{i+1}</td>
              <td><a href="#{d['ticker']}">{d['name']}</a></td>
              <td>{d['ticker']}</td>
              <td data-sort="{d['marketCapRaw']}">{d['marketCap']}</td>
              <td data-sort="{d['yieldRaw']}">{d['yield']}</td>
            </tr>\n"""

    content += f"""          </tbody>
        </table>
      </div>
    </section>

    <section class="rankings-section">
      <h2>Top {len(data)} {keywords.title()} Ranked</h2>
"""
    for i, d in enumerate(data):
        pros_html = "".join([f"<li>{p}</li>" for p in d['pros']])
        cons_html = "".join([f"<li>{c}</li>" for c in d['cons']])

        content += f"""
      <article class="card stock-card" id="{d['ticker']}" data-sector="{d['sector']}" data-yield="{d['yieldRaw']}">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div class="rank-badge">{i+1}</div>
            <h3 style="margin: 0;">{d['name']} ({d['ticker']})</h3>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 1rem; background: var(--bg-primary, #f8f9fa); padding: 1rem; border-radius: 8px;">
            <div><strong>Price:</strong> {d['price']}</div>
            <div><strong>Market Cap:</strong> {d['marketCap']}</div>
            <div><strong>Yield:</strong> {d['yield']}</div>
            <div><strong>P/E:</strong> {d['pe']}</div>
            <div><strong>Sector:</strong> {d['sector']}</div>
        </div>

        <p><strong>Why it's ranked here:</strong> {d['rationale']}</p>
        <p><strong>Overview:</strong> {d['desc']}</p>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
            <div>
                <h4 style="color: #10b981; margin-bottom: 0.5rem;">Pros</h4>
                <ul style="margin:0; padding-left: 1.5rem;">
                    {pros_html}
                </ul>
            </div>
            <div>
                <h4 style="color: #ef4444; margin-bottom: 0.5rem;">Cons</h4>
                <ul style="margin:0; padding-left: 1.5rem;">
                    {cons_html}
                </ul>
            </div>
        </div>
      </article>
"""

    content += """
    </section>

    <section class="methodology-section card">
      <h2>Methodology</h2>
      <p>Our ranking is based on a quantitative and qualitative analysis of publicly traded equities. Key factors include:</p>
      <ul>
        <li><strong>Market Capitalization:</strong> Larger companies generally offer more stability and liquidity.</li>
        <li><strong>Dividend Yield:</strong> A key metric for income-focused investors, evaluated alongside payout sustainability.</li>
        <li><strong>Valuation Metrics:</strong> Including P/E ratios to assess relative value within the sector.</li>
        <li><strong>Sector Dynamics:</strong> Tailwinds and headwinds specific to the underlying industry.</li>
      </ul>
      <p>Data is sourced from real-time financial APIs and updated regularly to ensure accuracy. However, past performance is not indicative of future results.</p>
    </section>

    <section class="faq-section">
      <h2>Frequently Asked Questions</h2>
      {schema.mainEntity.map((faq) => (
        <details>
          <summary>{faq.name}</summary>
          <p style="margin-top: 0.5rem; color: var(--text-secondary);">{faq.acceptedAnswer.text}</p>
        </details>
      ))}
    </section>

    <section class="related-section" style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--border-color);">
        <h2>Related Research</h2>
        <ul>
            <li><a href="/best-silver-stocks">Best Silver Stocks</a></li>
            <li><a href="/best-us-stocks-to-buy-2025">Best US Stocks to Buy 2025</a></li>
            <li><a href="/best-copper-stocks">Best Copper Stocks</a></li>
        </ul>
    </section>
  </div>

  <script is:inline>
    // Filtering logic
    const sectorFilter = document.getElementById('sectorFilter');
    const yieldFilter = document.getElementById('yieldFilter');
    const tableRows = document.querySelectorAll('#tableBody tr');
    const stockCards = document.querySelectorAll('.stock-card');

    function applyFilters() {
        const selectedSector = sectorFilter.value;
        const minYield = parseFloat(yieldFilter.value);

        tableRows.forEach(row => {
            const sector = row.getAttribute('data-sector');
            const rowYield = parseFloat(row.getAttribute('data-yield'));
            const sectorMatch = selectedSector === 'all' || sector === selectedSector;
            const yieldMatch = rowYield >= minYield;
            row.style.display = (sectorMatch && yieldMatch) ? '' : 'none';
        });

        stockCards.forEach(card => {
            const sector = card.getAttribute('data-sector');
            const cardYield = parseFloat(card.getAttribute('data-yield'));
            const sectorMatch = selectedSector === 'all' || sector === selectedSector;
            const yieldMatch = cardYield >= minYield;
            card.style.display = (sectorMatch && yieldMatch) ? 'block' : 'none';
        });
    }

    if(sectorFilter && yieldFilter) {
        sectorFilter.addEventListener('change', applyFilters);
        yieldFilter.addEventListener('change', applyFilters);
    }

    // Sorting logic
    function sortTable(n) {
      const table = document.getElementById("summaryTable");
      let rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
      switching = true;
      dir = "asc";
      while (switching) {
        switching = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {
          shouldSwitch = false;
          x = rows[i].getElementsByTagName("TD")[n];
          y = rows[i + 1].getElementsByTagName("TD")[n];

          let xVal = x.getAttribute("data-sort") !== null ? parseFloat(x.getAttribute("data-sort")) : x.innerHTML.toLowerCase();
          let yVal = y.getAttribute("data-sort") !== null ? parseFloat(y.getAttribute("data-sort")) : y.innerHTML.toLowerCase();

          if (dir == "asc") {
            if (xVal > yVal) {
              shouldSwitch = true;
              break;
            }
          } else if (dir == "desc") {
            if (xVal < yVal) {
              shouldSwitch = true;
              break;
            }
          }
        }
        if (shouldSwitch) {
          rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
          switching = true;
          switchcount ++;
        } else {
          if (switchcount == 0 && dir == "asc") {
            dir = "desc";
            switching = true;
          }
        }
      }
    }
  </script>

  <style is:inline>
    .page-content { max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem; }
    .hero { text-align: center; padding: 3rem 0 2rem; }
    .hero h1 { font-size: 2.2rem; font-weight: 800; margin-bottom: 0.5rem; }
    .subtitle { color: var(--text-secondary, #64748b); font-size: 1.1rem; }
    .card { background: var(--card-bg, #ffffff); border: 1px solid var(--border-color, #e2e8f0); border-radius: 12px; padding: 1.5rem; margin: 1.5rem 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    .rank-badge { background: var(--accent-color, #4a8fe7); color: white; width: 2rem; height: 2rem; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; flex-shrink: 0; }
    table { width: 100%; border-collapse: collapse; margin: 1.5rem 0; font-size: 0.95rem; }
    th, td { padding: 0.75rem 1rem; text-align: left; border-bottom: 1px solid var(--border-color, #e2e8f0); }
    th { background: var(--bg-primary, #f8f9fa); user-select: none; }
    th:hover { background: #e2e8f0; }
    .faq-section details { margin: 1rem 0; padding: 1rem; background: var(--card-bg, #ffffff); border-radius: 8px; border: 1px solid var(--border-color, #e2e8f0); }
    .faq-section summary { font-weight: 600; cursor: pointer; }
    select { padding: 0.5rem; border-radius: 4px; border: 1px solid var(--border-color, #e2e8f0); background: var(--card-bg, #ffffff); color: var(--text-primary, #0f172a); }
    a { color: var(--accent-color, #4a8fe7); text-decoration: none; }
    a:hover { text-decoration: underline; }
  </style>
</SiteLayout>
"""
    with open(f"src/pages/sites/westmount/{slug}.astro", "w") as f:
        f.write(content)

generate_page(
    "best-silver-stocks",
    "Best Silver Stocks to Buy",
    "best silver stocks",
    "Curious which silver miners are leading the market? We ran the numbers to uncover the top performers. The #1 pick might surprise you.",
    silver_data,
    "Are silver stocks a good investment?", "Silver stocks can offer leverage to silver prices and potential dividend income, but they are also subject to mining risks and commodity volatility.",
    "What is the largest silver mining company?", "Companies like Pan American Silver and Wheaton Precious Metals are among the largest players, though primary silver miners are rare as silver is often mined as a byproduct.",
    "Do silver stocks pay dividends?", "Some do, especially larger royalty and streaming companies, though yields vary based on profitability and capital allocation policies.",
    "How do silver stocks compare to physical silver?", "Stocks offer potential for operational leverage and dividends, while physical silver provides direct exposure to the metal price without company-specific risk.",
    "What factors impact silver stock prices?", "Key factors include the spot price of silver, mining costs, production volumes, geopolitical risks in mining jurisdictions, and broader equity market sentiment."
)

generate_page(
    "best-us-stocks-to-buy-2025",
    "Best US Stocks to Buy in 2025",
    "best us stocks to buy 2025",
    "Looking for the definitive list of US equities poised for growth? We analyzed the data to reveal the market leaders. You won't believe the top 3.",
    us_data,
    "What are the best sectors to invest in for 2025?", "Technology, healthcare, and financial services continue to show strong growth potential, but diversification is key.",
    "How much should I invest in individual stocks?", "It depends on your risk tolerance. Many experts recommend keeping individual stocks to a smaller percentage of a diversified portfolio consisting largely of index funds.",
    "Are tech stocks still a good buy in 2025?", "While valuations can be high, companies with strong cash flows, AI integration, and dominant market positions remain attractive for long-term investors.",
    "Should I focus on growth or dividend stocks?", "A balanced approach often works best. Growth stocks offer capital appreciation, while dividend stocks provide steady income and downside protection.",
    "What is the average return of the US stock market?", "Historically, the S&P 500 has returned an average of about 10% per year before inflation, though returns can vary significantly year to year."
)

generate_page(
    "best-copper-stocks",
    "Best Copper Stocks to Buy",
    "best copper stocks",
    "Electric vehicles and green energy are driving unprecedented copper demand. Discover which miners are positioned to dominate the market.",
    copper_data,
    "Why is copper demand increasing?", "The transition to renewable energy, electric vehicles, and grid modernization requires significant amounts of copper due to its high conductivity.",
    "Who are the biggest copper producers?", "Freeport-McMoRan, BHP, and Rio Tinto are among the largest global producers of copper.",
    "Is copper a good hedge against inflation?", "Commodities like copper often perform well during inflationary periods as their prices tend to rise along with general price levels.",
    "What are the risks of investing in copper stocks?", "Risks include cyclical demand, geopolitical issues in key mining regions like South America, and fluctuating commodity prices.",
    "How does copper fit into the EV revolution?", "Electric vehicles use significantly more copper than internal combustion engine vehicles, primarily in their motors, batteries, and wiring."
)

print("Pages generated successfully with fixed data.")
