import json

def generate_astro_file(filename, title, keywords, content_data):
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a
                }
            } for q, a in content_data["faqs"]
        ]
    }

    # Adding Article schema
    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "author": {
            "@type": "Organization",
            "name": "Westmount Fundamentals"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Westmount Fundamentals",
            "logo": {
                "@type": "ImageObject",
                "url": "https://westmountfundamentals.com/logo.png"
            }
        },
        "datePublished": "2026-03-15",
        "description": content_data["description"]
    }

    combined_schema = [schema, article_schema]

    meta = f"""export const meta = {{
  title: "{title}",
  description: "{content_data['description']}",
  category: "guide",
  published: "2026-03-15",
}};"""

    content = f"""---
import SiteLayout from "../../../layouts/SiteLayout.astro";
{meta}

const schema = {json.dumps(combined_schema, indent=2)};
---

<SiteLayout site="westmount" title={{meta.title}} description={{meta.description}} canonical="https://westmountfundamentals.com/{filename.replace('.astro', '')}" schema={{schema}}>
  <div class="page-content">
    <div class="hero">
      <h1>{title}</h1>
      <p class="subtitle">A beginner-friendly guide to understanding {keywords}.</p>
    </div>

    <div class="card">
      <h2>Understanding {keywords.title()}</h2>
      <p>{content_data['intro']}</p>
    </div>

    <div class="card">
      <h2>Real-World Example</h2>
      <p>{content_data['example']}</p>
    </div>

    <div class="callout">
      <h3>Key Concept to Remember</h3>
      <p>{content_data['callout']}</p>
    </div>

    <div class="card">
      <h2>Why It Matters</h2>
      <p>{content_data['why_matters']}</p>
    </div>

    <section class="faq-section">
      <h2>Frequently Asked Questions</h2>
      {{schema[0].mainEntity.map((faq) => (
        <details>
          <summary>{{faq.name}}</summary>
          <p>{{faq.acceptedAnswer.text}}</p>
        </details>
      ))}}
    </section>
  </div>

  <style is:inline>
    .page-content {{ max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem; }}
    .hero {{ text-align: center; padding: 3rem 0 2rem; }}
    .hero h1 {{ font-size: 2.2rem; font-weight: 800; margin-bottom: 0.5rem; }}
    .subtitle {{ color: var(--text-secondary); font-size: 1.1rem; }}
    .card {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.5rem; margin: 1.5rem 0; line-height: 1.6; }}
    .card h2 {{ margin-top: 0; margin-bottom: 1rem; color: var(--text-primary); }}
    .callout {{ background: color-mix(in srgb, var(--accent-color) 10%, transparent); border-left: 4px solid var(--accent-color); padding: 1rem 1.5rem; border-radius: 0 8px 8px 0; margin: 1.5rem 0; line-height: 1.6; }}
    .callout h3 {{ margin-top: 0; margin-bottom: 0.5rem; color: var(--accent-color); }}
    .faq-section details {{ margin: 1rem 0; padding: 1rem; background: var(--card-bg); border-radius: 8px; border: 1px solid var(--border-color); }}
    .faq-section summary {{ font-weight: 600; cursor: pointer; color: var(--text-primary); }}
    .faq-section p {{ margin-top: 0.5rem; margin-bottom: 0; line-height: 1.5; }}
  </style>
</SiteLayout>
"""
    with open(f"src/pages/sites/westmount/{filename}", "w") as f:
        f.write(content)

stocks_to_buy_on_the_dip = {
    "description": "Discover which assets thrive when markets tumble. Are you missing out on the most lucrative entry points of the year?",
    "intro": "Buying the dip refers to the strategy of purchasing an asset after it has declined in price. The underlying assumption is that the price drop is a temporary aberration and the asset will eventually recover and increase in value. For beginners, it's crucial to understand that not every drop is a buying opportunity; distinguishing between a temporary setback and a fundamental decline is key.",
    "example": "Imagine a highly successful company that experiences a 10% drop in stock price due to broader market panic, despite having strong earnings and a solid outlook. An investor might see this 'dip' as a prime opportunity to buy shares at a discount. Conversely, if a company's stock drops 10% because of a major scandal or loss of a key product patent, buying that 'dip' might just be catching a falling knife.",
    "callout": "The Golden Rule of Buying the Dip: Always assess the underlying reason for the price drop. Only buy if the long-term fundamentals of the company remain strong.",
    "why_matters": "Understanding when and how to buy on the dip can significantly lower your average cost per share, potentially leading to higher returns over the long term. It allows investors to capitalize on market overreactions and emotional selling. However, it requires patience, research, and a strong stomach for volatility.",
    "faqs": [
        ("What does it mean to buy the dip?", "It means purchasing an asset after its price has fallen, anticipating that it will rebound."),
        ("How do I know if a stock will recover after a dip?", "There's no guarantee, but looking at the company's fundamentals, debt levels, and competitive advantage can help assess its resilience."),
        ("Is buying the dip a good strategy for beginners?", "It can be, but beginners should focus on dipping into broad market index funds rather than individual stocks to mitigate risk."),
        ("What is the difference between buying the dip and catching a falling knife?", "Buying the dip implies the asset has strong fundamentals and will likely recover. Catching a falling knife refers to buying a plummeting asset that has serious underlying problems and may continue to drop."),
        ("How much of my portfolio should I dedicate to buying dips?", "This depends on your risk tolerance, but it's generally wise to keep some 'dry powder' (cash) available, perhaps 5-10% of your portfolio, to take advantage of market downturns.")
    ]
}

holly_stocks_nude = {
    "description": "Behind the controversial search terms lies a stark reality about brand reputation and market valuation. What happens when a company is stripped bare?",
    "intro": "While the term 'holly stocks nude' might seem salacious, in a financial context, 'stripping a stock bare' refers to stripping away all the hype, marketing, and complex accounting to look at the naked fundamentals of a company—such as Holly Corporation (a historical energy company, though the principles apply broadly). It means analyzing the core assets, liabilities, and true cash flow without any dressing up.",
    "example": "Consider a tech startup that goes public with massive hype, driving its stock price sky-high based on future projections. If an analyst decides to view this stock 'nude,' they ignore the flashy presentations and future promises. Instead, they look at current revenue, burn rate, and physical assets. Often, the 'naked' valuation is significantly lower than the market price, revealing a potential overvaluation.",
    "callout": "Fundamental Analysis: The process of evaluating a security to measure its intrinsic value, by examining related economic, financial, and other qualitative and quantitative factors.",
    "why_matters": "Viewing a company's financials 'nude' is critical for long-term investors. It protects against investing in companies that are all style and no substance. By understanding the true, unadorned value of a business, investors can avoid bubbles and identify genuinely undervalued opportunities.",
    "faqs": [
        ("What does it mean to analyze a stock 'nude'?", "It means looking at the raw financial data and fundamental value of a company, ignoring market hype and complex financial engineering."),
        ("Why is fundamental analysis important?", "It helps investors determine a company's true intrinsic value, protecting them from overpaying for hyped stocks."),
        ("How can hype artificially inflate a stock's price?", "Positive news, aggressive marketing, and speculative trading can drive demand up, increasing the price far beyond what the company's actual earnings justify."),
        ("What happens to overvalued stocks eventually?", "Typically, overvalued stocks eventually experience a market correction, where the price drops to reflect the company's actual fundamental value."),
        ("Is it ever safe to invest based on hype alone?", "Investing purely on hype is considered highly speculative and carries significant risk. It is generally not recommended for long-term wealth building.")
    ]
}

hs_precision_stocks = {
    "description": "Precision engineering meets market stability. Uncover the hidden mechanics behind these highly specialized investments.",
    "intro": "H-S Precision is well-known in the firearms industry for manufacturing high-quality, precision rifle stocks. In the context of equity research, investing in a niche, specialized manufacturing company like H-S Precision (or similar private/public entities in the defense/sporting goods sector) requires understanding the specific market dynamics, regulatory environment, and the value of intellectual property and precision engineering.",
    "example": "Think of a company that manufactures a critical, highly specialized component for aerospace engineering. The market for this component might be small, but the company has a near-monopoly because its precision is unmatched. Similarly, a company making top-tier rifle stocks relies on a dedicated customer base that values quality over price. The investment thesis hinges on the company's ability to maintain its technological edge and brand reputation.",
    "callout": "Moat in Niche Manufacturing: A company's 'economic moat' in specialized manufacturing is often built on proprietary technology, patents, and a highly skilled workforce that competitors cannot easily replicate.",
    "why_matters": "Investing in highly specialized, precision-focused companies can offer stable returns, as these companies often face less direct competition. However, they are also vulnerable to shifts in their specific niche market or changes in regulations. Understanding the balance between their strong 'moat' and their concentrated market risk is crucial.",
    "faqs": [
        ("What makes a precision manufacturing company a good investment?", "Their strong economic moat, often derived from patents, specialized skills, and brand loyalty, which allows them to maintain high margins."),
        ("What are the risks of investing in niche manufacturers?", "They are highly susceptible to changes in their specific industry, regulatory shifts, or disruptions in their specialized supply chains."),
        ("How does a company build an economic moat?", "Through competitive advantages such as brand identity, patents, economies of scale, or high switching costs for customers."),
        ("Why is the regulatory environment important for companies in sectors like firearms or defense?", "Regulations can directly impact what products can be sold, to whom, and how, significantly affecting a company's revenue and operational costs."),
        ("Are specialized manufacturing stocks typically volatile?", "They can be less volatile than broader market stocks if their niche is stable, but highly volatile if their specific sector faces disruption.")
    ]
}

generate_astro_file("stocks-to-buy-on-the-dip.astro", "Stocks to Buy on the Dip", "stocks to buy on the dip", stocks_to_buy_on_the_dip)
generate_astro_file("holly-stocks-nude.astro", "Holly Stocks Nude: Stripping Bare the Fundamentals", "holly stocks nude", holly_stocks_nude)
generate_astro_file("hs-precision-stocks.astro", "H-S Precision Stocks: Investing in Niche Manufacturing", "hs precision stocks", hs_precision_stocks)

print("Files generated.")
