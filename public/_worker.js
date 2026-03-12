export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const host = url.hostname;

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
      'www.migratingmammals.com': 'migratingmammals',
      'leeroyjenkins.quest': 'leeroyjenkins',
      'www.leeroyjenkins.quest': 'leeroyjenkins',
      'ijustwantto.live': 'ijustwantto',
      'www.ijustwantto.live': 'ijustwantto',
    };

    const site = SITE_MAP[host];

    if (!site) {
      return env.ASSETS.fetch(request);
    }

    const pathname = url.pathname;
    const base = `/sites/${site}`;

    // ALL requests for a mapped domain get rewritten to /sites/<site>/
    // This handles HTML, CSS, JS, images, fonts — everything
    const candidates = [];

    if (pathname === '/' || pathname === '') {
      candidates.push(`${base}/index.html`);
    } else {
      // Try exact path first (handles .html, .css, .js, .xml, images, etc.)
      candidates.push(`${base}${pathname}`);
      // If no extension, try adding .html or /index.html
      if (!pathname.includes('.')) {
        candidates.push(`${base}${pathname}.html`);
        candidates.push(`${base}${pathname}/index.html`);
      }
    }

    for (const path of candidates) {
      const assetUrl = new URL(path, url.origin);
      assetUrl.search = url.search;
      const assetReq = new Request(assetUrl.toString(), {
        method: request.method,
        headers: request.headers,
      });

      const resp = await env.ASSETS.fetch(assetReq);

      if (resp.status === 301 || resp.status === 302) {
        const loc = resp.headers.get('Location');
        if (loc) {
          const locUrl = new URL(loc, url.origin);
          const followReq = new Request(locUrl.toString(), {
            method: request.method,
            headers: request.headers,
          });
          const followResp = await env.ASSETS.fetch(followReq);
          if (followResp.ok) {
            return new Response(followResp.body, {
              status: followResp.status,
              headers: followResp.headers,
            });
          }
        }
        continue;
      }

      if (resp.ok) {
        return resp;
      }
    }

    // Fallback: try serving from root (for shared assets like fonts)
    return env.ASSETS.fetch(request);
  }
};
