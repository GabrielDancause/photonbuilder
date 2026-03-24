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
  tagline?: string;
  description?: string;
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
  tagline: 'Free Finance & Money Calculators',
  description: 'Mortgage, tax, retirement, investment, and budgeting calculators. Make smarter money decisions with real math.',
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
  tagline: 'Free Equity Research & Investing Tools',
  description: 'Short interest rankings, dividend data, ETF comparisons, intrinsic value calculators, and 380+ financial tools.',
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
  tagline: 'Free Developer Tools & Utilities',
  description: 'CSS frameworks, code generators, API tools, and developer utilities. Built by developers, for developers.',
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
  tagline: 'Cooking Tools, Recipes & Kitchen Science',
  description: 'Baking calculators, recipe converters, smoke points, and nutrition tools. Cook smarter with data.',
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
  tagline: 'Digital Nomad & Travel Tools',
  description: 'Cost of living comparisons, visa guides, travel calculators, and nomad city rankings. Travel smarter.',
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
  tagline: 'Gaming Gear Reviews & Performance Tools',
  description: 'Headset comparisons, mouse guides, monitor breakdowns, and FPS optimization tools. Gear up smarter.',
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
  tagline: 'Practical Home & DIY Calculators',
  description: 'Free home renovation calculators for concrete, paint, flooring, BTU, and more. Get accurate numbers before you start your next project.',
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
  tagline: 'Free Health & Body Calculators',
  description: 'BMI, BMR, body fat, calorie, heart rate, and macro calculators. Track your health with accurate tools.',
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
  tagline: 'Sexual Health Guides & Tools',
  description: 'Birth control comparisons, STI guides, fertility tools, and wellness resources. Informed choices, no judgment.',
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
  tagline: 'Career Tools & Job Resources',
  description: 'Free salary calculators, resume tips, interview prep guides, and job search tools to help you level up your career and earn more.',
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
  tagline: 'Free Education & Academic Calculators',
  description: 'GPA calculators, test score tools, citation generators, and study aids. Ace your academics.',
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
  tagline: 'Free Online Timers & Countdowns',
  description: 'Free online Pomodoro, meditation, workout, and custom timers plus time calculators. Simple, fast, and distraction-free productivity tools.',
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
  tagline: 'AI & SaaS Tool Reviews',
  description: 'Honest reviews and comparisons of AI tools, productivity software, and SaaS platforms. Find what actually works.',
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
  tagline: 'Text Tools & Character Generators',
  description: 'Free online font generators, binary and morse code translators, character counters, and text formatting tools. Transform, analyze, and style text instantly.',
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
  tagline: 'Random Generators & Decision Tools',
  description: 'Wheel spinners, name pickers, dice rollers, and randomizers. Let chance decide.',
  nav: [
    { label: 'Generators', href: '/#tools' },
    { label: 'Spinners', href: '/#guides' },
  ],
  footer: { text: '© 2026 Eenie Meenie', gabVentures: true },
};

sites['trunkpress'] = {
  id: 'trunkpress',
  name: 'Trunk Press',
  domain: 'trunkpress.photonbuilder.com',
  accent: '#FF3333',
  theme: { bg: '#0a0a0a', cardBg: '#141414', border: '#252525', textPrimary: '#f0f0f0', textSecondary: '#999999' },
  gaId: 'G-G86C7NJG3F',
  tagline: 'News That Hits Different',
  description: 'World news, politics, business, tech, science, and culture — raw, unfiltered, and straight to the point.',
  nav: [
    { label: 'US', href: '/#us' },
    { label: 'World', href: '/#world' },
    { label: 'Politics', href: '/#politics' },
    { label: 'Business', href: '/#business' },
    { label: 'Health', href: '/#health' },
    { label: 'Entertainment', href: '/#entertainment' },
    { label: 'Travel', href: '/#travel' },
    { label: 'Sports', href: '/#sports' },
    { label: 'Science', href: '/#science' },
    { label: 'Climate', href: '/#climate' },
    { label: 'Tech', href: '/#tech' },
  ],
  footer: { text: '© 2026 Trunk Press', gabVentures: true },
};

sites['pleasestartplease'] = {
  id: 'pleasestartplease',
  name: 'Please Start Please',
  domain: 'pleasestartplease.photonbuilder.com',
  accent: '#EF4444',
  theme: { bg: '#0a0606', cardBg: '#141010', border: '#2a1a1a', textPrimary: '#e8e0e0', textSecondary: '#a09090' },
  gaId: 'G-DVC7TK5BHV',
  tagline: 'Car Tools, Guides & Automotive Data',
  description: 'Maintenance schedules, insurance comparisons, fuel economy tools, and OBD code lookups. Keep your car running.',
  nav: [
    { label: 'Calculators', href: '/#tools' },
    { label: 'Guides', href: '/#guides' },
  ],
  footer: { text: '© 2026 Please Start Please', gabVentures: true },
};

sites['trunkpress'] = {
  id: 'trunkpress',
  name: 'Trunk Press',
  domain: 'trunkpress.photonbuilder.com',
  accent: '#FF3333',
  theme: { bg: '#080808', cardBg: '#121212', border: '#222222', textPrimary: '#e5e5e5', textSecondary: '#a3a3a3' },
  gaId: 'G-XXXXXXXXXX',
  tagline: 'Politics, Unfiltered.',
  description: 'A sharp, engaging editorial style — Vice meets Reuters. Factual but with personality.',
  nav: [
    { label: 'Politics', href: '/#politics' },
    { label: 'Geopolitics', href: '/#geopolitics' },
  ],
  footer: { text: '© 2026 Trunk Press', gabVentures: true },
};
