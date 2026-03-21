#!/usr/bin/env python3
"""
Apply approved SEO review items.

Usage:
  python3 scripts/seo-apply-review.py 1,3,5        # apply specific items
  python3 scripts/seo-apply-review.py all           # apply all
  python3 scripts/seo-apply-review.py 1-5           # apply range
"""

import os
import sys
import re
import json
from pathlib import Path

BASE = Path(os.path.expanduser("~/Desktop/photonbuilder"))
DATA = BASE / "data" / "seo"
REVIEW_PATH = DATA / "review-queue.json"
PAGES_DIR = BASE / "src" / "pages" / "sites"


def parse_selection(arg: str, total: int) -> set:
    """Parse selection like '1,3,5' or '1-5' or 'all'."""
    if arg.lower() == "all":
        return set(range(1, total + 1))
    
    selected = set()
    for part in arg.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            selected.update(range(int(start), int(end) + 1))
        else:
            selected.add(int(part))
    return selected


def apply_optimize(item: dict) -> bool:
    """Apply a title/description optimization."""
    site_dir = PAGES_DIR / item["site"]
    astro_file = site_dir / f"{item['page']}.astro"

    if not astro_file.exists():
        print(f"  ❌ File not found: {astro_file}")
        return False

    content = astro_file.read_text()

    # Replace title
    title_match = re.search(r'title:\s*["\'](.+?)["\']', content)
    if title_match and item.get("suggested_title"):
        old = title_match.group(0)
        new = f'title: "{item["suggested_title"]}"'
        content = content.replace(old, new)

    # Generate and replace description
    desc_match = re.search(r'description:\s*["\'](.+?)["\']', content)
    if desc_match:
        new_desc = f"Free {item['top_query']} data and analysis. Updated regularly."
        if len(new_desc) > 155:
            new_desc = new_desc[:152] + "..."
        old = desc_match.group(0)
        new = f'description: "{new_desc}"'
        content = content.replace(old, new)

    astro_file.write_text(content)
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 seo-apply-review.py 1,3,5")
        print("       python3 seo-apply-review.py all")
        sys.exit(1)

    if not REVIEW_PATH.exists():
        print("❌ No review queue. Run: python3 scripts/seo-review.py --save")
        sys.exit(1)

    items = json.loads(REVIEW_PATH.read_text())
    selection = parse_selection(sys.argv[1], len(items))

    applied = 0
    skipped = 0

    for idx in sorted(selection):
        if idx < 1 or idx > len(items):
            print(f"  ⚠️  #{idx} out of range")
            continue

        item = items[idx - 1]

        if item["type"] == "OPTIMIZE":
            print(f"  ✅ #{idx} {item['site']}/{item['page']}")
            print(f"     → {item['suggested_title'][:55]}")
            if apply_optimize(item):
                applied += 1
            else:
                skipped += 1

        elif item["type"] == "BUILD":
            print(f"  📋 #{idx} BUILD: {item['suggested_slug']} (queued, not auto-built)")
            # BUILD items need Jules/factory — just log approval
            skipped += 1

    print(f"\n📊 Applied: {applied} | Skipped: {skipped}")
    
    if applied > 0:
        print(f"\n🔜 Next: cd ~/Desktop/photonbuilder && npm run build && git add -A && git commit -m 'seo: approved title rewrites' && git push")


if __name__ == "__main__":
    main()
