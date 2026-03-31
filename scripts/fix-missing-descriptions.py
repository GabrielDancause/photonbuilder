#!/usr/bin/env python3
"""Generate proper meta descriptions for pages missing them or with short/duplicate-of-title descriptions."""

import os
import re
import html
from pathlib import Path

SITES_DIR = Path(__file__).resolve().parent.parent / "src" / "pages" / "sites"

def clean_html(text):
    """Remove HTML tags and decode entities."""
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_title(content):
    """Extract page title from content."""
    # Try meta.title
    m = re.search(r'title\s*:\s*["\']([^"\']+)["\']', content)
    if m:
        return m.group(1)
    # Try <h1>
    m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    if m:
        return clean_html(m.group(1))
    return None

def extract_first_paragraph(content):
    """Extract first meaningful paragraph from page content."""
    # Find content after the frontmatter
    fm_end = content.find('---', content.find('---') + 3)
    if fm_end == -1:
        return None
    body = content[fm_end + 3:]
    
    # Skip style/script tags
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL)
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    
    # Find paragraphs
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', body, re.DOTALL)
    for p in paragraphs:
        text = clean_html(p)
        # Skip very short paragraphs, navigation text, placeholders, and JS expressions
        if (len(text) > 50 and 
            not text.startswith('©') and 
            'cookie' not in text.lower() and
            '{' not in text and
            'paragraph 1 of section' not in text.lower() and
            not text.startswith('This is paragraph')):
            return text
    
    # Try subtitle
    m = re.search(r'class="subtitle[^"]*"[^>]*>(.*?)</', body, re.DOTALL)
    if m:
        return clean_html(m.group(1))
    
    return None

def generate_description(title, first_para):
    """Generate a ~150 char description from title and first paragraph."""
    if not title:
        return None
    
    if first_para:
        # Try to use the first paragraph, truncated to ~155 chars
        if len(first_para) <= 160:
            return first_para
        # Truncate at sentence or word boundary
        truncated = first_para[:157]
        # Try to end at a sentence
        last_period = truncated.rfind('.')
        if last_period > 80:
            return truncated[:last_period + 1]
        # End at word boundary
        last_space = truncated.rfind(' ')
        if last_space > 80:
            return truncated[:last_space] + '...'
        return truncated + '...'
    
    return None

def get_description_from_schema(content):
    """Try to get a description from the schema object."""
    descs = re.findall(r'"description"\s*:\s*"([^"]{50,})"', content)
    if descs:
        # Return the longest one
        return max(descs, key=len)
    return None

def needs_description_fix(content):
    """Check if a page needs its description fixed. Returns (needs_fix, current_desc, desc_location)."""
    # Find the SiteLayout tag
    layout_match = re.search(r'<SiteLayout\s(.*?)>', content, re.DOTALL)
    if not layout_match:
        return False, None, None
    
    tag = layout_match.group(1)
    
    # Direct description
    direct = re.findall(r'description="([^"]*)"', tag)
    if direct:
        desc = direct[0]
        if len(desc.strip()) >= 50:
            return False, desc, 'direct'
        return True, desc, 'direct'
    
    # Expression description  
    expr = re.findall(r'description=\{([^}]+)\}', tag)
    if expr:
        var_name = expr[0].strip()
        if 'meta.description' in var_name:
            meta_match = re.search(r'description\s*:\s*["\']([^"\']*)["\']', content)
            if meta_match:
                desc = meta_match.group(1)
                if len(desc.strip()) >= 50:
                    return False, desc, 'meta'
                return True, desc, 'meta'
            return True, '', 'meta_missing'
    
    # No description at all
    return True, None, 'missing'

def fix_description(filepath, content, new_desc):
    """Fix the description in the file."""
    needs_fix, current, location = needs_description_fix(content)
    
    if location == 'direct':
        # Replace the direct description
        content = re.sub(
            r'(description=")([^"]*?)(")',
            lambda m: m.group(1) + new_desc + m.group(3),
            content,
            count=1
        )
    elif location == 'meta':
        # Replace description in meta object
        # Find and replace the short description in meta
        content = re.sub(
            r"(description\s*:\s*['\"])([^'\"]*?)(['\"])",
            lambda m: m.group(1) + new_desc + m.group(3),
            content,
            count=1
        )
    elif location == 'meta_missing':
        # Need to add description to meta object
        meta_match = re.search(r"(export\s+const\s+meta\s*=\s*\{)", content)
        if meta_match:
            insert_after = meta_match.group(1)
            content = content.replace(
                insert_after,
                insert_after + f'\n  description: "{new_desc}",',
                1
            )
    elif location == 'missing':
        # Add description prop to SiteLayout
        layout_match = re.search(r'(<SiteLayout\s)', content)
        if layout_match:
            # Add after the opening tag
            content = content.replace(
                layout_match.group(1),
                layout_match.group(1) + f'\n  description="{new_desc}"',
                1
            )
    
    with open(filepath, 'w') as f:
        f.write(content)
    return True


def main():
    modified = 0
    skipped = 0
    
    for astro_file in sorted(SITES_DIR.rglob("*.astro")):
        if '[' in astro_file.name:
            continue
        
        content = astro_file.read_text()
        
        if 'SiteLayout' not in content:
            continue
        
        needs_fix, current, location = needs_description_fix(content)
        if not needs_fix:
            continue
        
        title = extract_title(content)
        
        # Try schema description first (often the best quality)
        schema_desc = get_description_from_schema(content)
        if schema_desc:
            new_desc = generate_description(title, schema_desc)
        else:
            first_para = extract_first_paragraph(content)
            new_desc = generate_description(title, first_para)
        
        if not new_desc or len(new_desc) < 40:
            skipped += 1
            continue
        
        # Escape quotes for HTML/JS
        new_desc = new_desc.replace('"', '\\"').replace("'", "\\'")
        
        if fix_description(astro_file, content, new_desc):
            modified += 1
            rel = astro_file.relative_to(SITES_DIR)
            print(f"  ✅ {rel}: \"{new_desc[:60]}...\"")
        else:
            skipped += 1
    
    print(f"\n📊 Results:")
    print(f"  Modified: {modified} pages")
    print(f"  Skipped: {skipped}")


if __name__ == "__main__":
    main()
