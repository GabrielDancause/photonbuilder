#!/usr/bin/env node
/**
 * Refactor siliconbased Astro pages from htmlContent template literal pattern
 * to native Astro component syntax.
 */

import fs from 'fs';
import path from 'path';

const DIR = 'src/pages/sites/siliconbased';
const files = fs.readdirSync(DIR).filter(f => f.endsWith('.astro'));

let processed = 0;
let skipped = 0;
const errors = [];

for (const file of files) {
  const filePath = path.join(DIR, file);
  const content = fs.readFileSync(filePath, 'utf8');

  // Skip files that don't use the htmlContent pattern
  if (!content.includes('const htmlContent = `')) {
    console.log(`SKIP: ${file} (no htmlContent pattern)`);
    skipped++;
    continue;
  }

  try {
    const result = transform(content, file);
    fs.writeFileSync(filePath, result);
    processed++;
    console.log(`OK: ${file}`);
  } catch (e) {
    errors.push({ file, error: e.message });
    console.error(`ERROR: ${file} — ${e.message}`);
  }
}

console.log(`\nDone: ${processed} processed, ${skipped} skipped, ${errors.length} errors`);
if (errors.length) {
  console.log('Errors:', errors);
}

function transform(content, fileName) {
  // 1. Split into frontmatter and template section
  // The file structure is:
  //   ---
  //   ...frontmatter...
  //   const htmlContent = `...`;
  //   ---
  //   <SiteLayout ...>
  //     <Fragment set:html={htmlContent} />
  //   </SiteLayout>

  // Find the htmlContent template literal
  const htmlContentStart = content.indexOf("const htmlContent = `");
  if (htmlContentStart === -1) throw new Error('No htmlContent found');

  // Find the end of the template literal: it ends with `;\n---
  // We need to find the closing backtick+semicolon that ends the template literal
  // The tricky part: there may be escaped backticks (\`) inside
  const templateStart = htmlContentStart + "const htmlContent = `".length;

  // Parse through the template literal character by character to find the unescaped closing backtick
  let i = templateStart;
  while (i < content.length) {
    if (content[i] === '\\' && i + 1 < content.length) {
      i += 2; // skip escaped character
      continue;
    }
    if (content[i] === '`') {
      break; // found the closing backtick
    }
    i++;
  }

  if (i >= content.length) throw new Error('Could not find end of template literal');

  const templateEnd = i; // position of closing backtick
  let htmlRaw = content.substring(templateStart, templateEnd);

  // 2. Unescape template literal escapes
  // \` -> `
  // \$ -> $ (for ${...} expressions that were escaped)
  // \\ -> \ (escaped backslashes)
  // But we need to be careful about the order
  htmlRaw = unescapeTemplateLiteral(htmlRaw);

  // 3. Get the frontmatter before htmlContent
  const frontmatterBefore = content.substring(0, htmlContentStart).trimEnd();

  // 4. Get the SiteLayout section after the closing ---
  // Find the closing --- after the template literal
  const afterTemplate = content.substring(templateEnd + 1); // skip the closing backtick
  // Should be ";\n---\n\n<SiteLayout..."
  const closingFenceMatch = afterTemplate.match(/^;\s*\n---\s*\n/);
  if (!closingFenceMatch) throw new Error('Could not find closing --- after template literal');

  const siteLayoutSection = afterTemplate.substring(closingFenceMatch[0].length);

  // 5. Parse the SiteLayout opening tag
  const siteLayoutMatch = siteLayoutSection.match(/(<SiteLayout[\s\S]*?>)\s*\n\s*<Fragment set:html=\{htmlContent\} \/>\s*\n<\/SiteLayout>/);
  if (!siteLayoutMatch) throw new Error('Could not find SiteLayout/Fragment pattern');

  const siteLayoutOpenTag = siteLayoutMatch[1];

  // 6. Extract <style>, <script>, and HTML from htmlRaw
  const { styles, scripts, html } = extractParts(htmlRaw);

  // 7. Rebuild the file
  let output = '';
  output += frontmatterBefore + '\n';
  output += '---\n\n';
  output += siteLayoutOpenTag + '\n';
  output += html + '\n';

  // Add scripts with is:inline
  for (const script of scripts) {
    output += `<script is:inline>${script}</script>\n`;
  }

  // Add styles
  for (const style of styles) {
    output += `<style>${style}</style>\n`;
  }

  output += '</SiteLayout>\n';

  return output;
}

function unescapeTemplateLiteral(str) {
  // Process escape sequences that are specific to template literals
  // We need to handle: \` -> `, \$ -> $, \\ -> \
  // But NOT other escape sequences that are part of the JavaScript code
  // (like \n, \t inside strings in <script> tags)
  //
  // Actually, in a JS template literal, the only special escapes are:
  // \` (escaped backtick) and \$ (escaped dollar sign, to prevent ${} interpolation)
  // Standard string escapes like \n, \t are also processed but those would already
  // be the intended characters in the HTML output.
  //
  // For our case: we're extracting content that was inside a template literal.
  // The escaped characters we need to convert:
  // \` -> ` (backtick that was escaped to not end the template)
  // \$ -> $ (dollar sign that was escaped to prevent interpolation)
  //   Actually \${} specifically - but \$ alone also needs unescaping
  // \\ -> \ (escaped backslash)

  let result = '';
  for (let i = 0; i < str.length; i++) {
    if (str[i] === '\\' && i + 1 < str.length) {
      const next = str[i + 1];
      if (next === '`' || next === '$' || next === '\\') {
        result += next;
        i++;
        continue;
      }
    }
    result += str[i];
  }
  return result;
}

function extractParts(html) {
  const styles = [];
  const scripts = [];

  // Extract all <style>...</style> blocks
  let remaining = html;

  // Extract styles (usually at the beginning)
  remaining = remaining.replace(/<style>([\s\S]*?)<\/style>/g, (match, inner) => {
    styles.push(inner);
    return '';
  });

  // Extract scripts
  remaining = remaining.replace(/<script>([\s\S]*?)<\/script>/g, (match, inner) => {
    scripts.push(inner);
    return '';
  });

  // Trim the remaining HTML
  remaining = remaining.trim();

  return { styles, scripts, html: remaining };
}
