#!/usr/bin/env python3
"""
Convert pSEO static HTML pages to Astro dynamic routes.

For each category (colors, regex, cron, chmod, security-headers):
1. Extract body content (between nav/header and footer)
2. Extract page-specific <style> and <script> blocks
3. Store metadata (title, description) in a JSON index
4. Create one Astro dynamic route [...slug].astro per category
5. Delete the static HTML files
"""

import re
import os
import json
import glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(BASE, "public/sites/siliconbased")
PAGES = os.path.join(BASE, "src/pages/sites/siliconbased")
DATA = os.path.join(BASE, "src/data/pseo")


def extract_page_content(html):
    """Extract the main content, styles, and scripts from a full HTML page."""
    
    # Extract title
    title_m = re.search(r'<title>(.*?)</title>', html)
    title = title_m.group(1) if title_m else ''
    
    # Extract description
    desc_m = re.search(r'<meta name="description" content="(.*?)"', html)
    description = desc_m.group(1) if desc_m else ''
    
    # Extract schema.org JSON-LD
    schema_m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    schema = schema_m.group(1).strip() if schema_m else None
    
    # Find body content - between </style> or </head> and <footer> or </body>
    # Strategy: find the main content container
    
    # Remove everything before the body content
    # Most pages have: <body> ... <header/nav> ... <main content> ... <footer> ... </body>
    
    # Try to find content after header/nav closes
    body_start = None
    for pattern in [
        r'</header>\s*\n',
        r'</nav>\s*\n', 
        r'<body[^>]*>\s*\n',
    ]:
        m = re.search(pattern, html)
        if m:
            body_start = m.end()
            break
    
    if body_start is None:
        # Fallback: after closing </style> tag  
        m = re.search(r'</style>\s*</head>\s*<body[^>]*>', html, re.DOTALL)
        if m:
            body_start = m.end()
        else:
            body_start = 0
    
    # Find footer
    body_end = None
    for pattern in [
        r'\s*<footer',
        r'\s*</body>',
    ]:
        m = re.search(pattern, html[body_start:])
        if m:
            body_end = body_start + m.start()
            break
    
    if body_end is None:
        body_end = len(html)
    
    body_content = html[body_start:body_end].strip()
    
    # Extract <style> blocks from the full page (page-specific CSS)
    styles = []
    for m in re.finditer(r'<style[^>]*>(.*?)</style>', html, re.DOTALL):
        css = m.group(1).strip()
        # Skip if it's just :root vars (SiteLayout handles those)
        if css and not re.match(r'^\s*:root\s*\{[^}]*\}\s*$', css):
            styles.append(css)
    
    # Extract <script> blocks from body (interactive features)
    scripts = re.findall(r'<script(?:\s[^>]*)?>.*?</script>', html[body_start:], re.DOTALL)
    # Filter out GA scripts and JSON-LD
    scripts = [s for s in scripts if 'gtag' not in s and 'application/ld+json' not in s]
    
    return {
        'title': title,
        'description': description,
        'schema': schema,
        'body': body_content,
        'styles': styles,
        'scripts': scripts,
    }


def process_category(category, subdir):
    """Process all pages in a pSEO category."""
    html_dir = os.path.join(PUBLIC, subdir)
    files = sorted(glob.glob(os.path.join(html_dir, "*.html")))
    
    if not files:
        print(f"  No files found in {html_dir}")
        return []
    
    # Create data directory for this category
    cat_data_dir = os.path.join(DATA, category)
    os.makedirs(cat_data_dir, exist_ok=True)
    
    index = []
    
    for filepath in files:
        slug = os.path.basename(filepath).replace('.html', '')
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        page = extract_page_content(html)
        
        # Store the body content as a separate file
        content_file = os.path.join(cat_data_dir, f"{slug}.html")
        
        # Combine body + scripts
        full_body = page['body']
        for script in page['scripts']:
            full_body += '\n' + script
        
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(full_body)
        
        # Store styles
        if page['styles']:
            style_file = os.path.join(cat_data_dir, f"{slug}.css")
            with open(style_file, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(page['styles']))
        
        index.append({
            'slug': slug,
            'title': page['title'],
            'description': page['description'],
        })
    
    # Write index
    with open(os.path.join(cat_data_dir, '_index.json'), 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)
    
    return index


def create_astro_route(category, subdir):
    """Create the Astro dynamic route file for a category."""
    route_dir = os.path.join(PAGES, subdir)
    os.makedirs(route_dir, exist_ok=True)
    
    route_file = os.path.join(route_dir, "[slug].astro")
    
    content = f'''---
import SiteLayout from '../../../../layouts/SiteLayout.astro';
import fs from 'node:fs';
import path from 'node:path';

export async function getStaticPaths() {{
  const indexPath = path.join(process.cwd(), 'src/data/pseo/{category}/_index.json');
  const index = JSON.parse(fs.readFileSync(indexPath, 'utf-8'));
  return index.map((item: any) => ({{
    params: {{ slug: item.slug }},
    props: {{ title: item.title, description: item.description }},
  }}));
}}

const {{ slug }} = Astro.params;
const {{ title, description }} = Astro.props;

const contentPath = path.join(process.cwd(), 'src/data/pseo/{category}/' + slug + '.html');
const htmlContent = fs.readFileSync(contentPath, 'utf-8');

const cssPath = path.join(process.cwd(), 'src/data/pseo/{category}/' + slug + '.css');
let cssContent = '';
try {{ cssContent = fs.readFileSync(cssPath, 'utf-8'); }} catch {{}}
---

<SiteLayout
  site="siliconbased"
  title={{title}}
  description={{description}}
  canonical={{`https://siliconbased.dev/{subdir}/${{slug}}`}}
>
  <Fragment set:html={{htmlContent}} />
  {{cssContent && <style is:inline set:html={{cssContent}} />}}
</SiteLayout>
'''
    
    with open(route_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Created {route_file}")


def main():
    os.makedirs(DATA, exist_ok=True)
    
    categories = [
        ('colors', 'colors'),
        ('regex', 'regex'),
        ('cron', 'cron'),
        ('chmod', 'chmod'),
        ('security-headers', 'security-headers'),
    ]
    
    for category, subdir in categories:
        print(f"Processing {category}...")
        index = process_category(category, subdir)
        print(f"  Extracted {len(index)} pages")
        create_astro_route(category, subdir)
    
    print(f"\nDone! Data stored in src/data/pseo/")
    print("Static HTML files NOT yet deleted — verify build first!")


if __name__ == "__main__":
    main()
