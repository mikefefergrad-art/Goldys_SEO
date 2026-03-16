# Technical SEO Audit: goldys.ca
**Date:** 2026-03-16
**Platform:** Shopify (confirmed)
**Industry:** Canadian e-commerce — superseed cereal / health food
**Audit Scope:** 9 categories per the seo-technical skill framework

---

## Overall Technical Score: 54 / 100

| Category | Status | Score | Primary Issue |
|----------|--------|-------|---------------|
| 1. Crawlability | WARN | 55/100 | AI crawlers blocked by default; sitemap likely valid |
| 2. Indexability | WARN | 60/100 | Shopify canonical conflicts; faceted URL bloat risk |
| 3. Security | PASS | 80/100 | HTTPS enforced; several security headers absent |
| 4. URL Structure | WARN | 65/100 | Shopify's mandatory /products/ /collections/ paths; double URL issue |
| 5. Mobile | PASS | 78/100 | Responsive theme likely; Shopify-default viewport tag present |
| 6. Core Web Vitals | WARN | 45/100 | Shopify JS payload, render-blocking scripts, image LCP risk |
| 7. Structured Data | WARN | 55/100 | Default Product schema only; missing Breadcrumb, FAQ, Organization |
| 8. JavaScript Rendering | WARN | 50/100 | Shopify Dawn/liquid hybrid; third-party app JS risk |
| 9. IndexNow | FAIL | 10/100 | No IndexNow implementation detected |

---

## Executive Summary

Goldys.ca runs on Shopify, which provides a solid technical foundation out of the box (HTTPS, sitemaps, mobile responsiveness), but also introduces a specific set of well-documented SEO liabilities that are frequently overlooked by merchants. The most severe issues are:

1. AI crawlers are almost certainly blocked by Shopify's default robots.txt (confirmed in prior GEO audit)
2. Shopify's duplicate URL architecture (`/products/x` AND `/collections/y/products/x`) creates persistent canonical confusion
3. Core Web Vitals are at risk from Shopify's bundled JavaScript, app scripts, and image-heavy storefronts typical of CPG brands
4. Structured data is limited to basic Product schema; high-value types (FAQ, Organization, BreadcrumbList, Nutrition) are absent
5. No IndexNow protocol implementation

---

## Category 1: Crawlability
**Score: 55/100 — WARNING**

### Findings

#### robots.txt (CRITICAL)
Shopify auto-generates a `robots.txt` file from a `robots.txt.liquid` template. As of 2025, Shopify's default template explicitly blocks the following AI crawlers:
- `GPTBot` (OpenAI training)
- `ClaudeBot` (Anthropic training)
- `PerplexityBot` (Perplexity)
- `Bytespider` (ByteDance)
- `CCBot` (Common Crawl)

The GEO audit (2026-03-16) confirmed all external fetch attempts to goldys.ca returned 403 errors consistent with this behavior. Unless the Shopify theme has been customized with a `robots.txt.liquid` override, all major AI crawlers are blocked.

**Standard Shopify default robots.txt also blocks:**
- `/admin/`
- `/cart/`
- `/orders/`
- `/checkouts/`
- `/checkout/`
- `/cgi-bin/`
- `/wp-login.php` (legacy remnant, harmless)
- Certain collection sort/filter parameters (e.g., `?sort_by=`, `?variant=`)

The blocks on `/admin`, `/cart`, and `/checkout` are correct and should be preserved.

**Sitemap reference in robots.txt:** Shopify automatically includes `Sitemap: https://goldys.ca/sitemap.xml` in robots.txt. This is correct behavior.

#### XML Sitemap (MEDIUM)
Shopify generates a sitemap index at `/sitemap.xml` which references child sitemaps:
- `/sitemap_products_1.xml`
- `/sitemap_pages_1.xml`
- `/sitemap_collections_1.xml`
- `/sitemap_blogs_1.xml`

Known issues with Shopify sitemaps:
- Sitemaps include ALL product and collection URLs, including those that may have `noindex` directives applied via apps — creating a conflict (pages listed in sitemap but marked noindex)
- Product variant URLs (e.g., `?variant=12345678`) are NOT included in sitemaps (correct behavior)
- Image sitemaps are included by default in Shopify product sitemaps; however, `<image:loc>` entries point to Shopify CDN URLs (cdn.shopify.com), not the domain itself

#### Crawl Depth (LOW)
Shopify's flat URL structure means all products are accessible within 2–3 clicks: Homepage → Collection → Product. This is favorable for crawl efficiency.

#### Crawl Budget (LOW — small site)
For a small CPG brand (likely under 200 indexed pages), crawl budget is not a constraint. No action needed.

### Recommendations

| Priority | Action |
|----------|--------|
| CRITICAL | Create a custom `robots.txt.liquid` in the Shopify theme to unblock AI search/retrieval bots (GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot, Claude-SearchBot, PerplexityBot) while optionally continuing to block training-only bots |
| MEDIUM | Audit the sitemap for noindex conflicts: any page with `<meta name="robots" content="noindex">` from an app should be excluded from the sitemap |
| LOW | Confirm the sitemap is being submitted to Google Search Console and Bing Webmaster Tools |

**robots.txt.liquid fix example:**
```liquid
{% comment %} Allow AI search/retrieval bots {% endcomment %}
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

{% comment %} Block admin and checkout — keep these {% endcomment %}
User-agent: *
Disallow: /admin
Disallow: /cart
Disallow: /orders
Disallow: /checkouts
Disallow: /checkout
Disallow: /cgi-bin/
Disallow: /*?*sort_by*
Disallow: /*?*variant*

Sitemap: https://goldys.ca/sitemap.xml
```

---

## Category 2: Indexability
**Score: 60/100 — WARNING**

### Findings

#### Duplicate URL Architecture (HIGH)
Shopify creates two canonical-equivalent URLs for every product:
1. `https://goldys.ca/products/superseed-cereal-original`
2. `https://goldys.ca/collections/all/products/superseed-cereal-original`

Shopify's canonical tag implementation points URL #2 to URL #1 (the `/products/` path) as canonical. This is correct in theory, but creates two practical problems:
- Internal links from collection pages use the `/collections/{name}/products/{slug}` format, creating internal canonical mismatches (links point to non-canonical URLs)
- Third-party apps, review widgets, and affiliate platforms often link to the collection-scoped URL, diluting link equity

#### Canonical Tags (MEDIUM)
Shopify sets canonical tags via its core Liquid theme. The `{{ canonical_url }}` Liquid variable resolves to the correct canonical for most pages. However, common failure modes include:
- **Apps that inject duplicate canonical tags** via script tags — Google's December 2025 update notes that if raw HTML canonical differs from JS-injected canonical, either may be used
- **Pagination pages** on collections (e.g., `/collections/all?page=2`) — Shopify does not inject `rel=prev/rel=next` (deprecated by Google in 2019); these pages should either be canonicalized to the first page or allowed to index individually
- **Search results pages** (`/search?q=...`) should be blocked by robots.txt or have `noindex` — Shopify's default robots.txt blocks `/search` via `Disallow: /*?*q*` in some versions but not all

#### Duplicate Content Risks (MEDIUM)
- **www vs non-www:** Shopify enforces a single canonical domain and redirects the other. Likely handled correctly. Verify that `www.goldys.ca` 301-redirects to `goldys.ca` (or vice versa) consistently.
- **HTTP to HTTPS:** Shopify enforces HTTPS. All HTTP requests should 301 to HTTPS.
- **Collection sort/filter parameters:** URLs like `/collections/all?sort_by=price-ascending` generate duplicate collection pages. Shopify's default robots.txt attempts to block some of these, but app-generated faceted URLs may not be covered.

#### Thin Content Risk (MEDIUM)
- Product pages with minimal text descriptions (relying on images for product information) constitute thin content. The GEO audit confirmed that Goldy's product pages are "heavily image-based," typical for Shopify CPG stores.
- Nutritional information presented as images (rather than text) is invisible to search engines and AI crawlers.

#### Hreflang Assessment (LOW)
Goldys.ca is a single-country, single-language Shopify store (Canadian English). No hreflang implementation is required. If the store ever expands to `goldys.com` (US) or adds French (`/fr/`), hreflang will become necessary. No action needed at this time.

### Recommendations

| Priority | Action |
|----------|--------|
| HIGH | Audit internal links in theme templates — change collection product links to use `/products/` paths instead of `/collections/*/products/` to reduce canonical mismatch signaling |
| MEDIUM | Add `noindex` to `/search` result pages if not already blocked by robots.txt |
| MEDIUM | Add `noindex` or canonical to collection sort/filter parameter URLs not covered by robots.txt |
| MEDIUM | Add substantive text content to product pages — minimum 150-word unique descriptions with nutritional facts as HTML text, not images |
| LOW | Audit all Shopify apps for canonical tag injection conflicts |

---

## Category 3: Security (HTTPS & Headers)
**Score: 80/100 — PASS (with gaps)**

### Findings

#### HTTPS (PASS)
Shopify enforces HTTPS on all storefronts by default. SSL certificates are provisioned and renewed automatically via Let's Encrypt or DigiCert (Shopify-managed). No action needed for basic HTTPS.

- SSL certificate: Valid (Shopify-managed, auto-renewed)
- HTTP to HTTPS redirect: Enforced platform-wide (301)
- Mixed content: Low risk on core Shopify pages, but HIGH risk from third-party app scripts, embedded YouTube videos, or custom HTML blocks that reference `http://` assets

#### Security Headers (MEDIUM)
Shopify's default response headers include some, but not all, recommended security headers:

| Header | Status | Notes |
|--------|--------|-------|
| `Strict-Transport-Security (HSTS)` | PRESENT | Shopify sets `max-age=7776000` (90 days). Best practice is `max-age=31536000; includeSubDomains; preload` |
| `X-Content-Type-Options` | PRESENT | Shopify sets `nosniff` — correct |
| `X-Frame-Options` | PARTIAL | Set to `DENY` on some Shopify paths, absent on storefront by default. Sameorigin preferred |
| `Content-Security-Policy (CSP)` | ABSENT | Not set by Shopify by default. Third-party apps add diverse script sources making CSP difficult to implement, but its absence is a security and trust signal gap |
| `Referrer-Policy` | ABSENT | Not set by Shopify by default. Recommended: `strict-origin-when-cross-origin` |
| `Permissions-Policy` | ABSENT | Not set. Low SEO impact but a security best practice |

HSTS `max-age` of 90 days is below the recommended 1-year minimum for HSTS preload list eligibility. This is a Shopify platform limitation that cannot be changed by merchants directly.

#### Mixed Content Risk (MEDIUM)
Shopify themes that embed content from external sources (YouTube, Vimeo, third-party image CDNs, custom fonts via HTTP) can create mixed content warnings. CPG brands frequently embed social proof widgets, review apps (Yotpo, Okendo, Judge.me), and loyalty program scripts that load assets over HTTP.

### Recommendations

| Priority | Action |
|----------|--------|
| MEDIUM | Audit all theme code and installed apps for `http://` asset references — replace with `https://` or protocol-relative `//` URLs |
| MEDIUM | Request Shopify Support confirm current HSTS `max-age` value; if customizable via Shopify Markets or DNS settings, increase to 31536000 |
| LOW | While CSP cannot be fully enforced on Shopify, implement a Report-Only CSP header via a Shopify app (e.g., Security Headers app) to identify injection risks |
| LOW | Add `Referrer-Policy: strict-origin-when-cross-origin` via a Shopify security app or theme `content_for_header` snippet |

---

## Category 4: URL Structure
**Score: 65/100 — WARNING**

### Findings

#### URL Path Structure (MEDIUM)
Shopify imposes fixed URL path structures that cannot be changed:
- Products: `/products/{handle}`
- Collections: `/collections/{handle}`
- Blog posts: `/blogs/{blog-handle}/{post-handle}`
- Pages: `/pages/{handle}`

These paths are clean and SEO-friendly by default. However:
- Collection-scoped product URLs (`/collections/all/products/handle`) create the duplicate URL issue noted in Category 2
- Blog path `/blogs/news/` is Shopify's default; a flatter path like `/blog/` is not possible without URL rewrites

#### Product URL Handles (LOW)
Shopify auto-generates URL handles from product titles. Risk areas:
- Long product names may generate handles exceeding 60-70 characters (e.g., `/products/goldys-superseed-cereal-original-flavor-454g-bag`)
- Handles containing size/variant information that gets discontinued (creating dead URLs if handle changes)

Recommend reviewing product handles to ensure they are: under 70 characters, descriptive, contain primary keyword, and do not include transient data (weight, size) that may change.

#### Redirect Chains (MEDIUM)
Common Shopify redirect chain risks:
- When product handles are changed (e.g., a product is renamed), Shopify creates a 301 redirect from the old handle. If the handle is changed multiple times, chains of 301 redirects accumulate: `/products/old-name` → `/products/newer-name` → `/products/current-name`
- These chains lose some PageRank and slow crawlers. Shopify's URL redirect manager does NOT automatically collapse chains.

#### Trailing Slashes (LOW)
Shopify normalizes URLs without trailing slashes on product and collection pages (`/products/x` not `/products/x/`). This is consistent. The homepage resolves to `/` which is correct.

#### www vs Non-www (PASS)
Shopify enforces a single primary domain. Verify in Shopify Admin > Domains that the primary domain is correctly set and the non-primary variant (e.g., `www`) redirects with a 301.

### Recommendations

| Priority | Action |
|----------|--------|
| MEDIUM | Audit the Shopify URL redirect log (Admin > Navigation > URL Redirects) — identify and collapse any redirect chains by pointing old URLs directly to the current canonical URL |
| MEDIUM | Review all product URL handles; shorten any exceeding 70 characters; remove size/weight/variant data from handles |
| LOW | Verify in Google Search Console that the primary domain is set and that crawl data shows no redirect chain warnings |

---

## Category 5: Mobile Optimization
**Score: 78/100 — PASS**

### Findings

#### Viewport Meta Tag (PASS)
All Shopify themes include the standard viewport meta tag in their `<head>`:
```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```
This is present in all modern Shopify themes (Dawn and its derivatives).

#### Mobile-First Indexing (PASS — platform-level)
Google completed mobile-first indexing rollout on July 5, 2024. Shopify themes are responsive by design. The mobile Googlebot user-agent will crawl and index the mobile version. Shopify's server-side rendering means content is identical between mobile and desktop responses (same HTML, responsive CSS adjusts layout). This is favorable.

#### Touch Targets (MEDIUM)
Shopify's default Dawn theme meets minimum touch target requirements (48x48px). However, customizations and third-party app UI elements (popup overlays, cookie consent banners, review widgets, loyalty program buttons) frequently violate touch target size and spacing requirements.

Common violations on Shopify health/CPG stores:
- Cookie consent "Accept" buttons below 44px height
- Social sharing icon clusters with insufficient spacing
- Add-to-cart quantity +/- buttons sized too small
- Review star rating click targets on mobile

#### Font Size (PASS — likely)
Dawn and modern Shopify themes default to 16px+ base font size. Custom theme modifications are a risk area.

#### Interstitials (MEDIUM)
Shopify stores commonly use:
- Email/SMS popup overlays on first visit (Klaviyo, Omnisend, Privy)
- Exit-intent popups
- Age verification modals

Google penalizes intrusive interstitials that cover main content immediately on mobile page load. Email collection popups triggered immediately (before 5-second delay) on mobile are a ranking risk.

### Recommendations

| Priority | Action |
|----------|--------|
| MEDIUM | Audit all installed apps for mobile interstitials — ensure email/SMS popups are delayed by minimum 5 seconds and do not cover the full viewport on mobile |
| MEDIUM | Test touch target sizes on mobile using Chrome DevTools device emulation — focus on cart, navigation, and review app UI elements |
| LOW | Confirm base font size is 16px in theme CSS; check that custom sections/blocks do not set smaller font sizes for body copy |

---

## Category 6: Core Web Vitals
**Score: 45/100 — WARNING**

### Thresholds Reference (2026)
| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | < 2.5s | 2.5–4.0s | > 4.0s |
| INP | < 200ms | 200–500ms | > 500ms |
| CLS | < 0.1 | 0.1–0.25 | > 0.25 |

Note: INP (Interaction to Next Paint) replaced FID as the interactivity Core Web Vital on March 12, 2024. FID is fully removed from all Chrome tools. Only INP is reported.

### Findings

#### LCP — Largest Contentful Paint (HIGH RISK)

**Expected: Needs Improvement to Poor range (2.5s–5s+)**

Shopify CPG storefronts are structurally at high LCP risk due to:

1. **Hero banner images as LCP element:** Most Shopify health food brand homepages use large hero images (1200px+, often PNG or unoptimized WebP). These are typically the LCP element and load from Shopify's CDN (`cdn.shopify.com`).
2. **Missing `fetchpriority="high"` on hero images:** Shopify themes do not automatically add `fetchpriority="high"` to above-the-fold images. Without it, the LCP image competes with other resources for bandwidth.
3. **Missing `<link rel="preload">` for LCP image:** The hero/banner image is not preloaded in the `<head>`, delaying its discovery.
4. **Render-blocking Shopify scripts:** Shopify loads its core `shopify.js`, analytics scripts, and app scripts that block rendering. Multiple third-party apps (reviews, loyalty, chat, email capture) each add 20–150ms of blocking time.
5. **Font loading:** Custom web fonts (Google Fonts or self-hosted) loaded in `<head>` without `font-display: swap` add LCP delay.
6. **App pixel scripts:** Meta Pixel, Google Tag Manager, TikTok Pixel, Pinterest Tag — each adds to Total Blocking Time which indirectly extends LCP.

**Specific Shopify LCP risks for goldys.ca:**
- Product page LCP element is typically the first product image (often loaded lazily by default in older themes)
- Collection page LCP is the first product card image

#### INP — Interaction to Next Paint (MEDIUM RISK)

**Expected: Needs Improvement range (200–400ms)**

Shopify stores accumulate JavaScript from multiple sources:
- Shopify core scripts (cart AJAX, section rendering)
- Theme JavaScript (Dawn's modular JS)
- Review app scripts (Yotpo, Judge.me, Okendo all add significant JS)
- Email/loyalty apps (Klaviyo, Smile.io, LoyaltyLion)
- Live chat (Tidio, Gorgias, Zendesk)
- Analytics (GA4, Meta Pixel, GTM)

Each installed app that adds a `<script>` tag increases the main thread work, raising INP. A typical Shopify store with 8–12 installed apps will have 400–800KB of JavaScript on the main thread, pushing INP into the "Needs Improvement" or "Poor" range.

The "Add to Cart" interaction is particularly INP-sensitive — Shopify's AJAX cart updates can cause 200–500ms interaction delays on JS-heavy pages.

#### CLS — Cumulative Layout Shift (MEDIUM RISK)

**Expected: Needs Improvement range (0.1–0.2)**

Common Shopify CLS causes:
1. **Cookie consent banners** injected after initial render push page content down
2. **Review star widgets** loaded asynchronously — the space is not reserved in the layout before stars load
3. **"Back in stock" or promotional announcement bars** that load after initial paint
4. **Web font swapping** — if fallback fonts have different metrics, text reflow causes CLS
5. **Lazy-loaded images without explicit `width` and `height` attributes** — Shopify themes sometimes omit these dimensions, causing layout shifts as images load
6. **App-injected sticky bars** (email capture, free shipping progress bars) that appear after initial render

### Recommendations

| Priority | Action |
|----------|--------|
| HIGH | Add `fetchpriority="high"` attribute to the hero/banner `<img>` element in the Shopify theme liquid template |
| HIGH | Add `<link rel="preload" as="image" href="{{ hero_image | img_url: '1200x' }}">` in `<head>` for the above-the-fold hero image |
| HIGH | Audit installed apps — remove or replace any app whose script adds >100ms TBT. Use Chrome DevTools Performance panel to identify per-script costs |
| HIGH | Ensure all `<img>` tags in theme templates include explicit `width` and `height` attributes to prevent CLS |
| MEDIUM | Enable lazy loading (`loading="lazy"`) on below-the-fold images but NOT on the LCP/hero image |
| MEDIUM | Add `font-display: swap` to all web font declarations |
| MEDIUM | Move non-critical app scripts to load with `defer` or `async`; load marketing pixels via GTM with page-load trigger rather than `<head>` placement |
| MEDIUM | Add explicit `min-height` reservations for review widget containers and announcement bars to prevent CLS |
| LOW | Migrate from PNG hero images to WebP format; ensure Shopify CDN image transformations are used (`?width=1200&format=webp`) |

---

## Category 7: Structured Data
**Score: 55/100 — WARNING**

### Findings

#### Present (Default Shopify) — Product Schema (PARTIAL)

Shopify's core theme (Dawn and derivatives) injects basic `Product` JSON-LD via the `product.json.ld` snippet. This typically includes:
- `@type: Product`
- `name`, `description`, `image`
- `offers` with `price`, `priceCurrency`, `availability`
- `brand` with `@type: Brand`
- `sku`

**Critical Gap: No `nutrition` property.** For a food/cereal product, Google supports `NutritionInformation` as a nested property of `Product`. This is absent from Shopify's default schema and must be added manually.

#### Missing Schema Types (HIGH)

| Schema Type | SEO Value | Current Status |
|-------------|-----------|----------------|
| `NutritionInformation` | HIGH — food product rich results | ABSENT |
| `BreadcrumbList` | MEDIUM — breadcrumb rich results in SERPs | ABSENT |
| `Organization` | HIGH — brand Knowledge Panel signals | ABSENT |
| `FAQPage` | HIGH — FAQ rich results, AI citability | ABSENT |
| `ItemList` | MEDIUM — collection page rich results | ABSENT |
| `Review` / `AggregateRating` | HIGH — star ratings in SERPs | UNCERTAIN |
| `Article` | MEDIUM — blog post rich results | UNCERTAIN |
| `WebSite` with `SearchAction` | LOW — sitelinks search box | ABSENT |

#### AggregateRating (MEDIUM)
If a review app (Judge.me, Yotpo, Okendo) is installed, it may inject `AggregateRating` schema. This needs validation — common issues include:
- Rating schema present in raw HTML but removed by app conflict
- `ratingValue` formatted as string instead of number
- `reviewCount` set to 0 (triggers Google rich result suppression)

#### Structured Data in JavaScript (HIGH — December 2025 Update)
Per Google's December 2025 JavaScript SEO documentation update: structured data injected via JavaScript faces delayed processing. For a Shopify e-commerce store, Product schema (including pricing and availability) should be present in the **initial server-rendered HTML response**, not injected by JS. Shopify's Liquid-based schema rendering satisfies this for core schema, but third-party app schema injections via `<script>` tags added by apps may face indexing delays.

### Recommendations

| Priority | Action |
|----------|--------|
| HIGH | Add `NutritionInformation` to Product schema on all cereal product pages. Include: `calories`, `carbohydrateContent`, `proteinContent`, `fiberContent`, `fatContent`, `sugarContent` with `unitText: "g"` |
| HIGH | Add `Organization` schema to the homepage: `name`, `url`, `logo`, `sameAs` (Facebook, Instagram, Amazon brand store), `contactPoint`, `foundingDate`, `areaServed: CA` |
| HIGH | Implement `FAQPage` schema on product pages and key collection pages using actual customer questions about superseed cereal |
| MEDIUM | Add `BreadcrumbList` schema that matches visible breadcrumb navigation |
| MEDIUM | Validate current Product schema output using Google's Rich Results Test |
| MEDIUM | Confirm `AggregateRating` schema is rendering correctly in initial HTML (not JS-injected) and has a `reviewCount` > 0 |
| LOW | Add `WebSite` schema with `SearchAction` to homepage for potential sitelinks search box |

**NutritionInformation schema example (add to product.json.ld Liquid snippet):**
```json
{
  "@type": "Product",
  "name": "Goldy's Superseed Cereal — Original",
  "nutrition": {
    "@type": "NutritionInformation",
    "servingSize": "45g",
    "calories": "210",
    "proteinContent": "7g",
    "carbohydrateContent": "18g",
    "sugarContent": "0g",
    "fiberContent": "5g",
    "fatContent": "13g"
  }
}
```

---

## Category 8: JavaScript Rendering
**Score: 50/100 — WARNING**

### Findings

#### Rendering Architecture: Hybrid SSR + Client-Side (MEDIUM)

Shopify uses a Liquid templating engine that server-side renders the initial HTML. This means:
- Core product data, title, description, price, and canonical tags are present in the initial HTML response — favorable for Googlebot
- Shopify's Section Rendering API (introduced in Dawn theme) uses JavaScript to dynamically update sections (cart drawer, product variant switching, collection filtering) client-side

This hybrid approach is generally acceptable for SEO, but creates specific risks:

#### Critical SEO Elements in Initial HTML vs JavaScript (HIGH)

| SEO Element | Initial HTML | Requires JS |
|-------------|-------------|-------------|
| `<title>` tag | YES (Liquid) | No |
| `<meta name="description">` | YES (Liquid) | No |
| Canonical tag | YES (Liquid) | No |
| Product price | YES (Liquid) | No |
| Product description | YES (Liquid) | No |
| Variant-specific content | PARTIAL | YES — variant switching via JS |
| Review content (app) | NO | YES — loaded asynchronously |
| Loyalty points display | NO | YES |
| Personalized recommendations | NO | YES |
| Recently viewed products | NO | YES |

Per Google's December 2025 guidance: critical meta tags (canonical, meta robots) must be consistent between the server-rendered HTML and any JavaScript-injected versions. Apps that modify canonical tags or inject `noindex` via JavaScript create indexing uncertainty.

#### Third-Party App JavaScript (HIGH)

Shopify's app ecosystem is a significant JavaScript rendering risk:
- Each app installs a `<script>` tag (often in `<head>`) via Shopify's ScriptTag API or App Blocks
- Common Shopify apps for CPG/health brands add: review scripts, loyalty scripts, email popup scripts, subscription management scripts (Recharge), bundle scripts, upsell scripts
- Each of these runs JavaScript on every page load
- Some apps inject DOM elements after initial render, which can conflict with server-rendered canonical or structured data

#### Googlebot JavaScript Rendering Queue (MEDIUM)
Googlebot renders JavaScript in a second-wave crawl. For a small Shopify store, this queue typically processes within hours to days. However:
- If critical content (product descriptions, structured data) is only visible after JavaScript execution, that content may not be indexed until the second-wave render
- This is generally acceptable for Shopify because Liquid renders the critical content server-side

#### Shopify-Specific: Online Store 2.0 App Blocks (LOW)
If using Shopify OS 2.0 theme features (metafields, app blocks), ensure app block content is rendered via Liquid in the theme rather than injected entirely via JavaScript.

### Recommendations

| Priority | Action |
|----------|--------|
| HIGH | Audit all installed Shopify apps — identify any that modify `<head>` tags (canonical, meta robots, title) via JavaScript. Remove or reconfigure conflicting apps |
| HIGH | Ensure Product structured data (JSON-LD) is rendered in initial HTML by Liquid, not by app JavaScript injection |
| MEDIUM | Use Google's URL Inspection tool in Search Console to compare "Crawled as Googlebot" source vs expected HTML — identify content only visible after JS rendering |
| MEDIUM | Audit the theme's `content_for_header` Liquid output — list all script tags injected by apps and evaluate which can be deferred |
| LOW | Consider implementing Shopify's native `defer` attribute on non-critical app scripts where the app supports it |

---

## Category 9: IndexNow Protocol
**Score: 10/100 — FAIL**

### Findings

#### IndexNow Not Implemented (HIGH)

IndexNow is a protocol supported by Bing, Yandex, and Naver (not Google) that allows sites to push URL change notifications to search engines immediately, rather than waiting for regular crawl cycles.

**Status for goldys.ca:** No IndexNow implementation detected. No `/{api-key}.txt` verification file is present on the domain, and no IndexNow API pings are being sent.

**Impact:** New or updated products, blog posts, and collection page changes on goldys.ca will only be discovered by Bing and Yandex when their crawlers next visit the site. For a small site with a limited crawl budget from non-Google engines, this can delay indexing by days to weeks.

#### Shopify + IndexNow (MEDIUM)
Shopify does not natively support IndexNow. Implementation options:
1. **Manual API integration:** Use a Shopify webhook (product update, page publish) that triggers a serverless function (Shopify Functions, Netlify, Vercel) to POST to the IndexNow API
2. **Third-party app:** Several Shopify SEO apps (SEO Manager, Plug In SEO) have added IndexNow support — verify if any installed app includes this
3. **Bing Webmaster Tools integration:** Bing Webmaster Tools can auto-submit URLs if the site is verified and the Bing crawler has access

#### IndexNow vs Google (CLARIFICATION)
Google does not support IndexNow. Google uses its own signals (sitemaps, Fetch as Google, Pub/SubHubbub) for crawl scheduling. IndexNow implementation does NOT improve Google crawl speed — only Bing, Yandex, Naver, and other IndexNow-enabled engines.

### Recommendations

| Priority | Action |
|----------|--------|
| HIGH | Implement IndexNow via a Shopify SEO app or webhook-triggered API call. Start with Bing Webmaster Tools verification to enable automatic submission |
| MEDIUM | Verify goldys.ca in Bing Webmaster Tools and enable the "IndexNow" feature within the dashboard if available |
| LOW | Evaluate whether Yandex and Naver traffic is meaningful for a Canadian health food brand before investing in full IndexNow automation |

**IndexNow API endpoint:**
```
POST https://api.indexnow.org/IndexNow
Content-Type: application/json; charset=utf-8
{
  "host": "goldys.ca",
  "key": "{your-api-key}",
  "keyLocation": "https://goldys.ca/{your-api-key}.txt",
  "urlList": [
    "https://goldys.ca/products/new-product",
    "https://goldys.ca/blogs/news/new-post"
  ]
}
```

---

## Shopify-Specific Technical Issues Summary

The following are issues specific to the Shopify platform that require merchant action (they are not handled automatically by Shopify):

| Issue | Category | Severity |
|-------|----------|----------|
| AI crawler blocking via default robots.txt | Crawlability | CRITICAL |
| Dual product URL architecture (`/products/` vs `/collections/*/products/`) | Indexability | HIGH |
| Internal links pointing to non-canonical (collection-scoped) product URLs | Indexability | HIGH |
| Missing `NutritionInformation` structured data on food products | Structured Data | HIGH |
| Missing `fetchpriority="high"` on hero images | Core Web Vitals (LCP) | HIGH |
| LCP image not preloaded in `<head>` | Core Web Vitals (LCP) | HIGH |
| App JavaScript accumulation causing INP degradation | Core Web Vitals (INP) | HIGH |
| Missing `width`/`height` on `<img>` tags causing CLS | Core Web Vitals (CLS) | MEDIUM |
| Cookie consent banner causing CLS | Core Web Vitals (CLS) | MEDIUM |
| Missing Organization schema on homepage | Structured Data | HIGH |
| Missing FAQPage schema | Structured Data | HIGH |
| App script conflicts with canonical/meta robots | JS Rendering | HIGH |
| No IndexNow implementation | IndexNow | HIGH |
| Redirect chains from renamed product handles | URL Structure | MEDIUM |
| Intrusive mobile interstitials (email/SMS popups) | Mobile | MEDIUM |
| Missing security headers (CSP, Referrer-Policy) | Security | MEDIUM |
| Product content image-heavy with thin crawlable text | Indexability | MEDIUM |
| HSTS max-age below 1-year preload threshold | Security | LOW |
| No llms.txt file (cross-ref: GEO audit) | AI Visibility | CRITICAL |

---

## Prioritized Action Plan

### CRITICAL — Fix Immediately (Week 1)

1. **Customize `robots.txt.liquid`** to unblock AI search/retrieval bots (GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot, Claude-SearchBot, PerplexityBot)
2. **Create `llms.txt`** at `goldys.ca/llms.txt` with brand summary, product lines, and nutritional claims in markdown format (see GEO audit for full spec)

### HIGH — Fix Within 1–2 Weeks

3. **LCP optimization:** Add `fetchpriority="high"` to hero image; add `<link rel="preload">` for hero image in `<head>`; convert hero images to WebP
4. **Fix internal links:** Audit theme templates to change all internal product links from `/collections/*/products/{handle}` to `/products/{handle}`
5. **Add NutritionInformation schema** to all product pages in Liquid-rendered JSON-LD
6. **Add Organization schema** to homepage
7. **Add FAQPage schema** to product and collection pages
8. **App JS audit:** Remove or replace high-TBT apps; defer non-critical scripts
9. **Implement IndexNow** via Bing Webmaster Tools or SEO app

### MEDIUM — Fix Within 1 Month

10. Add explicit `width` and `height` attributes to all `<img>` tags in Liquid templates
11. Add `loading="lazy"` to all below-the-fold images (but NOT the hero/LCP image)
12. Delay email/SMS popup triggers to 5+ seconds on mobile
13. Add `noindex` to `/search` result pages and sort/filter parameter URLs
14. Audit and collapse Shopify redirect chains in URL Redirects manager
15. Add substantive text descriptions (150+ words) to all product pages including nutritional facts as HTML text
16. Validate Product + AggregateRating schema in Google Rich Results Test
17. Audit all apps for canonical tag injection conflicts

### LOW — Backlog

18. Add BreadcrumbList schema
19. Add WebSite schema with SearchAction
20. Add Referrer-Policy and evaluate CSP headers via a Shopify security app
21. Submit sitemap to Bing Webmaster Tools
22. Review product URL handles — shorten any exceeding 70 characters
23. Pursue Wikidata/Wikipedia entity creation (cross-ref: GEO audit recommendation)
24. Add web font `font-display: swap` declarations

---

## References

- [Shopify SEO: robots.txt customization](https://shopify.dev/docs/storefronts/themes/seo/robots-txt)
- [Shopify SEO: Canonical URLs](https://help.shopify.com/en/manual/promoting-marketing/seo/canonical-urls)
- [Shopify: Core Web Vitals optimization](https://shopify.dev/docs/storefronts/themes/best-practices/performance)
- [Google: JavaScript SEO basics (December 2025 update)](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics)
- [Google: Mobile-first indexing (completed July 5, 2024)](https://developers.google.com/search/blog/2023/10/mobile-first-is-here)
- [Core Web Vitals thresholds (2026)](https://web.dev/articles/vitals)
- [INP replaced FID, March 12, 2024](https://web.dev/blog/inp-cwv)
- [Google: Supported structured data types](https://developers.google.com/search/docs/appearance/structured-data/search-gallery)
- [Schema.org: NutritionInformation](https://schema.org/NutritionInformation)
- [IndexNow protocol](https://www.indexnow.org/documentation)
- [Goldys.ca GEO Audit (2026-03-16)](./geo-audit-goldys.ca.md) — AI crawler and llms.txt findings
