export interface SiteTheme {
  bg: string;
  cardBg: string;
  border: string;
  textPrimary: string;
  textSecondary: string;
}

export interface SiteConfig {
  id: string;
  name: string;
  domain: string;
  accent: string;
  theme: SiteTheme;
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
    theme: { bg: '#0c0a00', cardBg: '#141008', border: '#2a2010', textPrimary: '#e0d8c8', textSecondary: '#888888' },
    gaId: 'G-ZSXFV0VP4L',
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
    theme: { bg: '#060a12', cardBg: '#0a1020', border: '#152040', textPrimary: '#c8d0de', textSecondary: '#94a3b8' },
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
    theme: { bg: '#060a12', cardBg: '#0a1020', border: '#152040', textPrimary: '#e2e8f0', textSecondary: '#94a3b8' },
    gaId: 'G-T4PEJFWXCY',
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
    theme: { bg: '#0a0b10', cardBg: '#111318', border: '#1e2030', textPrimary: '#e0e0e0', textSecondary: '#888888' },
    gaId: 'G-WGF4XXH1SP',
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
    theme: { bg: '#0a0806', cardBg: '#12100c', border: '#2a2418', textPrimary: '#e0d5c8', textSecondary: '#888888' },
    gaId: 'G-PGRXS7TCZV',
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
    theme: { bg: '#08060e', cardBg: '#100e18', border: '#221e30', textPrimary: '#d8d0e8', textSecondary: '#888888' },
    gaId: 'G-W1KVQZVVWE',
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
    theme: { bg: '#060c0a', cardBg: '#0c1410', border: '#1a2a24', textPrimary: '#c8e0d8', textSecondary: '#888888' },
    gaId: 'G-PRHBMYEWQC',
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
  theme: { bg: '#060a12', cardBg: '#0a1020', border: '#152040', textPrimary: '#c8d0de', textSecondary: '#5a6a80' },
  gaId: 'G-CYV604162T',
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
  theme: { bg: '#060a12', cardBg: '#0a1020', border: '#152040', textPrimary: '#e2e8f0', textSecondary: '#94a3b8' },
  gaId: 'G-CYV604162T',
  nav: [
    { label: 'Tools', href: '/#tools' },
    { label: 'Guides', href: '/#guides' },
    { label: 'Lists', href: '/#lists' },
    { label: 'Blog', href: '/#blog' },
  ],
  footer: { text: '© 2026 Photon Builder', gabVentures: true },
};

sites['health'] = {
  id: 'health',
  name: 'Health Tools',
  domain: 'photonbuilder.com',
  accent: '#E05A5A',
  theme: { bg: '#060a12', cardBg: '#0a1020', border: '#152040', textPrimary: '#e2e8f0', textSecondary: '#94a3b8' },
  gaId: 'G-CYV604162T',
  nav: [
    { label: 'Calculators', href: '/health/#tools' },
    { label: 'Studies', href: '/health/#studies' },
    { label: 'Guides', href: '/health/#guides' },
    { label: 'Lists', href: '/health/#lists' },
  ],
  footer: { text: '© 2026 Health Tools', gabVentures: true },
};

sites['nookienook'] = {
  id: 'nookienook',
  name: 'The Nookie Nook',
  domain: 'thenookienook.com',
  accent: '#E84393',
  theme: { bg: '#0c0610', cardBg: '#140e1a', border: '#2a1e34', textPrimary: '#e8ddf0', textSecondary: '#a090b0' },
  gaId: 'G-LQFGTRMFYR',
  nav: [
    { label: 'Guides', href: '/#guides' },
    { label: 'Tools', href: '/#tools' },
    { label: 'Studies', href: '/#studies' },
  ],
  footer: { text: '© 2026 The Nookie Nook · Educational content only. Not medical advice.', gabVentures: true },
};

sites['montrealjobs'] = {
  id: 'montrealjobs',
  name: 'Montreal Jobs',
  domain: 'montrealjobs.photonbuilder.com',
  accent: '#3B82F6',
  theme: { bg: '#060a12', cardBg: '#0a1020', border: '#152040', textPrimary: '#e2e8f0', textSecondary: '#94a3b8' },
  gaId: 'G-CYV604162T',
  nav: [
    { label: 'Market', href: '/#market' },
    { label: 'Jobs', href: '/#jobs' },
    { label: 'Skills', href: '/#skills' },
  ],
  footer: { text: '© 2026 Montreal Jobs', gabVentures: true },
};

sites['mathtools'] = {
  id: 'mathtools',
  name: 'Math Tools',
  domain: 'photonbuilder.com',
  accent: '#3B82F6',
  theme: { bg: '#060812', cardBg: '#0a1020', border: '#152040', textPrimary: '#e2e8f0', textSecondary: '#94a3b8' },
  gaId: 'G-CYV604162T',
  nav: [
    { label: 'Calculators', href: '/mathtools/#tools' },
    { label: 'Guides', href: '/mathtools/#guides' },
  ],
  footer: { text: '© 2026 Math Tools', gabVentures: true },
};

sites['misc'] = {
  id: 'misc',
  name: 'Misc Tools',
  domain: 'photonbuilder.com',
  accent: '#8B5CF6',
  theme: { bg: '#060812', cardBg: '#0a1020', border: '#152040', textPrimary: '#e2e8f0', textSecondary: '#94a3b8' },
  gaId: 'G-CYV604162T',
  nav: [
    { label: 'Tools', href: '/misc/#tools' },
    { label: 'Guides', href: '/misc/#guides' },
    { label: 'Lists', href: '/misc/#lists' },
  ],
  footer: { text: '© 2026 Misc Tools', gabVentures: true },
};
