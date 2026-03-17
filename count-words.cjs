const fs = require('fs');

const fileContent = fs.readFileSync('src/pages/sites/westmount/stock-profit-calculator.astro', 'utf-8');

// Strip out frontmatter
let noFrontmatter = fileContent.replace(/---[\s\S]*?---/, '');

// Strip out <style> blocks
let noStyle = noFrontmatter.replace(/<style[\s\S]*?<\/style>/gi, '');

// Strip out <script> blocks
let noScript = noStyle.replace(/<script[\s\S]*?<\/script>/gi, '');

// Strip out HTML tags
let textContent = noScript.replace(/<[^>]*>?/gm, '');

// Strip out extraneous whitespace and newlines
let cleanText = textContent.replace(/\s+/g, ' ').trim();

// Count words
let wordCount = cleanText.split(' ').filter(word => word.length > 0).length;

console.log("True word count:", wordCount);
