import json

def generate_page(slug, keyword, category, title, description, h1, is_tool=True):
    content = f"""---
import SiteLayout from "../../../layouts/SiteLayout.astro";

export const meta = {{
  title: "{title}",
  description: "{description}",
  category: "{category}",
  published: "2026-03-17"
}};

const schema = {{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "Article",
      "headline": meta.title,
      "description": meta.description,
      "author": {{
        "@type": "Organization",
        "name": "Westmount Fundamentals"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "Westmount Fundamentals"
      }},
      "datePublished": meta.published
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": [
        {{
          "@type": "Question",
          "name": "What is an {keyword}?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "An {keyword} is a specialized resource designed to help investors understand the potential outcomes of an options trade before risking capital. It factors in variables like strike price, underlying price, and premium paid."
          }}
        }},
        {{
          "@type": "Question",
          "name": "How do you calculate profit on a call option?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "For a long call, subtract the strike price and the premium paid from the current stock price, then multiply by 100 per contract. If the stock price is below the strike price, the loss is capped at the total premium paid."
          }}
        }},
        {{
          "@type": "Question",
          "name": "What happens if an option expires worthless?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "If an option expires out-of-the-money, it becomes worthless. The buyer loses the entire premium paid for the option, but has no further obligation."
          }}
        }},
        {{
          "@type": "Question",
          "name": "Are options riskier than stocks?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Options can be riskier than stocks because they use leverage and have an expiration date. However, certain strategies can be used to limit risk or generate income, making them versatile tools for knowledgeable investors."
          }}
        }},
        {{
          "@type": "Question",
          "name": "Why use an {keyword}?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Using an {keyword} helps visualize the profit and loss graph, clearly defining maximum risk, maximum reward, and breakeven points before entering a trade."
          }}
        }}
      ]
    }}
  ]
}};
---

<SiteLayout site="westmount" title={{meta.title}} description={{meta.description}} canonical={{`https://westmountfundamentals.com/{slug}`}} schema={{schema}}>
  <div class="page-container">
    <header class="page-header">
      <h1>{h1}</h1>
      <p class="subtitle">Understand your potential returns and risks before placing a trade.</p>
    </header>

"""

    if is_tool:
        content += f"""
    <section class="calculator-section">
      <div class="calculator-card">
        <h2>{h1} Tool</h2>
        <div class="input-grid">
          <div class="input-group">
            <label for="optionType">Option Type</label>
            <select id="optionType">
              <option value="call">Long Call</option>
              <option value="put">Long Put</option>
            </select>
          </div>
          <div class="input-group">
            <label for="strikePrice">Strike Price ($)</label>
            <input type="number" id="strikePrice" value="150" step="0.5" />
          </div>
          <div class="input-group">
            <label for="premiumPaid">Premium Paid ($ per share)</label>
            <input type="number" id="premiumPaid" value="5" step="0.05" />
          </div>
          <div class="input-group">
            <label for="contracts">Number of Contracts (x100)</label>
            <input type="number" id="contracts" value="1" step="1" />
          </div>
          <div class="input-group">
            <label for="stockPriceAtExpiry">Stock Price at Expiry ($)</label>
            <input type="number" id="stockPriceAtExpiry" value="160" step="0.5" />
          </div>
        </div>
        <button id="calculateBtn" class="calc-btn">Calculate P/L</button>
      </div>

      <div class="results-grid">
        <div class="stat-card highlight">
          <h3>Total Profit / Loss</h3>
          <p class="stat-value" id="totalPL">$0.00</p>
        </div>
        <div class="stat-card">
          <h3>Breakeven Price</h3>
          <p class="stat-value" id="breakevenPrice">$0.00</p>
        </div>
        <div class="stat-card">
          <h3>Max Risk</h3>
          <p class="stat-value" id="maxRisk">$0.00</p>
        </div>
        <div class="stat-card">
          <h3>Return on Investment</h3>
          <p class="stat-value" id="roi">0.00%</p>
        </div>
      </div>
    </section>

    <section class="comparison-section">
      <h2>P/L Scenarios at Expiration</h2>
      <div class="table-responsive">
        <table class="comparison-table">
          <thead>
            <tr>
              <th>Stock Price</th>
              <th>Intrinsic Value</th>
              <th>Total P/L ($)</th>
              <th>ROI (%)</th>
            </tr>
          </thead>
          <tbody id="scenarioTableBody">
            <!-- Populated by JS -->
          </tbody>
        </table>
      </div>
    </section>

    <script is:inline>
      document.addEventListener('DOMContentLoaded', () => {{
        const optionType = document.getElementById('optionType');
        const strikePrice = document.getElementById('strikePrice');
        const premiumPaid = document.getElementById('premiumPaid');
        const contracts = document.getElementById('contracts');
        const stockPriceAtExpiry = document.getElementById('stockPriceAtExpiry');
        const calculateBtn = document.getElementById('calculateBtn');

        const totalPL = document.getElementById('totalPL');
        const breakevenPrice = document.getElementById('breakevenPrice');
        const maxRisk = document.getElementById('maxRisk');
        const roi = document.getElementById('roi');
        const scenarioTableBody = document.getElementById('scenarioTableBody');

        function formatCurrency(val) {{
          return new Intl.NumberFormat('en-US', {{ style: 'currency', currency: 'USD' }}).format(val);
        }}

        function formatPercent(val) {{
          return val.toFixed(2) + '%';
        }}

        function calculate() {{
          const type = optionType.value;
          const strike = parseFloat(strikePrice.value) || 0;
          const premium = parseFloat(premiumPaid.value) || 0;
          const qty = parseFloat(contracts.value) || 0;
          const expiryPrice = parseFloat(stockPriceAtExpiry.value) || 0;

          const totalCost = premium * 100 * qty;
          maxRisk.textContent = formatCurrency(totalCost);

          let breakeven = 0;
          let intrinsic = 0;

          if (type === 'call') {{
            breakeven = strike + premium;
            intrinsic = Math.max(0, expiryPrice - strike);
          }} else {{
            breakeven = strike - premium;
            intrinsic = Math.max(0, strike - expiryPrice);
          }}

          breakevenPrice.textContent = formatCurrency(breakeven);

          const totalValue = intrinsic * 100 * qty;
          const pl = totalValue - totalCost;

          totalPL.textContent = formatCurrency(pl);
          totalPL.style.color = pl >= 0 ? 'var(--accent-color)' : '#ff4444';

          const returnPct = totalCost > 0 ? (pl / totalCost) * 100 : 0;
          roi.textContent = formatPercent(returnPct);
          roi.style.color = pl >= 0 ? 'var(--accent-color)' : '#ff4444';

          // Generate Scenarios
          scenarioTableBody.innerHTML = '';
          const startPrice = Math.max(0, strike * 0.7);
          const endPrice = strike * 1.3;
          const step = (endPrice - startPrice) / 6;

          for (let i = 0; i <= 6; i++) {{
            const simPrice = startPrice + (step * i);
            let simIntrinsic = 0;
            if (type === 'call') {{
              simIntrinsic = Math.max(0, simPrice - strike);
            }} else {{
              simIntrinsic = Math.max(0, strike - simPrice);
            }}

            const simTotalValue = simIntrinsic * 100 * qty;
            const simPl = simTotalValue - totalCost;
            const simRoi = totalCost > 0 ? (simPl / totalCost) * 100 : 0;

            const tr = document.createElement('tr');
            tr.innerHTML = `
              <td>${{formatCurrency(simPrice)}}</td>
              <td>${{formatCurrency(simIntrinsic)}}</td>
              <td style="color: ${{simPl >= 0 ? 'var(--accent-color)' : '#ff4444'}}">${{formatCurrency(simPl)}}</td>
              <td style="color: ${{simPl >= 0 ? 'var(--accent-color)' : '#ff4444'}}">${{formatPercent(simRoi)}}</td>
            `;
            scenarioTableBody.appendChild(tr);
          }}
        }}

        calculateBtn.addEventListener('click', calculate);
        calculate(); // initial
      }});
    </script>
"""

    content += f"""
    <article class="educational-content">
      <h2>Comprehensive Guide to the {keyword.title()}</h2>
      <p>Understanding potential outcomes in options trading is paramount. The <strong>{keyword}</strong> provides a crucial visual and numerical representation of what happens to a position at various expiration prices. Whether you are using an <a href="/options-calculator">options calculator</a> or a <a href="/stock-options-calculator">stock options calculator</a>, mapping your risk/reward scenario keeps your portfolio grounded.</p>

      <h3>The Core Mechanics of Options</h3>
      <p>Options contracts give buyers the right, but not the obligation, to buy or sell an underlying asset at a specified strike price. A <a href="/options-profit-calculator">options profit calculator</a> models the intrinsic value remaining at expiration. In contrast to standard equity trading discussed in our <a href="/options-vs-stocks">options vs stocks</a> guide, options carry a hard expiration date, which introduces time decay.</p>

      <p>If you prefer a hands-on approach without risking real capital, an <a href="/options-trading-simulator">options trading simulator</a> allows you to test hypotheses. Options are leveraged instruments, and just as knowing your overall portfolio trajectory via an <a href="/average-stock-market-return">average stock market return</a> analysis is important, knowing the precise breakeven of a single contract is essential for short-term trades.</p>

      <h3>Understanding the Profit Formula</h3>
      <p>For a standard long call contract, the mathematical model is straightforward but unforgiving:</p>
      <ul>
        <li><strong>Total Cost:</strong> Premium Paid × 100 × Number of Contracts</li>
        <li><strong>Breakeven Price:</strong> Strike Price + Premium Paid (for calls)</li>
        <li><strong>Intrinsic Value:</strong> Max(0, Stock Price - Strike Price)</li>
      </ul>
      <p>Because one contract typically represents 100 shares, a premium of $5.00 translates to a $500 actual cost. If the underlying asset undergoes a stock split, the strike price and multiplier adjust accordingly, which you can verify using our <a href="/stock-split-calculator">stock split calculator</a>.</p>

      <h3>Worked Example: Long Call</h3>
      <p>Suppose you purchase 1 call contract with a strike price of $150 for a $5.00 premium. The total capital at risk is $500. For the trade to be profitable at expiration, the underlying asset must rise above $155 (the $150 strike plus the $5.00 premium). If the asset closes at $160, the intrinsic value is $10.00. Multiplied by 100, the contract is worth $1,000. Your net profit is $500, yielding a 100% return on investment.</p>
      <p>If the stock closes below $150, the contract expires worthless, and the entire $500 premium is lost. This asymmetrical risk profile—defined downside, technically unlimited upside—is why many traders incorporate options into their strategies, but it also necessitates strict discipline.</p>

      <h3>Common Pitfalls to Avoid</h3>
      <p>Many new traders focus solely on the maximum profit potential while ignoring the probability of success. A common mistake is buying deep out-of-the-money options because they are cheap. However, these require significant directional movement just to break even.</p>
      <p>Moreover, ignoring the effects of implied volatility crush around earnings events can turn a seemingly correct directional prediction into a losing trade. A robust <strong>{keyword}</strong> helps visualize how far the underlying needs to move to overcome both intrinsic and extrinsic factors before expiration.</p>

      <h3>Integration with Broader Strategy</h3>
      <p>Trading options should not exist in a vacuum. It requires an understanding of overall market conditions, similar to understanding the <a href="/average-stock-market-return">average stock market return</a> over decades. Using a <a href="/options-profit-calculator">options profit calculator</a> or an <a href="/options-trading-simulator">options trading simulator</a> forms the tactical layer of a much larger strategic framework. Always weigh the explicit leverage of an options contract against the straightforward equity ownership detailed in our <a href="/options-vs-stocks">options vs stocks</a> analysis.</p>

      <p>By making these calculations a mandatory step before order entry, traders can eliminate emotional decision-making, setting strict target exits and stop-loss boundaries based on actual structural math rather than mere intuition.</p>

      <h3>Further Exploration</h3>
      <p>As you refine your approach, consider exploring different strike placements and expiration cycles. Adjusting the inputs in the <strong>{keyword}</strong> above will dynamically recalculate the critical thresholds. Continually modeling these scenarios is the fastest way to internalize the relationship between premium cost, strike distance, and overall profitability.</p>
    </article>
  </div>
</SiteLayout>

<style>
  .page-container {{
    max-width: 1000px;
    margin: 0 auto;
    padding: 2rem 1rem;
    font-family: system-ui, -apple-system, sans-serif;
  }}
  .page-header {{
    text-align: center;
    margin-bottom: 3rem;
  }}
  .page-header h1 {{
    color: var(--text-primary, #fff);
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
  }}
  .subtitle {{
    color: var(--text-secondary, #a0aec0);
    font-size: 1.1rem;
  }}
  .calculator-section {{
    margin-bottom: 4rem;
  }}
  .calculator-card {{
    background: var(--card-bg, #1a202c);
    border: 1px solid var(--border-color, #2d3748);
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 2rem;
  }}
  .calculator-card h2 {{
    color: var(--text-primary, #fff);
    margin-top: 0;
    margin-bottom: 1.5rem;
  }}
  .input-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-bottom: 1.5rem;
  }}
  .input-group label {{
    display: block;
    color: var(--text-secondary, #a0aec0);
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
  }}
  .input-group input, .input-group select {{
    width: 100%;
    padding: 0.75rem;
    background: var(--bg-color, #0f172a);
    border: 1px solid var(--border-color, #2d3748);
    border-radius: 6px;
    color: var(--text-primary, #fff);
    color-scheme: dark;
  }}
  .calc-btn {{
    width: 100%;
    padding: 1rem;
    background: var(--accent-color, #3b82f6);
    color: #fff;
    border: none;
    border-radius: 6px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: opacity 0.2s;
  }}
  .calc-btn:hover {{
    opacity: 0.9;
  }}
  .results-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
  }}
  .stat-card {{
    background: var(--card-bg, #1a202c);
    border: 1px solid var(--border-color, #2d3748);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
  }}
  .stat-card.highlight {{
    border-color: var(--accent-color, #3b82f6);
  }}
  .stat-card h3 {{
    color: var(--text-secondary, #a0aec0);
    font-size: 0.9rem;
    margin-top: 0;
    margin-bottom: 0.5rem;
  }}
  .stat-value {{
    color: var(--text-primary, #fff);
    font-size: 1.75rem;
    font-weight: 700;
    margin: 0;
  }}
  .comparison-section {{
    margin-bottom: 4rem;
  }}
  .comparison-section h2 {{
    color: var(--text-primary, #fff);
    margin-bottom: 1.5rem;
  }}
  .table-responsive {{
    overflow-x: auto;
  }}
  .comparison-table {{
    width: 100%;
    border-collapse: collapse;
    background: var(--card-bg, #1a202c);
    border-radius: 12px;
    overflow: hidden;
  }}
  .comparison-table th, .comparison-table td {{
    padding: 1rem;
    text-align: right;
    border-bottom: 1px solid var(--border-color, #2d3748);
    color: var(--text-primary, #fff);
  }}
  .comparison-table th {{
    background: rgba(255,255,255,0.05);
    color: var(--text-secondary, #a0aec0);
    font-weight: 600;
  }}
  .educational-content {{
    color: var(--text-primary, #e2e8f0);
    line-height: 1.7;
  }}
  .educational-content h2, .educational-content h3 {{
    color: #fff;
    margin-top: 2rem;
  }}
  .educational-content a {{
    color: var(--accent-color, #3b82f6);
    text-decoration: none;
  }}
  .educational-content a:hover {{
    text-decoration: underline;
  }}
  .educational-content ul {{
    margin-left: 1.5rem;
    margin-bottom: 1.5rem;
  }}
  .educational-content li {{
    margin-bottom: 0.5rem;
  }}
</style>
"""
    return content

pages = [
    {
        "slug": "options-profit-calculator",
        "keyword": "options profit calculator",
        "category": "tool",
        "title": "Options Profit Calculator | Visual P/L & Risk Tool",
        "description": "Discover exactly how much risk you take. Our interactive options profit calculator maps out scenarios so you never guess your max loss...",
        "h1": "Options Profit Calculator",
        "is_tool": True
    },
    {
        "slug": "options-calculator",
        "keyword": "options calculator",
        "category": "tool",
        "title": "Options Calculator | Trade Scenarios & Returns",
        "description": "Will your strike price hit profitability? Use this powerful options calculator to unearth hidden breakevens and project absolute returns...",
        "h1": "Options Calculator",
        "is_tool": True
    },
    {
        "slug": "stock-options-calculator",
        "keyword": "stock options calculator",
        "category": "tool",
        "title": "Stock Options Calculator | Equity Derivatives Modeler",
        "description": "Are stock options right for your strategy? Crunch the precise numbers with our stock options calculator before exposing real capital to the market...",
        "h1": "Stock Options Calculator",
        "is_tool": True
    },
    {
        "slug": "options-vs-stocks",
        "keyword": "options vs stocks",
        "category": "guide",
        "title": "Options vs Stocks: The Ultimate Comparison",
        "description": "What is the true cost of leverage? Our comprehensive options vs stocks guide reveals the staggering difference in risk and reward potential...",
        "h1": "Options vs Stocks",
        "is_tool": False
    },
    {
        "slug": "options-trading-simulator",
        "keyword": "options trading simulator",
        "category": "tool",
        "title": "Options Trading Simulator | Free Paper Trading Tool",
        "description": "Can you beat the market without risking a dime? Try our options trading simulator to test robust strategies and uncover critical mistakes early...",
        "h1": "Options Trading Simulator",
        "is_tool": True
    }
]

for p in pages:
    content = generate_page(
        slug=p["slug"],
        keyword=p["keyword"],
        category=p["category"],
        title=p["title"],
        description=p["description"],
        h1=p["h1"],
        is_tool=p["is_tool"]
    )
    with open(f"src/pages/sites/westmount/{p['slug']}.astro", "w") as f:
        f.write(content)

print("Generated pages successfully.")
