#!/usr/bin/env python3
"""
Cross-domain internal linking engine for PhotonBuilder.
Scans ALL sites, extracts page metadata, finds related pages by keyword overlap,
and injects "Related Tools" sections.

Usage:
  python3 scripts/internal-links-v2.py              # audit only
  python3 scripts/internal-links-v2.py --apply       # inject links
"""

import os, re, sys, json
from pathlib import Path
from collections import defaultdict

BASE = Path(os.path.expanduser("~/Desktop/photonbuilder"))
SITES_DIR = BASE / "src" / "pages" / "sites"

# Domain mapping
DOMAIN_MAP = {
    "westmount": "https://westmountfundamentals.com",
    "siliconbased": "https://siliconbased.dev",
    "firemaths": "https://firemaths.info",
    "leeroyjenkins": "https://leeroyjenkins.quest",
    "ijustwantto": "https://ijustwantto.live",
    "28grams": "https://28grams.vip",
    "migratingmammals": "https://migratingmammals.com",
    "nookienook": "https://thenookienook.com",
    "bodycount": "https://bodycount.photonbuilder.com",
    "sendnerds": "https://sendnerds.photonbuilder.com",
    "getthebag": "https://getthebag.photonbuilder.com",
    "fixitwithducttape": "https://fixitwithducttape.photonbuilder.com",
    "pleasestartplease": "https://pleasestartplease.photonbuilder.com",
    "justonemoment": "https://justonemoment.photonbuilder.com",
    "papyruspeople": "https://papyruspeople.photonbuilder.com",
    "eeniemeenie": "https://eeniemeenie.photonbuilder.com",
}

# Stop words for keyword extraction
STOP_WORDS = {'the','a','an','is','are','was','were','be','been','being','and','or','but','in',
    'on','at','to','for','of','with','by','from','as','into','about','between','through',
    'during','before','after','above','below','up','down','out','off','over','under','how',
    'what','when','where','why','which','who','this','that','these','those','i','my','your',
    'our','its','his','her','their','we','you','they','me','us','him','them','do','does',
    'did','has','have','had','will','would','shall','should','can','could','may','might',
    'must','need','not','no','nor','so','if','then','than','too','very','just','also','now',
    'all','each','every','both','few','more','most','other','some','such','only','own','same',
    'best','free','online','tool','calculator','guide','list','chart','top','vs','new','2026',
    '2025','2024','page','site','home','index','make','maker','get','use','find','using'}


def extract_meta(filepath):
    """Extract title, description, and category from an Astro file."""
    content = filepath.read_text(errors='replace')
    
    title_m = re.search(r'title:\s*["\'](.+?)["\']', content)
    desc_m = re.search(r'description:\s*["\'](.+?)["\']', content)
    cat_m = re.search(r'category:\s*["\'](.+?)["\']', content)
    
    title = title_m.group(1) if title_m else filepath.stem.replace('-', ' ').title()
    desc = desc_m.group(1) if desc_m else ''
    cat = cat_m.group(1) if cat_m else 'tool'
    
    return title, desc, cat, content


def extract_keywords(title, desc, slug):
    """Extract meaningful keywords from title, description, and slug."""
    text = f"{title} {desc} {slug.replace('-', ' ')}".lower()
    words = re.findall(r'[a-z]+', text)
    # Single words
    kw = set(w for w in words if w not in STOP_WORDS and len(w) > 2)
    # Bigrams from slug (most important)
    slug_words = slug.split('-')
    for i in range(len(slug_words) - 1):
        bigram = f"{slug_words[i]}_{slug_words[i+1]}"
        if slug_words[i] not in STOP_WORDS and slug_words[i+1] not in STOP_WORDS:
            kw.add(bigram)
    return kw


def similarity(kw1, kw2):
    """Jaccard-ish similarity with bigram bonus."""
    if not kw1 or not kw2:
        return 0
    common = kw1 & kw2
    # Bigram matches worth more
    bigram_matches = sum(1 for k in common if '_' in k)
    word_matches = len(common) - bigram_matches
    score = (word_matches + bigram_matches * 3) / (len(kw1 | kw2))
    return score


def find_related(pages, target_idx, max_results=3, same_domain_max=1):
    """Find most related pages for a given page, preferring cross-domain."""
    target = pages[target_idx]
    scores = []
    
    for i, page in enumerate(pages):
        if i == target_idx:
            continue
        sim = similarity(target['keywords'], page['keywords'])
        if sim > 0.12:  # minimum threshold — tighter to avoid noise
            scores.append((sim, i))
    
    scores.sort(reverse=True)
    
    # Pick results, limiting same-domain links
    results = []
    domain_counts = defaultdict(int)
    
    for sim, idx in scores:
        p = pages[idx]
        # Prefer cross-domain
        if p['site'] == target['site']:
            if domain_counts[p['site']] >= same_domain_max:
                continue
        domain_counts[p['site']] += 1
        results.append(idx)
        if len(results) >= max_results:
            break
    
    return results


def build_link_html(pages, related_indices, source_site):
    """Build the Related Tools HTML section."""
    cards = []
    for idx in related_indices:
        p = pages[idx]
        domain = DOMAIN_MAP.get(p['site'], '')
        if p['site'] == source_site:
            url = f"/{p['slug']}"
        else:
            url = f"{domain}/{p['slug']}"
        
        # Truncate description
        desc = p['desc'][:120] + '...' if len(p['desc']) > 120 else p['desc']
        if not desc:
            desc = p['title']
        
        cards.append(f'''      <a href="{url}" style="display:block;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:1.25rem;text-decoration:none;color:inherit;transition:border-color 0.2s,transform 0.2s;" onmouseover="this.style.borderColor='rgba(255,255,255,0.2)';this.style.transform='translateY(-2px)'" onmouseout="this.style.borderColor='rgba(255,255,255,0.08)';this.style.transform='none'">
        <strong style="font-size:0.95rem;">{p['title'].split(' — ')[0].split(' | ')[0].split(' - ')[0][:60]}</strong>
        <p style="opacity:0.6;font-size:0.83rem;margin:0.4rem 0 0;line-height:1.4;">{desc}</p>
      </a>''')
    
    return f'''
  <div class="related-tools" style="margin-top:3rem;padding-top:2rem;border-top:1px solid rgba(255,255,255,0.08);">
    <h2 style="font-size:1.2rem;margin-bottom:1rem;">🔗 Related Tools</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1rem;">
{chr(10).join(cards)}
    </div>
  </div>'''


def main():
    apply = "--apply" in sys.argv
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    
    if not apply:
        print("🔍 AUDIT MODE — use --apply to write changes\n")
    
    # 1. Scan all pages
    print("📂 Scanning all sites...")
    pages = []
    skipped = {'index', 'studies', 'tools', 'guides', 'lists', '404', '[...ivslug]', '[...prospectslug]'}
    
    for site_dir in sorted(SITES_DIR.iterdir()):
        if not site_dir.is_dir():
            continue
        site_name = site_dir.name
        if site_name not in DOMAIN_MAP:
            continue
        
        for astro_file in sorted(site_dir.glob("*.astro")):
            slug = astro_file.stem
            if slug in skipped or slug.startswith('['):
                continue
            
            title, desc, cat, content = extract_meta(astro_file)
            keywords = extract_keywords(title, desc, slug)
            has_related = "related-tools" in content
            
            pages.append({
                'site': site_name,
                'slug': slug,
                'title': title,
                'desc': desc,
                'cat': cat,
                'keywords': keywords,
                'has_related': has_related,
                'path': astro_file,
                'lines': content.count('\n'),
            })
    
    print(f"   Found {len(pages)} pages across {len(set(p['site'] for p in pages))} domains\n")
    
    # 2. Count existing links
    already = sum(1 for p in pages if p['has_related'])
    needs = sum(1 for p in pages if not p['has_related'])
    print(f"📊 Already linked: {already} | Needs links: {needs}\n")
    
    # 3. Find and inject related links
    injected = 0
    errors = 0
    
    for i, page in enumerate(pages):
        if page['has_related']:
            continue
        
        related = find_related(pages, i)
        if not related:
            if verbose:
                print(f"  ⚠️  {page['site']}/{page['slug']} — no related pages found")
            continue
        
        html = build_link_html(pages, related, page['site'])
        
        content = page['path'].read_text(errors='replace')
        
        # Find insertion point: before </SiteLayout>
        if "</SiteLayout>" in content:
            new_content = content.replace("</SiteLayout>", f"{html}\n</SiteLayout>", 1)
        else:
            if verbose:
                print(f"  ⚠️  {page['site']}/{page['slug']} — no </SiteLayout> found")
            errors += 1
            continue
        
        related_names = [f"{pages[r]['site']}/{pages[r]['slug']}" for r in related]
        
        if apply:
            page['path'].write_text(new_content)
            print(f"  ✅ {page['site']}/{page['slug']} → {', '.join(related_names)}")
        else:
            if verbose or injected < 20:
                print(f"  📋 {page['site']}/{page['slug']} → {', '.join(related_names)}")
        
        injected += 1
    
    print(f"\n{'✅ Injected' if apply else '📋 Would inject'}: {injected} pages")
    if errors:
        print(f"⚠️  Skipped {errors} pages (no SiteLayout closing tag)")
    
    # 4. Summary by domain
    print("\n📊 By domain:")
    domain_stats = defaultdict(lambda: {'total': 0, 'linked': 0, 'new': 0})
    for p in pages:
        domain_stats[p['site']]['total'] += 1
        if p['has_related']:
            domain_stats[p['site']]['linked'] += 1
    
    # Count new injections
    for i, page in enumerate(pages):
        if not page['has_related']:
            related = find_related(pages, i)
            if related:
                domain_stats[page['site']]['new'] += 1
    
    for site in sorted(domain_stats.keys()):
        s = domain_stats[site]
        print(f"   {site:<25} {s['total']:>4} pages | {s['linked']:>3} linked | +{s['new']:>3} new")


if __name__ == "__main__":
    main()
