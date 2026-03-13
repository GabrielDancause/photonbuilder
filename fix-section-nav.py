#!/usr/bin/env python3
"""Apply standardized nav to section index pages (tools/, guides/, lists/, studies/)."""
import re, os

SITES = {
    'firemaths': {'name': 'Fire Maths', 'links': [('Tools', '/#tools'), ('Studies', '/#studies'), ('Guides', '/#guides')], 'ga': 'G-G86C7NJG3F'},
    'siliconbased': {'name': 'Silicon Based', 'links': [('Tools', '/#tools'), ('Studies', '/#studies'), ('Guides', '/#guides')], 'ga': 'G-G86C7NJG3F'},
    '28grams': {'name': '28 Grams', 'links': [('Tools', '/#tools'), ('Guides', '/#guides'), ('Lists', '/#lists')], 'ga': 'G-G86C7NJG3F'},
    'migratingmammals': {'name': 'Migrating Mammals', 'links': [('Tools', '/#tools'), ('Guides', '/#guides'), ('Lists', '/#lists')], 'ga': 'G-G86C7NJG3F'},
    'leeroyjenkins': {'name': 'Leeroy Jenkins', 'links': [('Tools', '/#tools'), ('Guides', '/#guides'), ('Lists', '/#lists')], 'ga': 'G-G86C7NJG3F'},
    'ijustwantto': {'name': 'I Just Want To', 'links': [('Tools', '/#tools'), ('Guides', '/#guides'), ('Lists', '/#lists')], 'ga': 'G-G86C7NJG3F'},
    'westmount': {'name': 'Westmount Fundamentals', 'links': [('Studies', '/#studies'), ('Tools', '/#tools'), ('Guides', '/#guides'), ('Lists', '/#lists')], 'ga': 'G-VYF72NSC1Q'},
    'hpv-research': {'name': 'HPV Research', 'links': [('Studies', '/#studies'), ('Tools', '/#tools'), ('Guides', '/#guides')], 'ga': 'G-G86C7NJG3F'},
    'montrealjobs': {'name': 'Montreal Jobs', 'links': [('Market', '/#market'), ('Jobs', '/#jobs'), ('Skills', '/#skills')], 'ga': 'G-G86C7NJG3F'},
}

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

fixed = 0
for root, dirs, files in os.walk('public/sites'):
    for f in files:
        if f != 'index.html':
            continue
        path = os.path.join(root, f)
        # Determine site
        rel = os.path.relpath(path, 'public/sites')
        site_id = rel.split('/')[0]
        
        if site_id not in SITES:
            continue
        
        with open(path, 'r') as fh:
            html = fh.read()
        
        if '<nav' in html:
            continue  # already has nav
        
        cfg = SITES[site_id]
        nav_html = make_nav(cfg)
        
        # Insert after <body>
        new_html = re.sub(r'(<body[^>]*>)', r'\1\n' + nav_html, html, count=1)
        
        if new_html != html:
            with open(path, 'w') as fh:
                fh.write(new_html)
            print(f"  ✅ {rel}")
            fixed += 1

print(f"\nFixed {fixed} section pages")
