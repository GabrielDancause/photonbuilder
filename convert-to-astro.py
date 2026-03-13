#!/usr/bin/env python3
"""Convert static HTML pages to .astro files using SiteLayout."""
import re, os, json, html as html_module

SITE_ID = '28grams'
SRC_DIR = f'public/sites/{SITE_ID}'
DEST_DIR = f'src/pages/sites/{SITE_ID}'

def extract_meta(html_content):
    """Extract title, description, canonical, and JSON-LD from HTML."""
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.DOTALL)
    title = title_match.group(1).strip() if title_match else 'Untitled'
    
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html_content)
    if not desc_match:
        desc_match = re.search(r'<meta\s+content="([^"]*)"\s+name="description"', html_content)
    description = desc_match.group(1) if desc_match else ''
    
    canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', html_content)
    canonical = canonical_match.group(1) if canonical_match else ''
    
    # Extract JSON-LD
    jsonld_match = re.search(r'<script\s+type="application/ld\+json">\s*(.*?)\s*</script>', html_content, re.DOTALL)
    schema = None
    if jsonld_match:
        try:
            schema = json.loads(jsonld_match.group(1))
        except json.JSONDecodeError:
            pass
    
    return title, description, canonical, schema

def extract_body_content(html_content):
    """Extract content between <body> and </body>, stripping nav/header/footer."""
    body_match = re.search(r'<body[^>]*>(.*)</body>', html_content, re.DOTALL)
    if not body_match:
        return ''
    
    content = body_match.group(1)
    
    # Remove injected nav
    content = re.sub(r'<nav[\s>].*?</nav>', '', content, flags=re.DOTALL)
    # Remove header
    content = re.sub(r'<header[\s>].*?</header>', '', content, flags=re.DOTALL)
    # Remove footer (both <footer> tags and <div class="footer">)
    content = re.sub(r'<footer[\s>].*?</footer>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div\s+class="footer"[^>]*>.*?</div>', '', content, flags=re.DOTALL)
    # Remove nav.js
    content = re.sub(r'<script\s+src=["\'][^"\']*nav\.js["\']></script>\s*', '', content)
    
    return content.strip()

def extract_styles(html_content):
    """Extract all <style> blocks from <head>."""
    styles = re.findall(r'<style[^>]*>(.*?)</style>', html_content, re.DOTALL)
    return '\n'.join(styles).strip()

def extract_scripts(body_content):
    """Extract and remove <script> blocks from body content, return (clean_content, scripts)."""
    scripts = []
    
    # Find all script tags in body
    for match in re.finditer(r'<script(?:\s+src="([^"]*)")?[^>]*>(.*?)</script>', body_content, re.DOTALL):
        src = match.group(1)
        script_content = match.group(2).strip()
        if src:
            scripts.append(('src', src))
        elif script_content:
            # Skip GA scripts
            if 'googletagmanager' in script_content or 'gtag' in script_content:
                continue
            scripts.append(('inline', script_content))
    
    # Remove scripts from content
    clean = re.sub(r'<script[^>]*>.*?</script>', '', body_content, flags=re.DOTALL)
    
    return clean.strip(), scripts

def escape_astro(content):
    """Escape curly braces in content that aren't inside script/style tags."""
    # We need to be careful - only escape {} in HTML content, not in scripts
    # Since scripts are already extracted, we can safely escape remaining {}
    # But some content might have legitimate template-like syntax
    # For safety, replace lone { } that look like content (not JSX)
    
    # Replace { and } that are NOT part of HTML attributes
    # This is a simplified approach - might need manual fixes
    lines = content.split('\n')
    result = []
    for line in lines:
        # Don't escape inside style attributes or event handlers
        if 'style=' not in line and 'onclick=' not in line:
            # Escape standalone braces in text content
            line = re.sub(r'(?<!=")(?<!=\')(\{)(?![{%])', r"{'{'}", line)
            line = re.sub(r'(?<![%}])(\})(?!")', r"{'}'}", line)
        result.append(line)
    
    return '\n'.join(result)

def build_astro(title, description, canonical, schema, styles, content, scripts):
    """Build the .astro file."""
    # Frontmatter
    frontmatter = f'''---
import SiteLayout from '../../../layouts/SiteLayout.astro';
'''
    
    if schema:
        # Format schema as JS object
        schema_str = json.dumps(schema, indent=2)
        frontmatter += f'\nconst schema = {schema_str};\n'
    
    frontmatter += '---\n'
    
    # Escape quotes in title/description for attributes
    title_escaped = title.replace('"', '&quot;')
    desc_escaped = description.replace('"', '&quot;')
    
    # SiteLayout wrapper
    schema_prop = ' schema={schema}' if schema else ''
    layout_open = f'''
<SiteLayout
  site="{SITE_ID}"
  title="{title_escaped}"
  description="{desc_escaped}"
  canonical="{canonical}"{schema_prop}
>'''
    
    # Style block
    style_block = f'\n  <style>\n{styles}\n  </style>\n' if styles else ''
    
    # Script blocks
    script_blocks = ''
    for stype, sval in scripts:
        if stype == 'src':
            script_blocks += f'\n  <script is:inline src="{sval}"></script>'
        else:
            script_blocks += f'\n  <script is:inline>\n{sval}\n  </script>'
    
    layout_close = '\n</SiteLayout>\n'
    
    return frontmatter + layout_open + style_block + '\n' + content + script_blocks + layout_close

# Main
os.makedirs(DEST_DIR, exist_ok=True)

html_files = [f for f in os.listdir(SRC_DIR) if f.endswith('.html') and f != 'index.html']
print(f"Converting {len(html_files)} pages from {SITE_ID}...")

converted = 0
errors = []

for filename in sorted(html_files):
    src_path = os.path.join(SRC_DIR, filename)
    slug = filename.replace('.html', '')
    dest_path = os.path.join(DEST_DIR, f'{slug}.astro')
    
    try:
        with open(src_path, 'r', errors='replace') as f:
            html_content = f.read()
        
        title, description, canonical, schema = extract_meta(html_content)
        body_content = extract_body_content(html_content)
        styles = extract_styles(html_content)
        clean_content, scripts = extract_scripts(body_content)
        
        astro_content = build_astro(title, description, canonical, schema, styles, clean_content, scripts)
        
        with open(dest_path, 'w') as f:
            f.write(astro_content)
        
        converted += 1
        print(f"  ✅ {slug}")
        
    except Exception as e:
        errors.append((filename, str(e)))
        print(f"  ❌ {slug}: {e}")

print(f"\nConverted: {converted}/{len(html_files)}")
if errors:
    print(f"Errors: {len(errors)}")
    for name, err in errors:
        print(f"  - {name}: {err}")
