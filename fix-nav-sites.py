#!/usr/bin/env python3
"""Apply standardized nav to montrealjobs and hpv-research pages."""
import re, glob, os

SITES = {
    'hpv-research': {
        'name': 'HPV Research',
        'accent': '#10b981',
        'links': [
            ('Studies', '/#studies'),
            ('Tools', '/#tools'),
            ('Guides', '/#guides'),
        ],
        'ga': 'G-G86C7NJG3F',
    },
    'montrealjobs': {
        'name': 'Montreal Jobs',
        'accent': '#3B82F6',
        'links': [
            ('Market', '/#market'),
            ('Jobs', '/#jobs'),
            ('Skills', '/#skills'),
        ],
        'ga': 'G-G86C7NJG3F',
    },
}

GA_TEMPLATE = '''<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id={ga}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{ga}');</script>'''

def make_nav(site_cfg):
    links = ''.join(
        f'<a href="{href}" style="color:#8a94a6;text-decoration:none;font-size:0.82rem;font-weight:500;padding:6px 14px;border-radius:6px">{label}</a>'
        for label, href in site_cfg['links']
    )
    return f'''<nav style="position:sticky;top:0;z-index:1000;background:rgba(6,10,18,0.92);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid rgba(255,255,255,0.06)">
<div style="max-width:1200px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;padding:0 24px;height:48px">
<a href="/" style="font-size:0.9rem;font-weight:700;color:#fff;text-decoration:none;letter-spacing:-0.3px">{site_cfg['name']}</a>
<div style="display:flex;gap:8px">
{links}
</div>
</div>
</nav>'''

for site_id, cfg in SITES.items():
    files = glob.glob(f'public/sites/{site_id}/**/*.html', recursive=True)
    print(f"\n{cfg['name']}: {len(files)} files")
    
    nav_html = make_nav(cfg)
    
    for f in sorted(files):
        name = os.path.relpath(f, f'public/sites/{site_id}')
        with open(f, 'r') as fh:
            html = fh.read()
        
        original = html
        
        # Strip existing nav
        html = re.sub(r'<nav[\s>].*?</nav>', '', html, flags=re.DOTALL)
        
        # Strip existing header
        html = re.sub(r'<header[\s>].*?</header>', '', html, flags=re.DOTALL)
        
        # Remove nav.js references
        html = re.sub(r'<script\s+src=["\'][^"\']*nav\.js["\']></script>\s*', '', html)
        
        # Insert nav after <body>
        html = re.sub(r'(<body[^>]*>)', r'\1\n' + nav_html, html, count=1)
        
        # Ensure GA
        if 'googletagmanager' not in html:
            ga_tag = GA_TEMPLATE.format(ga=cfg['ga'])
            html = re.sub(r'(<head[^>]*>)', r'\1\n' + ga_tag, html, count=1)
        
        if html != original:
            with open(f, 'w') as fh:
                fh.write(html)
            print(f"  ✅ {name}")
        else:
            print(f"  ⏭️  {name} (no changes)")

print("\nDone!")
