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
      // photonbuilder.com or unknown — serve from root
      return env.ASSETS.fetch(request);
    }

    // Build rewritten paths to try
    const pathname = url.pathname;
    const base = `/sites/${site}`;
    const candidates = [];

    if (pathname === '/' || pathname === '') {
      candidates.push(`${base}/index.html`);
    } else {
      candidates.push(`${base}${pathname}`);
      if (!pathname.endsWith('.html') && !pathname.includes('.')) {
        candidates.push(`${base}${pathname}.html`);
        candidates.push(`${base}${pathname}/index.html`);
      }
    }

    for (const path of candidates) {
      // Create a clean new URL — don't carry over original request URL
      const assetUrl = new URL(path, url.origin);
      const assetReq = new Request(assetUrl.toString(), {
        method: request.method,
        headers: request.headers,
      });

      const resp = await env.ASSETS.fetch(assetReq);

      if (resp.status === 301 || resp.status === 302) {
        // Cloudflare is trying to redirect — follow it internally
        const loc = resp.headers.get('Location');
        if (loc) {
          const locUrl = new URL(loc, url.origin);
          const followReq = new Request(locUrl.toString(), {
            method: request.method,
            headers: request.headers,
          });
          const followResp = await env.ASSETS.fetch(followReq);
          if (followResp.ok) {
            // Return with original URL (no redirect visible to user)
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

    return new Response('Not Found', { status: 404 });
  }
};
