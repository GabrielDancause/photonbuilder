import os
import re

files = [
    "src/pages/sites/westmount/top-performing-ai-stocks-2025.astro",
    "src/pages/sites/westmount/best-us-stocks-to-invest-2025.astro",
    "src/pages/sites/westmount/best-performing-healthcare-stocks-in-india-2024.astro"
]

old_block = """          let valX = x.innerHTML.toLowerCase().replace(/[^0-9.-]+/g,"");
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

new_block = """          function parseValue(str) {
            let s = str.toUpperCase();
            let mult = 1;
            if (s.includes('T')) mult = 1e12;
            else if (s.includes('B')) mult = 1e9;
            else if (s.includes('M') && !s.includes('MO')) mult = 1e6;
            else if (s.includes('K')) mult = 1e3;
            else if (s.includes('CR')) mult = 1e7;

            let numStr = s.replace(/[^0-9.-]+/g,"");
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

    # Replace sort logic
    content = content.replace(old_block, new_block)

    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)

print("Updates applied to all files.")
