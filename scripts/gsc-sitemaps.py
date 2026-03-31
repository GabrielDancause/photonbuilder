#!/usr/bin/env python3
"""
Check and submit sitemaps to Google Search Console for all domains.
Uses the existing OAuth token from the SEO pipeline.

Usage:
  python3 scripts/gsc-sitemaps.py           # check status
  python3 scripts/gsc-sitemaps.py --submit   # submit missing sitemaps
"""

import os, sys, pickle
from pathlib import Path

# Google API
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN_PATH = Path(os.path.expanduser("~/Desktop/photonbuilder/data/seo/google_token.pickle"))

DOMAINS = {
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


def get_creds():
    with open(TOKEN_PATH, 'rb') as f:
        creds = pickle.load(f)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_PATH, 'wb') as f:
            pickle.dump(creds, f)
    return creds


def main():
    submit = "--submit" in sys.argv
    creds = get_creds()
    service = build('searchconsole', 'v1', credentials=creds)
    
    # 1. List all verified sites
    print("📋 Checking verified sites in GSC...\n")
    try:
        site_list = service.sites().list().execute()
        verified = {}
        for s in site_list.get('siteEntry', []):
            url = s['siteUrl']
            level = s.get('permissionLevel', '?')
            verified[url] = level
            # Check both sc-domain: and https:// variants
    except Exception as e:
        print(f"❌ Error listing sites: {e}")
        return
    
    print(f"Found {len(verified)} verified properties:\n")
    for url, level in sorted(verified.items()):
        print(f"  {level:<15} {url}")
    
    print("\n" + "="*60 + "\n")
    
    # 2. Check sitemap status for each domain
    for domain, sitemap_path in sorted(DOMAINS.items()):
        sitemap_url = f"https://{domain}/{sitemap_path}"
        
        # Try both property formats
        site_url = None
        for fmt in [f"sc-domain:{domain}", f"https://{domain}/", f"http://{domain}/"]:
            if fmt in verified:
                site_url = fmt
                break
        
        # For subdomains, also check parent domain
        if not site_url and '.photonbuilder.com' in domain:
            for fmt in ["sc-domain:photonbuilder.com", "https://photonbuilder.com/"]:
                if fmt in verified:
                    site_url = fmt
                    break
        
        if not site_url:
            print(f"⚠️  {domain} — NOT VERIFIED in GSC")
            continue
        
        # Check existing sitemaps
        try:
            sitemaps = service.sitemaps().list(siteUrl=site_url).execute()
            existing = [s['path'] for s in sitemaps.get('sitemap', [])]
            
            if sitemap_url in existing:
                sm = next(s for s in sitemaps['sitemap'] if s['path'] == sitemap_url)
                status = sm.get('lastDownloadDate', 'never')
                errors = sm.get('errors', 0)
                warnings = sm.get('warnings', 0)
                submitted = sm.get('lastSubmitted', '?')
                contents = sm.get('contents', [])
                indexed = sum(c.get('indexed', 0) for c in contents)
                total = sum(c.get('submitted', 0) for c in contents)
                print(f"✅ {domain}")
                print(f"   Sitemap: {sitemap_url}")
                print(f"   URLs: {indexed}/{total} indexed | Errors: {errors} | Warnings: {warnings}")
                print(f"   Last download: {status}")
            else:
                if submit:
                    try:
                        service.sitemaps().submit(siteUrl=site_url, feedpath=sitemap_url).execute()
                        print(f"📤 {domain} — SUBMITTED: {sitemap_url}")
                    except Exception as e:
                        print(f"❌ {domain} — Submit failed: {e}")
                else:
                    print(f"📋 {domain} — NOT SUBMITTED (use --submit)")
                    print(f"   Would submit: {sitemap_url}")
                    if existing:
                        print(f"   Existing sitemaps: {existing}")
        except Exception as e:
            print(f"❌ {domain} — Error: {e}")
        
        print()


if __name__ == "__main__":
    main()
