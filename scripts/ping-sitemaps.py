#!/usr/bin/env python3
"""Ping Google with all sitemaps and check accessibility."""
import subprocess, urllib.parse, sys

SITEMAPS = {
    "westmountfundamentals.com": "sites/westmount/sitemap.xml",
    "siliconbased.dev": "sites/siliconbased/sitemap.xml",
    "firemaths.info": "sites/firemaths/sitemap.xml",
    "leeroyjenkins.quest": "sites/leeroyjenkins/sitemap.xml",
    "ijustwantto.live": "sites/ijustwantto/sitemap.xml",
    "28grams.vip": "sites/28grams/sitemap.xml",
    "migratingmammals.com": "sites/migratingmammals/sitemap.xml",
    "thenookienook.com": "sites/nookienook/sitemap.xml",
    "bodycount.photonbuilder.com": "sites/bodycount/sitemap.xml",
    "sendnerds.photonbuilder.com": "sites/sendnerds/sitemap.xml",
    "getthebag.photonbuilder.com": "sites/getthebag/sitemap.xml",
    "fixitwithducttape.photonbuilder.com": "sites/fixitwithducttape/sitemap.xml",
    "pleasestartplease.photonbuilder.com": "sites/pleasestartplease/sitemap.xml",
    "justonemoment.photonbuilder.com": "sites/justonemoment/sitemap.xml",
    "papyruspeople.photonbuilder.com": "sites/papyruspeople/sitemap.xml",
    "eeniemeenie.photonbuilder.com": "sites/eeniemeenie/sitemap.xml",
}

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
    return r.stdout.strip()

total_urls = 0
ok = 0
fail = 0

for domain, path in sorted(SITEMAPS.items()):
    url = f"https://{domain}/{path}"
    
    # Check accessibility
    http_code = run(f'/usr/bin/curl -s -o /dev/null -w "%{{http_code}}" "{url}" --max-time 5')
    
    if http_code == "200":
        # Count URLs
        body = run(f'/usr/bin/curl -s "{url}" --max-time 5')
        count = body.count("<loc>")
        total_urls += count
        
        # Ping Google
        encoded = urllib.parse.quote(url, safe='')
        ping_code = run(f'/usr/bin/curl -s -o /dev/null -w "%{{http_code}}" "https://www.google.com/ping?sitemap={encoded}" --max-time 5')
        
        print(f"✅ {domain:<45} {count:>4} URLs | Google ping: {ping_code}")
        ok += 1
    else:
        print(f"❌ {domain:<45} HTTP {http_code}")
        fail += 1

print(f"\n📊 {ok}/{ok+fail} sitemaps accessible | {total_urls} total URLs pinged to Google")
