function getMimeType(path) {
  const ext = path.split('.').pop()?.toLowerCase();
  const types = {
    'html': 'text/html; charset=utf-8',
    'css': 'text/css; charset=utf-8',
    'js': 'application/javascript; charset=utf-8',
    'json': 'application/json; charset=utf-8',
    'xml': 'application/xml; charset=utf-8',
    'svg': 'image/svg+xml',
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'gif': 'image/gif',
    'webp': 'image/webp',
    'woff2': 'font/woff2',
    'woff': 'font/woff',
    'ttf': 'font/ttf',
    'ico': 'image/x-icon',
    'txt': 'text/plain; charset=utf-8',
  };
  return types[ext] || null;
}

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
      'thenookienook.com': 'nookienook',
      'www.thenookienook.com': 'nookienook',
      'montrealjobs.photonbuilder.com': 'montrealjobs',
    };

    const site = SITE_MAP[host];

    if (!site) {
      return env.ASSETS.fetch(request);
    }

    const pathname = url.pathname;
    const base = `/sites/${site}`;
    const hasExtension = pathname.includes('.');

    // Astro assets (CSS, JS) — try root /_astro/ first, then site-specific /sites/<site>/_astro/
    if (pathname.startsWith('/_astro/')) {
      // Try root first (shared Astro build assets)
      const rootResp = await env.ASSETS.fetch(new URL(pathname, url.origin).toString());
      if (rootResp.ok) {
        const headers = new Headers(rootResp.headers);
        const mime = getMimeType(pathname);
        if (mime) headers.set('Content-Type', mime);
        headers.set('Cache-Control', 'public, max-age=31536000, immutable');
        return new Response(rootResp.body, { status: rootResp.status, headers });
      }
      // Fall back to site-specific assets (legacy per-site Astro builds)
      const siteResp = await env.ASSETS.fetch(new URL(`${base}${pathname}`, url.origin).toString());
      if (siteResp.ok) {
        const headers = new Headers(siteResp.headers);
        const mime = getMimeType(pathname);
        if (mime) headers.set('Content-Type', mime);
        headers.set('Cache-Control', 'public, max-age=31536000, immutable');
        return new Response(siteResp.body, { status: siteResp.status, headers });
      }
    }

    // Simple rewrite: prefix with /sites/<site>/
    let assetPath;

    if (pathname === '/' || pathname === '') {
      assetPath = `${base}/index.html`;
    } else if (pathname.endsWith('/')) {
      assetPath = `${base}${pathname}index.html`;
    } else {
      assetPath = `${base}${pathname}`;
    }

    // Fetch the rewritten asset
    const assetUrl = new URL(assetPath, url.origin);
    assetUrl.search = url.search;
    const resp = await env.ASSETS.fetch(assetUrl.toString());

    if (resp.ok) {
      const headers = new Headers(resp.headers);
      const mime = getMimeType(assetPath);
      if (mime) headers.set('Content-Type', mime);
      if (!hasExtension || assetPath.endsWith('.html')) {
        headers.set('Cache-Control', 'public, max-age=0, must-revalidate');
      }
      return new Response(resp.body, { status: resp.status, headers });
    }

    // If no extension, try .html and /index.html
    if (!hasExtension) {
      for (const suffix of ['.html', '/index.html']) {
        const tryPath = `${base}${pathname}${suffix}`;
        const tryResp = await env.ASSETS.fetch(new URL(tryPath, url.origin).toString());
        if (tryResp.ok) {
          const headers = new Headers(tryResp.headers);
          headers.set('Content-Type', 'text/html; charset=utf-8');
          headers.set('Cache-Control', 'public, max-age=0, must-revalidate');
          return new Response(tryResp.body, { status: tryResp.status, headers });
        }
      }
    }

    return new Response('Not Found', { status: 404 });
  }
};
