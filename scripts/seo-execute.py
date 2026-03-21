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

def clean_query(query: str) -> str:
    """Remove search operators, filters, and junk from a query."""
    q = query
    # Remove -site: filters
    q = re.sub(r'\s*-site:\S+', '', q)
    # Remove before:/after: date filters
    q = re.sub(r'\s*before:\S+', '', q)
    q = re.sub(r'\s*after:\S+', '', q)
    # Remove quoted exact-match operators
    q = q.replace('"', '')
    # Remove OR operators
    q = re.sub(r'\s+OR\s+', ' ', q, flags=re.IGNORECASE)
    # Clean up extra whitespace
    q = re.sub(r'\s+', ' ', q).strip()
    return q


def is_junk_query(query: str) -> bool:
    """Detect queries that are too specific/noisy to base a title on."""
    q = query.lower()
    # Single stock ticker lookups
    if re.match(r'^[a-z]{1,5}\s+(beta|volatility|price|stock)\b', q):
        return True
    # Very long queries (>10 words) are usually too specific
    if len(q.split()) > 10:
        return True
    return False


def optimize_meta(site_id: str, actions: list, dry_run: bool) -> list:
    """Rewrite title and description based on top driving queries.
    
    Rules:
    - Never downgrade a good title (if current title already covers query intent, skip)
    - Clean all search operators from queries before using them
    - Skip junk queries (single ticker lookups, very long queries)
    - Prefer incorporating query keywords INTO existing title structure
    - Title must be human-readable, not a raw query
    """
    results = []
    site_dir = PAGES_DIR / site_id

    for action in actions[:20]:  # Process top 20 by priority
        page_path = action["page"].strip("/")
        astro_file = site_dir / f"{page_path}.astro"

        if not astro_file.exists():
            slug = page_path.split("/")[-1] if "/" in page_path else page_path
            astro_file = site_dir / f"{slug}.astro"

        if not astro_file.exists():
            results.append({"action": "skip", "reason": "file not found", "page": page_path})
            continue

        content = astro_file.read_text()

        title_match = re.search(r'title:\s*["\'](.+?)["\']', content)
        desc_match = re.search(r'description:\s*["\'](.+?)["\']', content)

        current_title = title_match.group(1) if title_match else ""
        current_desc = desc_match.group(1) if desc_match else ""

        driving_queries = action.get("driving_queries", [])
        if not driving_queries:
            continue

        # Clean all queries and find the best one
        clean_queries = []
        for dq in driving_queries:
            cleaned = clean_query(dq["query"])
            if cleaned and not is_junk_query(cleaned):
                clean_queries.append({**dq, "clean": cleaned})

        if not clean_queries:
            results.append({"action": "skip", "reason": "all driving queries are junk/noise", "page": page_path})
            continue

        top = clean_queries[0]
        top_clean = top["clean"]

        # Check if current title already covers query intent
        title_lower = current_title.lower()
        query_words = set(top_clean.lower().split()) - {"the", "a", "an", "in", "of", "for", "and", "or", "to", "by", "with", "on", "at", "is", "are"}
        title_words = set(title_lower.split()) - {"the", "a", "an", "in", "of", "for", "and", "or", "to", "by", "with", "on", "at", "is", "are", "—", "|", ":", "-"}
        overlap = query_words & title_words
        
        if len(overlap) >= len(query_words) * 0.6:
            results.append({
                "action": "skip",
                "reason": f"title already covers intent ({len(overlap)}/{len(query_words)} key words match)",
                "page": page_path,
                "current_title": current_title,
                "top_query": top_clean,
            })
            continue

        # Build improved title: keep the existing structure but inject key missing words
        # Strategy: prepend the top query keyword phrase, append existing differentiator
        missing_words = query_words - title_words
        
        # If only 1-2 words are missing, the title is close enough
        if len(missing_words) <= 1:
            results.append({
                "action": "skip",
                "reason": f"title nearly matches (only missing: {missing_words})",
                "page": page_path,
                "current_title": current_title,
                "top_query": top_clean,
            })
            continue

        # Generate new title: use query as base, keep it natural
        # Take the cleaned query and title-case it properly
        new_title = top_clean.title()
        # Keep the year if the original had it
        if "2026" in current_title and "2026" not in new_title:
            new_title += " (2026)"
        # Cap at 60 chars
        if len(new_title) > 60:
            new_title = new_title[:57] + "..."

        # Generate description using top 3 clean queries
        desc_queries = [cq["clean"] for cq in clean_queries[:3]]
        new_desc = f"Free {desc_queries[0]} data and analysis."
        if len(desc_queries) > 1:
            new_desc += f" Compare {desc_queries[1]} and more."
        new_desc += " Updated regularly."
        if len(new_desc) > 155:
            new_desc = new_desc[:152] + "..."

        print(f"  📝 {page_path}")
        print(f"     OLD: {current_title[:60]}")
        print(f"     NEW: {new_title[:60]}")
        print(f"     Top query: {top_clean[:60]}")
        print(f"     Impact: {action['impressions']} imp, pos {action['position']}")

        if not dry_run:
            if title_match:
                old_line = title_match.group(0)
                new_line = f'title: "{new_title}"'
                content = content.replace(old_line, new_line)
            if desc_match:
                old_line = desc_match.group(0)
                new_line = f'description: "{new_desc}"'
                content = content.replace(old_line, new_line)
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
            "top_query": top_clean,
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
