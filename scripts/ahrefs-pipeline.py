#!/usr/bin/env python3
"""
Ahrefs Keyword Pipeline v2
- Handles both UTF-8/comma and UTF-16/tab formats
- Per-keyword site assignment (not per-file)
- Scores, clusters, outputs build queue per site
"""

import csv
import os
import json
import re
import math
import sys
from pathlib import Path
from collections import defaultdict

RAW_DIR = Path(__file__).parent.parent / "data/seo/ahrefs/raw"
OUT_DIR = Path(__file__).parent.parent / "data/seo/ahrefs"
SITES_DIR = Path(__file__).parent.parent / "src/pages/sites"

# ── Site topic fingerprints ──
# Each keyword gets scored against ALL sites, assigned to best match
SITE_FINGERPRINTS = {
    "westmount": {
        "keywords": [
            "stock", "stocks", "etf", "etfs", "dividend", "dividends", "investing",
            "portfolio", "s&p 500", "sp500", "nasdaq", "dow jones", "market cap",
            "intrinsic value", "dcf", "pe ratio", "eps", "revenue", "earnings",
            "bull market", "bear market", "short interest", "short squeeze",
            "options trading", "put option", "call option", "hedge fund",
            "index fund", "mutual fund", "roth ira", "401k", "brokerage",
            "margin", "leverage", "volatility", "vix", "beta", "alpha",
            "buyback", "insider trading", "ipo", "spac", "reit",
            "equity", "equities", "bond", "bonds", "treasury", "yield",
            "valuation", "book value", "ebitda", "debt to equity",
            "return on equity", "roi", "economic moat", "large cap",
            "small cap", "mid cap", "growth stock", "value stock",
            "sector", "thematic", "expense ratio", "asset management",
            "financial statement", "balance sheet", "income statement",
            "depreciation", "amortization", "inflation", "interest rate",
            "trading fees", "broker", "ticker",
        ],
        "negative": ["gaming", "recipe", "cooking", "health", "medical", "car ", "auto"],
    },
    "firemaths": {
        "keywords": [
            "mortgage calculator", "compound interest", "tax calculator", "tax bracket",
            "retirement calculator", "investment calculator", "loan calculator",
            "amortization calculator", "budget", "net worth calculator", "savings",
            "apr calculator", "annuity", "fire calculator", "401k calculator",
            "529 calculator", "home insurance", "car insurance calculator",
            "debt payoff", "refinance", "down payment", "closing cost",
            "property tax", "cap rate", "rental yield", "cash flow",
            "lease vs buy", "cost of living calculator", "paycheck calculator",
            "salary calculator", "hourly to salary", "tip calculator",
        ],
        "negative": ["gaming", "recipe", "medical"],
    },
    "siliconbased": {
        "keywords": [
            "css framework", "api testing tool", "json formatter", "regex tester", "cron generator",
            "git command", "docker tutorial", "web hosting comparison", "ssl certificate", "dns lookup", "http status code",
            "developer tool", "dev tool", "code editor", "ide comparison",
            "javascript tutorial", "python tutorial", "html generator", "css generator", "typescript",
            "npm package", "webpack config", "vite",
            "favicon generator", "sitemap generator", "robots.txt generator", "seo tool",
            "chmod calculator", "linux command", "terminal command", "shell script",
            "color picker", "hex to rgb", "base64 encode", "url encode",
            "markdown editor", "yaml validator", "csv parser", "xml formatter",
        ],
        "negative": ["gaming", "recipe", "medical", "stock", "dividend", "digital marketing", "company list", "baby shower"],
    },
    "leeroyjenkins": {
        "keywords": [
            "gaming mouse", "gaming headset", "gaming monitor", "gaming keyboard",
            "gaming chair", "gaming desk", "gaming pc", "gaming laptop",
            "fps", "aim trainer", "sensitivity", "dpi", "polling rate",
            "gpu", "graphics card", "benchmark", "frame rate", "refresh rate",
            "streaming setup", "obs", "twitch", "game settings",
            "esports", "competitive", "fortnite", "valorant", "cs2",
            "call of duty", "warzone", "apex legends", "overwatch",
            "minecraft", "roblox", "steam", "xbox", "playstation", "nintendo",
            "rgb", "mechanical keyboard", "mousepad", "headphone",
            "best gaming", "budget gaming",
        ],
        "negative": ["recipe", "medical", "stock", "dividend", "mortgage"],
    },
    "bodycount": {
        "keywords": [
            "bmi calculator", "bmr calculator", "body fat", "calorie calculator",
            "blood pressure", "heart rate", "macro calculator", "ideal weight",
            "hydration calculator", "water intake", "protein calculator",
            "tdee calculator", "body mass", "waist to hip", "bac calculator",
            "a1c calculator", "cholesterol", "blood sugar", "glucose",
            "sleep calculator", "ovulation calculator", "pregnancy",
            "due date", "body type", "metabolism", "resting heart rate",
            "vo2 max", "lean body mass", "body water",
            "health calculator", "fitness calculator", "weight loss",
            "calories burned", "exercise", "workout",
        ],
        "negative": ["gaming", "recipe", "stock", "dividend", "car ", "sourdough", "bread", "dough", "pizza"],
    },
    "28grams": {
        "keywords": [
            "recipe", "cooking", "baking", "sourdough", "bread",
            "pizza dough", "hydration", "smoke point", "cooking temperature",
            "nutrition", "calories in", "food", "meal prep", "air fryer",
            "instant pot", "slow cooker", "grill", "bbq",
            "substitut", "conversion", "cup to gram", "tablespoon",
            "baker percentage", "yeast", "flour", "sugar",
            "avocado", "chicken", "beef", "fish", "vegetarian", "vegan",
            "spice", "herb", "sauce", "marinade",
        ],
        "negative": ["gaming", "stock", "medical", "car ", "coding"],
    },
    "migratingmammals": {
        "keywords": [
            "digital nomad", "nomad visa", "cost of living abroad", "expat",
            "travel insurance", "travel credit card", "best city for nomad",
            "coworking space", "remote work abroad", "visa requirements",
            "airport code", "backpacking", "luggage", "packing list",
            "time zone converter", "currency convert",
            "thailand visa", "bali visa", "portugal visa", "mexico visa", "colombia visa",
            "long term stay", "apartment rental abroad", "coliving",
        ],
        "negative": ["gaming", "recipe", "stock", "medical", "dividend", "etf", "equity", "bond", "fund"],
    },
    "sendnerds": {
        "keywords": [
            "gpa calculator", "grade calculator", "sat score", "act score",
            "study guide", "citation generator", "word counter", "reading level",
            "scholarship calculator", "college admission", "university ranking", "school grade",
            "test score calculator", "exam grade", "quiz score", "homework help", "essay",
            "apush score", "ap exam score", "math problem", "statistics calculator",
            "average calculator", "percentage calculator", "fraction calculator",
            "standard deviation calculator", "probability calculator",
        ],
        "negative": ["gaming", "recipe", "stock", "medical", "car ", "body fat", "calorie", "bmi", "bmr", "heart rate", "blood", "weight"],
    },
    "ijustwantto": {
        "keywords": [
            "concrete calculator", "btu calculator", "paint calculator",
            "flooring calculator", "fence calculator", "solar panel",
            "electrical", "plumbing", "roofing", "lumber",
            "square footage", "cubic yard", "gravel calculator",
            "mulch calculator", "drywall", "tile", "carpet",
            "home improvement", "diy", "renovation", "remodel",
            "bathroom", "kitchen", "deck", "patio",
            "circumference", "area calculator", "volume calculator",
        ],
        "negative": ["gaming", "recipe", "stock", "medical"],
    },
    "justonemoment": {
        "keywords": [
            "online timer", "countdown timer", "stopwatch online", "pomodoro timer",
            "interval timer", "meditation timer", "workout timer",
            "alarm clock", "minute timer", "hour timer", "second timer",
            "tabata timer", "hiit timer", "egg timer", "sleep timer",
        ],
        "negative": ["gaming", "recipe", "stock", "medical", "calculator", "timeshare", "growth chart", "roi", "bible", "beard", "hair", "vegetable"],
    },
    "nookienook": {
        "keywords": [
            "birth control", "condom guide", "sti testing", "std testing", "sexual health",
            "reproductive health", "fertility tracker", "menstrual cycle", "period tracker",
            "pelvic floor exercise", "sexual wellness", "lubricant guide", "libido",
            "orgasm", "intimacy", "contraceptive", "hpv vaccine", "herpes",
            "pregnancy test", "ovulation calculator", "bra size calculator", "cup size",
        ],
        "negative": ["gaming", "recipe", "stock", "car ", "pentest", "software test", "company list", "calorie", "roofing", "logistics", "streaming"],
    },
    "papyruspeople": {
        "keywords": [
            "font generator", "text converter", "unicode", "ascii art",
            "binary translator", "morse code", "cipher", "text formatter",
            "character counter", "fancy text", "zalgo", "cursive text",
            "small text", "bold text", "italic text", "strikethrough",
            "emoji", "symbol", "special character",
        ],
        "negative": ["gaming", "recipe", "stock", "medical"],
    },
    "eeniemeenie": {
        "keywords": [
            "random generator", "wheel spinner", "name picker",
            "coin flip", "dice roller", "decision maker",
            "random team", "lottery number", "random number",
            "spin the wheel", "picker", "chooser", "randomizer",
            "yes or no", "magic 8 ball",
        ],
        "negative": ["gaming", "recipe", "stock", "medical"],
    },
    "getthebag": {
        "keywords": [
            "salary", "resume", "job interview", "remote job",
            "career", "cover letter", "linkedin", "job search",
            "negotiat", "promotion", "raise", "freelance",
            "side hustle", "passive income", "career change",
            "work from home", "job board", "hiring",
        ],
        "negative": ["gaming", "recipe", "stock", "medical", "car "],
    },
    "fixitwithducttape": {
        "keywords": [
            "ai tool", "chatgpt", "ai writing", "ai image",
            "saas", "project management", "crm", "erp",
            "productivity app", "notion", "slack", "trello",
            "software review", "tool comparison", "alternative",
            "ai coding", "copilot", "automation", "no code", "low code",
            "ai video", "ai music", "ai voice",
        ],
        "negative": ["gaming", "recipe", "stock", "medical", "car "],
    },
    "pleasestartplease": {
        "keywords": [
            "car maintenance", "oil change", "tire pressure", "brake",
            "car insurance", "fuel economy", "mpg", "ev range",
            "obd2", "obd code", "check engine", "transmission",
            "car comparison", "car review", "best car",
            "horsepower", "torque", "towing capacity",
            "car payment", "auto loan", "lease",
            "motor oil", "coolant", "battery", "alternator",
        ],
        "negative": ["gaming", "recipe", "stock", "medical"],
    },
}


def detect_format(filepath):
    """Detect if file is UTF-8/comma or UTF-16/tab"""
    with open(filepath, "rb") as f:
        header = f.read(4)
        if header[:2] in (b'\xff\xfe', b'\xfe\xff'):
            return "utf-16", "\t"
    # Try UTF-8
    return "utf-8-sig", ","


def parse_csv(filepath):
    """Parse any Ahrefs CSV regardless of format"""
    encoding, delimiter = detect_format(filepath)
    keywords = []
    
    with open(filepath, "r", encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            try:
                # Handle quoted field names from tab-delimited exports
                def get(name):
                    return row.get(name, row.get(f'"{name}"', "")).strip().strip('"')
                
                kw = get("Keyword").lower()
                if not kw:
                    continue
                
                vol = int(get("Volume").replace(",", "") or 0)
                kd = int(get("Difficulty") or 0)
                cpc = float(get("CPC") or 0)
                tp = int(get("Traffic potential").replace(",", "") or 0)
                parent = get("Parent Keyword") or get("Parent Topic")
                intents = get("Intents")
                global_vol = int(get("Global volume").replace(",", "") or 0)
                
                # SERP-specific fields
                url = get("URL")
                position = get("Position")
                
                entry = {
                    "keyword": kw,
                    "volume": vol,
                    "kd": kd,
                    "cpc": cpc,
                    "traffic_potential": tp,
                    "parent": parent.lower(),
                    "intents": intents,
                    "global_volume": global_vol,
                }
                if url:
                    entry["serp_url"] = url
                if position:
                    entry["serp_position"] = position
                    
                keywords.append(entry)
            except (ValueError, KeyError):
                continue
    return keywords


def assign_site(keyword_text):
    """Assign a keyword to the best-matching site based on topic fingerprints"""
    kw = keyword_text.lower()
    
    scores = {}
    for site_id, fp in SITE_FINGERPRINTS.items():
        score = 0
        
        # Check negative keywords first (disqualifiers)
        for neg in fp.get("negative", []):
            if neg in kw:
                score -= 50
        
        # Score against positive keywords
        for term in fp["keywords"]:
            if term in kw:
                # Longer matches are more specific = worth more
                score += len(term)
        
        if score > 0:
            scores[site_id] = score
    
    if not scores:
        return None  # Unassigned
    
    # Return best match
    return max(scores, key=scores.get)


def get_existing_slugs():
    """Get existing page slugs per site"""
    slugs = {}
    if SITES_DIR.exists():
        for site_dir in SITES_DIR.iterdir():
            if site_dir.is_dir():
                site_slugs = set()
                for f in site_dir.glob("*.astro"):
                    if not f.name.startswith("["):
                        site_slugs.add(f.stem)
                slugs[site_dir.name] = site_slugs
    return slugs


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def score_keyword(kw, existing_slugs_for_site):
    vol = kw["volume"]
    kd = kw["kd"]
    cpc = kw["cpc"]
    tp = kw["traffic_potential"]
    
    vol_score = min(100, math.log10(max(vol, 1)) * 25) if vol > 0 else 0
    kd_score = max(0, 100 - kd)
    cpc_score = min(100, cpc * 20)
    tp_score = min(100, math.log10(max(tp, 1)) * 25) if tp > 0 else 0
    
    intent_bonus = 0
    intents = kw.get("intents", "").lower()
    if "commercial" in intents or "transactional" in intents:
        intent_bonus = 20
    
    gap_bonus = 0
    pos = kw.get("serp_position", "")
    if pos:
        try:
            p = float(pos)
            if 10 < p <= 30:
                gap_bonus = 30
            elif 30 < p <= 60:
                gap_bonus = 15
            elif p <= 10:
                gap_bonus = -50
        except ValueError:
            pass
    
    slug = slugify(kw["keyword"])
    if slug in existing_slugs_for_site:
        return -1
    
    score = (vol_score * 0.30) + (kd_score * 0.25) + (cpc_score * 0.15) + (tp_score * 0.15) + intent_bonus + gap_bonus
    return round(score, 1)


def suggest_page_type(kw):
    keyword = kw["keyword"]
    if any(w in keyword for w in ["calculator", "compute", "convert", "how much"]):
        return "calculator"
    elif any(w in keyword for w in ["best", "top", "list", "ranking"]):
        return "listicle"
    elif any(w in keyword for w in [" vs ", "versus", "compare", "comparison", "difference"]):
        return "comparison"
    elif any(w in keyword for w in ["what is", "what are", "how to", "guide", "meaning", "definition"]):
        return "educational"
    elif any(w in keyword for w in ["template", "example", "sample"]):
        return "template"
    return "educational"


def cluster_keywords(keywords, max_cluster_size=8):
    parent_groups = defaultdict(list)
    orphans = []
    
    for kw in keywords:
        parent = kw.get("parent", "")
        if parent and parent != kw["keyword"]:
            parent_groups[parent].append(kw)
        else:
            orphans.append(kw)
    
    clusters = []
    used = set()
    
    for parent, children in sorted(parent_groups.items(), key=lambda x: -sum(c["volume"] for c in x[1])):
        if parent in used:
            continue
        cluster_kws = [kw for kw in children if kw["keyword"] not in used][:max_cluster_size]
        if not cluster_kws:
            continue
        primary = max(cluster_kws, key=lambda x: x["volume"])
        cluster = {
            "primary": primary["keyword"],
            "slug": slugify(primary["keyword"]),
            "keywords": [kw["keyword"] for kw in cluster_kws],
            "total_volume": sum(kw["volume"] for kw in cluster_kws),
            "avg_kd": round(sum(kw["kd"] for kw in cluster_kws) / len(cluster_kws)),
            "max_cpc": max(kw["cpc"] for kw in cluster_kws),
            "score": max(kw.get("_score", 0) for kw in cluster_kws),
            "page_type": suggest_page_type(primary),
        }
        clusters.append(cluster)
        for kw in cluster_kws:
            used.add(kw["keyword"])
    
    for kw in orphans:
        if kw["keyword"] not in used and kw["volume"] >= 50:
            clusters.append({
                "primary": kw["keyword"],
                "slug": slugify(kw["keyword"]),
                "keywords": [kw["keyword"]],
                "total_volume": kw["volume"],
                "avg_kd": kw["kd"],
                "max_cpc": kw["cpc"],
                "score": kw.get("_score", 0),
                "page_type": suggest_page_type(kw),
            })
            used.add(kw["keyword"])
    
    return sorted(clusters, key=lambda x: -x["score"])


def main():
    print("📊 Ahrefs Keyword Pipeline v2 (per-keyword site assignment)")
    print("=" * 60)
    
    # 1. Parse all CSVs
    all_keywords = []
    file_count = 0
    format_stats = {"utf-8": 0, "utf-16": 0}
    
    for f in sorted(RAW_DIR.glob("*.csv")):
        file_count += 1
        enc, _ = detect_format(f)
        format_stats["utf-16" if "16" in enc else "utf-8"] += 1
        kws = parse_csv(f)
        all_keywords.extend(kws)
        if len(kws) > 0:
            print(f"  📄 {f.name}: {len(kws):,} kw ({enc})")
    
    print(f"\n  Total raw: {len(all_keywords):,} from {file_count} files")
    print(f"  Formats: {format_stats['utf-8']} UTF-8, {format_stats['utf-16']} UTF-16")
    
    # 2. Dedupe
    best = {}
    for kw in all_keywords:
        key = kw["keyword"]
        if key not in best or kw["volume"] > best[key]["volume"]:
            best[key] = kw
        elif kw["volume"] == best[key]["volume"] and kw.get("serp_url"):
            best[key].update({k: v for k, v in kw.items() if v})
    unique = list(best.values())
    print(f"  After dedupe: {len(unique):,} unique keywords")
    
    # 3. Assign to sites (per keyword!)
    site_keywords = defaultdict(list)
    unassigned = []
    
    for kw in unique:
        site = assign_site(kw["keyword"])
        if site:
            kw["assigned_site"] = site
            site_keywords[site].append(kw)
        else:
            unassigned.append(kw)
    
    print(f"\n  📍 Site assignment:")
    for site_id in sorted(site_keywords.keys()):
        count = len(site_keywords[site_id])
        vol = sum(kw["volume"] for kw in site_keywords[site_id])
        print(f"    {site_id:25s}: {count:>6,} keywords | {vol:>10,} total volume")
    print(f"    {'UNASSIGNED':25s}: {len(unassigned):>6,} keywords")
    
    # 4. Score & cluster per site
    existing_slugs = get_existing_slugs()
    all_queues = {}
    
    for site_id, kws in sorted(site_keywords.items()):
        site_existing = existing_slugs.get(site_id, set())
        
        scored = []
        skipped = 0
        for kw in kws:
            s = score_keyword(kw, site_existing)
            if s < 0:
                skipped += 1
                continue
            kw["_score"] = s
            scored.append(kw)
        
        clusters = cluster_keywords(scored)
        
        # Build queue for this site
        queue = []
        for c in clusters[:50]:  # Top 50 per site
            queue.append({
                "slug": c["slug"],
                "primary_keyword": c["primary"],
                "secondary_keywords": [k for k in c["keywords"] if k != c["primary"]][:5],
                "total_volume": c["total_volume"],
                "avg_kd": c["avg_kd"],
                "max_cpc": c["max_cpc"],
                "score": c["score"],
                "page_type": c["page_type"],
                "site": site_id,
                "status": "queued",
            })
        
        all_queues[site_id] = queue
        
        if clusters:
            print(f"\n  🏆 {site_id.upper()} — Top 10:")
            print(f"    {'#':>3} {'Score':>6} {'Vol':>8} {'KD':>4} {'Type':10} {'Keyword':<45}")
            for i, c in enumerate(clusters[:10], 1):
                print(f"    {i:>3} {c['score']:>6.1f} {c['total_volume']:>8,} {c['avg_kd']:>4} {c['page_type']:10} {c['primary'][:45]}")
    
    # 5. Save everything
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Combined build queue
    combined = []
    for site_id, queue in all_queues.items():
        combined.extend(queue)
    combined.sort(key=lambda x: -x["score"])
    
    queue_path = OUT_DIR / "build-queue-ahrefs.json"
    with open(queue_path, "w") as f:
        json.dump(combined, f, indent=2)
    
    # Per-site queues
    for site_id, queue in all_queues.items():
        if queue:
            site_dir = OUT_DIR / site_id
            site_dir.mkdir(exist_ok=True)
            with open(site_dir / "build-queue.json", "w") as f:
                json.dump(queue, f, indent=2)
    
    # Stats
    stats = {
        "generated": "2026-03-21",
        "total_raw": len(all_keywords),
        "unique_keywords": len(unique),
        "unassigned": len(unassigned),
        "files_parsed": file_count,
        "sites": {
            site_id: {
                "keywords": len(kws),
                "queue_items": len(all_queues.get(site_id, [])),
            }
            for site_id, kws in site_keywords.items()
        }
    }
    with open(OUT_DIR / "keyword-db.json", "w") as f:
        json.dump(stats, f, indent=2)
    
    # Unassigned keywords (for review)
    if unassigned:
        unassigned.sort(key=lambda x: -x["volume"])
        with open(OUT_DIR / "unassigned.json", "w") as f:
            json.dump([{"keyword": kw["keyword"], "volume": kw["volume"], "kd": kw["kd"]} 
                       for kw in unassigned[:500]], f, indent=2)
    
    print(f"\n{'=' * 60}")
    print(f"✅ Combined queue: {queue_path} ({len(combined)} items across {len(all_queues)} sites)")
    print(f"✅ Per-site queues in {OUT_DIR}/{{site}}/build-queue.json")
    if unassigned:
        print(f"⚠️  {len(unassigned)} unassigned keywords saved to unassigned.json (top 500 by volume)")


if __name__ == "__main__":
    main()
