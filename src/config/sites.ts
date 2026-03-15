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
      { label: 'Roadmap', href: '/coming-soon' },
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
      { label: 'Roadmap', href: '/coming-soon' },
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
      { label: 'Roadmap', href: '/coming-soon' },
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
      { label: 'Roadmap', href: '/coming-soon' },
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
      { label: 'Roadmap', href: '/coming-soon' },
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
      { label: 'Roadmap', href: '/coming-soon' },
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
      { label: 'Roadmap', href: '/coming-soon' },
    ],
    footer: { text: '© 2026 I Just Want To', gabVentures: true },
  },
};

sites['bodycount'] = {
  id: 'bodycount',
  name: 'Body Count',
  domain: 'photonbuilder.com',
  accent: '#E05A5A',
  theme: { bg: '#060a12', cardBg: '#0a1020', border: '#152040', textPrimary: '#e2e8f0', textSecondary: '#94a3b8' },
  gaId: 'G-CYV604162T',
  nav: [
    { label: 'Calculators', href: '/bodycount/#tools' },
    { label: 'Studies', href: '/bodycount/#studies' },
    { label: 'Guides', href: '/bodycount/#guides' },
    { label: 'Lists', href: '/bodycount/#lists' },
      { label: 'Roadmap', href: '/bodycount/coming-soon' },
  ],
  footer: { text: '© 2026 Body Count', gabVentures: true },
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
      { label: 'Roadmap', href: '/coming-soon' },
  ],
  footer: { text: '© 2026 The Nookie Nook · Educational content only. Not medical advice.', gabVentures: true },
};

sites['getthebag'] = {
  id: 'getthebag',
  name: 'Get The Bag',
  domain: 'photonbuilder.com',
  accent: '#3B82F6',
  theme: { bg: '#060a12', cardBg: '#0a1020', border: '#152040', textPrimary: '#e2e8f0', textSecondary: '#94a3b8' },
  gaId: 'G-CYV604162T',
  nav: [
    { label: 'Tools', href: '/getthebag/#tools' },
    { label: 'Guides', href: '/getthebag/#guides' },
    { label: 'Roadmap', href: '/getthebag/coming-soon' },
  ],
  footer: { text: '© 2026 Get The Bag', gabVentures: true },
};

sites['sendnerds'] = {
  id: 'sendnerds',
  name: 'Send Nerds',
  domain: 'photonbuilder.com',
  accent: '#3B82F6',
  theme: { bg: '#060812', cardBg: '#0a1020', border: '#152040', textPrimary: '#e2e8f0', textSecondary: '#94a3b8' },
  gaId: 'G-CYV604162T',
  nav: [
    { label: 'Calculators', href: '/sendnerds/#tools' },
    { label: 'Guides', href: '/sendnerds/#guides' },
      { label: 'Roadmap', href: '/sendnerds/coming-soon' },
  ],
  footer: { text: '© 2026 Send Nerds', gabVentures: true },
};

sites['justonemoment'] = {
  id: 'justonemoment',
  name: 'Just One Moment',
  domain: 'photonbuilder.com',
  accent: '#F59E0B',
  theme: { bg: '#060812', cardBg: '#0a1020', border: '#152040', textPrimary: '#e2e8f0', textSecondary: '#94a3b8' },
  gaId: 'G-CYV604162T',
  nav: [
    { label: 'Timers', href: '/justonemoment/#tools' },
    { label: 'Calculators', href: '/justonemoment/#calculators' },
      { label: 'Roadmap', href: '/justonemoment/coming-soon' },
  ],
  footer: { text: '© 2026 Just One Moment', gabVentures: true },
};

sites['fixitwithducttape'] = {
  id: 'fixitwithducttape',
  name: 'Fix It With Duct Tape',
  domain: 'photonbuilder.com',
  accent: '#A0A0A0',
  theme: { bg: '#0a0a0a', cardBg: '#141414', border: '#252525', textPrimary: '#e2e8f0', textSecondary: '#94a3b8' },
  gaId: 'G-CYV604162T',
  nav: [
    { label: 'Reviews', href: '/fixitwithducttape/#tools' },
    { label: 'Comparisons', href: '/fixitwithducttape/#guides' },
    { label: 'Roadmap', href: '/fixitwithducttape/coming-soon' },
  ],
  footer: { text: '© 2026 Fix It With Duct Tape', gabVentures: true },
};

sites['papyruspeople'] = {
  id: 'papyruspeople',
  name: 'Papyrus People',
  domain: 'photonbuilder.com',
  accent: '#D4A574',
  theme: { bg: '#0a0806', cardBg: '#12100c', border: '#2a2418', textPrimary: '#e8e0d0', textSecondary: '#a09880' },
  gaId: 'G-CYV604162T',
  nav: [
    { label: 'Translators', href: '/papyruspeople/#tools' },
    { label: 'Fonts', href: '/papyruspeople/#guides' },
    { label: 'Roadmap', href: '/papyruspeople/coming-soon' },
  ],
  footer: { text: '© 2026 Papyrus People', gabVentures: true },
};

sites['eeniemeenie'] = {
  id: 'eeniemeenie',
  name: 'Eenie Meenie',
  domain: 'photonbuilder.com',
  accent: '#E040FB',
  theme: { bg: '#0a060c', cardBg: '#140e18', border: '#2a1e34', textPrimary: '#e8e0f0', textSecondary: '#a090b8' },
  gaId: 'G-CYV604162T',
  nav: [
    { label: 'Generators', href: '/eeniemeenie/#tools' },
    { label: 'Spinners', href: '/eeniemeenie/#guides' },
    { label: 'Roadmap', href: '/eeniemeenie/coming-soon' },
  ],
  footer: { text: '© 2026 Eenie Meenie', gabVentures: true },
};

sites['pleasestartplease'] = {
  id: 'pleasestartplease',
  name: 'Please Start Please',
  domain: 'photonbuilder.com',
  accent: '#EF4444',
  theme: { bg: '#0a0606', cardBg: '#141010', border: '#2a1a1a', textPrimary: '#e8e0e0', textSecondary: '#a09090' },
  gaId: 'G-CYV604162T',
  nav: [
    { label: 'Calculators', href: '/pleasestartplease/#tools' },
    { label: 'Guides', href: '/pleasestartplease/#guides' },
    { label: 'Roadmap', href: '/pleasestartplease/coming-soon' },
  ],
  footer: { text: '© 2026 Please Start Please', gabVentures: true },
};
