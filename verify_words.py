import re
import sys

def verify_word_count(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Strip frontmatter
    content = re.sub(r'^---.*?---', '', content, flags=re.DOTALL)

    # Strip style blocks
    content = re.sub(r'<style.*?>.*?</style>', '', content, flags=re.DOTALL)

    # Strip script blocks
    content = re.sub(r'<script.*?>.*?</script>', '', content, flags=re.DOTALL)

    # Strip site layout wrapper and calculator specific stuff (quick dirty clean)
    content = re.sub(r'<SiteLayout.*?>|</SiteLayout>', '', content)
    content = re.sub(r'<div class="calculator-card">.*?</div>.*?</div>', '', content, flags=re.DOTALL) # remove most of calc

    # Strip all HTML tags
    text = re.sub(r'<[^>]+>', ' ', content)

    # Calculate word count
    words = text.split()
    word_count = len(words)

    print(f"Word count: {word_count}")

    if word_count < 1500:
        print("ERROR: Word count is less than 1500.")
        sys.exit(1)
    else:
        print("Word count verification passed.")
        sys.exit(0)

verify_word_count("src/pages/sites/westmount/stock-trading-simulator.astro")
