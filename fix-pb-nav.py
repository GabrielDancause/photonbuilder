#!/usr/bin/env python3
"""Apply standardized nav to PhotonBuilder blog/tool pages."""
import re, glob, os

NAV_HTML = '''<nav style="position:sticky;top:0;z-index:1000;background:rgba(6,10,18,0.92);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid rgba(255,255,255,0.06)">
<div style="max-width:1200px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;padding:0 24px;height:48px">
<a href="/" style="font-size:0.9rem;font-weight:700;color:#fff;text-decoration:none;letter-spacing:-0.3px">Photon Builder</a>
<div style="display:flex;gap:8px">
<a href="/#tools" style="color:#8a94a6;text-decoration:none;font-size:0.82rem;font-weight:500;padding:6px 14px;border-radius:6px">Tools</a>
<a href="/#guides" style="color:#8a94a6;text-decoration:none;font-size:0.82rem;font-weight:500;padding:6px 14px;border-radius:6px">Guides</a>
<a href="/#lists" style="color:#8a94a6;text-decoration:none;font-size:0.82rem;font-weight:500;padding:6px 14px;border-radius:6px">Lists</a>
</div>
</div>
</nav>'''

GA_TAG = '''<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-G86C7NJG3F"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-G86C7NJG3F');</script>'''

files = glob.glob('public/*.html')
print(f"Found {len(files)} files")

for f in sorted(files):
    name = os.path.basename(f)
    with open(f, 'r') as fh:
        html = fh.read()

    original = html

    # 1. Strip existing <nav>...</nav> blocks (inline nav)
    html = re.sub(r'<nav[\s>].*?</nav>', '', html, flags=re.DOTALL)

    # 2. Strip existing <header>...</header> blocks
    html = re.sub(r'<header[\s>].*?</header>', '', html, flags=re.DOTALL)

    # 3. Remove any existing nav.js script tags
    html = re.sub(r'<script\s+src=["\']/?nav\.js["\']></script>\s*', '', html)

    # 4. Insert standardized nav right after <body...>
    html = re.sub(r'(<body[^>]*>)', r'\1\n' + NAV_HTML, html, count=1)

    # 5. Ensure GA tag exists (add after <head> if missing)
    if 'G-G86C7NJG3F' not in html:
        html = re.sub(r'(<head[^>]*>)', r'\1\n' + GA_TAG, html, count=1)

    if html != original:
        with open(f, 'w') as fh:
            fh.write(html)
        print(f"  ✅ {name}")
    else:
        print(f"  ⏭️  {name} (no changes)")

print("Done!")
