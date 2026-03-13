export interface SiteConfig {
  id: string;
  name: string;
  domain: string;
  accent: string;
  gaId: string;
  nav: { label: string; href: string }[];
  footer: { text: string; gabVentures?: boolean };
}

export const sites: Record<string, SiteConfig> = {
  firemaths: {
    id: 'firemaths',
    name: 'Fire Maths',
    domain: 'firemaths.info',
    accent: '#D4A017',
    gaId: 'G-G86C7NJG3F',
    nav: [
      { label: 'Tools', href: '/#tools' },
      { label: 'Studies', href: '/#studies' },
      { label: 'Guides', href: '/#guides' },
    ],
    footer: { text: '© 2026 Fire Maths', gabVentures: true },
  },
  westmount: {
    id: 'westmount',
    name: 'Westmount Fundamentals',
    domain: 'westmountfundamentals.com',
    accent: '#4a8fe7',
    gaId: 'G-VYF72NSC1Q',
    nav: [
      { label: 'Studies', href: '/#studies' },
      { label: 'Tools', href: '/#tools' },
      { label: 'Guides', href: '/#guides' },
      { label: 'Lists', href: '/#lists' },
    ],
    footer: { text: '© 2026 Westmount Fundamentals', gabVentures: true },
  },
  siliconbased: {
    id: 'siliconbased',
    name: 'Silicon Based',
    domain: 'siliconbased.dev',
    accent: '#818cf8',
    gaId: 'G-G86C7NJG3F',
    nav: [
      { label: 'Tools', href: '/#tools' },
      { label: 'Studies', href: '/#studies' },
      { label: 'Guides', href: '/#guides' },
    ],
    footer: { text: '© 2026 Silicon Based', gabVentures: true },
  },
  '28grams': {
    id: '28grams',
    name: '28 Grams',
    domain: '28grams.vip',
    accent: '#C2185B',
    gaId: 'G-G86C7NJG3F',
    nav: [
      { label: 'Tools', href: '/#tools' },
      { label: 'Guides', href: '/#guides' },
      { label: 'Lists', href: '/#lists' },
    ],
    footer: { text: '© 2026 28 Grams', gabVentures: true },
  },
  migratingmammals: {
    id: 'migratingmammals',
    name: 'Migrating Mammals',
    domain: 'migratingmammals.com',
    accent: '#C4956A',
    gaId: 'G-G86C7NJG3F',
    nav: [
      { label: 'Tools', href: '/#tools' },
      { label: 'Guides', href: '/#guides' },
      { label: 'Lists', href: '/#lists' },
    ],
    footer: { text: '© 2026 Migrating Mammals', gabVentures: true },
  },
  leeroyjenkins: {
    id: 'leeroyjenkins',
    name: 'Leeroy Jenkins',
    domain: 'leeroyjenkins.quest',
    accent: '#9333EA',
    gaId: 'G-G86C7NJG3F',
    nav: [
      { label: 'Tools', href: '/#tools' },
      { label: 'Guides', href: '/#guides' },
      { label: 'Lists', href: '/#lists' },
    ],
    footer: { text: '© 2026 Leeroy Jenkins', gabVentures: true },
  },
  ijustwantto: {
    id: 'ijustwantto',
    name: 'I Just Want To',
    domain: 'ijustwantto.live',
    accent: '#2DB89A',
    gaId: 'G-G86C7NJG3F',
    nav: [
      { label: 'Tools', href: '/#tools' },
      { label: 'Guides', href: '/#guides' },
      { label: 'Lists', href: '/#lists' },
    ],
    footer: { text: '© 2026 I Just Want To', gabVentures: true },
  },
};
sites['hpv-research'] = {
  id: 'hpv-research',
  name: 'HPV Research',
  domain: 'hpvresearch.com',
  accent: '#10b981',
  gaId: 'G-G86C7NJG3F',
  nav: [
    { label: 'Tools', href: '/#tools' },
    { label: 'Studies', href: '/#studies' },
    { label: 'Guides', href: '/#guides' },
  ],
  footer: { text: '© 2026 HPV Research', gabVentures: true },
};

sites['photonbuilder'] = {
  id: 'photonbuilder',
  name: 'Photon Builder',
  domain: 'photonbuilder.com',
  accent: '#FF6B35',
  gaId: 'G-G86C7NJG3F',
  nav: [
    { label: 'Tools', href: '/#tools' },
    { label: 'Guides', href: '/#guides' },
    { label: 'Lists', href: '/#lists' },
    { label: 'Blog', href: '/#blog' },
  ],
  footer: { text: '© 2026 Photon Builder', gabVentures: true },
};

sites['montrealjobs'] = {
  id: 'montrealjobs',
  name: 'Montreal Jobs',
  domain: 'montrealjobs.photonbuilder.com',
  accent: '#3B82F6',
  gaId: 'G-G86C7NJG3F',
  nav: [
    { label: 'Market', href: '/#market' },
    { label: 'Jobs', href: '/#jobs' },
    { label: 'Skills', href: '/#skills' },
  ],
  footer: { text: '© 2026 Montreal Jobs', gabVentures: true },
};
