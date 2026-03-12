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
    const paths = [
      `/sites/${site}${pathname}`,
      pathname.endsWith('/') ? `/sites/${site}${pathname}index.html` : `/sites/${site}${pathname}.html`,
    ];

    for (const p of paths) {
      const newUrl = new URL(p, url.origin);
      newUrl.search = url.search;
      const resp = await env.ASSETS.fetch(new Request(newUrl, request));
      if (resp.status !== 404) return resp;
    }

    return new Response('Not Found', { status: 404 });
  }
};
