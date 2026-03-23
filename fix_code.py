import os
import re

files = [
    "src/pages/sites/westmount/top-performing-ai-stocks-2025.astro",
    "src/pages/sites/westmount/best-us-stocks-to-invest-2025.astro",
    "src/pages/sites/westmount/best-performing-healthcare-stocks-in-india-2024.astro"
]

related_guides = """
    <section class="related-guides" style="margin: 3rem 0; padding: 2rem; background: var(--card-bg); border-radius: 12px; border: 1px solid var(--border-color);">
      <h2 style="margin-top: 0; color: var(--text-primary);">Related Guides</h2>
      <ul style="line-height: 1.8;">
         <li><a href="/top-performing-ai-stocks-2025">Top Performing AI Stocks for 2025</a></li>
         <li><a href="/best-us-stocks-to-invest-2025">Best US Stocks to Invest in 2025</a></li>
         <li><a href="/best-performing-healthcare-stocks-in-india-2024">Best Performing Healthcare Stocks in India 2024</a></li>
      </ul>
    </section>
    <section class="faq-section">
"""

old_sort_logic = """          let valX = x.innerHTML.toLowerCase().replace(/[^0-9.-]+/g,"");
          let valY = y.innerHTML.toLowerCase().replace(/[^0-9.-]+/g,"");

          // Check if it's a number after stripping chars
          let isNum = !isNaN(parseFloat(valX)) && !isNaN(parseFloat(valY));

          if (dir == "asc") {
            if (isNum) {
                if (parseFloat(valX) > parseFloat(valY)) { shouldSwitch = true; break; }
            } else {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) { shouldSwitch = true; break; }
            }
          } else if (dir == "desc") {
             if (isNum) {
                if (parseFloat(valX) < parseFloat(valY)) { shouldSwitch = true; break; }
            } else {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) { shouldSwitch = true; break; }
            }
          }"""

new_sort_logic = """          function parseValue(str) {
            let s = str.toUpperCase();
            let mult = 1;
            if (s.includes('T')) mult = 1e12;
            else if (s.includes('B')) mult = 1e9;
            else if (s.includes('M')) mult = 1e6;
            else if (s.includes('K')) mult = 1e3;
            else if (s.includes('CR')) mult = 1e7;

            let numStr = str.replace(/[^0-9.-]+/g,"");
            if (numStr === "" || numStr === "-" || numStr === ".") return null;
            let num = parseFloat(numStr);
            return isNaN(num) ? null : num * mult;
          }

          let numX = parseValue(x.innerHTML);
          let numY = parseValue(y.innerHTML);
          let isNum = numX !== null && numY !== null;

          if (dir == "asc") {
            if (isNum) {
                if (numX > numY) { shouldSwitch = true; break; }
            } else {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) { shouldSwitch = true; break; }
            }
          } else if (dir == "desc") {
             if (isNum) {
                if (numX < numY) { shouldSwitch = true; break; }
            } else {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) { shouldSwitch = true; break; }
            }
          }"""

for fp in files:
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace FAQ section with Related Guides + FAQ section
    content = content.replace('<section class="faq-section">', related_guides)

    # Replace sort logic
    content = content.replace(old_sort_logic, new_sort_logic)

    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)

print("Updates applied to all files.")
