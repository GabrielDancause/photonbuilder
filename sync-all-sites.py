#!/usr/bin/env python3
"""Sync all site repos to photonbuilder + apply standardized nav."""
import re, glob, os, shutil

SITES = {
    'firemaths': {
        'repo': '/Users/gab/Desktop/firemaths-info',
        'name': 'Fire Maths',
        'links': [('Tools', '/#tools'), ('Studies', '/#studies'), ('Guides', '/#guides')],
        'ga': 'G-G86C7NJG3F',
    },
    'siliconbased': {
        'repo': '/Users/gab/Desktop/siliconbased-dev',
        'name': 'Silicon Based',
        'links': [('Tools', '/#tools'), ('Studies', '/#studies'), ('Guides', '/#guides')],
        'ga': 'G-G86C7NJG3F',
    },
    '28grams': {
        'repo': '/Users/gab/Desktop/28grams-vip',
        'name': '28 Grams',
        'links': [('Tools', '/#tools'), ('Guides', '/#guides'), ('Lists', '/#lists')],
        'ga': 'G-G86C7NJG3F',
    },
    'migratingmammals': {
        'repo': '/Users/gab/Desktop/migratingmammals-com',
        'name': 'Migrating Mammals',
        'links': [('Tools', '/#tools'), ('Guides', '/#guides'), ('Lists', '/#lists')],
        'ga': 'G-G86C7NJG3F',
    },
    'leeroyjenkins': {
        'repo': '/Users/gab/Desktop/leeroyjenkins-quest',
        'name': 'Leeroy Jenkins',
        'links': [('Tools', '/#tools'), ('Guides', '/#guides'), ('Lists', '/#lists')],
        'ga': 'G-G86C7NJG3F',
    },
    'ijustwantto': {
        'repo': '/Users/gab/Desktop/ijustwantto-live',
        'name': 'I Just Want To',
        'links': [('Tools', '/#tools'), ('Guides', '/#guides'), ('Lists', '/#lists')],
        'ga': 'G-G86C7NJG3F',
    },
}

PB_ROOT = '/Users/gab/Desktop/photonbuilder'

def make_nav(cfg):
    links = ''.join(
        f'<a href="{href}" style="color:#8a94a6;text-decoration:none;font-size:0.82rem;font-weight:500;padding:6px 14px;border-radius:6px">{label}</a>'
        for label, href in cfg['links']
    )
    return f'''<nav style="position:sticky;top:0;z-index:1000;background:rgba(6,10,18,0.92);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid rgba(255,255,255,0.06)">
<div style="max-width:1200px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;padding:0 24px;height:48px">
<a href="/" style="font-size:0.9rem;font-weight:700;color:#fff;text-decoration:none;letter-spacing:-0.3px">{cfg['name']}</a>
<div style="display:flex;gap:8px">
{links}
</div>
</div>
</nav>'''

def apply_nav(html, nav_html, ga_id):
    # Strip existing nav
    html = re.sub(r'<nav[\s>].*?</nav>', '', html, flags=re.DOTALL)
    # Strip header
    html = re.sub(r'<header[\s>].*?</header>', '', html, flags=re.DOTALL)
    # Remove nav.js
    html = re.sub(r'<script\s+src=["\'][^"\']*nav\.js["\']></script>\s*', '', html)
    # Insert nav after body
    html = re.sub(r'(<body[^>]*>)', r'\1\n' + nav_html, html, count=1)
    # Ensure GA
    if 'googletagmanager' not in html:
        ga_tag = f'<script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>\n<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{ga_id}");</script>'
        html = re.sub(r'(<head[^>]*>)', r'\1\n' + ga_tag, html, count=1)
    return html

total_synced = 0

for site_id, cfg in SITES.items():
    repo_public = os.path.join(cfg['repo'], 'public')
    dest_dir = os.path.join(PB_ROOT, 'public', 'sites', site_id)
    
    if not os.path.isdir(repo_public):
        print(f"⚠️  {site_id}: repo not found at {cfg['repo']}")
        continue
    
    # Find all HTML files (excluding node_modules, _astro)
    html_files = []
    for root, dirs, files in os.walk(repo_public):
        dirs[:] = [d for d in dirs if d not in ('node_modules', '_astro')]
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))
    
    # Skip Astro index pages that already exist in photonbuilder
    # Only copy content pages (not index.html in subdirs like tools/, guides/, etc.)
    nav_html = make_nav(cfg)
    copied = 0
    
    for src_path in html_files:
        rel_path = os.path.relpath(src_path, repo_public)
        
        # Skip subdirectory index files (tools/index.html etc) - Astro manages those
        if '/' in rel_path and rel_path.endswith('index.html'):
            continue
        
        dest_path = os.path.join(dest_dir, rel_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        # Read, apply nav, write
        with open(src_path, 'r', errors='replace') as fh:
            html = fh.read()
        
        # Skip the root index.html (Astro homepage)
        if rel_path == 'index.html':
            continue
        
        html = apply_nav(html, nav_html, cfg['ga'])
        
        with open(dest_path, 'w') as fh:
            fh.write(html)
        copied += 1
    
    print(f"✅ {site_id}: synced {copied} pages")
    total_synced += copied

print(f"\nTotal: {total_synced} pages synced to photonbuilder")
