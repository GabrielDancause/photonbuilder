import json

with open("real_data.json", "r") as f:
    data = json.load(f)

def format_money(val):
    if val is None:
        return "N/A"
    return f"${val:,.2f}"

def format_pct(val):
    if val is None:
        return "N/A"
    return f"{val:.2f}%"

def format_large(val):
    if val is None:
        return "N/A"
    if val > 1e9:
        return f"${val/1e9:.2f}B"
    if val > 1e6:
        return f"${val/1e6:.2f}M"
    return f"${val:,.0f}"

def get_history_rows(ticker):
    hist = data.get(ticker, {}).get('history', {})
    if not hist:
        return "<tr><td colspan='2'>N/A</td></tr>"
    rows = []
    # sort descending by year
    for year in sorted(map(int, hist.keys()), reverse=True):
        if year <= 2025:
            rows.append(f"<tr><td>{year} Total</td><td>{format_money(hist[str(year)])}</td></tr>")
    return "\n          ".join(rows)

pages_config = [
    {
        "filename": "schd-dividend.astro",
        "title": "SCHD Dividend Analysis & History",
        "slug": "schd-dividend",
        "ticker": "SCHD",
        "desc": "Discover the hidden trend in SCHD's quarterly distributions over the last 5 years. Are analysts' expectations aligning with reality? Find out before you invest.",
        "payout_freq": "4", # quarterly
        "internal_links": ["/best-dividend-stocks", "/jepq-dividend"],
        "paragraphs": [
            "The Schwab U.S. Dividend Equity ETF (SCHD) stands as a titan in the realm of dividend-focused exchange-traded funds. For years, investors seeking a potent combination of current yield and robust dividend growth have turned to SCHD as a cornerstone holding. The fund's methodology is famously stringent, tracking the Dow Jones U.S. Dividend 100 Index. This index doesn't just look for high yields; it demands a ten-year history of consecutive dividend payments, strong free cash flow, and healthy return on equity. This fundamental screening process ensures that the companies within the SCHD portfolio are not only willing to return capital to shareholders but possess the financial fortitude to do so sustainably.",
            "Understanding the SCHD dividend requires looking beyond the surface-level yield. While the current yield, often hovering in the mid-3% range, is attractive compared to the broader S&P 500, the true engine of SCHD's total return is its dividend growth rate. Historically, SCHD has delivered double-digit annualized dividend growth. This means that an investor holding the fund over a decade has seen their \"yield on cost\" skyrocket, effectively combatting inflation and significantly boosting their purchasing power. The quarterly distributions—typically paid in March, June, September, and December—provide a reliable, predictable cash flow stream that is highly coveted by retirees and income investors alike.",
            "Analyzing the fund's sector allocation reveals why its dividend is so resilient. SCHD traditionally leans heavily into industrials, financials, healthcare, and consumer defensive stocks. These sectors are populated by mature, cash-rich businesses with entrenched market positions—often referred to as having wide economic moats. Conversely, SCHD usually has minimal exposure to high-growth, low-yield technology stocks or highly cyclical, capital-intensive sectors that are prone to slashing dividends during economic downturns. This deliberate construction provides a defensive posture, allowing the fund to weather market volatility while maintaining its distribution trajectory.",
            "Looking ahead to the SCHD dividend yield in 2025 and beyond, the fundamental picture remains solid. Even in environments of fluctuating interest rates or economic uncertainty, the high-quality nature of SCHD's underlying holdings provides a buffer. While short-term price fluctuations will alter the trailing twelve-month yield, the nominal dollar amount of the dividend payouts is widely expected to continue its upward march. For long-term investors utilizing a dividend reinvestment plan (DRIP), this consistency is paramount, allowing them to accumulate more shares at varying price points and accelerate the compounding process.",
            "In comparison to its peers, such as VYM or DGRO, SCHD often strikes the optimal balance between starting yield and growth. Its incredibly low expense ratio ensures that the vast majority of the generated income flows directly into the investor's pocket rather than being consumed by management fees. Whether you are actively living off the income or diligently reinvesting for the future, a deep dive into SCHD's dividend history and financial metrics underscores why it remains a premier choice for equity income generation.",
            "The historical performance of SCHD's dividend is a testament to the power of fundamental screening. By requiring a minimum of ten consecutive years of dividend payments for inclusion, the fund naturally filters out companies that might treat their dividend as a discretionary luxury rather than a binding commitment to shareholders. This rigorous approach results in a portfolio that is incredibly resilient, even during periods of broader economic distress. When analyzing the year-over-year growth of these payouts, it becomes evident that the companies within SCHD are consistently expanding their earnings power and choosing to share that success with their investors.",
            "Furthermore, the tax efficiency of SCHD's distributions should not be overlooked. Because the fund focuses on established U.S. corporations, a significant portion of its dividend income is typically classified as \"qualified dividends.\" This classification is crucial for investors holding the ETF in taxable brokerage accounts, as qualified dividends are taxed at the much more favorable long-term capital gains rate rather than the higher ordinary income tax rate. This tax advantage effectively increases the net, after-tax yield of the fund, making it even more attractive compared to other income-generating assets like corporate bonds or REITs, whose distributions are often taxed as ordinary income.",
            "When evaluating the fund's key metrics, the Price-to-Earnings (P/E) ratio often stands out as a marker of value. Because SCHD heavily weights mature, slower-growing companies, its P/E ratio is frequently lower than that of the broader S&P 500. This value tilt provides a degree of downside protection; these stocks are less prone to the severe multiple compression that can devastate high-flying growth stocks during market corrections. Investors in SCHD are essentially buying a portfolio of highly profitable, reasonably priced businesses that prioritize returning cash to their owners.",
            "The sheer size of SCHD, measured by its Assets Under Management (AUM), also speaks to its widespread acceptance and liquidity. With tens of billions of dollars entrusted to the fund, investors can trade shares with extremely tight bid-ask spreads, minimizing transaction costs. This immense scale also ensures the fund's long-term viability; unlike niche, actively managed ETFs that may face closure if they fail to attract assets, SCHD is a permanent fixture in the ETF landscape, providing investors with the confidence that their chosen income vehicle will remain available for decades to come.",
            "Ultimately, the decision to invest in SCHD hinges on an individual's financial goals and time horizon. For those seeking aggressive capital appreciation in the short term, SCHD may not be the optimal choice, as its value-oriented holdings are unlikely to produce explosive, tech-like growth. However, for investors who prioritize a steadily growing stream of passive income, lower volatility, and the peace of mind that comes from owning a diversified basket of financially unassailable companies, SCHD's dividend profile is arguably unparalleled in the current market environment."
        ],
        "faqs": [
            ("schd dividend", "SCHD pays a quarterly dividend derived from a portfolio of 100 high-quality U.S. companies. These companies are selected based on a strict criteria that demands a minimum of 10 consecutive years of dividend payments, ensuring a focus on reliability and financial strength."),
            ("schd dividend yield", f"The current dividend yield for SCHD is approximately {format_pct(data['SCHD']['yield'])}. This yield is dynamic and changes daily based on the fund's market price, but it historically offers a significant premium over the broader S&P 500 average."),
            ("schd dividend history", "SCHD has an exceptional dividend history characterized by consistent, year-over-year growth. Since its inception, the fund has successfully increased its annual distribution, demonstrating the underlying fundamental strength of its constituent companies."),
            ("schd dividend yield 2025", "While exact future yields are impossible to predict, analysts anticipate SCHD's dividend yield in 2025 to remain robust. Based on the historical growth rate of its underlying holdings, the nominal dividend payout is expected to continue its upward trajectory."),
            ("schd dividend calculator", "An SCHD dividend calculator allows investors to input their share count and the estimated annual payout to project future income. By forecasting both quarterly and annual cash flows, investors can better plan for retirement or model the effects of dividend reinvestment."),
            ("schd dividend date", "SCHD typically goes ex-dividend in the middle of March, June, September, and December. Investors must own the shares prior to these specific dates to be eligible to receive the subsequent quarterly dividend payment."),
            ("schd dividend yield 2024", "Throughout 2024, SCHD maintained a highly competitive dividend yield, distributing steady quarterly payouts that provided a reliable income stream for investors despite varying macroeconomic conditions and fluctuating interest rates."),
            ("schd dividend payout", "The SCHD dividend payout is distributed in cash on a quarterly basis. These predictable, quarterly distributions are a primary reason why the fund is favored by income-focused investors and retirees seeking to cover living expenses.")
        ]
    },
    {
        "filename": "msty-dividend-history.astro",
        "title": "MSTY Dividend Analysis & History",
        "slug": "msty-dividend-history",
        "ticker": "MSTY",
        "payout_freq": "12", # monthly
        "internal_links": ["/ulty-dividend-history", "/jepq-dividend"],
        "desc": "Uncover the staggering yield numbers behind MSTY's recent distributions. Is this high-income strategy sustainable for the upcoming quarters? Read our breakdown.",
        "paragraphs": [
            "The YieldMax MSTR Option Income Strategy ETF (MSTY) represents one of the most aggressive and fascinating developments in the modern ETF landscape. Designed to generate massive amounts of current income, MSTY employs a synthetic covered call strategy on MicroStrategy Incorporated (MSTR). Because MicroStrategy's stock price is famously volatile—largely due to its immense holdings of Bitcoin—the option premiums that MSTY can harvest are extraordinarily high. This results in distribution yields that frequently stretch into the triple digits, numbers that are practically unheard of in traditional equity or fixed-income investing.",
            "However, analyzing the MSTY dividend requires a fundamental shift in how an investor views yield. The distributions paid by MSTY are not dividends in the traditional sense; they are not a portion of MicroStrategy's corporate profits being returned to shareholders. Instead, they are the cash proceeds generated by selling short-dated call options. When MSTR experiences wild price swings, implied volatility spikes, and the premiums MSTY collects swell massively. Conversely, if MSTR were to enter a period of prolonged consolidation and low volatility, those premiums—and consequently, MSTY's dividend—would plummet.",
            "The sheer magnitude of the MSTY dividend yield is entirely dependent on this sustained volatility. While the headline yield is undeniably alluring to income seekers, it comes with extreme trade-offs, most notably the near-certainty of net asset value (NAV) decay over time. Because the covered call strategy caps the upside potential of the underlying stock while fully exposing the fund to the downside risk, MSTY's share price will inevitably erode over long holding periods. Therefore, investors must calculate their 'total return'—the sum of the massive distributions minus the loss of capital—to truly evaluate the fund's performance.",
            "Given its monthly payout structure, MSTY appeals strongly to active traders and investors who demand immediate, high-velocity cash flow. The exact payout dates vary slightly but generally occur in the first half of the month. Managing a position in MSTY requires constant vigilance. It is not a \"set it and forget it\" asset like a broad-market index fund. Instead, it is a specialized tool designed to monetize extreme volatility. Many successful investors in this space utilize the massive distributions to immediately diversify into more stable assets, rather than reinvesting them back into the depreciating NAV of MSTY itself.",
            "Looking toward the future, the sustainability of MSTY's dividend is inextricably linked to the trajectory of the cryptocurrency market and MicroStrategy's role within it. As long as MSTR remains a highly volatile proxy for Bitcoin, MSTY will continue to generate substantial option premiums. However, if the market matures, stabilizes, or if regulatory changes alter MicroStrategy's operating environment, the sky-high yields currently associated with MSTY could evaporate rapidly. This renders the fund a high-risk, high-reward proposition suited only for investors who fully comprehend the mechanics of option income strategies.",
            "The mechanics of MSTY's synthetic covered call strategy are complex and warrant careful study. The fund does not actually own shares of MicroStrategy directly. Instead, it creates synthetic exposure by buying call options and selling put options at the same strike price, mimicking the price action of the underlying stock. It then sells out-of-the-money call options against this synthetic position to generate income. This intricate setup means the fund is highly sensitive not just to the price of MSTR, but to the pricing of the options market itself, including factors like time decay (theta) and implied volatility (vega).",
            "This structural complexity means that MSTY's distributions will be highly erratic. Unlike a traditional dividend growth stock that aims for steady, predictable increases, MSTY's monthly payouts will act like a rollercoaster. One month, the distribution might be a few dollars per share; the next, it might be mere cents if volatility has dried up or if a sudden, massive downward move in MSTR resulted in significant losses on the synthetic position. Investors must possess the psychological fortitude to handle this extreme variance in their monthly income stream.",
            "Tax implications for MSTY distributions are also vastly different from traditional dividend ETFs. Because the income is generated primarily through short-term option trading, the majority of the distributions are typically classified as ordinary income rather than qualified dividends. This means they are taxed at the investor's highest marginal tax rate. For high earners holding MSTY in a taxable account, the tax burden can severely degrade the net yield. Consequently, these types of ultra-high-yield option income funds are often better suited for tax-advantaged accounts like IRAs.",
            "Furthermore, the extreme NAV erosion associated with this strategy must be factored into any long-term analysis. When MSTR surges upward, MSTY's gains are capped by the short call options it sold. When MSTR crashes, MSTY absorbs the full blow. Over multiple volatile cycles, this asymmetric payoff profile inevitably grinds the fund's share price lower. Investors must view the massive dividend not as pure profit, but partially as a return of their own rapidly depreciating capital. If the distributions are not carefully managed or reinvested elsewhere, the total value of the investment can approach zero over a long enough timeline.",
            "In conclusion, MSTY is a highly specialized instrument designed for a very specific market environment: extreme, sustained volatility in the price of MicroStrategy. It offers unparalleled current income potential, but at the cost of intense risk, NAV decay, and complex tax considerations. It should not be viewed as a traditional investment or a long-term hold, but rather as a tactical tool for aggressive income generation that requires active management and a deep understanding of derivative strategies."
        ],
        "faqs": [
            ("msty dividend history", "MSTY's dividend history is characterized by extremely high, yet highly variable, monthly payouts. Because the distributions are derived from option premiums rather than corporate earnings, the historical amounts fluctuate wildly based on the underlying volatility of MicroStrategy (MSTR) stock during any given month."),
            ("msty dividend", "The MSTY dividend is generated by employing a synthetic covered call strategy. The fund harvests income by selling short-dated call options on its synthetic MicroStrategy position, meaning the dividend is essentially a monetization of the extreme implied volatility in the crypto-adjacent equities market."),
            ("msty dividend yield", f"The current MSTY dividend yield is an astonishing {format_pct(data['MSTY']['yield'])}. However, investors must understand this is a backward-looking metric based on recent, highly elevated option premiums and does not represent a guaranteed or sustainable forward-looking rate of return."),
            ("msty dividend date", "MSTY typically declares and pays its dividends on a monthly schedule. This frequent distribution cycle is designed to rapidly pass the harvested option premiums through to shareholders, providing immediate, high-velocity cash flow."),
            ("msty dividend payout date", "The exact MSTY dividend payout date varies month-to-month, generally occurring within the first or second week. Investors must track the fund's monthly declarations to confirm the specific ex-dividend, record, and payment dates for each cycle."),
            ("msty dividend calculator", "An MSTY dividend calculator can help project potential short-term income based on current shareholdings. However, due to the extreme variance in monthly payouts, any projections should be treated as highly speculative estimates rather than reliable forecasts."),
            ("msty dividend yield 2025", "Projecting the MSTY dividend yield for 2025 is incredibly difficult, as it relies entirely on the future volatility of MicroStrategy's stock. If the crypto market stabilizes and implied volatility drops, MSTY's yield will experience a corresponding and severe decline.")
        ]
    },
    {
        "filename": "best-dividend-stocks.astro",
        "title": "Best Dividend Analysis & History",
        "slug": "best-dividend-stocks",
        "ticker": "VYM", # proxy
        "payout_freq": "4", # quarterly
        "internal_links": ["/schd-dividend", "/jepq-dividend"],
        "desc": "We analyzed the top-yielding dividend growth equities to find the true long-term winners. See which stocks made the cut for consistent returns and reliability.",
        "paragraphs": [
            "The quest to identify the best dividend stocks is a central pursuit for millions of investors focused on building long-term, sustainable wealth. Unlike aggressive growth investing, which relies heavily on capital appreciation and market timing, dividend investing is anchored in fundamental business realities. The best dividend stocks are typically mature, cash-generating enterprises that possess a durable competitive advantage—an economic moat—allowing them to consistently profit and share those profits with their investors, regardless of the broader economic climate.",
            "When analyzing the landscape for the best dividend stocks in 2025 and beyond, it is critical to look past the superficial allure of the highest starting yield. A common pitfall for novice income investors is falling into a \"value trap\"—purchasing a stock simply because it boasts an 8% or 10% yield. Often, these ultra-high yields are the result of a collapsing share price driven by deteriorating fundamentals, signaling an impending dividend cut. Instead, the true \"best\" stocks are those that offer a respectable initial yield coupled with a strong, verifiable history of consecutive annual dividend increases.",
            "This focus on dividend growth is paramount. Companies that consistently raise their payouts demonstrate formidable pricing power and capital discipline. As inflation erodes the purchasing power of fiat currency, a stagnant dividend will gradually lose its real-world value. However, a dividend that grows at 7% or 8% annually will outpace inflation, ensuring that the investor's income stream actually increases in real terms over the decades. These companies are often found in defensive sectors: consumer staples, healthcare, utilities, and established industrials.",
            "Evaluating the payout ratio is another crucial step in identifying the best dividend stocks. The payout ratio measures the percentage of a company's earnings (or better yet, free cash flow) that is distributed as dividends. A low payout ratio indicates a high margin of safety; if earnings temporarily dip during a recession, the company still has ample cash to maintain or even grow the dividend. Conversely, a payout ratio nearing 100% is a massive red flag, suggesting the current distribution is unsustainable and severely limits the company's ability to reinvest in its core business.",
            "Ultimately, curating a portfolio of the best dividend stocks requires a balanced approach. It involves blending steady, high-yielding defensive names with faster-growing, lower-yielding companies that offer aggressive annual dividend hikes. By focusing on fundamental strength, low debt, strong free cash flow, and a demonstrable commitment to shareholder returns, investors can construct an income portfolio that acts as a financial fortress, providing reliable, growing cash flow that can fund a comfortable retirement and leave a lasting legacy.",
            "Beyond the payout ratio and growth history, the balance sheet of a prospective dividend stock demands rigorous scrutiny. The best dividend payers are characterized by conservative leverage. A company laden with massive debt obligations will always prioritize its creditors over its equity shareholders; if cash flow tightens, the dividend is the first expense to be slashed. Therefore, assessing metrics like the debt-to-equity ratio and interest coverage ratio is vital. Companies that can effortlessly service their debt from operational cash flow provide a much wider margin of safety for their dividend distributions.",
            "Furthermore, understanding the macroeconomic environment is essential when selecting the best dividend stocks. In a rising interest rate environment, traditional high-yield sectors like utilities and real estate investment trusts (REITs) often face significant headwinds, as risk-free Treasury bonds become a compelling alternative for income investors. Conversely, the financial sector—particularly large-cap banks and insurance companies—can actually benefit from higher rates, expanding their net interest margins and boosting the cash flow available for dividend hikes and share repurchases.",
            "The concept of the 'Dividend Aristocrats' is frequently referenced in this context. These are S&P 500 companies that have increased their dividend payout for at least 25 consecutive years. While past performance is not a guarantee of future results, achieving Aristocrat status requires a company to have successfully navigated multiple recessions, market crashes, and inflationary periods without ever reducing its commitment to shareholders. Starting an analysis with the Aristocrats is often a highly effective strategy for identifying businesses with exceptional long-term resilience.",
            "Another critical factor is the role of share repurchases, or buybacks. While a cash dividend provides direct, tangible income, buybacks are a more tax-efficient way for companies to return capital to shareholders. By reducing the total number of outstanding shares, buybacks artificially inflate earnings per share (EPS), which typically drives the stock price higher and makes future dividend increases easier to sustain on a per-share basis. The best dividend stocks often employ a balanced capital return program, utilizing both a growing cash dividend and opportunistic share repurchases.",
            "In summary, finding the best dividend stocks is an exercise in identifying fundamental quality and financial discipline. It requires looking beyond the headline yield to understand the mechanics of the underlying business. By prioritizing strong free cash flow, conservative balance sheets, pricing power, and a demonstrable history of prioritizing shareholder returns, investors can build a robust, inflation-resistant income portfolio capable of weathering any economic storm."
        ],
        "faqs": [
            ("best dividend stocks", "The best dividend stocks are characterized by strong free cash flow, durable competitive advantages, and a consistent history of raising their payouts. They typically operate in stable industries, allowing them to weather economic downturns without cutting their distributions to shareholders."),
            ("best dividend stocks 2025", "For 2025, the best dividend stocks are likely to be those with strong balance sheets and the pricing power necessary to navigate lingering inflation. Focus will remain on high-quality companies in defensive sectors like healthcare and consumer staples, alongside fundamentally sound industrials."),
            ("best dividend stocks 2024", "In 2024, the best-performing dividend stocks successfully balanced yield with capital appreciation. Companies that managed to aggressively grow their earnings and pass those gains onto shareholders via double-digit dividend hikes were the standout performers of the year."),
            ("best dividend growth stocks 2025", "The best dividend growth stocks for 2025 will feature low payout ratios, providing massive runway for future distribution increases. These companies prioritize reinvesting in their business while still generating sufficient excess cash to reward investors with compounding annual income."),
            ("best dividend stocks 2026", "Looking toward 2026, the best dividend stocks will be those that have successfully adapted to the prevailing interest rate environment. Companies that have locked in low-cost debt and boast expanding profit margins will be best positioned to sustain and grow their yields."),
            ("best dividend growth stocks", "Top dividend growth stocks focus on the rate of distribution increase rather than just the initial starting yield. By aggressively raising their dividends year over year, these stocks provide investors with a powerful hedge against inflation and a rapidly expanding yield on cost."),
            ("best dividend yield stocks", "The best high-yield stocks offer substantial current income without sacrificing the safety of the principal. Investors must carefully analyze the payout ratio and cash flow to ensure the high yield is sustainable and not a \"value trap\" signaling an impending dividend cut."),
            ("best growth dividend stocks", "These hybrid equities offer a compelling blend of capital appreciation and a rapidly expanding dividend. Often found in the technology or financial sectors, these companies start with a modest yield but leverage massive earnings growth to aggressively hike their payouts over time.")
        ]
    },
    {
        "filename": "ulty-dividend-history.astro",
        "title": "ULTY Dividend Analysis & History",
        "slug": "ulty-dividend-history",
        "ticker": "ULTY",
        "payout_freq": "12", # monthly
        "internal_links": ["/msty-dividend-history", "/jepq-dividend"],
        "desc": "Analyze the extreme yield metrics and payout schedule of ULTY. Can this fund maintain its current distribution trajectory through 2025 and 2026?",
        "paragraphs": [
            "The YieldMax Ultra Option Income Strategy ETF (ULTY) is designed for the absolute extreme edge of the income investing spectrum. Unlike funds that target a specific sector or a single high-volatility stock, ULTY's mandate is far broader and significantly more aggressive: it actively seeks out the most volatile equities in the market and writes covered calls against them. The goal is singular—to harvest the absolute maximum option premiums available, transforming extreme market turbulence into massive, immediate cash distributions for its shareholders.",
            "To understand the ULTY dividend, one must understand the relationship between implied volatility and option pricing. When a stock is highly volatile—experiencing massive, unpredictable price swings—the options contracts associated with that stock become significantly more expensive. ULTY's portfolio managers dynamically allocate capital to a rotating basket of these high-volatility names, selling short-dated call options to capture these elevated premiums. The cash generated from these sales is what funds the fund's astonishingly high monthly distributions, leading to yields that consistently sit in the triple digits.",
            "However, this ultra-aggressive strategy carries substantial, unavoidable risks that directly impact the fund's long-term viability. By definition, highly volatile stocks are prone to massive price collapses. If the underlying stocks in ULTY's portfolio crash, the fund absorbs the full impact of those losses. Conversely, if those volatile stocks experience explosive upward growth, ULTY's gains are strictly capped by the call options it sold. This asymmetrical risk profile—capturing all the downside while limiting the upside—almost guarantees severe net asset value (NAV) decay over an extended period.",
            "Therefore, evaluating the ULTY dividend yield requires extreme caution. The headline yield is a backward-looking calculation based on recent, massive distributions. It does not factor in the ongoing erosion of the principal investment. An investor might receive a 100%+ annualized yield in cash, but if the underlying share price drops by 50% over that same period, their total return is drastically reduced. ULTY is best utilized not as a core portfolio holding, but as a tactical, highly speculative instrument for investors seeking aggressive monthly cash flow who possess a high tolerance for principal risk.",
            "The future of the ULTY dividend yield in 2025 and beyond hinges entirely on the continuation of broad market volatility. If the equity markets enter a prolonged period of calm, steady growth, the implied volatility across the board will crush. When volatility drops, option premiums shrink, and the cash available for ULTY to distribute will inevitably collapse. Investors holding ULTY must constantly monitor the VIX and the specific volatility profiles of the fund's underlying holdings, as the spectacular dividend is a direct byproduct of market chaos, not fundamental corporate strength.",
            "Diving deeper into the mechanics of ULTY, the fund's high turnover rate is a critical factor. Because the managers are constantly hunting for the highest implied volatility, the underlying portfolio is in a state of perpetual churn. This active management generates significant transaction costs, which act as a constant drag on the fund's overall performance. While these costs are often masked by the massive influx of option premiums during highly volatile periods, they become painfully apparent when volatility subsides and the premium income dries up, accelerating the downward pressure on the fund's NAV.",
            "The psychological aspect of holding an asset like ULTY cannot be overstated. The monthly distributions are undeniably seductive, depositing massive sums of cash directly into an investor's account. However, watching the share price steadily grind lower month after month requires significant discipline. The temptation is to view the dividend as pure profit, ignoring the realizing capital loss. Successful investors in this space must meticulously track their total return—combining the distributed cash with the current value of their remaining shares—to accurately assess if the strategy is actually generating positive wealth.",
            "Furthermore, the tax implications of ULTY's distributions are highly complex and generally unfavorable for taxable accounts. The income generated by short-term option writing is overwhelmingly classified as ordinary income, subjecting it to the investor's highest marginal tax bracket. For a high-income earner, a 100% yield could easily be slashed in half by taxes, severely diminishing the appeal of the strategy. Consequently, ULTY and similar ultra-high-yield option funds are vastly more efficient when held within tax-advantaged accounts like a Roth IRA, where the massive distributions can compound without immediate tax drag.",
            "When comparing ULTY to other covered call ETFs, its unique 'go-anywhere' mandate for volatility sets it apart. While funds like JEPQ or SCHD focus on specific indices and aim for a balance of yield and capital preservation, ULTY sacrifices all pretense of capital preservation in the singular pursuit of maximum yield. It is the financial equivalent of a dragster: built for explosive, short-term performance, but highly unstable and entirely unsuited for a long, steady journey. It requires constant monitoring and a clear exit strategy.",
            "In conclusion, ULTY represents the absolute bleeding edge of the ETF income space. It offers distributions that defy traditional financial logic, but it demands an investor who fully comprehends the severe risks of NAV decay and the mechanics of option pricing. It is a tool for monetizing market fear and uncertainty, not a vehicle for long-term, passive wealth accumulation. Those who utilize it successfully treat it as a high-octane speculative trade, carefully managing their position size and aggressively reallocating the massive distributions into more stable, fundamentally sound assets."
        ],
        "faqs": [
            ("ulty dividend history", "ULTY's dividend history reflects its aggressive mandate to maximize income, resulting in highly variable but substantial past payouts. By focusing on a rotating portfolio of the market's most volatile stocks, the fund generates massive option premiums, which are subsequently distributed to shareholders, though the amounts fluctuate wildly."),
            ("ulty dividend", "The ULTY dividend is derived entirely from a complex, actively managed options strategy. Unlike traditional dividend funds based on corporate cash flows, ULTY's distributions are a function of market volatility and the successful execution of selling short-dated covered calls against highly volatile underlying equities."),
            ("ulty dividend yield", f"ULTY's current dividend yield is an extreme {format_pct(data['ULTY']['yield'])}, highlighting its singular focus on maximum yield generation. While this figure is attractive, it is crucial to understand that such yields are inevitably accompanied by significant net asset value (NAV) decay over long holding periods."),
            ("ulty dividend calculator", "An ULTY dividend calculator can project potential distributions based on current shareholdings. However, because the monthly payout is entirely dependent on fluctuating option premiums and market volatility, the calculator provides a highly speculative estimate rather than a reliable forecast of future income."),
            ("ulty dividend yield 2025", "The ULTY dividend yield in 2025 will remain completely dependent on the presence of extreme market volatility. Should the broader equity markets experience extended periods of calm and low implied volatility, the premiums harvested by the fund will decline sharply, leading to a massive reduction in the distributed yield.")
        ]
    },
    {
        "filename": "jepq-dividend.astro",
        "title": "JEPQ Dividend Analysis & History",
        "slug": "jepq-dividend",
        "ticker": "JEPQ",
        "payout_freq": "12", # monthly
        "internal_links": ["/schd-dividend", "/best-dividend-stocks"],
        "desc": "Dive into the monthly income data of the JPMorgan Nasdaq Equity Premium Income ETF. How does its yield compare to traditional index funds in 2025?",
        "paragraphs": [
            "The JPMorgan Nasdaq Equity Premium Income ETF (JEPQ) has rapidly emerged as a powerhouse in the income investing space, offering a compelling solution for investors seeking high yield without entirely sacrificing the growth potential of the technology sector. JEPQ operates with a dual-mandate: it holds a portfolio of equities heavily weighted toward the Nasdaq-100 index, and it employs a sophisticated, actively managed covered call strategy (via equity-linked notes) to generate significant monthly income. This combination allows investors to participate in the capital appreciation of big tech while receiving a substantial, tangible cash flow stream.",
            "A deep dive into the JEPQ dividend reveals a highly engineered payout structure. The fund's distributions are composed of two distinct elements: the traditional dividends paid by the underlying tech companies in its portfolio, and the massive premiums generated by selling out-of-the-money call options. Because the Nasdaq-100 is inherently more volatile than broader market indices like the S&P 500, the option premiums JEPQ can harvest are significantly richer. This dynamic translates directly into a robust dividend yield that routinely reaches into the low double digits, vastly outperforming traditional fixed-income instruments or standard dividend growth ETFs.",
            "Analyzing JEPQ's historical performance over recent years highlights the effectiveness of its active management. Unlike passive covered call ETFs that mechanically sell options on the entire index at predetermined strike prices, JEPQ's portfolio managers possess the flexibility to adjust their option overlays based on current market conditions and volatility levels. This active approach aims to capture more of the underlying market's upside during bull runs while still generating the necessary premium income to support the high monthly distributions. It represents a more nuanced, flexible approach to option income generation.",
            "However, investors evaluating the JEPQ dividend must understand the inherent trade-offs. The covered call strategy fundamentally caps the fund's upside potential. If the Nasdaq-100 experiences a sudden, massive surge, JEPQ will inevitably lag behind the broader index, as its gains are limited by the strike prices of the options it sold. This means that while JEPQ will likely outperform the unhedged index during flat or down markets due to the cushion provided by its massive premium income, it will underperform during raging bull markets. It is a strategy designed for lower volatility and high cash flow, not maximum capital appreciation.",
            "Looking toward the JEPQ dividend yield in 2025, the outlook remains highly positive for income seekers. As long as the technology sector continues to exhibit healthy levels of implied volatility, the fund will be able to harvest the rich option premiums necessary to sustain its double-digit yield. For retirees or investors focused on current income, JEPQ provides a powerful tool for converting the inherent chaos of the tech sector into a steady, reliable stream of monthly cash, acting as a potent diversifier in a broader income-focused portfolio.",
            "The specific composition of JEPQ's underlying portfolio is crucial to its success. While it mirrors the broad strokes of the Nasdaq-100, the active management team utilizes a proprietary data science process to evaluate fundamental factors, aiming to select stocks that offer a slightly better risk-adjusted return profile than the raw index. This means JEPQ might underweight significantly overvalued tech darlings while overweighting more reasonably priced, fundamentally solid companies within the index. This active stock selection provides a layer of fundamental defense that works in tandem with the income-generating options overlay.",
            "When examining the monthly payout history of JEPQ, consistency is a defining trait. While the exact distribution amount fluctuates slightly month-to-month based on the prevailing option premiums and the timing of corporate dividends from the underlying holdings, the fund has established a highly reliable track record of delivering substantial cash to its shareholders. This reliability is highly prized by investors who depend on their portfolio to cover monthly living expenses, as it eliminates the sequence-of-returns risk associated with having to sell off shares of stock during market downturns to generate cash.",
            "The tax efficiency of JEPQ's distributions is an important consideration for investors in taxable accounts. Because a significant portion of the dividend is derived from the option premiums generated via equity-linked notes (ELNs), these distributions are generally treated as ordinary income for tax purposes, rather than qualified dividends. This means they are taxed at the investor's highest marginal rate. While the absolute yield remains highly attractive, investors must factor in their individual tax situations when calculating the net, after-tax return of holding JEPQ outside of a tax-advantaged account like an IRA.",
            "Comparing JEPQ to its older sibling, JEPI (which focuses on the S&P 500), provides valuable context. Because the Nasdaq-100 is historically more volatile than the S&P 500, JEPQ typically generates higher option premiums, resulting in a consistently higher dividend yield than JEPI. However, this higher yield comes with correspondingly higher volatility in the fund's NAV. Investors must decide which risk/reward profile better suits their goals: the slightly lower, more stable yield of JEPI, or the higher-octane, tech-focused yield of JEPQ.",
            "In conclusion, JEPQ has carved out a dominant position in the income ETF landscape by offering a highly effective, actively managed approach to covered call writing on the Nasdaq-100. It provides a unique bridge between the high-growth potential of big tech and the immediate cash flow requirements of income investors. While it will not capture the full upside of a raging tech bull market, its massive, consistent monthly distributions provide a powerful psychological and financial anchor, making it an excellent core holding for a diversified, high-yield portfolio."
        ],
        "faqs": [
            ("jepq dividend", "The JEPQ dividend is funded by a combination of corporate dividends from its underlying Nasdaq-100 stock holdings and massive premiums generated from selling out-of-the-money call options. This dual-engine approach transforms the inherent growth and volatility of the technology sector into immediate, distributable cash flow."),
            ("jepq dividend history", "Since its inception, JEPQ has established a robust history of providing consistent, double-digit monthly yields. The fund has proven its ability to navigate various market environments, leveraging the natural volatility of Nasdaq-listed companies to generate substantial, reliable option premiums month after month."),
            ("jepq dividend yield", f"The current JEPQ dividend yield stands at an impressive {format_pct(data['JEPQ']['yield'])}, making it a premier option for income seekers. This high-yield profile is particularly appealing to investors looking to boost portfolio cash flow without relying entirely on traditional, low-growth fixed-income instruments."),
            ("jepq dividend yield 2025", "While variable, the JEPQ dividend yield for 2025 is anticipated to remain strong, especially if tech sector volatility persists. The exact yield heavily depends on implied volatility; higher volatility typically leads to richer option premiums, supporting higher monthly distributions to shareholders."),
            ("jepq dividend calculator", "An interactive JEPQ dividend calculator allows investors to estimate their monthly income by entering their specific share count. This tool helps investors visualize how their holdings contribute to overall cash flow and model the compounding effects of reinvesting those massive monthly dividends over time."),
            ("jepq dividend date", "JEPQ typically declares its dividends near the end of the month and pays them out during the first week of the following month. Investors seeking to capture a specific month's distribution must ensure they purchase shares prior to the ex-dividend date, usually the first business day of the payout month."),
            ("jepq dividend yield 2024", "In 2024, JEPQ maintained a highly robust yield, rewarding investors with significant monthly cash flow derived from option premiums. The fund successfully balanced its objective of delivering high current income with maintaining exposure to the underlying capital appreciation of its tech-heavy portfolio."),
            ("jepq dividend yield history", "A review of JEPQ's dividend yield history shows it consistently outperforms the yield of traditional broad-market tech ETFs. By actively trading away a portion of potential upside gains through its covered call strategy, the fund consistently delivers a much higher rate of return via monthly cash distributions.")
        ]
    }
]

for page in pages_config:
    ticker = page['ticker']
    t_data = data.get(ticker, {})

    # EXACTLY sync JSON-LD schema with the HTML details blocks
    schema = {
        "@context": "https://schema.org",
        "@type": ["Article", "FAQPage"],
        "mainEntity": []
    }

    for q, a in page['faqs']:
        schema["mainEntity"].append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })

    faqs_html = ""
    for q, a in page['faqs']:
        faqs_html += f"""
      <details>
        <summary>{q.title()}</summary>
        <p>{a}</p>
      </details>"""

    paragraphs_html = ""
    for p in page['paragraphs']:
        paragraphs_html += f"\n      <p>{p}</p>"

    calc_annual_div = t_data.get('price', 100) * (t_data.get('yield', 0)/100)

    # Custom links block
    links_html = ""
    for link in page['internal_links']:
        title_text = link.replace("/", "").replace("-", " ").title()
        links_html += f"<a href=\"{link}\">{title_text}</a>, "
    links_html = links_html.rstrip(", ")

    content = f"""---
import SiteLayout from "../../../layouts/SiteLayout.astro";

const schema = {json.dumps(schema, indent=2)};

export const meta = {{
  title: "{page['title']}",
  description: "{page['desc']}",
  category: "tool",
  published: "2026-03-15",
}};
---
<SiteLayout site="westmount" title="{page['title']}" description="{page['desc']}" canonical="https://westmountfundamentals.com/{page['slug']}" schema={{schema}}>
  <div class="page-content">
    <div class="hero">
      <h1>{page['title']}</h1>
      <p class="subtitle">A Deep Dive into Yield, Growth, and Payout Stability</p>
    </div>

    <section>
      {paragraphs_html}

      <h2>Current Dividend Yield & Payout Details</h2>
      <p>Understanding the immediate income potential begins with its current yield. The yield represents the annual dividend income relative to the current share price. While market fluctuations cause this figure to move daily, tracking the average yield over time provides a more accurate picture of what an investor can expect. Furthermore, the payout frequency plays a significant role in how an investor manages their cash flow and plans their reinvestment strategies.</p>

      <div class="card">
        <h3>Key Metrics</h3>
        <ul>
          <li><strong>Current Yield:</strong> {format_pct(t_data.get('yield'))}</li>
          <li><strong>Price to Earnings (P/E):</strong> {t_data.get('pe') if t_data.get('pe') else 'N/A'}</li>
          <li><strong>Assets Under Management (AUM):</strong> {format_large(t_data.get('aum'))}</li>
          <li><strong>Current Price:</strong> {format_money(t_data.get('price'))}</li>
        </ul>
      </div>

      <h2>Historical Dividend Performance (5-Year Lookback)</h2>
      <p>The true power lies not just in its starting yield, but in its ability to grow that payout over time. Let's examine the actual payouts from recent years to observe the trajectory of cash returned to shareholders. Historical performance is not a guarantee of future results, but it does serve as a powerful indicator of management's commitment to shareholder returns.</p>

      <table>
        <thead>
          <tr>
            <th>Year</th>
            <th>Total Annual Amount (USD)</th>
          </tr>
        </thead>
        <tbody>
          {get_history_rows(ticker)}
        </tbody>
      </table>
    </section>

    <section>
      <h2>Interactive Dividend Reinvestment Calculator</h2>
      <p>To better visualize the income potential, use the calculator below. Input the number of shares you currently own (or plan to buy) to see your projected income. Dividend reinvestment is one of the most effective strategies for accelerating wealth creation. By automatically using your distributions to purchase additional shares, you increase your share count, which in turn increases your future dividend payments, creating a powerful snowball effect.</p>

      <div class="card" id="calculator-card">
        <h3>Income Projection Calculator</h3>
        <div style="margin-bottom: 1rem;">
          <label for="shares" style="display: block; font-weight: 600; margin-bottom: 0.5rem;">Number of Shares Owned:</label>
          <input type="number" id="shares" value="100" min="1" style="width: 100%; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 6px; background: var(--bg-color); color: var(--text-primary); font-size: 1rem;">
        </div>
        <div style="margin-bottom: 1rem;">
          <label for="estAnnualDiv" style="display: block; font-weight: 600; margin-bottom: 0.5rem;">Estimated Annual Dividend per Share ($):</label>
          <input type="number" id="estAnnualDiv" value="{format_money(calc_annual_div).replace('$', '').replace(',', '')}" step="0.01" min="0" style="width: 100%; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 6px; background: var(--bg-color); color: var(--text-primary); font-size: 1rem;">
        </div>
        <button id="calcBtn" style="background: var(--accent-color); color: #fff; border: none; padding: 0.75rem 1.5rem; border-radius: 6px; font-weight: 600; cursor: pointer; width: 100%; font-size: 1rem;">Calculate Projected Income</button>

        <div id="results" style="margin-top: 1.5rem; display: none; padding-top: 1.5rem; border-top: 1px solid var(--border-color);">
          <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span>Projected Annual Income:</span>
            <strong id="resAnnual" style="color: var(--accent-color); font-size: 1.2rem;">$0.00</strong>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span>Average {'Monthly' if page['payout_freq'] == '12' else 'Quarterly'} Income:</span>
            <strong id="resQuarterly">$0.00</strong>
          </div>
        </div>
      </div>
    </section>

    <section>
      <h2>Comparison to Category Average</h2>
      <p>When evaluated against its peers, this asset offers competitive metrics. Its sector breakdown provides a layer of diversification that can help mitigate risk, though investors should always assess how it fits within their broader portfolio strategy. No investment exists in a vacuum; understanding how an asset compares to the broader market and its direct competitors is essential for determining its relative value. Are you being adequately compensated for the risk you are taking compared to what you could earn in a standard index fund?</p>
    </section>

    <section>
      <h2>Internal Links</h2>
      <p>Explore more dividend strategies: {links_html}.</p>
    </section>

    <section class="faq-section">
      <h2>Frequently Asked Questions</h2>
      {faqs_html}
    </section>
  </div>

  <script is:inline>
    document.addEventListener('DOMContentLoaded', function() {{
      const calcBtn = document.getElementById('calcBtn');
      if(calcBtn) {{
        calcBtn.addEventListener('click', function() {{
          const shares = parseFloat(document.getElementById('shares').value) || 0;
          const annualDiv = parseFloat(document.getElementById('estAnnualDiv').value) || 0;

          const totalAnnual = shares * annualDiv;
          const totalQuarterly = totalAnnual / {page['payout_freq']};

          document.getElementById('resAnnual').textContent = '$' + totalAnnual.toLocaleString(undefined, {{minimumFractionDigits: 2, maximumFractionDigits: 2}});
          document.getElementById('resQuarterly').textContent = '$' + totalQuarterly.toLocaleString(undefined, {{minimumFractionDigits: 2, maximumFractionDigits: 2}});

          document.getElementById('results').style.display = 'block';
        }});
      }}
    }});
  </script>

  <style is:inline>
    .page-content {{ max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem; }}
    .hero {{ text-align: center; padding: 3rem 0 2rem; }}
    .hero h1 {{ font-size: 2.2rem; font-weight: 800; margin-bottom: 0.5rem; }}
    .subtitle {{ color: var(--text-secondary); font-size: 1.1rem; }}
    .card {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.5rem; margin: 1.5rem 0; }}
    table {{ width: 100%; border-collapse: collapse; margin: 1.5rem 0; }}
    th, td {{ padding: 0.75rem 1rem; text-align: left; border-bottom: 1px solid var(--border-color); }}
    th {{ font-weight: 600; color: var(--text-secondary); font-size: 0.85rem; text-transform: uppercase; }}
    .faq-section details {{ margin: 1rem 0; padding: 1rem; background: var(--card-bg); border-radius: 8px; border: 1px solid var(--border-color); }}
    .faq-section summary {{ font-weight: 600; cursor: pointer; }}
    a {{ color: var(--accent-color); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    h2 {{ margin-top: 2rem; margin-bottom: 1rem; }}
    p {{ line-height: 1.6; margin-bottom: 1rem; }}
    ul {{ margin-bottom: 1rem; padding-left: 1.5rem; }}
    li {{ margin-bottom: 0.5rem; }}
  </style>
</SiteLayout>
"""

    with open(f"src/pages/sites/westmount/{page['filename']}", "w") as f:
        f.write(content)
