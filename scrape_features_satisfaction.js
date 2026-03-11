import https from 'https';

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
  try {
    const urls = [
      'https://api.github.com/repos/wordpress/wordpress',
      'https://api.github.com/repos/Shopify/liquid',
      'https://api.github.com/repos/wix/react-native-navigation'
    ];
    for(const u of urls) {
       const res = await fetch(u);
       console.log(u, res.status);
    }
  } catch (e) {
    console.error(e);
  }
}
run();
