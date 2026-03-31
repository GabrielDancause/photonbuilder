#!/usr/bin/env python3
"""Fix duplicate page titles by making them unique."""

import os
import re
from pathlib import Path
from collections import defaultdict

SITES_DIR = Path(__file__).resolve().parent.parent / "src" / "pages" / "sites"

def extract_title(content):
    """Extract page title - check SiteLayout tag and meta."""
    # Direct title in SiteLayout tag
    layout_match = re.search(r'<SiteLayout\s(.*?)>', content, re.DOTALL)
    if layout_match:
        tag = layout_match.group(1)
        direct = re.findall(r'title="([^"]*)"', tag)
        if direct:
            return direct[0], 'direct'
        expr = re.findall(r'title=\{([^}]+)\}', tag)
        if expr:
            var = expr[0].strip()
            if 'meta.title' in var:
                m = re.search(r"title\s*:\s*['\"]([^'\"]+)['\"]", content)
                if m:
                    return m.group(1), 'meta'
    return None, None


def set_title(filepath, content, new_title, location):
    """Update the title in the file."""
    if location == 'direct':
        # Find the SiteLayout tag and replace title
        def replace_title(m):
            tag = m.group(0)
            return re.sub(r'title="[^"]*"', f'title="{new_title}"', tag, count=1)
        content = re.sub(r'<SiteLayout\s[^>]*>', replace_title, content, count=1)
    elif location == 'meta':
        # Replace in meta object
        content = re.sub(
            r"(title\s*:\s*['\"])([^'\"]*?)(['\"])",
            lambda m: m.group(1) + new_title + m.group(3),
            content,
            count=1
        )
    
    with open(filepath, 'w') as f:
        f.write(content)


def slug_to_words(slug):
    """Convert slug to human-readable words."""
    words = slug.replace('.astro', '').replace('-', ' ').replace('_', ' ')
    return words.title()


def make_unique_title(title, filepath, all_files_with_title):
    """Generate a unique title based on the file path/slug."""
    slug = filepath.stem  # filename without extension
    site = filepath.parent.name
    
    # Strategy: add specificity based on the slug
    slug_words = slug_to_words(slug)
    
    # If the title is very generic (like "Tools" or "Guides"), add the site name
    generic_titles = {'tools', 'guides', 'lists', 'studies', 'home', 'index'}
    if title.lower().strip() in generic_titles or slug == 'index':
        # For index/category pages, include site info
        site_name = slug_to_words(site)
        if slug == 'index':
            return f"{site_name} — Free {title} & Resources"
        return f"{title} — {site_name}"
    
    # For duplicate tool/content pages, enhance the title
    if title == slug_words:
        # Title is just the slug - add "Online" or "Free" or a descriptor
        return f"{title} Online — Free Tool"
    
    # Add the site context or differentiate
    site_name = slug_to_words(site)
    
    # Check if the duplicate is from different sites
    sites_involved = set(f.parent.name for f in all_files_with_title)
    if len(sites_involved) > 1:
        # Different sites have the same title - add site name
        site_display = site_name.replace('Siliconbased', 'SiliconBased').replace('Fixitwithducttape', 'FixItWithDuctTape').replace('Ijustwantto', 'iJustWantTo').replace('Justonemoment', 'JustOneMoment').replace('Migratingmammals', 'MigratingMammals').replace('Leeroyjenkins', 'LeeroyJenkins').replace('Sendnerds', 'SendNerds').replace('Pleasestartplease', 'PleaseStartPlease').replace('Nookienook', 'NookieNook').replace('Eeniemeenie', 'EenieMeenie').replace('Getthebag', 'GetTheBag').replace('Papyruspeople', 'PapyrusPeople').replace('Bodycount', 'BodyCount').replace('Firemaths', 'FireMaths').replace('Trunkpress', 'TrunkPress')
        return f"{title} | {site_display}"
    
    # Same site, different pages - the slug provides differentiation
    # Make sure we don't just repeat the title
    if slug_words.lower().replace(' ', '') in title.lower().replace(' ', '').replace('-', ''):
        return f"{title} — Complete Guide & Calculator"
    return f"{title} — {slug_words} Guide"


def main():
    # Collect all titles
    titles = defaultdict(list)
    
    for astro_file in sorted(SITES_DIR.rglob("*.astro")):
        if '[' in astro_file.name:
            continue
        
        content = astro_file.read_text()
        if 'SiteLayout' not in content:
            continue
        
        title, location = extract_title(content)
        if title:
            titles[title].append((astro_file, location))
    
    # Find duplicates
    duplicates = {t: files for t, files in titles.items() if len(files) > 1}
    
    modified = 0
    print(f"Found {len(duplicates)} duplicate title groups ({sum(len(f) for f in duplicates.values())} total pages)")
    
    for title, files in sorted(duplicates.items()):
        print(f"\n  📋 \"{title}\" ({len(files)} pages)")
        all_paths = [f for f, _ in files]
        
        for filepath, location in files:
            content = filepath.read_text()
            new_title = make_unique_title(title, filepath, all_paths)
            
            if new_title != title:
                set_title(filepath, content, new_title, location)
                modified += 1
                print(f"    ✅ {filepath.relative_to(SITES_DIR)} → \"{new_title}\"")
            else:
                print(f"    ⚠️ {filepath.relative_to(SITES_DIR)} — no change")
    
    print(f"\n📊 Results:")
    print(f"  Duplicate groups: {len(duplicates)}")
    print(f"  Pages modified: {modified}")


if __name__ == "__main__":
    main()
