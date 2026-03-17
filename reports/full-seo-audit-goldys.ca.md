# Full SEO Audit: goldys.ca

**Date:** 2026-03-16
**Site:** Goldy's — Canadian Superseed Cereal (Shopify e-commerce)
**Domain:** https://goldys.ca

---

## SEO Health Score: 44 / 100

| Category | Weight | Raw Score | Weighted Score | Report |
|----------|--------|-----------|----------------|--------|
| Technical SEO | 22% | 54/100 | 11.9/22 | technical-seo-audit-goldys.ca.md |
| Content Quality (E-E-A-T) | 23% | 34/100 | 7.8/23 | content-eeat-audit-goldys.ca.md |
| On-Page SEO | 20% | 30/100 | 6.0/20 | (rolled into content + technical) |
| Schema / Structured Data | 10% | 32/100 | 3.2/10 | schema-audit-goldys.ca.md |
| Performance (CWV) | 10% | 40/100 | 4.0/10 | cwv-performance-goldys.ca.md |
| AI Search Readiness (GEO) | 10% | 35/100 | 3.5/10 | geo-audit-goldys.ca.md |
| Images | 5% | 45/100 | 2.25/5 | visual-seo-audit-goldys.ca.md |

**Overall: 44/100 — Needs Significant Work**

> Goldy's has a legitimate, established Canadian brand with solid off-site authority (retail distribution, #1 organic for "best superseed cereal Canada") but critically underperforms on-site across every measured dimension. The site's Shopify foundation provides structural safety nets (HTTPS, sitemaps, mobile-responsive themes) but the content is largely locked in images, AI crawlers are blocked by default, and no foundational schema or E-E-A-T signals exist in crawlable HTML.

---

## Business Context

- **Platform:** Shopify
- **Industry:** Canadian health food / CPG e-commerce
- **Primary products:** Superseed cereal (chia, hemp, pumpkin seed, buckwheat) — multiple flavors
- **Certifications:** Non-GMO, gluten-free, grain-free, zero added sugar, plant-based
- **Distribution:** NaturaMarket, Healthy Planet Canada, The Low Carb Grocery, Mindful Snacks, Amazon.ca, and others
- **Organic strength:** #1 for "best superseed cereal Canada"; invisible for "gluten free cereal Canada"
- **Direct competitor:** Holy Crap Foods (stronger editorial/E-E-A-T presence)

---

## Critical Issues (Fix Immediately)

These issues block indexing, AI visibility, or cause significant ranking loss.

### CRIT-1: AI Crawlers Blocked by Shopify Default robots.txt
**Impact:** Complete invisibility in AI-generated search answers (ChatGPT, Claude, Perplexity, Google AI Overviews)

Shopify's default `robots.txt` blocks GPTBot, ClaudeBot, PerplexityBot, Bytespider, and CCBot. Unless Goldy's has customized their `robots.txt.liquid`, every AI search crawler is denied access to the site.

**Fix:** Create/edit `robots.txt.liquid` in the Shopify theme to explicitly allow AI search bots:
```
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /
```
**Effort:** 30 minutes | **Files:** `templates/robots.txt.liquid`

---

### CRIT-2: No llms.txt File
**Impact:** AI systems have no structured brand/product summary for citation; defaults to less accurate third-party content

**Fix:** Create `goldys.ca/llms.txt` — a markdown file describing the brand, products, nutritional claims, certifications, and key URLs. Serve as a static file via Shopify's Files section or a Liquid page template.

**Effort:** 1–2 hours to draft

---

### CRIT-3: No Crawlable Title Tag, Meta Description, or H1 on Homepage
**Impact:** Google has no text anchor for the homepage; no keyword signal; no click-through optimization in SERPs

Homepage title returned empty in crawl. Meta description absent. No H1 in crawlable HTML. All content appears to be rendered client-side or stored in image files.

**Fix:** In Shopify admin → Online Store → Preferences → set homepage title and meta description. In the theme hero section, ensure the headline is an HTML `<h1>` element, not an image.

**Effort:** 30 minutes

---

### CRIT-4: Nutritional Statistics Not in Crawlable Text
**Impact:** Google and all AI systems cannot index nutritional claims; product pages effectively invisible for nutrition-based queries; "12g protein per serving" cannot appear in AI Overviews

Nutrition facts exist only as images of the nutrition label. Neither search engines nor AI crawlers can read image text.

**Fix:** Add an HTML text block beneath each product's nutrition label image with exact per-serving values (protein, fiber, calories, omega-3, fat, carbs, sugar, sodium).

**Effort:** 15–30 minutes per product

---

### CRIT-5: Zero Author Attribution Across All Content
**Impact:** Violates December 2025 QRG author attribution standards; all blog content treated as anonymous; reduced E-E-A-T trust score

No author bylines on any blog post. No founder name associated with content. No expertise credentials for nutritional claims.

**Fix:** Attribute all blog posts to the founder by name. Create an author bio page (photo, background, why they created the product). Enable Shopify's blog author display in theme settings.

**Effort:** 2–4 hours

---

### CRIT-6: No Organization Schema
**Impact:** No Knowledge Panel eligibility; no entity disambiguation in Google's Knowledge Graph; blocks Article rich results

Shopify never injects Organization schema. The brand has zero structured entity presence in the knowledge graph.

**Fix:** Add Organization JSON-LD to `layout/theme.liquid`:
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Goldy's",
  "url": "https://goldys.ca/",
  "logo": { "@type": "ImageObject", "url": "https://goldys.ca/cdn/shop/files/goldys-logo.png" },
  "sameAs": ["https://www.facebook.com/goldyscereal"],
  "description": "Goldy's makes superseed cereal — gluten-free, grain-free, non-GMO, zero added sugar. Made in Canada."
}
```
**Effort:** 30 minutes

---

## High Priority Issues (Fix Within 1–2 Weeks)

### HIGH-1: Hero Image Not Preloaded — LCP Failure on Mobile
Estimated mobile LCP: 3.2s–4.8s (Google threshold: ≤2.5s). Missing `<link rel="preload">` and `fetchpriority="high"` on the hero image.

**Fix:** Add preload hint in the hero section Liquid template. Serve hero as WebP/AVIF with mobile-specific srcset.

---

### HIGH-2: Product Pages Below 400-Word Content Floor
All product pages estimated at 50–100 crawlable words. E-E-A-T minimum for complex product pages is 400+ words covering ingredients, benefits with numbers, certifications, and usage.

**Fix:** Expand each product description to 400+ words of HTML text organized as: tagline → key benefits with numbers → ingredient spotlight → serving suggestions → certifications with issuing body names.

---

### HIGH-3: App JavaScript Accumulating — INP Risk
Multiple Shopify apps (email, reviews, loyalty, chat, analytics) add 400–800KB of JS, pushing INP above 200ms on mobile. Klaviyo loads synchronously by default.

**Fix:** Add `defer` to Klaviyo and non-critical app scripts. Audit per-app TBT cost. Remove or replace high-cost apps.

---

### HIGH-4: Internal Links Pointing to Non-Canonical Product URLs
Theme collection templates link to `/collections/{handle}/products/{slug}` (non-canonical) rather than `/products/{slug}` (canonical). Splits link equity.

**Fix:** Update Liquid collection card templates to use `/products/` path.

---

### HIGH-5: No NutritionInformation Schema on Product Pages
`NutritionInformation` nested in `Product` JSON-LD is a high-value schema type for food brands. Absent on goldys.ca. **No direct Canadian superseed cereal competitor has this implemented** — a first-mover advantage.

**Fix:** Add NutritionInformation to the product JSON-LD Liquid snippet (see schema-audit report for full template).

---

### HIGH-6: Blog Contains Only Recipes — No Informational Authority Content
Recipes don't capture mid-funnel queries ("is superseed cereal healthy", "best high-protein breakfast cereal Canada"). Blog named "News" but delivers recipes — user expectation mismatch.

**Fix:** Create 3 informational articles (1,500+ words each, author-attributed, dated):
1. "Superseed Cereal: What It Is and Why It's Different From Regular Cereal"
2. "High Protein Gluten-Free Cereal: A Canadian Guide"
3. "Health Benefits of Chia, Hemp, and Pumpkin Seeds for Breakfast"

---

### HIGH-7: No Founder Story on About Page
The LCG Foods brand story page (off-site) proves the narrative exists. On-site About page has no crawlable founder story.

**Fix:** Write 600–800 words of crawlable HTML covering: who Goldy is, why they created the product, what makes the seeds special, Canadian manufacturing commitment.

---

### HIGH-8: Article Schema Missing publisher — Blocks Rich Results
All blog posts are currently ineligible for Article rich results because the `publisher` Organization link is absent from the Article JSON-LD.

**Fix:** Update `sections/main-article.liquid` to add publisher with logo (see schema-audit report for template).

---

### HIGH-9: Missing Brand Signals — Wikipedia, Wikidata, Crunchbase
No Knowledge Panel exists. No Wikipedia page, Wikidata entry, or Crunchbase profile.

**Fix (Medium effort):** Create Wikidata entity. Pursue Wikipedia stub if notability threshold can be met. Set up Crunchbase company profile.

---

## Medium Priority Issues (Fix Within 1 Month)

| # | Issue | Category | Effort |
|---|-------|----------|--------|
| M-1 | Missing `width`/`height` on `<img>` tags — causing CLS | Performance | 2–4 hrs |
| M-2 | No FAQ schema on product pages (AI/GEO value) | Schema | 2–4 hrs |
| M-3 | Collection pages return ~0 crawlable content | Content | Medium |
| M-4 | No publication dates on blog posts | Content/Trust | Low |
| M-5 | Tagged collection filter URLs in sitemap (non-canonical) | Sitemap | Low |
| M-6 | lastmod dates inaccurate (app-triggered updates) | Sitemap | Medium |
| M-7 | CSP and Referrer-Policy security headers absent | Technical | Low |
| M-8 | BreadcrumbList schema — verify/add if absent | Schema | Low |
| M-9 | No IndexNow implementation for Bing/Yandex | Technical | Low |
| M-10 | No image sitemap (product photography) | Sitemap | Low (app) |
| M-11 | No LinkedIn company page | Brand | Low |
| M-12 | Blog section rename: "News" → "Recipes & Tips" | Content/UX | Low |
| M-13 | No comparison content vs. traditional cereal | Content | Medium |
| M-14 | Redirect chain accumulation from renamed handles | Technical | Low |
| M-15 | Intrusive popup interstitial timing risk (mobile) | Technical | Low |

---

## Low Priority / Backlog

- `font-display: swap` missing on web fonts (CLS/performance)
- Server-side GTM implementation (advanced performance optimization)
- Sitemap submission to Bing Webmaster Tools
- Predictive search JS firing on all pages (defer to focus event)
- Product URL handle length audit (flag >70 chars)
- HSTS max-age below 1-year preload threshold
- Video sitemap (if recipe videos are added)
- Press/media coverage page on-site

---

## Prioritized Action Roadmap

### Week 1 — Critical Fixes (All Low-Effort, High-Impact)

| Day | Action | Time | Owner |
|-----|--------|------|-------|
| 1 | Edit `robots.txt.liquid` to allow AI crawlers | 30 min | Dev |
| 1 | Set homepage title + meta description in Shopify admin | 30 min | Marketing |
| 1 | Add Organization schema to `layout/theme.liquid` | 30 min | Dev |
| 2 | Add NutritionInformation schema per product | 2 hrs | Dev |
| 2 | Add crawlable nutritional stats text per product | 2 hrs | Marketing |
| 3 | Draft `llms.txt` file and publish | 2 hrs | Marketing |
| 3–4 | Add author bylines + create founder bio page | 3 hrs | Marketing |
| 5 | Add `fetchpriority="high"` + preload to hero image | 30 min | Dev |
| 5 | Add `defer` to Klaviyo and non-critical app scripts | 1 hr | Dev |

### Month 1 — High Priority

- Expand all product pages to 400+ words of HTML text
- Rewrite About page as crawlable founder story (600–800 words)
- Fix Article schema — add publisher + mainEntityOfPage
- Update internal links to use `/products/` canonical path
- Add FAQ schema to product pages (5–7 Q&A each)
- Create 3 informational blog articles (1,500+ words, attributed, dated)
- Add explicit `width`/`height` to all `<img>` elements
- Implement IndexNow via Shopify SEO app

### Months 2–3 — Authority Building

- Create Wikidata entity for the brand
- Build topical content cluster (10–15 posts) around "Superseed Cereals," "Gluten-Free Breakfast Canada," "Plant-Based Protein Breakfast"
- Pursue independent editorial coverage (Canadian RDs, health food blogs, "best of" lists)
- Implement WebP/AVIF hero image with mobile-specific srcset
- Review and reduce app JS payload (target: <300KB total third-party JS)

---

## Subagent Reports

All detailed reports are in the `/reports/` directory:

| Report | File |
|--------|------|
| GEO / AI Search Readiness | `geo-audit-goldys.ca.md` |
| Technical SEO | `technical-seo-audit-goldys.ca.md` |
| E-E-A-T / Content Quality | `content-eeat-audit-goldys.ca.md` |
| Schema / Structured Data | `schema-audit-goldys.ca.md` |
| XML Sitemap | `sitemap-audit-goldys.ca.md` |
| Core Web Vitals / Performance | `cwv-performance-goldys.ca.md` |
| Visual / Mobile Rendering | `visual-seo-audit-goldys.ca.md` |

---

## Competitive Position Summary

Goldy's currently holds the #1 organic position for "best superseed cereal Canada" — a strong signal of brand authority from retail distribution and off-site mentions. However:

- For broader category queries ("gluten free cereal Canada", "high protein breakfast cereal"), the brand is **invisible**
- Holy Crap Foods outperforms on E-E-A-T (named founders, editorial coverage, informational content)
- The current ranking advantage is **fragile** — built on off-site signals, not on-site content quality
- With the December 2025 core update's tightened E-E-A-T standards, this gap will compress unless on-site content is urgently built out
- Implementing NutritionInformation schema and crawlable nutritional stats would be a **competitive first-mover advantage** — no direct Canadian competitor has done this
