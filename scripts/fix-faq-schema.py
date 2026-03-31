#!/usr/bin/env python3
"""Add FAQPage JSON-LD schema to pages that have FAQ content but no FAQPage schema."""

import os
import re
import json
import html
from pathlib import Path

SITES_DIR = Path(__file__).resolve().parent.parent / "src" / "pages" / "sites"

def clean_html(text):
    """Remove HTML tags and decode entities."""
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_faq_pairs_h3(content):
    """Extract Q&A pairs from .faq-item divs with h3/h4 questions and p answers."""
    pairs = []
    # Pattern: <div class="faq-item">...<h3/h4>Question?</h3/h4>...<p>Answer</p>...</div>
    faq_items = re.findall(r'<div\s+class="faq-item"[^>]*>(.*?)</div>\s*(?=<div\s+class="faq-item"|</div>|<footer|<h2|$)', content, re.DOTALL)
    for item in faq_items:
        q_match = re.search(r'<h[34][^>]*>(.*?)</h[34]>', item, re.DOTALL)
        p_matches = re.findall(r'<p[^>]*>(.*?)</p>', item, re.DOTALL)
        if q_match and p_matches:
            question = clean_html(q_match.group(1))
            answer = clean_html(' '.join(p_matches))
            if question and answer and len(answer) > 10:
                pairs.append((question, answer))
    return pairs

def extract_faq_pairs_faq_question(content):
    """Extract Q&A from .faq-question/.faq-answer or .faq-q/.faq-a divs."""
    pairs = []
    # Try faq-question / faq-answer
    questions = re.findall(r'<div\s+class="faq-question"[^>]*>(.*?)</div>', content, re.DOTALL)
    answers = re.findall(r'<div\s+class="faq-answer"[^>]*>(.*?)</div>', content, re.DOTALL)
    for q, a in zip(questions, answers):
        question = clean_html(q)
        answer = clean_html(a)
        if question and answer and len(answer) > 10:
            pairs.append((question, answer))
    if pairs:
        return pairs
    # Try faq-q / faq-a
    questions = re.findall(r'<div\s+class="faq-q"[^>]*>(.*?)</div>', content, re.DOTALL)
    answers = re.findall(r'<div\s+class="faq-a"[^>]*>(.*?)</div>', content, re.DOTALL)
    for q, a in zip(questions, answers):
        question = clean_html(q)
        answer = clean_html(a)
        if question and answer and len(answer) > 10:
            pairs.append((question, answer))
    if pairs:
        return pairs
    # Try faq-item blocks with faq-q + p (answer in <p> not faq-a)
    items = re.findall(r'<div\s+class="faq-item"[^>]*>(.*?)</div>\s*</div>', content, re.DOTALL)
    if not items:
        # Try broader: faq-item to next faq-item or end
        items = re.findall(r'<div\s+class="faq-item"[^>]*>(.*?)(?=<div\s+class="faq-item"|</main|</section|<script)', content, re.DOTALL)
    for item in items:
        q_match = re.search(r'<div\s+class="faq-q"[^>]*>(.*?)</div>', item, re.DOTALL)
        if q_match:
            question = clean_html(q_match.group(1))
            p_matches = re.findall(r'<p[^>]*>(.*?)</p>', item, re.DOTALL)
            answer = clean_html(' '.join(p_matches))
            if question and answer and len(answer) > 10:
                pairs.append((question, answer))
    return pairs

def extract_faq_pairs_details(content):
    """Extract Q&A from <details><summary> patterns."""
    pairs = []
    details_blocks = re.findall(r'<details[^>]*>(.*?)</details>', content, re.DOTALL)
    for block in details_blocks:
        q_match = re.search(r'<summary[^>]*>(.*?)</summary>', block, re.DOTALL)
        if q_match:
            question = clean_html(q_match.group(1))
            # Remove any trailing SVG/icon markup from question
            question = re.sub(r'\s*$', '', question)
            # Get answer: everything after </summary>
            answer_html = re.sub(r'<summary[^>]*>.*?</summary>', '', block, flags=re.DOTALL)
            answer = clean_html(answer_html)
            if question and answer and len(answer) > 10:
                pairs.append((question, answer))
    return pairs

def extract_faq_pairs_h3_in_section(content):
    """Extract Q&A from h3 questions inside faq-section."""
    pairs = []
    # Find the faq-section
    section_match = re.search(r'<(?:div|section)\s+class="faq-section"[^>]*>(.*?)(?:</div>|</section>)\s*(?=<(?:div|section|footer)|$)', content, re.DOTALL)
    if not section_match:
        return pairs
    section = section_match.group(1)
    # Split by h3 tags
    parts = re.split(r'(<h3[^>]*>.*?</h3>)', section, flags=re.DOTALL)
    for i in range(1, len(parts), 2):
        q = clean_html(parts[i])
        if i + 1 < len(parts):
            # Get all <p> tags in the following content
            p_matches = re.findall(r'<p[^>]*>(.*?)</p>', parts[i+1], re.DOTALL)
            answer = clean_html(' '.join(p_matches))
            if q and answer and len(answer) > 10:
                pairs.append((q, answer))
    return pairs

def extract_faq_pairs_after_faq_header(content):
    """Extract Q&A from h3 questions that follow an h2 FAQ header."""
    pairs = []
    # Find h2 that mentions FAQ or Frequently Asked
    faq_header = re.search(r'<h2[^>]*>[^<]*(?:FAQ|Frequently Asked)[^<]*</h2>', content, re.IGNORECASE)
    if not faq_header:
        return pairs
    after = content[faq_header.end():]
    # Extract h3 + p pairs until we hit another h2 or main/footer/script
    parts = re.split(r'(<h3[^>]*>.*?</h3>)', after, flags=re.DOTALL)
    for i in range(1, len(parts), 2):
        q = clean_html(parts[i])
        if not q:
            continue
        if i + 1 < len(parts):
            # Stop at next section
            section = re.split(r'<h2|<main|<footer|<script|</main|</div>\s*</main', parts[i+1])[0]
            p_matches = re.findall(r'<p[^>]*>(.*?)</p>', section, re.DOTALL)
            answer = clean_html(' '.join(p_matches))
            if q and answer and len(answer) > 10:
                pairs.append((q, answer))
    return pairs

def extract_all_faq_pairs(content):
    """Try all extraction methods and return the best result."""
    results = []
    results.append(extract_faq_pairs_h3(content))
    results.append(extract_faq_pairs_faq_question(content))
    results.append(extract_faq_pairs_details(content))
    results.append(extract_faq_pairs_h3_in_section(content))
    results.append(extract_faq_pairs_after_faq_header(content))
    # Return the longest non-empty result
    best = max(results, key=len) if results else []
    return best

def make_faq_schema(pairs):
    """Create FAQPage JSON-LD schema from Q&A pairs."""
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a
                }
            }
            for q, a in pairs
        ]
    }

def uses_site_layout(content):
    """Check if the page uses SiteLayout."""
    return 'SiteLayout' in content

def has_existing_schema_var(content):
    """Check if there's a const schema = ... in frontmatter."""
    return bool(re.search(r'const\s+schema\s*=', content))

def add_schema_to_page(filepath, content, faq_schema):
    """Add FAQPage schema to an .astro page."""
    faq_json = json.dumps(faq_schema, indent=2)
    
    if not uses_site_layout(content):
        # Inject <script type="application/ld+json"> before </head> or at end
        script_tag = f'\n<script type="application/ld+json">\n{faq_json}\n</script>\n'
        if '</head>' in content:
            content = content.replace('</head>', script_tag + '</head>', 1)
        else:
            content += script_tag
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    
    if has_existing_schema_var(content):
        # There's a `const schema = {...}` - wrap it in array with FAQPage
        # Find the schema variable assignment
        schema_match = re.search(r'(const\s+schema\s*=\s*)', content)
        if schema_match:
            start = schema_match.end()
            # Check if it's already an array
            rest = content[start:].lstrip()
            if rest.startswith('['):
                # Already an array - insert FAQPage schema before the closing ]
                # Find the matching ]
                bracket_count = 0
                for i, ch in enumerate(content[start:]):
                    if ch == '[':
                        bracket_count += 1
                    elif ch == ']':
                        bracket_count -= 1
                        if bracket_count == 0:
                            insert_pos = start + i
                            faq_entry = ',\n  ' + json.dumps(faq_schema, indent=2).replace('\n', '\n  ')
                            content = content[:insert_pos] + faq_entry + '\n' + content[insert_pos:]
                            break
            else:
                # It's a single object - wrap in array
                # Find end of the object (matching brace)
                brace_count = 0
                obj_start = start
                for i, ch in enumerate(content[start:]):
                    if ch == '{':
                        brace_count += 1
                    elif ch == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            obj_end = start + i + 1
                            existing = content[obj_start:obj_end]
                            replacement = f'[\n  {existing},\n  {json.dumps(faq_schema, indent=2).replace(chr(10), chr(10) + "  ")}\n]'
                            content = content[:obj_start] + replacement + content[obj_end:]
                            break
            
            with open(filepath, 'w') as f:
                f.write(content)
            return True
    else:
        # No schema variable exists - add one before the closing ---
        # Find the frontmatter section (between --- markers)
        fm_match = re.search(r'(---\n)(.*?)(---)', content, re.DOTALL)
        if fm_match:
            frontmatter = fm_match.group(2)
            faq_var = f'\nconst schema = {faq_json};\n'
            new_fm = frontmatter + faq_var
            content = content[:fm_match.start(2)] + new_fm + content[fm_match.start(3):]
            
            # Also need to add schema prop to SiteLayout tag if not present
            if 'schema=' not in content and 'schema =' not in content:
                # Find the SiteLayout tag and add schema prop
                layout_match = re.search(r'(<SiteLayout\s[^>]*?)(/?>)', content)
                if layout_match:
                    content = content[:layout_match.end(1)] + ' schema={schema}' + content[layout_match.start(2):]
            
            with open(filepath, 'w') as f:
                f.write(content)
            return True
    
    return False


def main():
    modified = 0
    skipped = 0
    no_pairs = 0
    total_pairs = 0
    
    for astro_file in sorted(SITES_DIR.rglob("*.astro")):
        # Skip dynamic routes
        if '[' in astro_file.name:
            continue
        
        content = astro_file.read_text()
        
        # Skip if already has FAQPage
        if 'FAQPage' in content:
            continue
        
        # Check if has FAQ content
        has_faq = any([
            'faq-item' in content,
            'faq-section' in content,
            'faq_item' in content,
            'faq-question' in content,
            'faq-q' in content,
            bool(re.search(r'Frequently Asked', content, re.IGNORECASE)),
            bool(re.search(r'<details[^>]*>.*?<summary', content, re.DOTALL)),
        ])
        
        if not has_faq:
            continue
        
        # Extract FAQ pairs
        pairs = extract_all_faq_pairs(content)
        
        if not pairs:
            no_pairs += 1
            skipped += 1
            continue
        
        faq_schema = make_faq_schema(pairs)
        
        if add_schema_to_page(astro_file, content, faq_schema):
            modified += 1
            total_pairs += len(pairs)
            print(f"  ✅ {astro_file.relative_to(SITES_DIR)} ({len(pairs)} Q&A pairs)")
        else:
            skipped += 1
            print(f"  ⚠️ {astro_file.relative_to(SITES_DIR)} - could not add schema")
    
    print(f"\n📊 Results:")
    print(f"  Modified: {modified} pages")
    print(f"  Total Q&A pairs added: {total_pairs}")
    print(f"  Skipped (no pairs extracted): {no_pairs}")
    print(f"  Skipped (other): {skipped - no_pairs}")


if __name__ == "__main__":
    main()
