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

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const host = url.hostname;
  const site = SITE_MAP[host];

  if (!site) {
    // Default: serve photonbuilder.com from root
    return env.ASSETS.fetch(request);
  }

  // Rewrite to site subfolder
  const paths = [
    `/sites/${site}${url.pathname}`,
    url.pathname.endsWith('/')
      ? `/sites/${site}${url.pathname}index.html`
      : `/sites/${site}${url.pathname}.html`,
  ];

  for (const path of paths) {
    const newUrl = new URL(path, url.origin);
    newUrl.search = url.search;
    const resp = await env.ASSETS.fetch(new Request(newUrl, request));
    if (resp.status !== 404) return resp;
  }

  return new Response('Not Found', { status: 404 });
}
