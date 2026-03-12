const SITE_MAP = {
  'firemaths.info': 'firemaths',
  'www.firemaths.info': 'firemaths',
  'siliconbased.dev': 'siliconbased',
  'www.siliconbased.dev': 'siliconbased',
  'westmountfundamentals.com': 'westmount',
  'www.westmountfundamentals.com': 'westmount',
  '28grams.vip': '28grams',
  'www.28grams.vip': '28grams',
  'migratingmammals.com': 'migratingmammals',
  'leeroyjenkins.quest': 'leeroyjenkins',
  'ijustwantto.live': 'ijustwantto',
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const host = url.hostname;
    const site = SITE_MAP[host];
    
    if (site) {
      // Rewrite to site subfolder
      const newPath = `/sites/${site}${url.pathname}`;
      // Try the exact path first, then with .html, then index.html
      const attempts = [
        newPath,
        newPath.endsWith('/') ? newPath + 'index.html' : newPath + '.html',
      ];
      
      for (const path of attempts) {
        const newUrl = new URL(path, url.origin);
        newUrl.search = url.search;
        const response = await env.ASSETS.fetch(new Request(newUrl, request));
        if (response.status !== 404) return response;
      }
      
      // 404 fallback
      return new Response('Not Found', { status: 404 });
    }
    
    // Default: serve photonbuilder.com content from root
    return env.ASSETS.fetch(request);
  }
};