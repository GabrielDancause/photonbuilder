#!/usr/bin/env python3
"""
SEO Factory Executor — processes the action queue.

Phase 1: FIX (automated)
  - Stale dated URLs → create evergreen slug + redirect
  - Missing .html sources → create redirect rules
  - High bounce → log for manual review

Phase 2: OPTIMIZE (AI-assisted)
  - Rewrite title/description based on driving queries
  - Updates export const meta in .astro files directly

Phase 3: BUILD (queues for dispatch)
  - Generates build queue for Jules/content factory

Usage:
  python3 scripts/seo-execute.py                    # dry run (show what would happen)
  python3 scripts/seo-execute.py --apply             # execute changes
  python3 scripts/seo-execute.py --fix-only --apply  # only fixes
  python3 scripts/seo-execute.py --optimize-only --apply
  python3 scripts/seo-execute.py westmount --apply   # one site
"""

import os
import sys
import re
import json
import shutil
from pathlib import Path
from datetime import datetime

BASE = Path(os.path.expanduser("~/Desktop/photonbuilder"))
DATA = BASE / "data" / "seo"
PAGES_DIR = BASE / "src" / "pages" / "sites"
REDIRECTS_DIR = BASE / "public" / "sites"

QUEUE_PATH = DATA / "action-queue.json"
LOG_PATH = DATA / "execution-log.json"


def load_queue() -> dict:
    if QUEUE_PATH.exists():
        return json.loads(QUEUE_PATH.read_text())
    print("❌ No action queue found. Run seo-analyze.py first.")
    sys.exit(1)


def load_log() -> list:
    if LOG_PATH.exists():
        return json.loads(LOG_PATH.read_text())
    return []


def save_log(log: list):
    LOG_PATH.write_text(json.dumps(log, indent=2))


# ─── FIX: Stale Dated URLs ───────────────────────────────────────────────

def fix_stale_urls(site_id: str, actions: list, dry_run: bool) -> list:
    """Create evergreen versions of dated URLs and set up redirects."""
    results = []
    site_dir = PAGES_DIR / site_id
    
    month_pattern = re.compile(r'-(january|february|march|april|may|june|july|august|september|october|november|december)-\d{4}')

    seen_slugs = set()
    for action in actions:
        if action.get("subtype") != "stale_url":
            continue

        page_path = action["page"].strip("/")
        evergreen_slug = month_pattern.sub('', page_path)

        if evergreen_slug in seen_slugs:
            continue
        seen_slugs.add(evergreen_slug)

        source_file = site_dir / f"{page_path}.astro"
        evergreen_file = site_dir / f"{evergreen_slug}.astro"

        if not source_file.exists():
            results.append({"action": "skip", "reason": f"Source {source_file.name} not found", "page": page_path})
            continue

        if evergreen_file.exists():
            results.append({"action": "skip", "reason": f"Evergreen {evergreen_slug}.astro already exists", "page": page_path})
            continue

        print(f"  📄 {page_path} → {evergreen_slug}")

        if not dry_run:
            # Copy to evergreen slug
            content = source_file.read_text()
            
            # Update title to remove date references
            content = re.sub(
                r"(title:\s*['\"])(.+?)(March|April|May|June|July|August|September|October|November|December)\s+\d{4}",
                r"\1\2Latest",
                content
            )
            # Update meta description similarly
            content = re.sub(
                r"(march|april|may|june|july|august|september|october|november|december)\s+2026",
                "this month",
                content,
                flags=re.IGNORECASE
            )

            evergreen_file.write_text(content)

            # Create redirect from old slug to new
            # We'll collect these and write a _redirects file
            results.append({
                "action": "created_evergreen",
                "old_slug": page_path,
                "new_slug": evergreen_slug,
                "redirect": f"/{page_path}/ /{evergreen_slug}/ 301",
            })
        else:
            results.append({"action": "would_create", "old_slug": page_path, "new_slug": evergreen_slug})

    return results


# ─── FIX: Missing .html Sources ──────────────────────────────────────────

def fix_html_redirects(site_id: str, actions: list, dry_run: bool) -> list:
    """Generate redirect rules for .html URLs that have impressions."""
    results = []
    site_dir = PAGES_DIR / site_id

    for action in actions:
        if action.get("subtype") != "missing_source":
            continue

        page_path = action["page"].strip("/")
        
        # Check if it's a .html URL
        if ".html" in page_path:
            # Find the astro equivalent
            base_slug = page_path.replace(".html", "").replace("/", "")
            astro_file = site_dir / f"{base_slug}.astro"

            if astro_file.exists():
                print(f"  🔗 {page_path} → /{base_slug}/ (astro exists)")
                results.append({
                    "action": "redirect_html",
                    "from": f"/{page_path}",
                    "to": f"/{base_slug}/",
                    "redirect": f"/{page_path} /{base_slug}/ 301",
                    "impressions": action["impressions"],
                })
            else:
                print(f"  ⚠️  {page_path} — no astro equivalent found")
                results.append({"action": "needs_rebuild", "page": page_path, "impressions": action["impressions"]})
        else:
            # Non-html missing page — might be dynamic route or deleted
            print(f"  ⚠️  {page_path} — missing source, {action['impressions']} impressions")
            results.append({"action": "needs_investigation", "page": page_path, "impressions": action["impressions"]})

    return results


# ─── OPTIMIZE: Title/Description Rewrites ─────────────────────────────────

def optimize_meta(site_id: str, actions: list, dry_run: bool) -> list:
    """Rewrite title and description based on top driving queries."""
    results = []
    site_dir = PAGES_DIR / site_id

    for action in actions[:20]:  # Process top 20 by priority
        page_path = action["page"].strip("/")
        astro_file = site_dir / f"{page_path}.astro"

        if not astro_file.exists():
            # Try without trailing parts
            slug = page_path.split("/")[-1] if "/" in page_path else page_path
            astro_file = site_dir / f"{slug}.astro"

        if not astro_file.exists():
            results.append({"action": "skip", "reason": "file not found", "page": page_path})
            continue

        content = astro_file.read_text()

        # Extract current title and description
        title_match = re.search(r'title:\s*["\'](.+?)["\']', content)
        desc_match = re.search(r'description:\s*["\'](.+?)["\']', content)

        current_title = title_match.group(1) if title_match else ""
        current_desc = desc_match.group(1) if desc_match else ""

        driving_queries = action.get("driving_queries", [])
        if not driving_queries:
            continue

        # Generate optimized title based on top queries
        top_query = driving_queries[0]["query"]
        
        # Clean up query (remove site: filters, prediction market filters)
        clean_query = re.sub(r'\s*-site:\S+', '', top_query).strip()
        clean_query = re.sub(r'\s*before:\S+', '', clean_query).strip()
        
        # Build new title incorporating the top query intent
        # Rule: keep it under 60 chars, include the main keyword
        query_words = clean_query.lower().split()
        
        # Check if current title already contains the main query words
        title_words = current_title.lower().split()
        overlap = set(query_words) & set(title_words)
        
        if len(overlap) >= len(query_words) * 0.7:
            # Title already matches query reasonably well
            results.append({
                "action": "skip",
                "reason": "title already matches top query",
                "page": page_path,
                "current_title": current_title,
                "top_query": clean_query,
            })
            continue

        # Generate new title suggestion
        # Capitalize query and add site name
        new_title = clean_query.title()
        if len(new_title) > 50:
            new_title = new_title[:47] + "..."
        
        # Generate description from multiple queries
        all_query_text = " ".join(q["query"] for q in driving_queries[:3])
        all_query_text = re.sub(r'\s*-site:\S+', '', all_query_text)
        all_query_text = re.sub(r'\s*before:\S+', '', all_query_text)
        
        new_desc = f"Free {clean_query} data and analysis. Updated regularly with the latest market data."
        if len(new_desc) > 155:
            new_desc = new_desc[:152] + "..."

        print(f"  📝 {page_path}")
        print(f"     OLD: {current_title[:60]}")
        print(f"     NEW: {new_title[:60]}")
        print(f"     Query: {clean_query[:60]}")
        print(f"     Impact: {action['impressions']} imp, pos {action['position']}")

        if not dry_run:
            # Replace title
            if title_match:
                old_title_line = title_match.group(0)
                new_title_line = f'title: "{new_title}"'
                content = content.replace(old_title_line, new_title_line)

            # Replace description
            if desc_match:
                old_desc_line = desc_match.group(0)
                new_desc_line = f'description: "{new_desc}"'
                content = content.replace(old_desc_line, new_desc_line)

            astro_file.write_text(content)

        results.append({
            "action": "optimized" if not dry_run else "would_optimize",
            "page": page_path,
            "old_title": current_title,
            "new_title": new_title,
            "old_desc": current_desc[:80],
            "new_desc": new_desc[:80],
            "impressions": action["impressions"],
            "ctr": action["ctr"],
            "position": action["position"],
            "top_query": clean_query,
        })

    return results


# ─── BUILD: Queue for Content Factory ─────────────────────────────────────

def queue_builds(site_id: str, actions: list, dry_run: bool) -> list:
    """Generate build queue entries for new page opportunities."""
    results = []

    for action in actions[:10]:  # Top 10 build opportunities
        results.append({
            "action": "queued_for_build",
            "site": site_id,
            "suggested_slug": action["suggested_slug"],
            "primary_query": action["primary_query"],
            "related_queries": action.get("related_queries", []),
            "total_impressions": action["total_impressions"],
            "best_position": action["best_position"],
        })
        print(f"  🏗️  Queue: {action['suggested_slug']} ({action['total_impressions']} imp)")

    return results


# ─── Write Redirects ──────────────────────────────────────────────────────

def write_redirects(site_id: str, redirect_rules: list, dry_run: bool):
    """Write redirect rules to Cloudflare _redirects or worker config."""
    if not redirect_rules:
        return

    redirects_file = BASE / "data" / "seo" / f"{site_id}-redirects.txt"
    
    lines = [f"# Generated {datetime.now().isoformat()} by seo-execute.py"]
    for rule in redirect_rules:
        if "redirect" in rule:
            lines.append(rule["redirect"])

    if not dry_run:
        redirects_file.write_text("\n".join(lines) + "\n")
        print(f"\n  📁 Redirect rules saved to {redirects_file}")
    else:
        print(f"\n  📁 Would write {len(redirect_rules)} redirects to {redirects_file}")


# ─── Main ─────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    dry_run = "--apply" not in args
    fix_only = "--fix-only" in args
    optimize_only = "--optimize-only" in args
    build_only = "--build-only" in args
    
    site_args = [a for a in args if not a.startswith("--")]
    
    queue = load_queue()
    log = load_log()
    
    target_sites = site_args if site_args else list(queue.keys())

    if dry_run:
        print("🔍 DRY RUN — no changes will be made. Use --apply to execute.\n")
    else:
        print("⚡ APPLYING CHANGES\n")

    all_results = {}
    
    for site_id in sorted(target_sites):
        if site_id not in queue:
            print(f"⚠️  No actions for {site_id}")
            continue

        site_queue = queue[site_id]
        print(f"\n{'='*60}")
        print(f"🌐 {site_id.upper()}")
        print(f"{'='*60}")

        site_results = {"fix": [], "optimize": [], "build": []}
        all_redirects = []

        # Phase 1: FIX
        if not optimize_only and not build_only:
            fix_actions = site_queue.get("fix", [])
            if fix_actions:
                print(f"\n🔧 FIX ({len(fix_actions)} issues)")
                
                stale_results = fix_stale_urls(site_id, fix_actions, dry_run)
                site_results["fix"].extend(stale_results)
                all_redirects.extend([r for r in stale_results if "redirect" in r])

                html_results = fix_html_redirects(site_id, fix_actions, dry_run)
                site_results["fix"].extend(html_results)
                all_redirects.extend([r for r in html_results if "redirect" in r])

                write_redirects(site_id, all_redirects, dry_run)

        # Phase 2: OPTIMIZE
        if not fix_only and not build_only:
            opt_actions = site_queue.get("optimize", [])
            if opt_actions:
                print(f"\n📝 OPTIMIZE ({len(opt_actions)} pages, processing top 20)")
                opt_results = optimize_meta(site_id, opt_actions, dry_run)
                site_results["optimize"] = opt_results

        # Phase 3: BUILD
        if not fix_only and not optimize_only:
            build_actions = site_queue.get("build", [])
            if build_actions:
                print(f"\n🏗️  BUILD ({len(build_actions)} opportunities)")
                build_results = queue_builds(site_id, build_actions, dry_run)
                site_results["build"] = build_results

        all_results[site_id] = site_results

    # Save build queue for factory dispatch
    build_queue = []
    for site_id, results in all_results.items():
        for b in results.get("build", []):
            build_queue.append(b)

    if build_queue:
        bq_path = DATA / "build-queue.json"
        if not dry_run:
            bq_path.write_text(json.dumps(build_queue, indent=2))
            print(f"\n📁 Build queue ({len(build_queue)} items) saved to {bq_path}")
        else:
            print(f"\n📁 Would save {len(build_queue)} build items to {bq_path}")

    # Log execution
    if not dry_run:
        log.append({
            "timestamp": datetime.now().isoformat(),
            "results": all_results,
        })
        save_log(log)

    # Summary
    print(f"\n{'='*60}")
    print("📊 EXECUTION SUMMARY")
    print(f"{'='*60}")
    for site_id, results in sorted(all_results.items()):
        fixes = len([r for r in results.get("fix", []) if r["action"] not in ("skip",)])
        opts = len([r for r in results.get("optimize", []) if r["action"] not in ("skip",)])
        builds = len(results.get("build", []))
        print(f"  {site_id:<20} Fixed:{fixes:>3}  Optimized:{opts:>3}  Queued:{builds:>3}")

    if dry_run:
        print(f"\n💡 Run with --apply to execute these changes.")


if __name__ == "__main__":
    main()
