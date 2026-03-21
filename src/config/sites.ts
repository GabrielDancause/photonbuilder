export interface SiteTheme {
  bg: string;
  cardBg: string;
  border: string;
  textPrimary: string;
  textSecondary: string;
}

export interface NewsletterConfig {
  emoji: string;
  title: string;
  subtitle: string;
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
  newsletter?: NewsletterConfig;
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
    newsletter: { emoji: '🔥', title: 'Weekly FIRE Brief', subtitle: 'Free calculators & strategies for financial independence. No spam.' },
  },
  westmount: {
    id: 'westmount',
    name: 'Westmount Fundamentals',
    domain: 'westmountfundamentals.com',
    accent: '#4a8fe7',
    theme: { bg: '#060a12', cardBg: '#0a1020', border: '#152040', textPrimary: '#c8d0de', textSecondary: '#94a3b8' },
    gaId: 'G-VYF72NSC1Q',
    nav: [
      { label: 'Tools', href: '/#tools' },
      { label: 'Guides', href: '/#guides' },
      { label: 'Lists', href: '/#lists' },
      { label: 'IV Dashboard', href: '/intrinsic-value-dashboard/' },
    ],
    footer: { text: '© 2026 Westmount Fundamentals', gabVentures: true },
    newsletter: { emoji: '📬', title: 'Weekly Market Brief', subtitle: 'Free data-driven insights. No spam. Unsubscribe anytime.' },
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
    newsletter: { emoji: '🤖', title: 'Weekly Dev Brief', subtitle: 'Tools, benchmarks & dev insights. No spam.' },
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
    newsletter: { emoji: '🍳', title: 'Weekly Kitchen Brief', subtitle: 'Recipes, techniques & food science. No spam.' },
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
    newsletter: { emoji: '✈️', title: 'Weekly Nomad Brief', subtitle: 'Travel tools, visa guides & cost-of-living data. No spam.' },
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
    newsletter: { emoji: '🎮', title: 'Weekly Gaming Brief', subtitle: 'Builds, tier lists & gaming tools. No spam.' },
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
    newsletter: { emoji: '✅', title: 'Weekly Life Hacks', subtitle: 'Practical tools & how-to guides. No spam.' },
  },
};

sites['bodycount'] = {
  id: 'bodycount',
  name: 'Body Count',
  domain: 'bodycount.photonbuilder.com',
  accent: '#E05A5A',
  theme: { bg: '#060a12', cardBg: '#0a1020', border: '#152040', textPrimary: '#e2e8f0', textSecondary: '#94a3b8' },
  gaId: 'G-S2NRZFV4BW',
  nav: [
    { label: 'Calculators', href: '/#tools' },
    { label: 'Studies', href: '/#studies' },
    { label: 'Guides', href: '/#guides' },
    { label: 'Lists', href: '/#lists' },
  ],
  footer: { text: '© 2026 Body Count', gabVentures: true },
  newsletter: { emoji: '🔍', title: 'Weekly True Crime Brief', subtitle: 'Data, stats & analysis. No spam.' },
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
  newsletter: { emoji: '💕', title: 'Weekly Intimacy Brief', subtitle: 'Guides, tips & research-backed insights. No spam.' },
};

sites['getthebag'] = {
  id: 'getthebag',
  name: 'Get The Bag',
  domain: 'getthebag.photonbuilder.com',
  accent: '#3B82F6',
  theme: { bg: '#060a12', cardBg: '#0a1020', border: '#152040', textPrimary: '#e2e8f0', textSecondary: '#94a3b8' },
  gaId: 'G-52ZPK1JZ45',
  nav: [
    { label: 'Tools', href: '/#tools' },
    { label: 'Guides', href: '/#guides' },
  ],
  footer: { text: '© 2026 Get The Bag', gabVentures: true },
};

sites['sendnerds'] = {
  id: 'sendnerds',
  name: 'Send Nerds',
  domain: 'sendnerds.photonbuilder.com',
  accent: '#3B82F6',
  theme: { bg: '#060812', cardBg: '#0a1020', border: '#152040', textPrimary: '#e2e8f0', textSecondary: '#94a3b8' },
  gaId: 'G-Z7NENQMJQP',
  nav: [
    { label: 'Calculators', href: '/#tools' },
    { label: 'Guides', href: '/#guides' },
  ],
  footer: { text: '© 2026 Send Nerds', gabVentures: true },
};

sites['justonemoment'] = {
  id: 'justonemoment',
  name: 'Just One Moment',
  domain: 'justonemoment.photonbuilder.com',
  accent: '#F59E0B',
  theme: { bg: '#060812', cardBg: '#0a1020', border: '#152040', textPrimary: '#e2e8f0', textSecondary: '#94a3b8' },
  gaId: 'G-PNBZ1VJM9R',
  nav: [
    { label: 'Timers', href: '/#tools' },
    { label: 'Calculators', href: '/#calculators' },
  ],
  footer: { text: '© 2026 Just One Moment', gabVentures: true },
};

sites['fixitwithducttape'] = {
  id: 'fixitwithducttape',
  name: 'Fix It With Duct Tape',
  domain: 'fixitwithducttape.photonbuilder.com',
  accent: '#A0A0A0',
  theme: { bg: '#0a0a0a', cardBg: '#141414', border: '#252525', textPrimary: '#e2e8f0', textSecondary: '#94a3b8' },
  gaId: 'G-3Y23ZLX5C3',
  nav: [
    { label: 'Reviews', href: '/#tools' },
    { label: 'Comparisons', href: '/#guides' },
  ],
  footer: { text: '© 2026 Fix It With Duct Tape', gabVentures: true },
};

sites['papyruspeople'] = {
  id: 'papyruspeople',
  name: 'Papyrus People',
  domain: 'papyruspeople.photonbuilder.com',
  accent: '#D4A574',
  theme: { bg: '#0a0806', cardBg: '#12100c', border: '#2a2418', textPrimary: '#e8e0d0', textSecondary: '#a09880' },
  gaId: 'G-26Z3FPWKM6',
  nav: [
    { label: 'Translators', href: '/#tools' },
    { label: 'Fonts', href: '/#guides' },
  ],
  footer: { text: '© 2026 Papyrus People', gabVentures: true },
};

sites['eeniemeenie'] = {
  id: 'eeniemeenie',
  name: 'Eenie Meenie',
  domain: 'eeniemeenie.photonbuilder.com',
  accent: '#E040FB',
  theme: { bg: '#0a060c', cardBg: '#140e18', border: '#2a1e34', textPrimary: '#e8e0f0', textSecondary: '#a090b8' },
  gaId: 'G-CS7D4WKPVP',
  nav: [
    { label: 'Generators', href: '/#tools' },
    { label: 'Spinners', href: '/#guides' },
  ],
  footer: { text: '© 2026 Eenie Meenie', gabVentures: true },
};

sites['pleasestartplease'] = {
  id: 'pleasestartplease',
  name: 'Please Start Please',
  domain: 'pleasestartplease.photonbuilder.com',
  accent: '#EF4444',
  theme: { bg: '#0a0606', cardBg: '#141010', border: '#2a1a1a', textPrimary: '#e8e0e0', textSecondary: '#a09090' },
  gaId: 'G-DVC7TK5BHV',
  nav: [
    { label: 'Calculators', href: '/#tools' },
    { label: 'Guides', href: '/#guides' },
  ],
  footer: { text: '© 2026 Please Start Please', gabVentures: true },
};
