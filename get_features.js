import https from 'https';
import * as cheerio from 'cheerio';

function fetch(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve({status: res.statusCode, data}));
    }).on('error', reject);
  });
}

async function run() {
   const urls = {
       "WordPress": "https://en.wikipedia.org/wiki/WordPress",
       "Shopify": "https://en.wikipedia.org/wiki/Shopify",
       "Wix": "https://en.wikipedia.org/wiki/Wix.com",
       "Squarespace": "https://en.wikipedia.org/wiki/Squarespace",
       "Webflow": "https://en.wikipedia.org/wiki/Webflow"
   };

   for (let [name, url] of Object.entries(urls)) {
       const {status, data} = await fetch(url);
       if (status === 200) {
           const $ = cheerio.load(data);
           let p = '';
           $('.mw-parser-output > p').each((i, el) => {
               const text = $(el).text().trim();
               if(text.length > 100) {
                   p += text + ' ';
                   if(p.length > 250) return false;
               }
           });
           console.log(`\n--- ${name} ---\n${p.substring(0, 300).replace(/\n/g, ' ')}...`);
       }
   }
}
run();
