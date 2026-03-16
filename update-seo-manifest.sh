#!/bin/bash
# Regenerate CSV manifests for the SEO dashboard.
# Run after adding/removing CSVs in public/data/seo/*/csv/
# Usage: ./update-seo-manifest.sh

BASEDIR="$(cd "$(dirname "$0")" && pwd)/public/data/seo"

for domain_dir in "$BASEDIR"/*/; do
  csv_dir="${domain_dir}csv"
  [ -d "$csv_dir" ] || continue
  
  domain=$(basename "$domain_dir")
  manifest="${domain_dir}csv-manifest.json"
  
  # List all CSV files, output as JSON array
  (cd "$csv_dir" && ls *.csv 2>/dev/null) | python3 -c "
import sys, json
files = sorted([l.strip() for l in sys.stdin if l.strip()])
print(json.dumps(files, indent=2))
" > "$manifest"
  
  count=$(python3 -c "import json; print(len(json.load(open('$manifest'))))")
  echo "✓ $domain: $count CSVs → csv-manifest.json"
done

echo "Done. Commit & push to update the live dashboard."
