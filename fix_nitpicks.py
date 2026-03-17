import re
filepath = "src/pages/sites/westmount/dividend-investing-guide.astro"

with open(filepath, "r") as f:
    content = f.read()

# Remove the unused marketData block
market_data_block = re.search(r"// Injected financial data from Python script.*?};\n", content, re.DOTALL)
if market_data_block:
    content = content.replace(market_data_block.group(0), "")

# Fix hardcoded rgba color
content = content.replace("background-color: rgba(255, 255, 255, 0.03);", "background-color: var(--bg-color);")

# Fix hardcoded box shadow
content = content.replace("box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);", "box-shadow: 0 10px 15px -3px var(--border-color);")

with open(filepath, "w") as f:
    f.write(content)

print("Nitpicks fixed.")
