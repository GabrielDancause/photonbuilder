import glob

# Replace any internal links pointing to the old -2025 URLs
files = [
    "src/pages/sites/westmount/top-gold-mining-stocks.astro",
    "src/pages/sites/westmount/best-monthly-dividend-etfs.astro",
    "src/pages/sites/westmount/top-index-funds-and-etfs.astro"
]

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace("/top-gold-mining-stocks-2025", "/top-gold-mining-stocks")
    content = content.replace("/best-monthly-dividend-etfs-2025", "/best-monthly-dividend-etfs")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
