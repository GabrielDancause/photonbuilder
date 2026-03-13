#!/usr/bin/env python3
"""
Extract content + metadata from self-contained HTML pages.
Outputs: src/data/{site}/{slug}.html (content only) + src/data/{site}/{slug}.json (metadata)
"""
import re
import json
import sys
import os

def extract(html_path, site, slug):
    html = open(html_path).read()
    
    # Extract metadata
    title_match = re.search(r'<title>(.*?)</title>', html)
    title = title_match.group(1) if title_match else slug
    
    desc_match = re.search(r'<meta\s+name="description"\s+content="(.*?)"', html, re.IGNORECASE)
    description = desc_match.group(1) if desc_match else ''
    
    canonical_match = re.search(r'<link\s+rel="canonical"\s+href="(.*?)"', html, re.IGNORECASE)
    canonical = canonical_match.group(1) if canonical_match else f'https://westmountfundamentals.com/{slug}'
    
    # Extract JSON-LD schemas
    schemas = []
    for m in re.finditer(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.DOTALL):
        try:
            schemas.append(json.loads(m.group(1)))
        except:
            pass
    
    # Extract content: everything between </head><body> ... </body>
    # First, get the body content
    body_match = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL)
    if not body_match:
        print(f"ERROR: No body found in {html_path}")
        return
    
    content = body_match.group(1)
    
    # Strip nav elements
    content = re.sub(r'<nav[^>]*>.*?</nav>', '', content, flags=re.DOTALL)
    
    # Strip header elements (standalone nav-like headers)
    content = re.sub(r'<header[^>]*>.*?</header>', '', content, flags=re.DOTALL)
    
    # Strip footer elements (all types)
    content = re.sub(r'<footer[^>]*>.*?</footer>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div\s+class="footer"[^>]*>.*?</div>\s*</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div\s+class="disclaimer"[^>]*>.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div[^>]*>\s*©.*?(?:westmount|GAB Ventures).*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Strip nav.js references
    content = re.sub(r'<script[^>]*src=["\'][^"\']*nav\.js["\'][^>]*>\s*</script>', '', content)
    
    # Strip GA scripts (template handles this)
    content = re.sub(r'<script[^>]*src=["\'][^"\']*gtag[^"\']*["\'][^>]*>\s*</script>', '', content)
    content = re.sub(r'<script>\s*window\.dataLayer.*?</script>', '', content, flags=re.DOTALL)
    
    # Strip JSON-LD scripts (template handles this)
    content = re.sub(r'<script\s+type="application/ld\+json">.*?</script>', '', content, flags=re.DOTALL)
    
    # Extract page-specific <style> blocks (keep them — they have the page's CSS)
    # These stay in the content
    
    # Clean up excessive whitespace
    content = re.sub(r'\n{3,}', '\n\n', content).strip()
    
    # Write content HTML
    data_dir = f'src/data/{site}'
    os.makedirs(data_dir, exist_ok=True)
    
    with open(f'{data_dir}/{slug}.html', 'w') as f:
        f.write(content)
    
    # Write metadata JSON
    meta = {
        'title': title,
        'description': description,
        'canonical': canonical,
        'schemas': schemas,
    }
    
    with open(f'{data_dir}/{slug}.json', 'w') as f:
        json.dump(meta, f, indent=2)
    
    content_kb = len(content) / 1024
    print(f"✓ {slug}: {content_kb:.1f}KB content, {len(schemas)} schemas")
    return meta

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 extract-content.py <site> <slug1> [slug2] ...")
        sys.exit(1)
    
    site = sys.argv[1]
    for slug in sys.argv[2:]:
        html_path = f'public/sites/{site}/{slug}.html'
        if os.path.exists(html_path):
            extract(html_path, site, slug)
        else:
            print(f"NOT FOUND: {html_path}")
