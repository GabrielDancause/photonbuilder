#!/usr/bin/env python3
"""
Strip :root CSS variables from page <style> blocks that are now provided by SiteLayout.

Removes vars that match the theme (bg, card, border, accent, text, font aliases).
Keeps page-specific vars (chart colors, game colors, etc.).
If :root block becomes empty after stripping, removes the whole block.
"""

import re
import os
import glob

SITES_DIR = "src/pages/sites"

# Variable names that SiteLayout now provides (any of these can be stripped)
THEME_VARS = {
    # Background
    '--bg-color', '--bg', '--bg-main', '--bg-base',
    # Card background
    '--card-bg', '--card', '--bg-card',
    # Border
    '--border-color', '--border',
    # Accent
    '--accent-color', '--accent', '--accent-hover',
    # Text
    '--text-primary', '--text-main', '--text', '--text-color',
    '--text-secondary', '--text-muted', '--text-dim', '--text-sec', '--text-light',
    # Fonts
    '--font-ui', '--font-body', '--font-sans', '--font-main', '--font-mono', '--font-code',
    # Nav (SiteLayout handles nav)
    '--nav-bg',
}


def strip_root_vars(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if ':root' not in content:
        return False

    name = os.path.basename(filepath)

    # Find all :root { ... } blocks in style sections
    # We need to handle both <style> and <style is:inline> blocks
    modified = False

    def process_root_block(match):
        nonlocal modified
        full_block = match.group(0)
        indent = match.group(1) or ''
        vars_content = match.group(2)

        # Parse individual var declarations
        lines = vars_content.split('\n')
        kept_lines = []
        stripped_count = 0

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            # Check if this is a var declaration
            var_match = re.match(r'\s*(--[\w-]+)\s*:', stripped)
            if var_match:
                var_name = var_match.group(1)
                if var_name in THEME_VARS:
                    stripped_count += 1
                    continue
            
            # Keep non-var lines (comments, etc.) and page-specific vars
            kept_lines.append(line)

        if stripped_count == 0:
            return full_block  # Nothing to strip

        modified = True

        if not kept_lines or all(l.strip() == '' for l in kept_lines):
            # All vars were stripped — remove entire :root block
            return ''
        else:
            # Rebuild :root with remaining vars
            remaining = '\n'.join(kept_lines)
            return f'{indent}:root {{\n{remaining}\n{indent}}}'

    # Match :root { ... } blocks
    content_new = re.sub(
        r'(\s*):root\s*\{([^}]*)\}',
        process_root_block,
        content
    )

    # Clean up empty lines left by removed :root blocks
    content_new = re.sub(r'\n\s*\n\s*\n', '\n\n', content_new)

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content_new)
        return True

    return False


def main():
    total_stripped = 0
    total_files = 0

    for site_dir in sorted(glob.glob(os.path.join(SITES_DIR, '*'))):
        if not os.path.isdir(site_dir):
            continue
        site_name = os.path.basename(site_dir)

        files = sorted(glob.glob(os.path.join(site_dir, '*.astro')))
        site_stripped = 0

        for filepath in files:
            if strip_root_vars(filepath):
                site_stripped += 1
                total_stripped += 1

        if site_stripped > 0:
            print(f"  {site_name}: {site_stripped} files stripped")
        total_files += len(files)

    print(f"\nDone: {total_stripped}/{total_files} files had :root vars stripped")


if __name__ == "__main__":
    main()
