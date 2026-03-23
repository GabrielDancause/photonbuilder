#!/usr/bin/env python3
"""
Auto-generate sitemap.xml for each site from the file system.
Reads all .astro pages in src/pages/sites/<site>/ and generates
public/sites/<site>/sitemap.xml with correct domain URLs.

Run after build or as part of CI:
  python3 scripts/generate-sitemaps.py
"""

import os
import json
from pathlib import Path
from datetime import datetime

PHOTON_DIR = Path(__file__).parent.parent
SITES_DIR = PHOTON_DIR / "src" / "pages" / "sites"
PUBLIC_DIR = PHOTON_DIR / "public" / "sites"
CONFIG_PATH = PHOTON_DIR / "src" / "config" / "sites.ts"

# Domain mapping (must match sites.ts)
SITE_DOMAINS = {
    "28grams": "28grams.vip",
    "firemaths": "firemaths.info",
    "ijustwantto": "ijustwantto.live",
    "leeroyjenkins": "leeroyjenkins.quest",
    "migratingmammals": "migratingmammals.com",
    "nookienook": "thenookienook.com",
    "siliconbased": "siliconbased.dev",
    "westmount": "westmountfundamentals.com",
    "bodycount": "bodycount.photonbuilder.com",
    "sendnerds": "sendnerds.photonbuilder.com",
    "justonemoment": "justonemoment.photonbuilder.com",
    "getthebag": "getthebag.photonbuilder.com",
    "fixitwithducttape": "fixitwithducttape.photonbuilder.com",
    "papyruspeople": "papyruspeople.photonbuilder.com",
    "eeniemeenie": "eeniemeenie.photonbuilder.com",
    "pleasestartplease": "pleasestartplease.photonbuilder.com",
}

SUB_SITES = {"bodycount", "sendnerds", "justonemoment", "getthebag",
             "fixitwithducttape", "papyruspeople", "eeniemeenie", "pleasestartplease"}

TODAY = datetime.now().strftime("%Y-%m-%d")


def _collect_dynamic_pages(site_id, domain):
    """Collect URLs from JSON-driven dynamic routes (IV & prospect pages)."""
    data_dir = PHOTON_DIR / "src" / "data"
    page_data = []

    for kind in ("iv", "prospect"):
        json_dir = data_dir / kind
        if not json_dir.is_dir():
            continue
        for json_file in sorted(json_dir.glob("*.json")):
            try:
                data = json.loads(json_file.read_text())
            except (json.JSONDecodeError, OSError):
                continue
            slug = data.get("slug")
            if not slug:
                continue
            mtime = datetime.fromtimestamp(json_file.stat().st_mtime).strftime("%Y-%m-%d")
            page_data.append((f"https://{domain}/{slug}", mtime))

    return page_data


def generate_sitemap(site_id):
    site_dir = SITES_DIR / site_id
    domain = SITE_DOMAINS.get(site_id)
    if not domain or not site_dir.is_dir():
        return 0

    # Recursively find all .astro pages, skip dynamic route templates
    pages = sorted(site_dir.rglob("*.astro"))

    page_data = []  # (url, lastmod)
    for page in pages:
        stem = page.stem
        # Skip dynamic route files like [...ivslug].astro
        if stem.startswith("["):
            continue

        # Use file's actual modification time for lastmod
        mtime = datetime.fromtimestamp(page.stat().st_mtime).strftime("%Y-%m-%d")

        # Build the URL path from the file's relative position
        rel = page.relative_to(site_dir).with_suffix("")
        parts = list(rel.parts)

        if parts[-1] == "index":
            # index.astro → directory URL with trailing slash
            parts.pop()
            url_path = "/".join(parts)
            page_data.append((f"https://{domain}/{url_path}{'/' if url_path else ''}", mtime))
        else:
            url_path = "/".join(parts)
            page_data.append((f"https://{domain}/{url_path}", mtime))

    # Add dynamic pages from JSON data (IV & prospect for westmount)
    if site_id == "westmount":
        page_data.extend(_collect_dynamic_pages(site_id, domain))

    # Deduplicate by URL (keep first occurrence)
    seen = set()
    unique_data = []
    for url, lastmod in page_data:
        if url not in seen:
            seen.add(url)
            unique_data.append((url, lastmod))
    page_data = sorted(unique_data, key=lambda x: x[0])

    # Build XML
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for url, lastmod in page_data:
        xml_lines.append(f"  <url>")
        xml_lines.append(f"    <loc>{url}</loc>")
        xml_lines.append(f"    <lastmod>{lastmod}</lastmod>")
        xml_lines.append(f"  </url>")

    xml_lines.append("</urlset>")
    xml_lines.append("")

    # Write
    output_dir = PUBLIC_DIR / site_id
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "sitemap.xml"
    output_path.write_text("\n".join(xml_lines))

    return len(page_data)


def generate_robots_txt(site_id):
    """Generate robots.txt with sitemap reference."""
    domain = SITE_DOMAINS.get(site_id)
    if not domain:
        return

    output_dir = PUBLIC_DIR / site_id
    output_dir.mkdir(parents=True, exist_ok=True)
    robots_path = output_dir / "robots.txt"
    robots_path.write_text(
        f"User-agent: *\n"
        f"Allow: /\n"
        f"\n"
        f"Sitemap: https://{domain}/sitemap.xml\n"
    )


def main():
    total_urls = 0
    for site_dir in sorted(SITES_DIR.iterdir()):
        if not site_dir.is_dir():
            continue
        site_id = site_dir.name
        count = generate_sitemap(site_id)
        if count:
            generate_robots_txt(site_id)
            print(f"  {site_id}: {count} URLs")
            total_urls += count

    print(f"\nTotal: {total_urls} URLs across {len(SITE_DOMAINS)} sites")


if __name__ == "__main__":
    main()
