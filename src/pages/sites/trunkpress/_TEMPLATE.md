# Trunk Press Article Template

Every article MUST follow this exact structure. Do not change class names.

```astro
---
import SiteLayout from '../../../layouts/SiteLayout.astro';

export const meta = {
  title: 'Headline Here',
  description: 'One-sentence summary for SEO.',
  category: 'world',  // world, us, politics, business, health, entertainment, travel, sports, science, climate, tech
  published: '2026-03-24',
};

const schema = {
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": meta.title,
  "description": meta.description,
  "datePublished": meta.published,
  "dateModified": meta.published,
  "author": { "@type": "Organization", "name": "Trunk Press" },
  "publisher": { "@type": "Organization", "name": "Trunk Press" },
  "mainEntityOfPage": { "@type": "WebPage", "@id": `https://trunkpress.photonbuilder.com/${slug}` }
};
---

<SiteLayout site="trunkpress" title={meta.title} description={meta.description} canonical={`https://trunkpress.photonbuilder.com/${slug}`} schema={schema}>
  <article class="tp-article max-w-3xl mx-auto py-10">
    <!-- Category + Date -->
    <div class="flex items-center gap-3 mb-4">
      <span class="text-xs font-black tracking-[2px] uppercase text-[var(--accent-color)]">🌍 WORLD</span>
      <span class="text-xs text-[var(--text-secondary)]">March 24, 2026</span>
    </div>

    <!-- Headline -->
    <h1 class="text-3xl md:text-4xl font-black leading-tight mb-4 text-[var(--text-primary)]">
      Headline Here
    </h1>

    <!-- Lede -->
    <p class="text-lg text-[var(--text-secondary)] leading-relaxed mb-8 border-l-4 border-[var(--accent-color)] pl-4">
      The key facts in 2-3 sentences. Bold, direct, sets the scene.
    </p>

    <!-- Article body -->
    <div class="space-y-5 text-[var(--text-secondary)] leading-relaxed">
      <h2 class="text-xl font-bold text-[var(--text-primary)] mt-10 mb-4">What Happened</h2>
      <p>Body paragraph with real facts.</p>
      <p>Second paragraph with context.</p>

      <h2 class="text-xl font-bold text-[var(--text-primary)] mt-10 mb-4">Why It Matters</h2>
      <p>Analysis and implications.</p>

      <h2 class="text-xl font-bold text-[var(--text-primary)] mt-10 mb-4">The Bigger Picture</h2>
      <p>Broader context.</p>

      <h2 class="text-xl font-bold text-[var(--text-primary)] mt-10 mb-4">What's Next</h2>
      <p>Forward-looking analysis.</p>
    </div>

    <!-- Tags -->
    <div class="mt-12 pt-6 border-t border-[var(--border-color)]">
      <div class="flex flex-wrap gap-2">
        <span class="text-xs bg-[var(--card-bg)] text-[var(--text-secondary)] px-3 py-1 rounded">#tag1</span>
        <span class="text-xs bg-[var(--card-bg)] text-[var(--text-secondary)] px-3 py-1 rounded">#tag2</span>
      </div>
    </div>
  </article>
</SiteLayout>
```

## Rules
- Wrapper: ALWAYS `<article class="tp-article max-w-3xl mx-auto py-10">` — no px (layout handles padding)
- h1: ALWAYS `text-3xl md:text-4xl font-black leading-tight mb-4 text-[var(--text-primary)]`
- h2: ALWAYS `text-xl font-bold text-[var(--text-primary)] mt-10 mb-4`
- Body text: use `<p>` tags, no extra classes needed (layout handles defaults)
- NO `<style>` tags — Tailwind only
- NO `prose` or `prose-custom` classes
- Category emojis: 🌍 WORLD, 🇺🇸 US, 🏛️ POLITICS, 💼 BUSINESS, 🏥 HEALTH, 🎬 ENTERTAINMENT, ✈️ TRAVEL, ⚽ SPORTS, 🔬 SCIENCE, 🌡️ CLIMATE, 💻 TECH
