#!/usr/bin/env python3
"""
Convert siliconbased Astro pages from `const htmlContent` template literal pattern
to proper Astro HTML with separated style/script blocks.

Structure:
  ---
  import SiteLayout from '...';
  const schema = {...};
  const htmlContent = `<style>...</style><div>...</div><script>...</script>`;
  ---
  <SiteLayout ...>
    <Fragment set:html={htmlContent} />
  </SiteLayout>

Target:
  ---
  import SiteLayout from '...';
  const schema = {...};
  ---
  <SiteLayout ...>
    <div>...</div>
    <script is:inline>...</script>
    <style>...</style>
  </SiteLayout>
"""

import re
import os
import glob

PAGES_DIR = "src/pages/sites/siliconbased"


def convert_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'const htmlContent' not in content:
        return False

    name = os.path.basename(filepath)

    # Find frontmatter boundaries (first and last ---)
    lines = content.split('\n')
    fm_start = None
    fm_end = None
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if fm_start is None:
                fm_start = i
            else:
                fm_end = i
                break

    if fm_start is None or fm_end is None:
        print(f"  SKIP: Can't find frontmatter in {name}")
        return False

    frontmatter_lines = lines[fm_start + 1:fm_end]
    after_frontmatter = '\n'.join(lines[fm_end + 1:])

    # Find htmlContent in frontmatter
    fm_text = '\n'.join(frontmatter_lines)
    
    # Find the start of const htmlContent = `
    hc_match = re.search(r'const htmlContent\s*=\s*`', fm_text)
    if not hc_match:
        print(f"  SKIP: Can't find htmlContent in frontmatter of {name}")
        return False

    hc_start = hc_match.end()  # position after the opening backtick

    # Find the closing backtick - handle escaped backticks
    pos = hc_start
    while pos < len(fm_text):
        if fm_text[pos] == '\\' and pos + 1 < len(fm_text):
            pos += 2
            continue
        if fm_text[pos] == '`':
            break
        pos += 1

    if pos >= len(fm_text):
        print(f"  SKIP: Can't find closing backtick in {name}")
        return False

    template_content = fm_text[hc_start:pos]

    # Get the frontmatter BEFORE htmlContent
    fm_before = fm_text[:hc_match.start()].rstrip()
    # Get the frontmatter AFTER htmlContent (usually just `;\n`)
    fm_after = fm_text[pos + 1:].strip()
    if fm_after.startswith(';'):
        fm_after = fm_after[1:].strip()

    # Clean frontmatter (just imports + schema)
    clean_fm = fm_before
    if fm_after:
        clean_fm += '\n' + fm_after

    # Unescape template literal content
    template_content = template_content.replace('\\`', '`')
    template_content = template_content.replace('\\${', '${')

    # Extract <style> blocks
    style_blocks = re.findall(r'<style[^>]*>[\s\S]*?</style>', template_content)

    # Extract <script> blocks  
    script_blocks = re.findall(r'<script[^>]*>[\s\S]*?</script>', template_content)

    # Get HTML body
    body_html = template_content
    for block in style_blocks:
        body_html = body_html.replace(block, '', 1)
    for block in script_blocks:
        body_html = body_html.replace(block, '', 1)
    body_html = body_html.strip()

    # Add is:inline to script tags
    processed_scripts = []
    for script in script_blocks:
        if 'is:inline' not in script:
            script = re.sub(r'<script([^>]*)>', r'<script is:inline\1>', script, count=1)
            script = script.replace('<script is:inline >', '<script is:inline>')
        processed_scripts.append(script)

    # Extract SiteLayout from after frontmatter
    layout_match = re.search(
        r'<SiteLayout([^>]*?)>\s*(?:<Fragment[^/]*/>\s*)?</SiteLayout>',
        after_frontmatter,
        re.DOTALL
    )
    if not layout_match:
        print(f"  SKIP: Can't find SiteLayout in {name}")
        return False

    layout_attrs = layout_match.group(1)

    # Build new file
    out = []
    out.append(f"---\n{clean_fm.strip()}\n---\n")
    out.append(f"\n<SiteLayout{layout_attrs}>\n")
    out.append(body_html)
    out.append('\n')

    if processed_scripts:
        out.append('\n')
        for s in processed_scripts:
            out.append(s)
            out.append('\n')

    if style_blocks:
        out.append('\n')
        for s in style_blocks:
            out.append(s)
            out.append('\n')

    out.append('</SiteLayout>\n')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(''.join(out))

    return True


def main():
    pattern = os.path.join(PAGES_DIR, "*.astro")
    files = sorted(glob.glob(pattern))

    converted = 0
    skipped = 0
    errors = 0

    for filepath in files:
        name = os.path.basename(filepath)
        try:
            if convert_file(filepath):
                converted += 1
                print(f"  ✓ {name}")
        except Exception as e:
            errors += 1
            print(f"  ✗ {name}: {e}")

    not_converted = len(files) - converted - errors
    print(f"\nDone: {converted} converted, {not_converted} skipped, {errors} errors")


if __name__ == "__main__":
    main()
