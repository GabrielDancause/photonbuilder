#!/usr/bin/env python3
"""
SEO Analysis Engine — reads cached GSC/GA/Ahrefs data and generates
prioritized action queues for the factory.

3 action types:
  FIX      — technical issues (stale URLs, orphan pages, redirects)
  OPTIMIZE — high impressions, low CTR → rewrite title/description
  BUILD    — queries we rank for but lack dedicated pages

Usage:
  python3 scripts/seo-analyze.py                    # analyze all sites
  python3 scripts/seo-analyze.py westmount          # one site
  python3 scripts/seo-analyze.py --output actions    # write action queue to file
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BASE = Path(os.path.expanduser("~/Desktop/photonbuilder"))
DATA = BASE / "data" / "seo"
PAGES_DIR = BASE / "src" / "pages" / "sites"


def load_latest(source: str, site_id: str) -> dict | None:
    """Load latest cached data for a source+site."""
    latest = DATA / source / site_id / "latest.json"
    if latest.exists():
        target = latest.resolve() if latest.is_symlink() else latest
        return json.loads(target.read_text())
    return None


def get_existing_slugs(site_id: str) -> set:
    """Get all existing page slugs for a site."""
    site_dir = PAGES_DIR / site_id
    if not site_dir.exists():
        return set()
    slugs = set()
    for f in site_dir.glob("*.astro"):
        name = f.stem
        if name != "index" and not name.startswith("["):
            slugs.add(name)
    return slugs


def analyze_optimize(gsc_data: dict, ga_data: dict | None, site_id: str) -> list:
    """Find pages with high impressions but low CTR — title/description rewrites."""
    actions = []

    if not gsc_data or not gsc_data.get("pages"):
        return actions

    # Get GA bounce rate data for cross-reference
    ga_bounce = {}
    if ga_data:
        for p in ga_data.get("pages", []):
            ga_bounce[p["path"]] = {
                "sessions": p["sessions"],
                "bounceRate": p.get("bounceRate", 0),
                "avgDuration": p.get("avgDuration", 0),
            }

    for page in gsc_data["pages"]:
        impressions = page["impressions"]
        clicks = page["clicks"]
        ctr = page["ctr"]
        position = page["position"]

        # Skip low-impression pages
        if impressions < 20:
            continue

        path = page["page"].split("//")[-1].split("/", 1)[-1].strip("/")

        # High impressions, low CTR, decent position → title/description sucks
        if impressions >= 50 and ctr < 0.03 and position <= 15:
            # Find the queries driving this page
            driving_queries = []
            for combo in gsc_data.get("query_page_combos", []):
                if page["page"] in combo["page"]:
                    driving_queries.append({
                        "query": combo["query"],
                        "impressions": combo["impressions"],
                        "position": combo["position"],
                    })
            driving_queries.sort(key=lambda x: x["impressions"], reverse=True)

            priority = impressions * (1 - ctr)  # higher impressions + lower CTR = higher priority
            if position <= 5:
                priority *= 2  # already ranking well, just need better CTR

            ga_info = ga_bounce.get(f"/{path}/") or ga_bounce.get(f"/{path}")
            
            actions.append({
                "type": "OPTIMIZE",
                "priority": round(priority),
                "page": f"/{path}/",
                "impressions": impressions,
                "clicks": clicks,
                "ctr": ctr,
                "position": position,
                "driving_queries": driving_queries[:5],
                "ga_sessions": ga_info["sessions"] if ga_info else None,
                "ga_bounce": ga_info["bounceRate"] if ga_info else None,
                "reason": f"{impressions} impressions, {ctr*100:.1f}% CTR, pos {position} — rewrite title/description to match search intent",
            })

    actions.sort(key=lambda x: x["priority"], reverse=True)
    return actions


def analyze_build(gsc_data: dict, site_id: str, existing_slugs: set) -> list:
    """Find queries we rank for but don't have dedicated pages for."""
    actions = []

    if not gsc_data:
        return actions

    # Group queries by intent/topic
    query_groups = defaultdict(lambda: {"queries": [], "total_impressions": 0, "best_position": 100})

    for q in gsc_data.get("queries", []):
        if q["impressions"] < 5:
            continue

        query_text = q["query"].lower().strip()
        # Skip branded queries
        if any(brand in query_text for brand in ["westmount", "photonbuilder", "siliconbased", "firemaths"]):
            continue
        # Skip queries with search operators (these are power-user queries, not page opportunities)
        if "-site:" in query_text or "before:" in query_text or "after:" in query_text:
            continue

        # Normalize to a slug-like key
        slug_key = re.sub(r'[^a-z0-9]+', '-', query_text).strip('-')
        # Remove date suffixes for evergreen grouping
        slug_key = re.sub(r'-(?:january|february|march|april|may|june|july|august|september|october|november|december)-\d{4}$', '', slug_key)
        slug_key = re.sub(r'-\d{4}$', '', slug_key)

        # Check if we already have a page matching this query
        has_page = False
        for slug in existing_slugs:
            # Fuzzy match: if the query words overlap significantly with the slug
            query_words = set(query_text.split())
            slug_words = set(slug.split('-'))
            overlap = query_words & slug_words
            if len(overlap) >= min(3, len(query_words) * 0.6):
                has_page = True
                break

        if not has_page:
            group = query_groups[slug_key]
            group["queries"].append(q)
            group["total_impressions"] += q["impressions"]
            group["best_position"] = min(group["best_position"], q["position"])

    # Convert groups to actions
    for slug_key, group in query_groups.items():
        if group["total_impressions"] < 15:
            continue

        # Sort queries by impressions
        group["queries"].sort(key=lambda x: x["impressions"], reverse=True)
        primary_query = group["queries"][0]

        priority = group["total_impressions"]
        if group["best_position"] <= 10:
            priority *= 1.5  # already showing on page 1 without a dedicated page

        actions.append({
            "type": "BUILD",
            "priority": round(priority),
            "suggested_slug": slug_key,
            "primary_query": primary_query["query"],
            "total_impressions": group["total_impressions"],
            "query_count": len(group["queries"]),
            "best_position": group["best_position"],
            "related_queries": [q["query"] for q in group["queries"][:5]],
            "reason": f'{group["total_impressions"]} impressions across {len(group["queries"])} queries, best pos {group["best_position"]:.0f} — no dedicated page exists',
        })

    actions.sort(key=lambda x: x["priority"], reverse=True)
    return actions


def analyze_fix(gsc_data: dict, ga_data: dict | None, site_id: str, existing_slugs: set) -> list:
    """Find technical issues: stale dated URLs, zero-traffic pages, orphans."""
    actions = []

    if not gsc_data:
        return actions

    # 1. Stale dated URLs (contain month names or year that's not current)
    month_pattern = re.compile(r'(january|february|march|april|may|june|july|august|september|october|november|december)-(\d{4})')
    
    for page in gsc_data.get("pages", []):
        url = page["page"].lower()
        match = month_pattern.search(url)
        if match:
            month_name = match.group(1)
            year = match.group(2)
            path = page["page"].split("//")[-1].split("/", 1)[-1].strip("/")
            
            actions.append({
                "type": "FIX",
                "subtype": "stale_url",
                "priority": page["impressions"] * 2,  # high priority — losing freshness
                "page": f"/{path}/",
                "impressions": page["impressions"],
                "reason": f"Dated URL ({month_name} {year}) — create evergreen version and redirect. {page['impressions']} impressions at risk.",
            })

    # 2. Pages in GSC with impressions but not matching any existing astro file
    gsc_paths = set()
    for page in gsc_data.get("pages", []):
        path = page["page"].split("//")[-1].split("/", 1)[-1].strip("/")
        if path:
            gsc_paths.add(path)

    for path in gsc_paths:
        slug = path.strip("/")
        if slug and slug not in existing_slugs:
            page_data = next((p for p in gsc_data["pages"] if path in p["page"]), None)
            if page_data and page_data["impressions"] > 10:
                actions.append({
                    "type": "FIX",
                    "subtype": "missing_source",
                    "priority": page_data["impressions"],
                    "page": f"/{path}/",
                    "impressions": page_data["impressions"],
                    "reason": f"Page has {page_data['impressions']} GSC impressions but no .astro source file found — may be from old build or dynamic route",
                })

    # 3. GA pages with sessions but high bounce + low duration
    if ga_data:
        for page in ga_data.get("pages", []):
            if page["sessions"] >= 5 and page["bounceRate"] > 0.85 and page["avgDuration"] < 10:
                actions.append({
                    "type": "FIX",
                    "subtype": "high_bounce",
                    "priority": page["sessions"],
                    "page": page["path"],
                    "sessions": page["sessions"],
                    "bounceRate": page["bounceRate"],
                    "avgDuration": page["avgDuration"],
                    "reason": f'{page["sessions"]} sessions but {page["bounceRate"]*100:.0f}% bounce, {page["avgDuration"]:.0f}s avg duration — content not matching intent',
                })

    actions.sort(key=lambda x: x["priority"], reverse=True)
    return actions


def print_report(site_id: str, fix_actions: list, optimize_actions: list, build_actions: list):
    """Print a human-readable report."""
    total = len(fix_actions) + len(optimize_actions) + len(build_actions)
    print(f"\n{'='*60}")
    print(f"🌐 {site_id.upper()} — {total} actions identified")
    print(f"{'='*60}")

    if fix_actions:
        print(f"\n🔧 FIX ({len(fix_actions)} issues)")
        for a in fix_actions[:10]:
            print(f"  [{a['priority']:>5}] {a['page']}")
            print(f"         {a['reason']}")

    if optimize_actions:
        print(f"\n📝 OPTIMIZE ({len(optimize_actions)} pages)")
        for a in optimize_actions[:10]:
            queries = ", ".join(q["query"][:40] for q in a.get("driving_queries", [])[:3])
            print(f"  [{a['priority']:>5}] {a['page']} — {a['impressions']} imp, {a['ctr']*100:.1f}% CTR, pos {a['position']}")
            if queries:
                print(f"         Top queries: {queries}")

    if build_actions:
        print(f"\n🏗️  BUILD ({len(build_actions)} opportunities)")
        for a in build_actions[:10]:
            print(f"  [{a['priority']:>5}] «{a['primary_query']}»")
            print(f"         {a['total_impressions']} imp, {a['query_count']} related queries, best pos {a['best_position']:.0f}")

    if not total:
        print("\n  ℹ️  No actions — not enough data yet. Keep building content!")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    write_output = "--output" in sys.argv

    # Determine which sites to analyze
    all_site_dirs = [d.name for d in (DATA / "gsc").iterdir() if d.is_dir()] if (DATA / "gsc").exists() else []
    target_sites = args if args else all_site_dirs

    all_actions = {}

    for site_id in sorted(target_sites):
        gsc_data = load_latest("gsc", site_id)
        ga_data = load_latest("ga", site_id)
        existing_slugs = get_existing_slugs(site_id)

        fix_actions = analyze_fix(gsc_data, ga_data, site_id, existing_slugs)
        optimize_actions = analyze_optimize(gsc_data, ga_data, site_id)
        build_actions = analyze_build(gsc_data, site_id, existing_slugs)

        print_report(site_id, fix_actions, optimize_actions, build_actions)

        all_actions[site_id] = {
            "analyzed": datetime.now().isoformat(),
            "fix": fix_actions,
            "optimize": optimize_actions,
            "build": build_actions,
            "summary": {
                "fix_count": len(fix_actions),
                "optimize_count": len(optimize_actions),
                "build_count": len(build_actions),
                "total_impression_opportunity": sum(a.get("impressions", 0) for a in optimize_actions),
            },
        }

    if write_output:
        out_path = DATA / "action-queue.json"
        out_path.write_text(json.dumps(all_actions, indent=2))
        print(f"\n📁 Action queue saved to {out_path}")

    # Network summary
    print(f"\n{'='*60}")
    print("📊 NETWORK SUMMARY")
    print(f"{'='*60}")
    for site_id, data in sorted(all_actions.items(), key=lambda x: x[1]["summary"]["total_impression_opportunity"], reverse=True):
        s = data["summary"]
        print(f"  {site_id:<20} FIX:{s['fix_count']:>3}  OPT:{s['optimize_count']:>3}  BUILD:{s['build_count']:>3}  | {s['total_impression_opportunity']:>6} impression opportunity")


if __name__ == "__main__":
    main()
