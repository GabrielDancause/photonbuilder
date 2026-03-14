#!/usr/bin/env python3
"""
Convert siliconbased Astro pages: extract <style> and <script> from the
htmlContent template literal into proper Astro blocks. Keep HTML body in
a variable with set:html to avoid Astro expression parsing of curly braces.

Before: const htmlContent = `<style>...</style><div>...</div><script>...</script>`;
        <Fragment set:html={htmlContent} />

After:  const htmlBody = `<div>...</div>`;
        <Fragment set:html={htmlBody} />
        <script is:inline>...</script>
        <style>...</style>
"""
import re
import os
import glob

PAGES_DIR = os.path.expanduser("~/Desktop/photonbuilder/src/pages/sites/siliconbased")


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'const htmlContent' not in content:
        return False

    # Find template literal boundaries
    hc_marker = "const htmlContent = `"
    hc_start = content.index(hc_marker)
    literal_start = hc_start + len(hc_marker)
    
    close_pattern = "`;\n---"
    close_idx = content.index(close_pattern, literal_start)
    literal_end = close_idx
    
    # Extract template literal content (raw, with escapes intact)
    raw_html = content[literal_start:literal_end]
    
    # Extract <style> blocks (from raw content, before unescaping)
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', raw_html, re.DOTALL)
    html_no_style = re.sub(r'<style[^>]*>.*?</style>\s*', '', raw_html, flags=re.DOTALL)
    
    # Extract <script> blocks
    script_blocks = re.findall(r'<script[^>]*>(.*?)</script>', html_no_style, re.DOTALL)
    html_body = re.sub(r'<script[^>]*>.*?</script>\s*', '', html_no_style, flags=re.DOTALL).strip()
    
    # Build new frontmatter: replace "const htmlContent = `...`" with "const htmlBody = `...`"
    # Keep the body in a template literal (with original escapes) for set:html
    new_var = f"const htmlBody = `{html_body}`"
    
    # Replace in original content
    old_literal = content[hc_start:close_idx + 2]  # includes closing `;
    new_content = content[:hc_start] + new_var + content[close_idx + 2:]
    
    # Replace Fragment set:html={htmlContent} with Fragment set:html={htmlBody}
    new_content = new_content.replace('set:html={htmlContent}', 'set:html={htmlBody}')
    
    # Find where to insert style and script blocks (before </SiteLayout>)
    site_layout_close = new_content.rindex('</SiteLayout>')
    
    insert_parts = ""
    for script in script_blocks:
        # Unescape the script content for proper inline usage
        unescaped = script.replace('\\`', '`').replace('\\${', '${')
        insert_parts += f"\n  <script is:inline>{unescaped}</script>\n"
    
    # Style blocks - unescape for proper CSS
    for style in style_blocks:
        unescaped = style.replace('\\`', '`').replace('\\${', '${')
        insert_parts += f"\n  <style>{unescaped}</style>\n"
    
    new_content = new_content[:site_layout_close] + insert_parts + new_content[site_layout_close:]
    
    # Verify
    if 'const htmlContent' in new_content:
        print(f"  ERROR (htmlContent still present): {os.path.basename(filepath)}")
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True


def main():
    files = sorted(glob.glob(os.path.join(PAGES_DIR, "*.astro")))
    total = 0
    converted = 0
    errors = 0
    
    for f in files:
        with open(f, 'r') as fh:
            if 'const htmlContent' not in fh.read():
                continue
        total += 1
        try:
            if process_file(f):
                converted += 1
                print(f"  ✓ {os.path.basename(f)}")
            else:
                errors += 1
        except Exception as e:
            errors += 1
            print(f"  ✗ {os.path.basename(f)}: {e}")
    
    print(f"\nDone: {converted}/{total} converted, {errors} errors")


if __name__ == '__main__':
    main()
