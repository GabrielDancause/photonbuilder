#!/bin/bash

set -e

echo "🚀 PhotonBuilder Build Verification"
echo "=================================="

# Clean previous build
echo "🧹 Cleaning previous build..."
rm -rf dist

# Run Astro build
echo "🏗️  Running Astro build..."
npx astro build

echo ""
echo "✅ Build completed! Verifying..."
echo ""

# Check if dist directory exists
if [ ! -d "dist" ]; then
  echo "❌ dist directory not found!"
  exit 1
fi

# Check if _worker.js exists in dist
if [ ! -f "dist/_worker.js" ]; then
  echo "❌ _worker.js not found in dist!"
  exit 1
else
  echo "✅ _worker.js found in dist/"
fi

# Check if sites/firemaths directory exists in dist
if [ ! -d "dist/sites/firemaths" ]; then
  echo "❌ dist/sites/firemaths directory not found!"
  exit 1
else
  echo "✅ dist/sites/firemaths/ directory exists"
fi

# Count HTML files in dist/sites/firemaths
HTML_COUNT=$(find dist/sites/firemaths -name "*.html" | wc -l)
echo "📄 Found ${HTML_COUNT} HTML files in dist/sites/firemaths/"

# Check if sitemap.xml exists
if [ -f "dist/sites/firemaths/sitemap.xml" ]; then
  echo "✅ sitemap.xml found in dist/sites/firemaths/"
else
  echo "⚠️  sitemap.xml not found in dist/sites/firemaths/"
fi

# Check a sample HTML file exists
if [ -f "dist/sites/firemaths/401k-calculator/index.html" ]; then
  echo "✅ Sample file (401k-calculator.html) found"
else
  echo "❌ Sample file (401k-calculator.html) not found!"
  exit 1
fi

echo ""
echo "🎉 Build verification successful!"
echo ""
echo "📊 Summary:"
echo "  - HTML files: ${HTML_COUNT}"
echo "  - Worker: ✅"
echo "  - Sitemap: $([ -f "dist/sites/firemaths/sitemap.xml" ] && echo "✅" || echo "❌")"
echo ""
echo "🌍 Sites configured for domain routing:"
echo "  - firemaths.info → /sites/firemaths/"
echo "  - siliconbased.dev → /sites/siliconbased/"
echo "  - westmountfundamentals.com → /sites/westmount/"
echo "  - 28grams.vip → /sites/28grams/"
echo "  - migratingmammals.com → /sites/migratingmammals/"
echo "  - leeroyjenkins.quest → /sites/leeroyjenkins/"
echo "  - ijustwantto.live → /sites/ijustwantto/"
echo ""
echo "🚀 Ready to deploy to Cloudflare Pages!"