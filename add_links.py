files = [
    ("src/pages/sites/westmount/best-performing-stocks-june-2025.astro", "<p>While evaluating June's leaders, you might also want to compare them against our comprehensive list of the <a href='/best-us-stocks-to-invest-in-2025'>best US stocks to invest in for 2025</a> or specifically look into the <a href='/best-oil-stocks'>best oil stocks</a> if you are seeking energy sector exposure.</p>"),
    ("src/pages/sites/westmount/best-us-stocks-to-invest-in-2025.astro", "<p>As you build your core portfolio for 2025, it's also worth tracking short-term momentum. Check out our analysis of the <a href='/best-performing-stocks-june-2025'>best performing stocks in June 2025</a>, or if you prefer high-yield energy plays, see our guide to the <a href='/best-oil-stocks'>best oil stocks</a>.</p>"),
    ("src/pages/sites/westmount/best-oil-stocks.astro", "<p>Energy is just one piece of the puzzle. To see how these oil giants stack up against the broader market, explore our definitive guide to the <a href='/best-us-stocks-to-invest-in-2025'>best US stocks to invest in 2025</a> and review the <a href='/best-performing-stocks-june-2025'>best performing stocks of June 2025</a> to identify emerging trends.</p>")
]

for file, link_html in files:
    with open(file, 'r') as f:
        content = f.read()

    # Insert right after the <p class="subtitle">Subtitle</p></div>
    insert_pos = content.find('</div>\n\n    <section class="methodology-section')
    if insert_pos != -1:
        new_content = content[:insert_pos] + '\n      <div style="margin-top: 1rem; font-size: 1.1rem; color: var(--text-primary); max-width: 800px; margin-left: auto; margin-right: auto; line-height: 1.6;">' + link_html + '</div>' + content[insert_pos:]
        with open(file, 'w') as f:
            f.write(new_content)
