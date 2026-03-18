import os

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # Replace {STYLE} with actual style component
    STYLE_CONTENT = """
<style is:inline>
  .page-content { max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem; }
  .hero { text-align: center; padding: 3rem 0 2rem; }
  .hero h1 { font-size: 2.2rem; font-weight: 800; margin-bottom: 0.5rem; }
  .subtitle { color: var(--text-secondary); font-size: 1.1rem; }
  .card { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.5rem; margin: 1.5rem 0; }
  .callout { background: color-mix(in srgb, var(--accent-color) 10%, transparent); border-left: 4px solid var(--accent-color); padding: 1rem 1.5rem; border-radius: 0 8px 8px 0; margin: 1.5rem 0; }
  .faq-section details { margin: 1rem 0; padding: 1rem; background: var(--card-bg); border-radius: 8px; border: 1px solid var(--border-color); }
  .faq-section summary { font-weight: 600; cursor: pointer; }
</style>
"""

    content = content.replace("{STYLE}", STYLE_CONTENT)

    with open(path, 'w') as f:
        f.write(content)

fix_file("src/pages/sites/westmount/spyi-stock-dividend.astro")
fix_file("src/pages/sites/westmount/oxlc-stock-dividend.astro")
fix_file("src/pages/sites/westmount/bank-of-america-buyback-dividend-increase.astro")

print("Fixed files")
