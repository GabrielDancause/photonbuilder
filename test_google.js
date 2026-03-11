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
   const {status, data} = await fetch('https://www.google.com/search?q=wordpress+features+satisfaction+rating+2024');
   const $ = cheerio.load(data);
   console.log("Status:", status);
   console.log("Text snippet:", $('body').text().substring(0, 500).replace(/\s+/g, ' '));
}
run();
