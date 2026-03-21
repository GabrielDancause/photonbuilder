#!/usr/bin/env python3
"""
SEO Review Queue — generates approve/reject suggestions for WhatsApp.

Reads action queue, produces numbered suggestions.
User replies with approved numbers → seo-apply-review.py handles it.

Usage:
  python3 scripts/seo-review.py                    # all sites
  python3 scripts/seo-review.py westmount          # one site
  python3 scripts/seo-review.py --format whatsapp  # WhatsApp-friendly output
  python3 scripts/seo-review.py --save             # save review queue to file
"""

import os
import sys
import re
import json
from pathlib import Path

BASE = Path(os.path.expanduser("~/Desktop/photonbuilder"))
DATA = BASE / "data" / "seo"
QUEUE_PATH = DATA / "action-queue.json"
REVIEW_PATH = DATA / "review-queue.json"


def clean_query(query: str) -> str:
    q = re.sub(r'\s*-site:\S+', '', query)
    q = re.sub(r'\s*before:\S+', '', q)
    q = re.sub(r'\s*after:\S+', '', q)
    q = q.replace('"', '')
    q = re.sub(r'\s+OR\s+', ' ', q, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', q).strip()


def is_junk_query(query: str) -> bool:
    q = query.lower()
    if re.match(r'^[a-z]{1,5}\s+(beta|volatility|price|stock)\b', q):
        return True
    if len(q.split()) > 10:
        return True
    return False


def generate_review(site_id: str, actions: dict) -> list:
    """Generate review items for a site."""
    items = []

    # OPTIMIZE suggestions
    for action in actions.get("optimize", [])[:15]:
        driving = action.get("driving_queries", [])
        clean_queries = []
        for dq in driving:
            cleaned = clean_query(dq["query"])
            if cleaned and not is_junk_query(cleaned):
                clean_queries.append({"clean": cleaned, "impressions": dq["impressions"]})

        if not clean_queries:
            continue

        top = clean_queries[0]
        page_path = action["page"].strip("/")

        # Extract current title from action data or read file
        pages_dir = BASE / "src" / "pages" / "sites" / site_id
        astro_file = pages_dir / f"{page_path}.astro"
        
        current_title = ""
        if astro_file.exists():
            content = astro_file.read_text()
            m = re.search(r'title:\s*["\'](.+?)["\']', content)
            if m:
                current_title = m.group(1)

        # Generate suggestion
        new_title = top["clean"].title()
        if "2026" in current_title and "2026" not in new_title:
            new_title += " (2026)"
        if len(new_title) > 60:
            new_title = new_title[:57] + "..."

        # Check if it's actually different enough
        if current_title.lower().strip() == new_title.lower().strip():
            continue

        items.append({
            "type": "OPTIMIZE",
            "site": site_id,
            "page": page_path,
            "current_title": current_title,
            "suggested_title": new_title,
            "top_query": top["clean"],
            "impressions": action["impressions"],
            "ctr": action["ctr"],
            "position": action["position"],
            "query_count": len(clean_queries),
        })

    # BUILD suggestions
    for action in actions.get("build", [])[:5]:
        items.append({
            "type": "BUILD",
            "site": site_id,
            "suggested_slug": action["suggested_slug"],
            "primary_query": action["primary_query"],
            "impressions": action["total_impressions"],
            "position": action["best_position"],
            "related_queries": action.get("related_queries", [])[:3],
        })

    return items


def format_whatsapp(items: list) -> str:
    """Format review items for WhatsApp (no markdown tables!)."""
    lines = ["*🔍 SEO Review Queue*\n"]
    lines.append("Reply with numbers to approve (e.g. *1,3,5* or *all*)\n")

    optimize_items = [i for i in items if i["type"] == "OPTIMIZE"]
    build_items = [i for i in items if i["type"] == "BUILD"]

    if optimize_items:
        lines.append("*📝 TITLE REWRITES*\n")
        for idx, item in enumerate(optimize_items, 1):
            lines.append(f"*{idx}.* /{item['page']}/")
            lines.append(f"   📊 {item['impressions']} imp | pos {item['position']} | {item['ctr']*100:.1f}% CTR")
            lines.append(f"   OLD: {item['current_title'][:55]}")
            lines.append(f"   NEW: {item['suggested_title'][:55]}")
            lines.append(f"   🔎 \"{item['top_query'][:50]}\"")
            lines.append("")

    if build_items:
        offset = len(optimize_items)
        lines.append("*🏗️ NEW PAGES*\n")
        for idx, item in enumerate(build_items, offset + 1):
            lines.append(f"*{idx}.* {item['suggested_slug']}")
            lines.append(f"   📊 {item['impressions']} imp | pos {item['position']:.0f}")
            lines.append(f"   🔎 \"{item['primary_query'][:50]}\"")
            lines.append("")

    lines.append(f"_{len(items)} items total. Reply with numbers to approve._")
    return "\n".join(lines)


def format_plain(items: list) -> str:
    """Format for terminal output."""
    lines = []
    for idx, item in enumerate(items, 1):
        if item["type"] == "OPTIMIZE":
            lines.append(f"  {idx:>2}. [{item['impressions']:>5} imp] /{item['page']}/")
            lines.append(f"      OLD: {item['current_title'][:60]}")
            lines.append(f"      NEW: {item['suggested_title'][:60]}")
            lines.append(f"      Query: {item['top_query'][:60]}")
        elif item["type"] == "BUILD":
            lines.append(f"  {idx:>2}. [{item['impressions']:>5} imp] NEW: {item['suggested_slug']}")
            lines.append(f"      Query: {item['primary_query'][:60]}")
        lines.append("")
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    whatsapp = "--format" in args and "whatsapp" in args
    save = "--save" in args
    site_args = [a for a in args if not a.startswith("--") and a != "whatsapp"]

    queue = json.loads(QUEUE_PATH.read_text()) if QUEUE_PATH.exists() else {}
    target_sites = site_args if site_args else list(queue.keys())

    all_items = []
    for site_id in sorted(target_sites):
        if site_id not in queue:
            continue
        items = generate_review(site_id, queue[site_id])
        all_items.extend(items)

    if not all_items:
        print("No review items. Run seo-analyze.py first.")
        return

    if whatsapp:
        print(format_whatsapp(all_items))
    else:
        print(f"\n📋 SEO Review Queue ({len(all_items)} items)\n")
        print(format_plain(all_items))

    if save:
        REVIEW_PATH.write_text(json.dumps(all_items, indent=2))
        print(f"\n📁 Review queue saved to {REVIEW_PATH}")


if __name__ == "__main__":
    main()
