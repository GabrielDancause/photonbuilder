# PhotonBuilder

A monorepo serving multiple sites from one Cloudflare Pages deployment with domain routing.

## 🏗️ Architecture

PhotonBuilder uses Cloudflare Workers to route different domains to their respective site folders:

```text
photonbuilder/
├── public/
│   ├── _worker.js           ← Domain routing logic
│   └── sites/
│       ├── firemaths/       ← firemaths.info content
│       ├── siliconbased/    ← siliconbased.dev (future)
│       ├── westmount/       ← westmountfundamentals.com (future)
│       └── ...              ← More sites as needed
├── src/
│   ├── layouts/
│   │   └── SiteLayout.astro ← Shared base layout
│   └── pages/
│       └── index.astro      ← photonbuilder.com landing page
├── scripts/
│   └── verify-build.sh      ← Build verification
└── astro.config.mjs
```

## 🌍 Domain Routing

The Cloudflare Worker (`public/_worker.js`) maps domains to site folders:

| Domain | Folder | Status |
|--------|--------|--------|
| `firemaths.info` | `/sites/firemaths/` | ✅ Active |
| `siliconbased.dev` | `/sites/siliconbased/` | 🚧 Planned |
| `westmountfundamentals.com` | `/sites/westmount/` | 🚧 Planned |
| `28grams.vip` | `/sites/28grams/` | 🚧 Planned |
| `migratingmammals.com` | `/sites/migratingmammals/` | 🚧 Planned |
| `leeroyjenkins.quest` | `/sites/leeroyjenkins/` | 🚧 Planned |
| `ijustwantto.live` | `/sites/ijustwantto/` | 🚧 Planned |

## 🚀 Adding a New Site

1. **Prepare your static files:**
   ```bash
   mkdir -p public/sites/yoursite
   # Copy your HTML/CSS/JS files to public/sites/yoursite/
   ```

2. **Update the domain mapping:**
   Edit `public/_worker.js` and add your domain to `SITE_MAP`:
   ```js
   'yourdomain.com': 'yoursite',
   'www.yourdomain.com': 'yoursite',
   ```

3. **Build and verify:**
   ```bash
   npm run build
   ./scripts/verify-build.sh
   ```

4. **Deploy to Cloudflare Pages** with the new domain configured.

## 🧞 Commands

| Command | Action |
|---------|--------|
| `npm install` | Install dependencies |
| `npm run dev` | Start local dev server at `localhost:4321` |
| `npm run build` | Build production site to `./dist/` |
| `npm run preview` | Preview build locally |
| `./scripts/verify-build.sh` | Verify build structure and files |

## 📦 Current Sites

### FireMaths.info
- **Content:** 62 financial calculator pages
- **Type:** Static HTML (self-contained)
- **Theme:** Dark with #D4A017 accent
- **Status:** ✅ Migrated to PhotonBuilder

## 🔧 Technical Details

- **Framework:** Astro 5 + Tailwind 4
- **Output:** Static site generation
- **Hosting:** Cloudflare Pages
- **Routing:** Cloudflare Workers (domain-based)
- **CDN:** Global edge network via Cloudflare

## 📖 How It Works

1. **Request arrives** at Cloudflare edge
2. **Worker checks** the hostname against `SITE_MAP`
3. **If matched**, rewrite URL to `/sites/{sitename}/...`
4. **Static assets** served from appropriate folder
5. **If no match**, serve PhotonBuilder landing page

This architecture allows:
- ✅ Multiple domains from one deployment
- ✅ Shared build pipeline and CDN
- ✅ Independent site content
- ✅ Cost-effective hosting
- ✅ Global performance

## 🚀 Deployment

Deploy to Cloudflare Pages with:
- Build command: `npm run build`
- Output directory: `dist`
- Add your custom domains in Cloudflare Pages dashboard

The Worker will automatically handle routing based on the requesting domain.