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
   // W3techs provides a small list of "Market Position"
   // and "Satisfaction" scores are available from a known static domain for tech metrics: trustradius

   const res = await fetch("https://www.capterra.com/website-builder-software/");
   console.log("Capterra:", res.status);

   const res2 = await fetch("https://www.g2.com/categories/website-builder");
   console.log("G2:", res2.status);
}
run();
