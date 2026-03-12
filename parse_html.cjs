const fs = require('fs');

const html = fs.readFileSync('public/sites/siliconbased/dns-lookup.html', 'utf8');

const titleMatch = html.match(/<title>(.*?)<\/title>/is);
const title = titleMatch ? titleMatch[1] : '';

const descMatch = html.match(/<meta\s+name="description"\s+content="(.*?)">/is);
const description = descMatch ? descMatch[1] : '';

const canonicalMatch = html.match(/<link\s+rel="canonical"\s+href="(.*?)">/is);
const canonical = canonicalMatch ? canonicalMatch[1] : '';

const schemas = [];
const schemaRegex = /<script\s+type="application\/ld\+json">(.*?)<\/script>/igs;
let match;
while ((match = schemaRegex.exec(html)) !== null) {
  schemas.push(JSON.parse(match[1].trim()));
}

const styleMatch = html.match(/<style>(.*?)<\/style>/is);
let styleContent = styleMatch ? styleMatch[1] : '';

// Remove basic resets to match layout
styleContent = styleContent.replace(/\*\s*\{[^}]*\}\s*/, '');
styleContent = styleContent.replace(/body\s*\{[^}]*\}\s*/, '');

const mainMatch = html.match(/<main>(.*?)<\/main>/is);
const mainContent = mainMatch ? mainMatch[0] : '';

// Find the interactive script (skip the gtag script and schema scripts)
const scripts = html.match(/<script>(.*?)<\/script>/igs) || [];
let scriptContent = '';
for (const s of scripts) {
  if (s.includes('dataLayer') || s.includes('application/ld+json')) continue;
  scriptContent = s;
}

const astroContent = `---
import SiteLayout from '../../../layouts/SiteLayout.astro';

const schemas = ${JSON.stringify(schemas, null, 2)};
---

<SiteLayout
  site="siliconbased"
  title="${title}"
  description="${description}"
  canonical="${canonical}"
  schema={schemas}
>
  <style>
${styleContent}
  </style>

${mainContent}

${scriptContent}
</SiteLayout>
`;

fs.writeFileSync('src/pages/sites/siliconbased/dns-lookup.astro', astroContent);
console.log('Astro page updated successfully.');
