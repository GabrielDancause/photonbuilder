#!/usr/bin/env python3
"""
Extract data from pSEO static HTML pages into JSON data files.
Then these can be used with Astro dynamic routes ([slug].astro).
"""

import re
import os
import json
import glob
from html.parser import HTMLParser

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(BASE, "public/sites/siliconbased")


def extract_colors():
    """Extract data from color pages."""
    colors = []
    for filepath in sorted(glob.glob(os.path.join(PUBLIC, "colors/*.html"))):
        name = os.path.basename(filepath).replace('.html', '')
        with open(filepath, 'r') as f:
            html = f.read()

        data = {'slug': name}

        # Title
        m = re.search(r'<title>(.*?)</title>', html)
        if m: data['title'] = m.group(1)

        # Description
        m = re.search(r'<meta name="description" content="(.*?)"', html)
        if m: data['description'] = m.group(1)

        # Hex value
        m = re.search(r'id="val-hex"[^>]*>(.*?)</div>', html)
        if m: data['hex'] = m.group(1).strip()

        # RGB value
        m = re.search(r'id="val-rgb"[^>]*>(.*?)</div>', html)
        if m: data['rgb'] = m.group(1).strip()

        # HSL value
        m = re.search(r'id="val-hsl"[^>]*>(.*?)</div>', html)
        if m: data['hsl'] = m.group(1).strip()

        # Contrast ratios
        m = re.search(r'White Text.*?>([\d.]+:1)</div>', html, re.DOTALL)
        if m: data['contrastWhite'] = m.group(1)
        m = re.search(r'Black Text.*?>([\d.]+:1)</div>', html, re.DOTALL)
        if m: data['contrastBlack'] = m.group(1)

        # Harmonies
        harmonies = []
        for hm in re.finditer(r'harmony-swatch.*?background-color:\s*([^"]+)".*?href="/colors/(.*?)\.html".*?harmony-hex">(.*?)</div>', html, re.DOTALL):
            harmonies.append({
                'color': hm.group(1).strip().rstrip(';'),
                'name': hm.group(2),
                'hex': hm.group(3).strip()
            })
        data['harmonies'] = harmonies

        colors.append(data)

    return colors


def extract_regex():
    """Extract data from regex pages."""
    items = []
    for filepath in sorted(glob.glob(os.path.join(PUBLIC, "regex/*.html"))):
        name = os.path.basename(filepath).replace('.html', '')
        with open(filepath, 'r') as f:
            html = f.read()

        data = {'slug': name}

        m = re.search(r'<title>(.*?)</title>', html)
        if m: data['title'] = m.group(1)

        m = re.search(r'<meta name="description" content="(.*?)"', html)
        if m: data['description'] = m.group(1)

        # Regex pattern
        m = re.search(r'id="regex-pattern"[^>]*>(.*?)</(?:div|code|pre|span)>', html, re.DOTALL)
        if m: data['pattern'] = m.group(1).strip()

        items.append(data)

    return items


def extract_cron():
    """Extract data from cron pages."""
    items = []
    for filepath in sorted(glob.glob(os.path.join(PUBLIC, "cron/*.html"))):
        name = os.path.basename(filepath).replace('.html', '')
        with open(filepath, 'r') as f:
            html = f.read()

        data = {'slug': name}

        m = re.search(r'<title>(.*?)</title>', html)
        if m: data['title'] = m.group(1)

        m = re.search(r'<meta name="description" content="(.*?)"', html)
        if m: data['description'] = m.group(1)

        items.append(data)

    return items


def extract_chmod():
    """Extract data from chmod pages."""
    items = []
    for filepath in sorted(glob.glob(os.path.join(PUBLIC, "chmod/*.html"))):
        name = os.path.basename(filepath).replace('.html', '')
        with open(filepath, 'r') as f:
            html = f.read()

        data = {'slug': name}

        m = re.search(r'<title>(.*?)</title>', html)
        if m: data['title'] = m.group(1)

        m = re.search(r'<meta name="description" content="(.*?)"', html)
        if m: data['description'] = m.group(1)

        items.append(data)

    return items


def extract_security_headers():
    """Extract data from security-headers pages."""
    items = []
    for filepath in sorted(glob.glob(os.path.join(PUBLIC, "security-headers/*.html"))):
        name = os.path.basename(filepath).replace('.html', '')
        with open(filepath, 'r') as f:
            html = f.read()

        data = {'slug': name}

        m = re.search(r'<title>(.*?)</title>', html)
        if m: data['title'] = m.group(1)

        m = re.search(r'<meta name="description" content="(.*?)"', html)
        if m: data['description'] = m.group(1)

        items.append(data)

    return items


def main():
    os.makedirs(os.path.join(BASE, "src/data"), exist_ok=True)

    print("Extracting colors...")
    colors = extract_colors()
    with open(os.path.join(BASE, "src/data/colors.json"), 'w') as f:
        json.dump(colors, f, indent=2)
    print(f"  {len(colors)} colors")

    print("Extracting regex...")
    regex = extract_regex()
    with open(os.path.join(BASE, "src/data/regex.json"), 'w') as f:
        json.dump(regex, f, indent=2)
    print(f"  {len(regex)} regex patterns")

    print("Extracting cron...")
    cron = extract_cron()
    with open(os.path.join(BASE, "src/data/cron.json"), 'w') as f:
        json.dump(cron, f, indent=2)
    print(f"  {len(cron)} cron expressions")

    print("Extracting chmod...")
    chmod = extract_chmod()
    with open(os.path.join(BASE, "src/data/chmod.json"), 'w') as f:
        json.dump(chmod, f, indent=2)
    print(f"  {len(chmod)} chmod values")

    print("Extracting security-headers...")
    sec = extract_security_headers()
    with open(os.path.join(BASE, "src/data/security-headers.json"), 'w') as f:
        json.dump(sec, f, indent=2)
    print(f"  {len(sec)} security header analyses")


if __name__ == "__main__":
    main()
