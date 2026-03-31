#!/usr/bin/env python3
"""
Submit all URLs to IndexNow (Bing, Yandex, Seznam, Naver).
Reads sitemaps from dist/ and batches submissions (max 10,000 per request).

Usage:
  python3 scripts/indexnow-submit.py           # dry run
  python3 scripts/indexnow-submit.py --submit   # submit to IndexNow
"""

import os, sys, json, subprocess, xml.etree.ElementTree as ET
from pathlib import Path

KEY = "ddb65220289543b589d6deadc9bcc754"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"

DOMAIN_MAP = {
    "westmount": "https://westmountfundamentals.com",
    "siliconbased": "https://siliconbased.dev",
    "firemaths": "https://firemaths.info",
    "leeroyjenkins": "https://leeroyjenkins.quest",
    "ijustwantto": "https://ijustwantto.live",
    "28grams": "https://28grams.vip",
    "migratingmammals": "https://migratingmammals.com",
    "nookienook": "https://thenookienook.com",
    "bodycount": "https://bodycount.photonbuilder.com",
    "sendnerds": "https://sendnerds.photonbuilder.com",
    "getthebag": "https://getthebag.photonbuilder.com",
    "fixitwithducttape": "https://fixitwithducttape.photonbuilder.com",
    "pleasestartplease": "https://pleasestartplease.photonbuilder.com",
    "justonemoment": "https://justonemoment.photonbuilder.com",
    "papyruspeople": "https://papyruspeople.photonbuilder.com",
    "eeniemeenie": "https://eeniemeenie.photonbuilder.com",
}

DIST = Path(os.path.expanduser("~/Desktop/photonbuilder/dist"))

def get_urls_from_sitemap(sitemap_path):
    """Parse sitemap.xml and extract all URLs."""
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        return [url.find('sm:loc', ns).text for url in root.findall('sm:url', ns) if url.find('sm:loc', ns) is not None]
    except Exception as e:
        print(f"  ⚠️  Error parsing {sitemap_path}: {e}")
        return []

def submit_batch(host, urls):
    """Submit a batch of URLs to IndexNow."""
    payload = {
        "host": host,
        "key": KEY,
        "keyLocation": f"https://{host}/{KEY}.txt",
        "urlList": urls
    }
    
    payload_json = json.dumps(payload)
    cmd = f'/usr/bin/curl -s -o /dev/null -w "%{{http_code}}" -X POST "{INDEXNOW_ENDPOINT}" -H "Content-Type: application/json" -d \'{payload_json}\' --max-time 15'
    
    # Use subprocess to avoid shell escaping issues
    result = subprocess.run(
        ['/usr/bin/curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
         '-X', 'POST', INDEXNOW_ENDPOINT,
         '-H', 'Content-Type: application/json',
         '-d', payload_json,
         '--max-time', '15'],
        capture_output=True, text=True, timeout=20
    )
    return result.stdout.strip().strip('"')

def main():
    submit = "--submit" in sys.argv
    
    if not submit:
        print("🔍 DRY RUN — use --submit to send to IndexNow\n")
    
    total_urls = 0
    total_submitted = 0
    
    for site_name, domain_url in sorted(DOMAIN_MAP.items()):
        host = domain_url.replace("https://", "")
        sitemap_path = DIST / "sites" / site_name / "sitemap.xml"
        
        if not sitemap_path.exists():
            print(f"⚠️  {host} — no sitemap found")
            continue
        
        urls = get_urls_from_sitemap(sitemap_path)
        if not urls:
            print(f"⚠️  {host} — empty sitemap")
            continue
        
        total_urls += len(urls)
        
        if submit:
            # IndexNow accepts max 10,000 URLs per request
            for i in range(0, len(urls), 10000):
                batch = urls[i:i+10000]
                status = submit_batch(host, batch)
                if status in ('200', '202'):
                    print(f"✅ {host:<45} {len(batch):>4} URLs submitted (HTTP {status})")
                    total_submitted += len(batch)
                else:
                    print(f"❌ {host:<45} HTTP {status} — submission failed")
        else:
            print(f"📋 {host:<45} {len(urls):>4} URLs ready")
    
    print(f"\n📊 Total: {total_urls} URLs across {len(DOMAIN_MAP)} domains")
    if submit:
        print(f"✅ Successfully submitted: {total_submitted} URLs to IndexNow")
    else:
        print("   Run with --submit to send to Bing/Yandex/Seznam/Naver")

if __name__ == "__main__":
    main()
