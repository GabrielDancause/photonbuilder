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
    "montrealjobs": "montrealjobs.ca",
    "nookienook": "nookienook.com",
    "siliconbased": "siliconbased.dev",
    "westmount": "westmountfundamentals.com",
    "mathtools": "photonbuilder.com",
    "misc": "photonbuilder.com",
    "justonemoment": "photonbuilder.com",
    "bodycount": "health.example.com",
}

TODAY = datetime.now().strftime("%Y-%m-%d")


def generate_sitemap(site_id):
    site_dir = SITES_DIR / site_id
    domain = SITE_DOMAINS.get(site_id)
    if not domain or not site_dir.is_dir():
        return 0

    pages = sorted(site_dir.glob("*.astro"))
    urls = []

    for page in pages:
        slug = page.stem
        if slug == "index":
            urls.append(f"https://{domain}/")
        else:
            urls.append(f"https://{domain}/{slug}")

    # Build XML
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for url in urls:
        xml_lines.append(f"  <url>")
        xml_lines.append(f"    <loc>{url}</loc>")
        xml_lines.append(f"    <lastmod>{TODAY}</lastmod>")
        xml_lines.append(f"  </url>")

    xml_lines.append("</urlset>")
    xml_lines.append("")

    # Write
    output_dir = PUBLIC_DIR / site_id
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "sitemap.xml"
    output_path.write_text("\n".join(xml_lines))

    return len(urls)


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
