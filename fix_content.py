with open("src/pages/sites/westmount/how-to-buy-stocks.astro", "r") as f:
    content = f.read()

faq_html = """
    <section class="faq-section">
      <h2>Frequently Asked Questions</h2>

      <details>
        <summary>How much money do I need to start buying stocks?</summary>
        <p>You can start with as little as $1 to $5. Thanks to fractional shares offered by most major brokers (like Fidelity, Schwab, and Robinhood), you no longer need to buy a full share. You can invest a fixed dollar amount into companies whose shares might trade for hundreds or thousands of dollars.</p>
      </details>

      <details>
        <summary>What is the difference between a stock and an ETF?</summary>
        <p>A stock represents ownership in a single specific company (e.g., Apple or Microsoft). An ETF (Exchange-Traded Fund) is a basket of many different stocks bundled together. While buying a single stock exposes you to the risks and rewards of one company, buying an ETF instantly diversifies your investment across dozens or hundreds of companies.</p>
      </details>

      <details>
        <summary>Is it safe to buy stocks?</summary>
        <p>All stock investments carry risk, and it is entirely possible to lose money, especially in the short term. However, historically, the broad stock market has gone up over long periods. You can manage risk by diversifying your investments (such as buying index funds), investing for the long term (5+ years), and never investing money you will need in the near future.</p>
      </details>

      <details>
        <summary>When is the best time to buy a stock?</summary>
        <p>Attempting to time the market—predicting exactly when a stock is at its lowest point—is notoriously difficult even for professionals. For most investors, the best approach is "dollar-cost averaging," which means investing a set amount of money at regular intervals (like every month) regardless of what the market is doing.</p>
      </details>

      <details>
        <summary>Do I have to pay taxes on stocks I buy?</summary>
        <p>You do not pay taxes simply for buying a stock. Taxes are generally owed in two situations: when you sell a stock for a profit (capital gains tax) and when a stock pays you a dividend (dividend tax). If you invest through a tax-advantaged account like an IRA or 401(k), you can defer or eliminate some of these taxes.</p>
      </details>
    </section>
  </div>

  <style is:inline>"""

content = content.replace("  </div>\n\n  <style is:inline>", faq_html)
content = content.replace("  </div>\n  <style is:inline>", faq_html)
content = content.replace("</div>\n<style is:inline>", faq_html)

with open("src/pages/sites/westmount/how-to-buy-stocks.astro", "w") as f:
    f.write(content)
