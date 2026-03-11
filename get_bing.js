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
   const urls = [
       "https://www.forbes.com/advisor/business/software/best-website-builders/",
       "https://www.techradar.com/best/website-builder",
       "https://www.pcmag.com/picks/the-best-website-builders"
   ];

   for (let u of urls) {
     try {
       const {status, data} = await fetch(u);
       console.log(`URL: ${u} - Status: ${status}`);
       if (status === 200) {
           const $ = cheerio.load(data);
           console.log($('body').text().substring(0, 500).replace(/\s+/g, ' '));
       }
     } catch(e) {}
   }
}
run();
