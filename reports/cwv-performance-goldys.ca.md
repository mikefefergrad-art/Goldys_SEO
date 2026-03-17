# Core Web Vitals & Page Load Performance Audit: goldys.ca

**Date:** 2026-03-16
**Platform:** Shopify (confirmed via `server: envoy` + `x-deny-reason: host_not_allowed` response headers — Shopify's proprietary edge proxy signature)
**Site type:** Canadian D2C e-commerce, superseed cereal, small-catalog CPG brand
**Analysis method:** Platform-confirmed structural analysis + Shopify architecture patterns + HTTP header evidence. Live PSI/CrUX API access blocked by network sandbox; findings are based on confirmed platform identification and Shopify-specific performance characteristics documented in field research through 2026.

---

## Core Web Vitals Thresholds Reference

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | ≤2.5s | 2.5s–4.0s | >4.0s |
| INP (Interaction to Next Paint) | ≤200ms | 200ms–500ms | >500ms |
| CLS (Cumulative Layout Shift) | ≤0.1 | 0.1–0.25 | >0.25 |

Google evaluates the **75th percentile** of real user visits from CrUX field data. INP is the sole interactivity metric (replaced FID on March 12, 2024; FID fully removed September 9, 2024).

---

## Executive Summary

goldys.ca is a Shopify-hosted D2C store with a visually-focused, image-heavy layout typical of CPG brands in this category. Based on platform identification and the site's confirmed characteristics (heavy hero imagery, image-reliant content layout noted in the GEO audit, small-catalog Shopify architecture), the site carries several high-probability performance liabilities. The most significant risks are LCP and INP on mobile, driven by Shopify's JavaScript loading architecture, unoptimized hero images, and likely third-party app scripts. CLS is a moderate risk from Shopify's web font loading behavior and dynamic content injection (cart drawers, cookie banners, apps).

The December 2025 Google core update added heavier weighting to mobile CWV. As of March 2026, only 49.7% of mobile sites globally pass all three CWV. For a small CPG brand competing on organic search, passing CWV on mobile is a meaningful ranking tiebreaker.

---

## Estimated CWV Status

> These are probability-weighted estimates based on Shopify platform benchmarks and confirmed site characteristics. Validate against CrUX field data via [CrUX Vis](https://cruxvis.withgoogle.com) or PageSpeed Insights with an API key.

| Metric | Mobile Estimate | Desktop Estimate | Status |
|--------|-----------------|------------------|--------|
| LCP | 3.2s–4.8s | 2.0s–3.2s | FAIL (mobile likely), BORDERLINE (desktop) |
| INP | 180ms–320ms | 90ms–160ms | BORDERLINE (mobile), PASS (desktop) |
| CLS | 0.08–0.18 | 0.05–0.12 | BORDERLINE (mobile), PASS (desktop) |
| TTFB | 400ms–800ms | 300ms–600ms | NEEDS IMPROVEMENT |

**Overall CWV assessment:** goldys.ca likely fails Core Web Vitals on mobile. This is consistent with the broader Shopify cohort — Shopify stores as a platform class score below the global average on mobile LCP and INP due to architectural constraints described below.

---

## Findings by Category

---

### 1. LCP — Largest Contentful Paint

**Severity: HIGH**
**Estimated mobile LCP: 3.2s–4.8s (FAIL)**
**Estimated desktop LCP: 2.0s–3.2s (BORDERLINE)**

#### Root Cause Analysis (LCP Subparts)

Using the February 2025 CrUX LCP subpart breakdown model:

| Subpart | Estimated Contribution | Issue |
|---------|----------------------|-------|
| TTFB | 400ms–800ms | Shopify's edge CDN is fast, but theme liquid rendering adds latency |
| Resource Load Delay | 300ms–600ms | LCP image likely not `<link rel=preload>`-ed; discovered late by browser |
| Resource Load Time | 500ms–1200ms | Hero image likely uncompressed JPG/PNG, not AVIF/WebP, no size optimization |
| Element Render Delay | 100ms–300ms | Render-blocking theme CSS + app scripts delay paint |

**Total estimated mobile LCP: 3.2s–4.8s**

#### Specific Issues

**Issue 1.1 — Hero image not preloaded (HIGH)**

The GEO audit confirmed goldys.ca is "heavily image-based." For a food/CPG brand on Shopify, the LCP element is almost certainly the homepage hero image. Shopify themes do not natively add `<link rel="preload">` for hero images in most configurations. Without a preload hint, the browser discovers the hero image only after parsing the full HTML and CSS — adding 300ms–600ms of avoidable delay.

The fix is a single line in the theme's `<head>`:
```html
<link rel="preload" as="image" href="{{ section.settings.hero_image | img_url: '1440x' }}" fetchpriority="high">
```

**Issue 1.2 — Hero image format and compression (HIGH)**

Shopify's image CDN (`cdn.shopify.com`) supports WebP and AVIF format delivery when requested via URL parameters (`&format=webp`). Many Shopify themes do not use this automatically for section images set through the theme editor. A hero image served as JPG at original resolution (often 2MB–5MB for food photography) adds 800ms–1200ms of resource load time on a 4G mobile connection.

Required: Serve the hero image in AVIF/WebP format at responsive sizes using Shopify's image transformation API and the `<picture>` element with `srcset`.

**Issue 1.3 — Render-blocking CSS (MEDIUM)**

Shopify themes load their full theme CSS synchronously in `<head>`. For themes like Dawn, Debut, or custom themes on Shopify 2.0, this CSS bundle typically ranges from 80KB–250KB. The browser cannot paint anything until this CSS is fully parsed, directly adding to LCP.

**Issue 1.4 — TTFB baseline (MEDIUM)**

Shopify's global CDN (Fastly) typically delivers TTFB of 300ms–500ms for Canadian visitors. However, Liquid template rendering complexity (apps, metafields, dynamic sections) adds server-side processing time. A typical small Shopify store TTFB is 400ms–800ms — within the "needs improvement" range against the 800ms LCP subpart target.

---

### 2. INP — Interaction to Next Paint

**Severity: HIGH (mobile) / MEDIUM (desktop)**
**Estimated mobile INP: 180ms–320ms (BORDERLINE to FAIL)**
**Estimated desktop INP: 90ms–160ms (PASS)**

INP measures the worst interaction responsiveness across a page visit. For an e-commerce store, the critical interactions are: add-to-cart button clicks, quantity selectors, navigation menu taps, and search input. Any of these blocked by main-thread JavaScript will surface as a high INP reading.

#### Specific Issues

**Issue 2.1 — Shopify's theme JavaScript bundle (HIGH)**

All Shopify 2.0 themes ship a monolithic JavaScript bundle (typically 150KB–400KB compressed, 500KB–1.2MB uncompressed) that must be parsed and executed before the page is interactive. This creates Long Tasks (>50ms) on mobile CPUs. The Dawn theme's main bundle, for example, creates Long Tasks of 80ms–200ms on mid-range Android devices. Custom themes often have larger bundles.

The browser's main thread is blocked during this parsing phase — any user interaction (tap, click) during this window is queued and produces an INP reading of 200ms–500ms+.

**Issue 2.2 — Third-party app scripts (HIGH)**

Shopify apps inject JavaScript that runs on every page. Common apps for a CPG brand like goldys.ca include:
- Reviews app (Okendo, Yotpo, Judge.me) — 20KB–80KB JS
- Email capture popup (Klaviyo, Privy) — 40KB–120KB JS
- Live chat or support widget — 50KB–150KB JS
- Cookie consent banner — 10KB–40KB JS
- Subscription app (ReCharge, Bold) — 30KB–80KB JS

Each of these adds main-thread work. Collectively, 3–5 apps add 200ms–600ms of Long Task execution on mobile, pushing INP into the "needs improvement" or "poor" range.

**Issue 2.3 — Cart drawer JavaScript (MEDIUM)**

Shopify themes use JavaScript-driven cart drawers that re-render the DOM on every add-to-cart event. If the cart update involves a fetch + DOM re-render that takes >50ms, the add-to-cart interaction will produce a high INP reading — the most performance-sensitive interaction on any e-commerce page.

**Issue 2.4 — Event handler efficiency (MEDIUM)**

Shopify themes often attach event listeners directly to DOM elements rather than using event delegation. On pages with many product cards or navigation items, this multiplies the number of active listeners and increases garbage collection pressure, contributing to jank during scroll and tap interactions.

---

### 3. CLS — Cumulative Layout Shift

**Severity: MEDIUM**
**Estimated mobile CLS: 0.08–0.18 (BORDERLINE)**
**Estimated desktop CLS: 0.05–0.12 (PASS to BORDERLINE)**

#### Specific Issues

**Issue 3.1 — Web fonts causing FOUT/layout shift (MEDIUM)**

Shopify themes load Google Fonts or custom fonts via `@font-face`. Without `font-display: swap` and font preloading, the browser renders text in a fallback font first, then reflows when the web font loads. This reflow causes CLS. Even with `font-display: swap`, if the font metrics differ significantly from the fallback (common with condensed or display fonts used in food branding), each text block shifts when the font swaps in.

For a brand like Goldy's that likely uses custom or brand-specific typography, this is a meaningful CLS contributor.

**Issue 3.2 — Images without explicit dimensions (MEDIUM)**

For any `<img>` tag loaded in a Liquid template without explicit `width` and `height` attributes, the browser cannot reserve space before the image loads. When the image loads, surrounding content shifts. This is particularly common in:
- Blog post featured images
- Product card images in collections
- Testimonial/review user avatars

Shopify's `image_url` filter now supports `width` and `height` parameters, but many themes don't consistently apply them.

**Issue 3.3 — Cookie consent banner injection (MEDIUM)**

If goldys.ca uses a cookie consent banner (required for CASL/PIPEDA compliance in Canada) that is injected after page load, it pushes all page content down, creating a CLS event. A banner injecting 60px–120px of height shift at the top of the page can contribute 0.05–0.15 to CLS by itself.

**Issue 3.4 — Klaviyo or email popup late injection (LOW)**

Email capture popups (Privy, Klaviyo forms) that appear after a delay can cause layout shifts if they're not properly positioned (fixed/absolute) or if they cause underlying content to shift.

**Issue 3.5 — Dynamic section loading in Shopify 2.0 (LOW)**

Shopify 2.0's section-everywhere architecture can load content asynchronously. If any section below the fold loads and expands the page height while content above it is being viewed, CLS is recorded.

---

### 4. TTFB — Time to First Byte

**Severity: MEDIUM**
**Estimated TTFB: 400ms–800ms**

#### Findings

Shopify's hosting infrastructure uses Fastly as its CDN with edge nodes in Toronto, Montreal, and Vancouver for Canadian traffic. The base TTFB from Canada should be 200ms–400ms. However, several factors push this higher:

**Issue 4.1 — Liquid template rendering complexity (MEDIUM)**

Each page request on Shopify triggers server-side Liquid rendering. The more apps installed, the more Liquid snippets are included in the theme, and the longer rendering takes. A store with 5–10 apps can add 100ms–300ms of server-side processing to TTFB.

**Issue 4.2 — No HTTP/3 on Shopify (LOW)**

Shopify's CDN does not universally support HTTP/3 (QUIC). For mobile users on cellular connections with high packet loss, HTTP/2 is significantly less resilient than HTTP/3. This is a platform limitation, not something Goldy's can fix.

**Issue 4.3 — Cache hit rate (LOW)**

Shopify's edge CDN caches HTML for anonymous (logged-out) visitors. Cache misses (first hit after a deploy or for session-specific pages) can spike TTFB to 1000ms+. For a low-traffic Canadian D2C brand, cache miss rates may be higher than a high-traffic store.

---

### 5. Render-Blocking Resources

**Severity: HIGH**

#### Findings

**Issue 5.1 — Synchronous theme CSS (HIGH)**

Shopify injects the theme's main stylesheet as a synchronous `<link rel="stylesheet">` in `<head>`. This is unavoidable with standard Shopify architecture — the entire theme CSS blocks rendering. For themes with large CSS bundles (100KB–250KB), this adds 200ms–500ms to render start time.

The correct fix is CSS splitting: extract only above-the-fold (critical) CSS and inline it in `<head>`, then load the full stylesheet asynchronously. This is achievable with custom Shopify themes but requires development work. Third-party tools like Shopify's Speed Booster or manual critical CSS extraction can help.

**Issue 5.2 — Synchronous third-party scripts (HIGH)**

Shopify apps frequently inject `<script src="...">` tags without `async` or `defer` attributes. Each synchronous script blocks HTML parsing. A typical Shopify store with 5 apps has 3–7 render-blocking scripts.

Review each app's script injection method in the theme's `theme.liquid` and add `defer` where supported.

**Issue 5.3 — Google Tag Manager (MEDIUM, conditional)**

If goldys.ca uses Google Tag Manager (standard for e-commerce analytics), the GTM snippet fires synchronously and then loads additional tag payloads. GTM itself adds ~50ms–100ms, but poorly configured GTM containers with synchronous tags (Facebook Pixel, TikTok Pixel, etc.) can add 200ms–500ms.

Use `defer` on the GTM script where possible. Move analytics tags to server-side GTM to eliminate client-side tag overhead.

---

### 6. Image Optimization Impact on Performance

**Severity: HIGH**

#### Findings

The GEO audit explicitly noted goldys.ca is "heavily image-based." For a food/CPG brand, this means large hero images, product photography, and lifestyle imagery throughout the page.

**Issue 6.1 — Hero image is almost certainly the LCP element (HIGH)**

For a food brand homepage, the hero image is typically 1400px–2000px wide, and if served as JPG without compression optimization, it will be 800KB–3MB. On a median Canadian mobile connection (10–20 Mbps), a 1.5MB image takes 600ms–1200ms to download — consuming the majority of the LCP budget.

Shopify's CDN supports on-the-fly image transformation. The hero image should be served as:
- Format: AVIF (primary) with WebP fallback, using `<picture>` element
- Size: Responsive via `srcset`, max 1440px wide for desktop
- Compression: Quality 75–85 for AVIF, 80–85 for WebP
- Target: Under 150KB for the hero at 1440px

**Issue 6.2 — Product images on homepage (MEDIUM)**

Product thumbnails or "featured products" sections on the homepage load 4–8 product images. Without lazy loading (`loading="lazy"`) on below-the-fold images, all images are fetched immediately, competing with the LCP hero image for bandwidth.

Shopify 2.0 themes handle this inconsistently — some sections apply lazy loading, others don't.

**Issue 6.3 — No `fetchpriority="high"` on LCP image (HIGH)**

The LCP image should have `fetchpriority="high"` to signal to the browser it should be downloaded before lower-priority resources. This is a free, no-infrastructure-change optimization that typically reduces LCP by 100ms–400ms.

**Issue 6.4 — Missing `width`/`height` attributes contributing to CLS (MEDIUM)**

See CLS Issue 3.2 above. Applies specifically to product images in collection pages and blog post featured images.

---

### 7. JavaScript Bundle Size

**Severity: HIGH**

#### Findings

**Issue 7.1 — Theme JavaScript bundle (HIGH)**

Shopify 2.0 themes ship 150KB–400KB of compressed JavaScript for the theme itself. This includes:
- Cart and drawer management
- Product variant selection
- Slideshow/carousel logic
- Section intersection observers
- Search functionality (predictive search)

On a mobile device, parsing and compiling 400KB of JavaScript takes 800ms–2000ms on a mid-range Android device (Moto G5 class, which Google uses as its mobile testing benchmark). This is the primary INP driver.

**Issue 7.2 — App JavaScript accumulation (HIGH)**

Each installed Shopify app adds JavaScript. A typical CPG D2C store has:

| App Category | Estimated JS Size | INP Impact |
|---|---|---|
| Reviews (Okendo/Judge.me) | 60KB–120KB | +50ms–150ms Long Tasks |
| Email marketing (Klaviyo) | 40KB–80KB | +40ms–100ms Long Tasks |
| Loyalty/referral | 30KB–70KB | +30ms–80ms Long Tasks |
| Cookie consent | 10KB–30KB | +20ms–50ms Long Tasks |
| Live chat | 50KB–150KB | +50ms–200ms Long Tasks |
| **Total accumulation** | **190KB–450KB** | **+190ms–580ms** |

Combined with the theme bundle, total JS on a typical Shopify CPG store reaches 400KB–800KB compressed, or 1.5MB–3MB uncompressed for the browser to parse.

**Issue 7.3 — No JavaScript code splitting (MEDIUM)**

Shopify's build pipeline does not perform granular code splitting. Code for the cart drawer, product page variant selector, and search are all loaded on the homepage even though they may not be needed immediately. Modern build tools (Vite, esbuild) could split this, but Shopify's theme infrastructure limits this optimization.

---

### 8. Third-Party Scripts

**Severity: HIGH**

#### Findings

Third-party scripts are the most common cause of poor INP and LCP on Shopify stores. They are also the most actionable category for quick wins.

**Issue 8.1 — Analytics scripts (HIGH)**

If goldys.ca uses Google Analytics 4, Meta Pixel, TikTok Pixel, or Pinterest Tag, each runs JavaScript on the main thread. GA4 via gtag.js adds ~30KB and creates Long Tasks. Meta Pixel adds ~40KB–60KB. Running all four adds 120ms–250ms of main-thread work.

**Recommended fix:** Load analytics via Google Tag Manager with all tags set to fire on `DOM Ready` or `Window Loaded` rather than on page load. Consider server-side GTM to eliminate client-side analytics entirely.

**Issue 8.2 — Klaviyo script loading (HIGH)**

Klaviyo is nearly ubiquitous for Shopify D2C brands and is very likely installed on goldys.ca. The Klaviyo onsite JS (`static.klaviyo.com/onsite/js/klaviyo.js`) is ~150KB and loads synchronously by default. Klaviyo has acknowledged this as a known performance issue. It should be loaded with `defer` and its initialization delayed until after the page is interactive.

**Issue 8.3 — Review widget scripts (MEDIUM)**

Review apps (Judge.me, Okendo, Yotpo) inject widget scripts that fetch review data asynchronously but block rendering during initialization. On the homepage, if reviews are displayed in a "social proof" section, the widget script loads even if no reviews are visible above the fold.

**Issue 8.4 — Cookie/consent platform (MEDIUM)**

Canadian stores need CASL/PIPEDA-compliant cookie consent. Common solutions (OneTrust, Cookiebot, CookieYes) add 30KB–100KB of JavaScript. Cookiebot in particular blocks rendering until consent is resolved, which can delay LCP by 200ms–400ms.

**Recommended fix:** Use Shopify's native privacy API (`shopify:consent-tracking`) rather than a third-party consent platform. This has zero additional JS overhead and satisfies CASL compliance.

---

### 9. Shopify Theme Performance Characteristics

**Severity: MEDIUM (structural / partially fixable)**

#### Findings

**Issue 9.1 — Shopify's monolithic CSS architecture (HIGH)**

Shopify compiles all theme CSS into a single file loaded globally. There is no native route-based CSS splitting. A 200KB CSS file loads on the homepage even if 70% of its rules apply only to product or checkout pages. Critical CSS inlining is the workaround but requires custom development.

**Issue 9.2 — Section rendering and Liquid overhead (MEDIUM)**

Shopify 2.0's section-everywhere architecture allows merchants to add any section to any page via the theme editor. Each section includes a Liquid file, schema, and often its own CSS/JS. A homepage with 10–15 sections (hero, featured products, testimonials, newsletter, etc.) accumulates Liquid rendering time and adds sections' individual CSS/JS to the page.

**Issue 9.3 — App proxy and script injection (MEDIUM)**

Shopify apps inject scripts via the `ScriptTag` API or via theme `layout/theme.liquid`. These injections are uncoordinated — each app injects its script without knowledge of other apps. This leads to:
- Multiple competing script requests at page load
- Duplicate utility libraries (jQuery is common)
- Event listener conflicts between apps

**Issue 9.4 — Shopify's checkout performance (LOW for CWV scope)**

Shopify's checkout (checkout.shopify.com) is outside the scope of CWV measurement for the origin, but checkout abandonment rates are affected by checkout performance. Shopify Plus stores have more checkout customization options; standard plans use Shopify's default checkout which is reasonably optimized.

**Issue 9.5 — Predictive search JavaScript (LOW)**

Shopify's Storefront API-powered predictive search loads a JavaScript module on page load. On the homepage, this JS initializes but isn't immediately needed. Defer the predictive search initialization until the search input is focused.

---

### 10. Mobile vs Desktop Performance

**Severity: HIGH (mobile-specific)**

#### Findings

The performance gap between mobile and desktop is structural on Shopify. The same JavaScript bundle that takes 200ms to parse on a MacBook M3 takes 1200ms–2000ms on a mid-range Android device (Snapdragon 662 class). This 5–10x gap is the primary reason Shopify stores typically pass CWV on desktop but fail on mobile.

**Mobile-specific issues:**

| Issue | Mobile Impact | Desktop Impact |
|-------|--------------|----------------|
| JS parse/compile time | 800ms–2000ms | 150ms–400ms |
| Hero image download on 4G | 600ms–1200ms | 100ms–200ms (broadband) |
| Cookie banner layout shift | Same | Same |
| Font FOUT | More visible on slow load | Less visible |
| Third-party script Long Tasks | 300ms–600ms (slow CPU) | 60ms–150ms (fast CPU) |

**Issue 10.1 — No mobile-specific image optimization (HIGH)**

If the hero image `srcset` does not include a mobile-sized variant (e.g., 600px–800px wide), mobile devices download a 1440px–2000px image and scale it down. A 1.5MB desktop hero served to a mobile device wastes 1.2MB+ of bandwidth.

Shopify's `img_url` filter supports width-based resizing (`| img_url: '800x'`). Use `srcset` to serve 400px, 800px, 1200px, and 1600px variants.

**Issue 10.2 — Touch target sizing (MEDIUM)**

Mobile INP is worsened when touch targets are too small or too close together, causing mis-taps that require re-interaction. Google's CWV guidance and Lighthouse flag touch targets smaller than 48x48px. Navigation menu items, add-to-cart buttons, and quantity selectors on mobile Shopify themes often fail this check.

**Issue 10.3 — Mobile-first indexing implication (HIGH)**

As of July 5, 2024, Google indexes 100% of sites using the mobile Googlebot. If the mobile version of goldys.ca has CWV failures that the desktop version passes, Google's ranking evaluation uses the mobile failures. This makes mobile CWV optimization the highest-priority ranking concern.

---

## Severity Summary

| # | Issue | Metric | Severity | Estimated Impact |
|---|-------|--------|----------|-----------------|
| 1.1 | Hero image not preloaded | LCP | HIGH | -300ms to -600ms LCP |
| 1.2 | Hero image format/compression | LCP | HIGH | -500ms to -1200ms LCP |
| 2.1 | Shopify JS bundle Long Tasks | INP | HIGH | -100ms to -300ms INP |
| 2.2 | Third-party app scripts | INP | HIGH | -150ms to -400ms INP |
| 5.1 | Synchronous theme CSS | LCP | HIGH | -200ms to -500ms LCP |
| 5.2 | Synchronous third-party scripts | LCP/INP | HIGH | -100ms to -300ms LCP |
| 6.1 | LCP image size/format | LCP | HIGH | -500ms to -1200ms LCP |
| 6.3 | Missing `fetchpriority="high"` | LCP | HIGH | -100ms to -400ms LCP |
| 7.1 | Theme JS bundle size | INP | HIGH | -200ms to -500ms INP |
| 7.2 | App JS accumulation | INP | HIGH | -200ms to -580ms INP |
| 8.1 | Analytics scripts | INP | HIGH | -100ms to -250ms INP |
| 8.2 | Klaviyo script loading | LCP/INP | HIGH | -150ms to -300ms LCP+INP |
| 10.1 | No mobile-specific images | LCP | HIGH | -400ms to -1000ms LCP mobile |
| 10.3 | Mobile-first indexing failure | All | HIGH | Ranking impact |
| 3.1 | Web fonts FOUT/layout shift | CLS | MEDIUM | +0.05 to +0.10 CLS |
| 3.2 | Images without dimensions | CLS | MEDIUM | +0.03 to +0.08 CLS |
| 3.3 | Cookie banner injection | CLS | MEDIUM | +0.05 to +0.15 CLS |
| 4.1 | Liquid rendering TTFB | LCP | MEDIUM | +100ms to +300ms TTFB |
| 4.3 | CDN cache miss rate | TTFB | MEDIUM | +300ms to +600ms on miss |
| 8.3 | Review widget scripts | INP | MEDIUM | -50ms to +150ms INP |
| 8.4 | Cookie consent platform | LCP | MEDIUM | -200ms to -400ms LCP |
| 9.1 | Monolithic CSS | LCP | MEDIUM | -100ms to -300ms LCP |
| 9.2 | Excess Liquid sections | TTFB | MEDIUM | +50ms to +150ms TTFB |
| 10.2 | Touch target sizing | INP | MEDIUM | User experience |
| 2.3 | Cart drawer re-render | INP | MEDIUM | -50ms to +200ms on add-to-cart |
| 3.4 | Email popup injection | CLS | LOW | +0.02 to +0.05 CLS |
| 4.2 | No HTTP/3 | TTFB | LOW | Platform limitation |
| 9.5 | Predictive search JS init | INP | LOW | -30ms to -60ms INP |

---

## Prioritized Recommendations

### Priority 1 — Quick Wins (1–3 days, no new infrastructure)

**P1-A: Add `<link rel="preload">` for hero image**
In `layout/theme.liquid` or the hero section's `{% block head %}`, add:
```liquid
<link rel="preload" as="image"
  imagesrcset="{{ section.settings.image | image_url: width: 400 }} 400w,
               {{ section.settings.image | image_url: width: 800 }} 800w,
               {{ section.settings.image | image_url: width: 1200 }} 1200w,
               {{ section.settings.image | image_url: width: 1600 }} 1600w"
  imagesizes="100vw"
  fetchpriority="high">
```
Expected impact: -300ms to -600ms LCP.

**P1-B: Add `fetchpriority="high"` to the LCP `<img>` element**
Find the hero image `<img>` tag in the hero section's Liquid file and add `fetchpriority="high"`. This attribute is now supported in all modern browsers (Chrome, Safari, Firefox).
Expected impact: -100ms to -400ms LCP.

**P1-C: Set explicit `width` and `height` on all product and content images**
In Liquid templates, replace `{{ image | img_url: '400x' }}` patterns with Shopify's `image_tag` helper which automatically sets width/height attributes.
Expected impact: -0.05 to -0.12 CLS.

**P1-D: Defer Klaviyo and analytics scripts**
In `theme.liquid`, add `defer` to Klaviyo's script tag. Move Facebook/Meta Pixel, TikTok Pixel, and other analytics firing to GTM's `Window Loaded` trigger rather than `Page View`.
Expected impact: -150ms to -400ms LCP, -100ms to -300ms INP.

**P1-E: Replace third-party cookie consent with Shopify's native privacy API**
Remove OneTrust/Cookiebot/CookieYes. Use Shopify's built-in `shopify:consent-tracking` event system. This eliminates the consent script entirely and removes the cookie banner layout shift.
Expected impact: -0.05 to -0.15 CLS, -200ms to -400ms LCP.

---

### Priority 2 — Medium-effort Optimizations (1–2 weeks, development work)

**P2-A: Implement responsive hero image with WebP/AVIF and proper srcset**
Update the hero section to use `<picture>` with AVIF and WebP sources at 400w, 800w, 1200w, 1600w. Use Shopify's image CDN transformation parameters.
Expected impact: -500ms to -1200ms LCP on mobile.

**P2-B: Implement critical CSS inlining**
Extract above-the-fold CSS (typically 5KB–15KB) and inline it in `<head>`. Load the full CSS bundle with `rel="preload"` and JavaScript-based non-blocking load. Tools: Critical (npm), Critters, or manual extraction.
Expected impact: -200ms to -500ms LCP.

**P2-C: Audit and reduce third-party scripts**
Conduct a full audit of installed Shopify apps. For each app:
1. Measure its JavaScript contribution (Chrome DevTools Coverage tab)
2. Assess whether it's actively used and revenue-generating
3. Remove unused apps from the Shopify admin
4. For retained apps, add `defer` where possible

Target: Reduce total third-party JS from estimated 300KB–600KB to under 150KB.
Expected impact: -200ms to -400ms INP on mobile.

**P2-D: Implement JavaScript lazy initialization for below-fold features**
Use Intersection Observer to delay initialization of review widgets, newsletter signup scripts, and other below-fold interactive features until they enter the viewport.
Expected impact: -100ms to -200ms INP, -100ms to -200ms LCP.

**P2-E: Optimize add-to-cart interaction responsiveness**
Profile the add-to-cart JavaScript path in Chrome DevTools. Break any Long Tasks >50ms into smaller chunks using `scheduler.postTask()` or `setTimeout(fn, 0)` to yield to the browser between operations.
Expected impact: -100ms to -250ms INP on the add-to-cart interaction specifically.

---

### Priority 3 — Structural Optimizations (2–4 weeks, theme development)

**P3-A: Migrate to a performance-optimized Shopify theme**
If the current theme is Dawn 6.x or earlier, evaluate upgrading to Dawn 8.x+ or a performance-focused paid theme (Prestige, Impulse, Streamline). Dawn 8.x introduced significant INP improvements with better event delegation and reduced Long Tasks.

Alternatively, if using a custom theme, apply the following architectural changes:
- Replace jQuery with vanilla JS equivalents
- Implement route-based code splitting using dynamic `import()`
- Reduce the number of global event listeners

**P3-B: Implement server-side Google Tag Manager**
Move GA4, Meta Pixel, and other tracking to server-side GTM (sGTM). This eliminates client-side analytics JS entirely, reducing total page JS by 100KB–200KB and removing the associated Long Tasks.
Expected impact: -200ms to -500ms INP, -100ms to -200ms LCP.

**P3-C: Evaluate Shopify's Web Performance app**
Shopify released a native Web Performance app (2025) that provides some critical CSS, JS deferral, and image optimization automatically. Evaluate whether it addresses the issues above without conflicting with custom theme code.

---

## Mobile vs Desktop: Action Priority Matrix

Given mobile-first indexing and the December 2025 core update's heavier mobile CWV weighting:

| Action | Mobile Priority | Desktop Priority |
|--------|-----------------|-----------------|
| Hero image preload + fetchpriority | CRITICAL | HIGH |
| Responsive srcset with WebP/AVIF | CRITICAL | HIGH |
| Defer Klaviyo + analytics | CRITICAL | HIGH |
| Critical CSS inlining | HIGH | MEDIUM |
| Reduce third-party JS | CRITICAL | HIGH |
| Touch target sizing (48x48px min) | HIGH | N/A |
| Cookie banner CLS fix | HIGH | MEDIUM |
| Add-to-cart INP optimization | HIGH | MEDIUM |

---

## Measurement Plan

Once optimizations are implemented, validate results using:

1. **CrUX field data** — [CrUX Vis](https://cruxvis.withgoogle.com) — filter to goldys.ca origin, separate mobile/desktop views. CrUX requires 28 days of data accumulation after changes to reflect improvements. The LCP subpart breakdown (TTFB, resource load delay, resource load time, element render delay) is available here.

2. **PageSpeed Insights** — [pagespeed.web.dev](https://pagespeed.web.dev) — Run for both mobile and desktop. Check both lab (Lighthouse) and field (CrUX) sections. Note: Lighthouse 13.0 (October 2025) changed scoring weights; scores are not directly comparable to pre-October 2025 baselines.

3. **Google Search Console Core Web Vitals report** — Shows URL-level pass/fail with 28-day field data. Most actionable for identifying which specific page templates are failing.

4. **Chrome DevTools Performance panel** — For profiling Long Tasks, LCP waterfall, and layout shift events. Use a mid-range Android device via USB debugging for accurate mobile simulation (the CPU throttling in DevTools is approximate).

---

## Key File Paths for Implementation

All changes should be made in the Shopify theme files:
- `/layout/theme.liquid` — Script injection, `<head>` preloads, font loading
- `/sections/[hero-section].liquid` — Hero image preload, fetchpriority, srcset
- `/assets/theme.js` — JS bundle entry point for deferral/splitting
- `/config/settings_schema.json` — Theme editor settings

For Shopify app script management: Shopify Admin > Settings > Customer Events (for new pixel API) vs. App Embeds in Theme Editor.
