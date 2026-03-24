const MIME_TYPES = {
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
  'bodycount.photonbuilder.com': 'bodycount',
  'www.bodycount.photonbuilder.com': 'bodycount',
  'sendnerds.photonbuilder.com': 'sendnerds',
  'www.sendnerds.photonbuilder.com': 'sendnerds',
  'justonemoment.photonbuilder.com': 'justonemoment',
  'www.justonemoment.photonbuilder.com': 'justonemoment',
  'getthebag.photonbuilder.com': 'getthebag',
  'www.getthebag.photonbuilder.com': 'getthebag',
  'fixitwithducttape.photonbuilder.com': 'fixitwithducttape',
  'www.fixitwithducttape.photonbuilder.com': 'fixitwithducttape',
  'papyruspeople.photonbuilder.com': 'papyruspeople',
  'www.papyruspeople.photonbuilder.com': 'papyruspeople',
  'eeniemeenie.photonbuilder.com': 'eeniemeenie',
  'www.eeniemeenie.photonbuilder.com': 'eeniemeenie',
  'trunkpress.photonbuilder.com': 'trunkpress',
  'www.trunkpress.photonbuilder.com': 'trunkpress',
  'pleasestartplease.photonbuilder.com': 'pleasestartplease',
  'www.pleasestartplease.photonbuilder.com': 'pleasestartplease',
};

// SEO redirects per site (from → to)
const REDIRECTS = {
  'westmount': {
    '/most-shorted-stocks-march-2026/': '/most-shorted-stocks/',
    '/most-shorted-stocks-march-2026': '/most-shorted-stocks/',
    '/short-squeeze-candidates-march-2026/': '/short-squeeze-candidates/',
    '/short-squeeze-candidates-march-2026': '/short-squeeze-candidates/',
    '/ceo-compensation.html': '/ceo-compensation/',
    '/fire-retirement-calculator.html': '/fire-retirement-calculator/',
    '/dividend-aristocrats-analysis-2026.html': '/dividend-aristocrats-analysis-2026/',
    '/guide-reading-financial-statements.html': '/guide-reading-financial-statements/',
    '/margin-calculator.html': '/margin-calculator/',
  },
  'siliconbased': {
    '/js-framework-sizes.html': '/js-framework-sizes/',
    '/crontab-guru.html': '/crontab-guru/',
    '/gitignore-generator.html': '/gitignore-generator/',
    '/cron-expression-generator.html': '/cron-expression-generator/',
    '/list-icon-sets.html': '/list-icon-sets/',
    '/favicon-generator.html': '/favicon-generator/',
    '/sitemap-generator.html': '/sitemap-generator/',
  },
};

// ⚡ Bolt: Extract static array to module scope to avoid reallocation on every request
const HTML_SUFFIXES = ['.html', '/index.html'];

const SUB_SITES = [
  'bodycount', 'sendnerds', 'justonemoment', 'getthebag',
  'fixitwithducttape', 'papyruspeople', 'eeniemeenie', 'pleasestartplease'
];

// ⚡ Bolt: Use Set for O(1) lookup
const SUB_SITES_SET = new Set(SUB_SITES);

// ⚡ Bolt: Use lastIndexOf instead of split().pop() to avoid array allocation on every request
function getMimeType(path) {
  const lastDot = path.lastIndexOf('.');
  if (lastDot === -1 || lastDot === path.length - 1) return null;
  const ext = path.slice(lastDot + 1).toLowerCase();
  return MIME_TYPES[ext] || null;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const host = url.hostname;

    const site = SITE_MAP[host];

    // For photonbuilder.com: check if path starts with a sub-site folder
    if (!site && (host === 'photonbuilder.com' || host === 'www.photonbuilder.com')) {
      // ⚡ Bolt: Extract first segment using indexOf/slice instead of split to avoid array allocation
      const secondSlash = url.pathname.indexOf('/', 1);
      const firstSegment = secondSlash === -1 ? url.pathname.slice(1) : url.pathname.slice(1, secondSlash);
      if (SUB_SITES_SET.has(firstSegment)) {
        // Rewrite /bodycount/foo → /sites/bodycount/foo
        const subPath = url.pathname.slice(firstSegment.length + 1) || '/';
        const base = `/sites/${firstSegment}`;
        let assetPath;
        if (subPath === '/' || subPath === '') {
          assetPath = `${base}/index.html`;
        } else if (subPath.endsWith('/')) {
          assetPath = `${base}${subPath}index.html`;
        } else {
          assetPath = `${base}${subPath}`;
        }
        const resp = await env.ASSETS.fetch(new URL(assetPath, url.origin).toString());
        if (resp.ok) {
          const headers = new Headers(resp.headers);
          const mime = getMimeType(assetPath);
          if (mime) headers.set('Content-Type', mime);
          headers.set('Cache-Control', 'public, max-age=0, must-revalidate');
          return new Response(resp.body, { status: resp.status, headers });
        }
        // Try .html and /index.html
        if (!subPath.includes('.')) {
          for (const suffix of HTML_SUFFIXES) {
            const tryPath = `${base}${subPath}${suffix}`;
            const tryResp = await env.ASSETS.fetch(new URL(tryPath, url.origin).toString());
            if (tryResp.ok) {
              const headers = new Headers(tryResp.headers);
              headers.set('Content-Type', 'text/html; charset=utf-8');
              headers.set('Cache-Control', 'public, max-age=0, must-revalidate');
              return new Response(tryResp.body, { status: tryResp.status, headers });
            }
          }
        }
      }
      // Not a sub-site path, serve from root assets (photonbuilder.com homepage etc.)
      return env.ASSETS.fetch(request);
    }

    if (!site) {
      return env.ASSETS.fetch(request);
    }

    const pathname = url.pathname;

    // Check for SEO redirects
    const siteRedirects = REDIRECTS[site];
    if (siteRedirects && siteRedirects[pathname]) {
      return Response.redirect(new URL(siteRedirects[pathname], url.origin).toString(), 301);
    }
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
      for (const suffix of HTML_SUFFIXES) {
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

    // Serve 404 page
    const notFoundResp = await env.ASSETS.fetch(new URL('/404.html', url.origin).toString());
    if (notFoundResp.ok) {
      return new Response(notFoundResp.body, {
        status: 404,
        headers: { 'Content-Type': 'text/html; charset=utf-8' },
      });
    }
    return new Response('Not Found', { status: 404 });
  }
};
