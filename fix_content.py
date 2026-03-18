import os
import glob
import re

files = [
    "src/pages/sites/westmount/top-gold-mining-stocks-2025.astro",
    "src/pages/sites/westmount/best-monthly-dividend-etfs-2025.astro",
    "src/pages/sites/westmount/top-index-funds-and-etfs.astro"
]

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The user complained about "Dated listicles, not evergreen content" AND "2025" in titles/text.
    # This means we need to remove "2025" from the filenames AND update the content to be evergreen.

    # 1. Update the meta published date to something more neutral if needed, or leave it.

    # 2. Update the text: replace "2025" with "2026" or "the current year" or remove it to make it evergreen.
    # Actually, replacing "2025" with "the coming years" or just removing it makes it truly evergreen.
    content = content.replace(" 2025", "")
    content = content.replace("2025 ", "")
    content = content.replace("-2025", "")

    # Ensure titles are still okay
    content = content.replace("Top Gold Mining Stocks", "Top Gold Mining Stocks")
    content = content.replace("Best Monthly Dividend ETFs", "Best Monthly Dividend ETFs")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
