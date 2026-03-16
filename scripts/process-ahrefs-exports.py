#!/usr/bin/env python3
"""
Process Ahrefs CSV exports into clean per-site keyword JSONs.
Reads from workspace/ahrefs-exports/ (with manifest.json),
outputs to src/data/seo/{site}/keywords.json

Usage: python3 scripts/process-ahrefs-exports.py
"""

import csv, json, os, sys
from pathlib import Path
from datetime import datetime

EXPORTS_DIR = os.path.expanduser("~/.openclaw/workspace/ahrefs-exports")
OUTPUT_DIR = "src/data/seo"
PAGES_DIR = "src/pages/sites"

def load_manifest():
    manifest_path = os.path.join(EXPORTS_DIR, "manifest.json")
    if not os.path.exists(manifest_path):
        print("ERROR: No manifest.json found")
        sys.exit(1)
    with open(manifest_path) as f:
        return json.load(f)

def get_existing_pages(site):
    """Get list of existing page slugs for a site"""
    site_dir = os.path.join(PAGES_DIR, site)
    if not os.path.exists(site_dir):
        return set()
    return {f.replace('.astro', '') for f in os.listdir(site_dir) if f.endswith('.astro')}

def slugify(keyword):
    """Convert keyword to likely page slug"""
    return keyword.lower().replace('?', '').replace("'", '').replace('&', 'and').replace(' ', '-').replace('/', '-').strip('-')

def parse_csv(filepath):
    """Parse an Ahrefs CSV export into keyword dicts"""
    keywords = []
    try:
        with open(filepath, encoding='utf-8-sig') as f:
            # Skip the # column issue
            reader = csv.DictReader(f)
            for row in reader:
                kw = row.get('Keyword', '').strip()
                if not kw:
                    continue
                
                try:
                    kd = int(row.get('Difficulty', 0) or 0)
                except (ValueError, TypeError):
                    kd = 999
                
                try:
                    vol = int(row.get('Volume', 0) or 0)
                except (ValueError, TypeError):
                    vol = 0
                
                try:
                    cpc = float(row.get('CPC', 0) or 0)
                except (ValueError, TypeError):
                    cpc = 0
                
                intents = row.get('Intents', '')
                
                keywords.append({
                    'keyword': kw,
                    'kd': kd,
                    'volume': vol,
                    'cpc': cpc,
                    'intents': intents,
                })
    except Exception as e:
        print(f"  WARNING: Failed to parse {filepath}: {e}")
    
    return keywords

def main():
    manifest = load_manifest()
    files = manifest.get('files', {})
    
    # Group files by domain
    domain_files = {}
    for filename, meta in files.items():
        domain = meta.get('domain', 'unknown')
        if domain not in domain_files:
            domain_files[domain] = []
        domain_files[domain].append((filename, meta))
    
    print(f"Found {len(files)} exports across {len(domain_files)} domains")
    print()
    
    for domain, file_list in sorted(domain_files.items()):
        print(f"=== {domain} ({len(file_list)} files) ===")
        
        # Parse all CSVs for this domain
        all_keywords = {}
        topics = set()
        
        for filename, meta in file_list:
            filepath = os.path.join(EXPORTS_DIR, filename)
            if not os.path.exists(filepath):
                print(f"  SKIP: {filename} (not found)")
                continue
            
            topic = meta.get('topic', 'unknown')
            topics.add(topic)
            
            keywords = parse_csv(filepath)
            for kw in keywords:
                key = kw['keyword'].lower()
                # Deduplicate: keep the one with higher volume (fresher data)
                if key not in all_keywords or kw['volume'] > all_keywords[key]['volume']:
                    kw['topic'] = topic
                    all_keywords[key] = kw
        
        # Get existing pages for this site
        existing = get_existing_pages(domain)
        
        # Mark coverage status
        keywords_list = []
        covered = 0
        for kw_data in all_keywords.values():
            slug = slugify(kw_data['keyword'])
            if slug in existing or any(slug in page for page in existing):
                kw_data['status'] = 'covered'
                covered += 1
            else:
                kw_data['status'] = 'uncovered'
            keywords_list.append(kw_data)
        
        # Sort by volume desc
        keywords_list.sort(key=lambda x: (-x['volume'], x['kd']))
        
        # Write output
        site_dir = os.path.join(OUTPUT_DIR, domain)
        os.makedirs(site_dir, exist_ok=True)
        
        output = {
            'exported': datetime.now().strftime('%Y-%m-%d'),
            'source': 'Ahrefs',
            'domain': domain,
            'topics': sorted(topics),
            'total_keywords': len(keywords_list),
            'covered': covered,
            'uncovered': len(keywords_list) - covered,
            'keywords': keywords_list
        }
        
        outpath = os.path.join(site_dir, 'keywords.json')
        with open(outpath, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"  Keywords: {len(keywords_list)} ({covered} covered, {len(keywords_list)-covered} uncovered)")
        print(f"  Topics: {', '.join(sorted(topics))}")
        print(f"  Output: {outpath}")
        
        # Show top uncovered opportunities
        uncovered_kws = [k for k in keywords_list if k['status'] == 'uncovered' and k['kd'] <= 10 and k['volume'] >= 500]
        if uncovered_kws:
            print(f"  Top uncovered (KD≤10, Vol≥500):")
            for k in uncovered_kws[:5]:
                print(f"    KD:{k['kd']:>3}  Vol:{k['volume']:>7}  {k['keyword']}")
        print()

    print("Done!")

if __name__ == '__main__':
    main()
