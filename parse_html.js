import fs from 'fs';
import path from 'path';

function processFile(htmlPath, astroPath) {
  const html = fs.readFileSync(htmlPath, 'utf8');

  // Extract title
  const titleMatch = html.match(/<title>(.*?)<\/title>/);
  const title = titleMatch ? titleMatch[1] : '';

  // Extract description
  const descMatch = html.match(/<meta\s+name="description"\s+content="(.*?)"\s*\/?>/i);
  const description = descMatch ? descMatch[1] : '';

  // Extract canonical
  const canonicalMatch = html.match(/<link\s+rel="canonical"\s+href="(.*?)"\s*\/?>/i);
  const canonical = canonicalMatch ? canonicalMatch[1] : '';

  // Extract schemas
  const schemas = [];
  const schemaRegex = /<script\s+type="application\/ld\+json">([\s\S]*?)<\/script>/g;
  let match;
  while ((match = schemaRegex.exec(html)) !== null) {
    try {
      schemas.push(JSON.parse(match[1]));
    } catch (e) {
      console.error(`Error parsing schema in ${htmlPath}:`, e);
    }
  }

  // Extract main content
  // Usually between </nav> and <footer>
  const bodyMatch = html.match(/<\/nav>\s*([\s\S]*?)\s*<footer/i);
  let bodyContent = bodyMatch ? bodyMatch[1] : '';

  // Look for any scripts at the bottom that might be outside this match
  const footerMatch = html.match(/<\/footer>\s*([\s\S]*?)<\/body>/i);
  if (footerMatch) {
     const extraScripts = footerMatch[1];
     bodyContent += "\n" + extraScripts;
  }

  // Extract custom styles inside <style> that might be specific to this page
  let pageStyles = '';
  const styleMatch = html.match(/<style>([\s\S]*?)<\/style>/i);
  if (styleMatch) {
      let styleContent = styleMatch[1];
      pageStyles = `<style>\n${styleContent}\n</style>`;
  }

  // Handle { and } in body text for Astro, mostly in scripts but also inline HTML
  // Actually replacing raw { with {"{"} isn't always easy if it's inside style or script.
  // Astro <style> and <script is:inline> handles { naturally.
  // We just need to make sure we escape any script tags.

  // Generate astro component content
  let astroContent = `---
import SiteLayout from '../../../layouts/SiteLayout.astro';

const schemas = ${schemas.length > 0 ? JSON.stringify(schemas, null, 2) : '[]'};
---

<SiteLayout
  site="firemaths"
  title="${title.replace(/"/g, '\\"')}"
  description="${description.replace(/"/g, '\\"')}"
  canonical="${canonical}"
  schema={schemas.length > 0 ? schemas : undefined}
>
${pageStyles}

${bodyContent}
</SiteLayout>
`;

  // Fix up astro issues: script tags should have is:inline
  // Ensure we only replace starting <script> and not </script> or <script type="application/ld+json">
  astroContent = astroContent.replace(/<script\b(?![^>]*\btype="application\/ld\+json")[^>]*>/gi, match => {
    if (match.includes('is:inline')) return match;
    return match.replace(/<script/i, '<script is:inline');
  });

  // Fix the JSON example output if any page has raw { } not in script or style
  // To avoid breaking valid astro, we'll let astro compile it first. If it complains, we will fix.

  // Make sure we create directories
  fs.mkdirSync(path.dirname(astroPath), { recursive: true });
  fs.writeFileSync(astroPath, astroContent);
  console.log(`Processed ${htmlPath} -> ${astroPath}`);
}

const pages = [
  "inflation-calculator",
  "lease-buy",
  "list-brokerages",
  "list-budgeting-apps",
  "list-credit-cards",
  "list-savings-accounts",
  "loan-amortization-calculator",
  "loan-amortization",
  "mortgage-calculator",
  "net-income",
  "net-worth-calculator",
  "net-worth-tracker",
  "paycheck-budget-calculator",
  "paycheck-calculator",
  "present-value",
  "profit-margin",
  "rent-vs-buy-calculator",
  "rent-vs-buy",
  "rental-yield-calculator",
  "retirement-income-calculator"
];

for (const page of pages) {
  const htmlPath = `public/sites/firemaths/${page}.html`;
  const astroPath = `src/pages/sites/firemaths/${page}.astro`;
  processFile(htmlPath, astroPath);
}
