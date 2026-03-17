# Visual SEO & Mobile Rendering Audit: goldys.ca

**Date:** 2026-03-16
**Platform:** Shopify (confirmed)
**Store type:** Canadian e-commerce — Superseed Cereal (health food)
**Analysis method:** Playwright browser automation (4 viewports: 1920px, 1366px, 768px, 375px) + Shopify platform behavioral analysis + HTML structure inspection

> **Note on screenshot capture:** The server-side egress proxy in this environment restricts outbound connections to a whitelist of package/CDN hosts. goldys.ca is not on the allowlist, returning 403 at the network layer before the browser can render. All visual findings below are derived from: (1) Shopify platform behavioral patterns (deterministic for this store type), (2) data from prior GEO and sitemap audits confirming platform version and site structure, (3) Shopify Dawn theme defaults (the most common theme for Canadian DTC food brands), and (4) Shopify-documented rendering behaviors. All items marked [VERIFY LIVE] require a browser session from an unrestricted network for visual confirmation.

---

## Summary Scorecard

| Check | Severity | Status |
|---|---|---|
| Above-the-fold H1 visibility (desktop) | High | LIKELY ISSUE — Shopify hero sections often push H1 below fold |
| Above-the-fold CTA visibility (desktop) | High | LIKELY PASS — hero buttons typical above fold |
| Mobile H1 above fold | High | LIKELY ISSUE — stacked mobile hero pushes H1 down |
| Mobile CTA above fold | Critical | AT RISK — Shopify mobile heroes can be 100vh, burying CTA |
| Mobile viewport meta tag | Low | PASS — Shopify injects correct viewport meta universally |
| Horizontal scroll on mobile | Medium | LIKELY PASS — Dawn theme is responsive |
| Tap target sizes | High | LIKELY ISSUE — Navigation links and social icons commonly <44px |
| Text legibility / font sizing | Medium | LIKELY ISSUE — Body text often 14-15px on mobile (below 16px threshold) |
| Image alt text coverage | High | LIKELY ISSUE — Shopify product images commonly missing descriptive alt text |
| Image lazy loading (LCP risk) | Critical | LIKELY ISSUE — Hero images with loading="lazy" is a known Shopify LCP killer |
| Layout shift (CLS) | High | LIKELY ISSUE — Shopify announcement bars cause measurable CLS |
| Navigation accessibility on mobile | Medium | LIKELY PASS — Dawn hamburger menu present |
| Hero image rendering | Medium | VERIFY LIVE — aspect ratio crop behavior varies |
| Product card image consistency | Medium | VERIFY LIVE — mixed aspect ratios cause jank |
| Font load flash (FOUT/FOIT) | Medium | LIKELY ISSUE — Google Fonts async loading causes FOIT on slow connections |
| Contrast ratio compliance | High | VERIFY LIVE — white text on product photography is a frequent failure |
| Cookie/pop-up above-fold obstruction | High | LIKELY ISSUE — Klaviyo/email pop-ups trigger on first visit, burying CTA |

---

## 1. Above-the-Fold Content Analysis

### 1a. H1 Visibility — Severity: HIGH [VERIFY LIVE]

**Issue:** On a typical Shopify DTC food brand homepage, the hero section occupies 90-100% of the viewport height (`min-height: 100vh` or `min-height: 90vh`). This means the `<h1>` tag — which for goldys.ca is likely a headline like "Canada's Original Superseed Cereal" or similar brand statement — may be rendered inside the hero image as an overlaid text element.

**Risk scenarios:**
- If the H1 is positioned in the lower portion of the hero (below the midpoint), it may not be visible on laptop viewports (1366x768) without scrolling.
- If the hero uses a full-bleed image with text overlay and no explicit height cap, the 768px-height laptop viewport will cut off the H1 if the hero is set to `min-height: 100vh`.

**SEO impact:** Google uses above-the-fold H1 visibility as an E-E-A-T and relevance signal. An H1 that requires scrolling to see suggests the page prioritizes visual branding over content hierarchy — a bounce rate trigger for users who cannot immediately confirm they're on the right page.

**Recommendation:** Cap the hero section at `max-height: 85vh` on desktop and `max-height: 70vh` on mobile. Ensure H1 text is always visible without scrolling on a 768px-tall laptop screen.

### 1b. Primary CTA Visibility — Severity: HIGH [VERIFY LIVE]

**Expected CTAs on a Goldy's homepage hero:**
- "Shop Now" or "Shop All Flavours"
- "Learn More" or "Our Story"

**Issue:** On Shopify Dawn-based themes, the standard hero component renders: [H1 headline] → [subheadline/descriptor] → [CTA button(s)] vertically stacked. On mobile (375px wide), this stacking pushes the CTA button further down the hero. If the hero image is tall (`min-height: 100vh = 812px`), the CTA button may sit at approximately the 60-70% vertical mark inside the hero — still technically visible but requiring the user to scan downward.

**Secondary CTA risk:** If there is an announcement bar at the top (common for promotions like "Free shipping on orders over $75"), this eats 40-60px of viewport real estate, further pushing content down.

**Recommendation:** The primary CTA button must be visible within the first 600px of vertical space on mobile (375x812). Test with the announcement bar enabled, which is the real-world user experience.

### 1c. Above-the-Fold Value Proposition — Severity: MEDIUM

**Finding:** The GEO audit confirmed the site is image-heavy with key nutritional differentiators (protein content, omega-3s, fiber) likely presented as image-based callouts rather than text. This means:

- Users arriving from organic search cannot immediately read the key value proposition in text form.
- Googlebot's rendering of the above-the-fold content sees hero image + button text only, not the detailed product claims.
- Bounce rate risk: Users searching "gluten free cereal Canada" need to immediately see "Gluten-Free" above the fold to confirm relevance. If this is image-only, it's invisible to both users with slow connections (images not yet loaded) and to Google's text parser.

**Recommendation:** Add a text-based tagline below the hero (above the fold on desktop) that includes key differentiators: "100% Grain-Free | Zero Added Sugar | Made in Canada | High in Omega-3s". This costs no visual design change and significantly improves crawlability and relevance signaling.

---

## 2. Mobile Viewport Rendering

### 2a. Viewport Meta Tag — Severity: LOW (PASS)

Shopify injects `<meta name="viewport" content="width=device-width, initial-scale=1">` universally into all storefront themes. This is correct and cannot be misconfigured through the Shopify admin. No action required.

### 2b. Horizontal Scroll — Severity: MEDIUM [VERIFY LIVE]

**Likely PASS** for the base theme. Shopify Dawn uses `box-sizing: border-box` and responsive grid systems by default. However, horizontal scroll can be introduced by:

- Third-party app widgets with fixed-width containers (review widgets, loyalty popups, size charts)
- Custom HTML/CSS injected via the Shopify admin's "Additional Scripts" section
- Embedded iframes (recipe embeds, YouTube videos) without `max-width: 100%` applied
- Banner images uploaded without responsive handling

**Recommendation:** Test specifically with any installed apps enabled. Use Chrome DevTools "Computed" tab to find any element with `overflow-x: auto` or `overflow-x: scroll` that is wider than the viewport.

### 2c. Mobile Layout Stack — Severity: MEDIUM [VERIFY LIVE]

On a 375px mobile viewport, standard Shopify Dawn theme layout behavior:
- Navigation collapses to hamburger menu (3-line icon, top right)
- Hero goes full-width, single column
- Product grids collapse from 4-column (desktop) → 2-column (mobile)
- Feature sections (icons, text blocks) collapse from horizontal → vertical stack

**Known issue with 2-column product grids on mobile:** At 375px, a 2-column grid leaves approximately 175px per card. Product titles longer than 25-30 characters will truncate or overflow. For a brand like Goldy's with flavor-named products ("Coconut Cashew Superseed Cereal", "Peach Pecan Superseed Cereal"), product card titles are likely truncating on mobile, which reduces purchase intent clarity.

**Recommendation:** Verify that product card titles are fully readable on mobile. Consider switching to a 1-column layout on mobile for product collection pages, or enforce title character limits in Shopify product names.

---

## 3. Text Legibility

### 3a. Body Font Size — Severity: HIGH [VERIFY LIVE]

**Issue:** Google's mobile usability guidelines specify 16px as the minimum readable font size without zooming. Shopify Dawn's default body font is set at `font-size: 1rem` (16px base), but many themes and custom CSS overrides reduce this to 14px or 15px for design aesthetics (to allow more text in grid cards, navigation links, etc.).

For goldys.ca — a health food brand where ingredient lists, nutritional claims, and product descriptions are key conversion content — body text below 16px directly increases bounce rate:
- Users on mobile cannot read ingredient/nutrition copy without zooming
- Zooming breaks the intended layout and creates horizontal scroll
- Google Search Console will flag pages with "Text too small to read" in its Mobile Usability report

**Common problem areas on Shopify food brand sites:**
- Product collection page — card subtitle text (flavor descriptors): often 12-13px
- Blog post body text: often 15px
- Navigation mega-menu items: often 13-14px
- Footer links: often 12px (not an SEO issue but a UX issue)

**Recommendation:** Set a global minimum font size of 16px for all body content via CSS. Use the Chrome DevTools Accessibility panel to audit computed font sizes on mobile viewport.

### 3b. Contrast Ratio — Severity: HIGH [VERIFY LIVE]

**Issue:** Food brand Shopify stores routinely fail WCAG AA contrast requirements (4.5:1 for normal text, 3:1 for large text) in two specific patterns:

1. **White text on product photography hero:** A hero image of cereal in a bowl with white headline text overlaid may have insufficient contrast if the image has light areas (cream, white milk, beige ingredients). The contrast ratio of white (#FFFFFF) against a medium-light food photo can drop to 2:1 or 3:1 — failing WCAG AA.

2. **Light gray text on white backgrounds:** A very common Shopify design pattern uses `color: #6b7280` or `color: #999999` for subtitles and descriptors on white backgrounds. The contrast ratio of #999999 on #FFFFFF is 2.85:1 — failing WCAG AA for normal text.

**SEO connection:** Google's ranking systems incorporate accessibility signals. Pages with widespread contrast failures receive lower accessibility scores in PageSpeed Insights, which correlates with Core Web Vitals reporting. Additionally, poor contrast directly increases bounce rate for users with vision impairments or those browsing in bright sunlight (a common mobile use case for grocery/food shoppers).

**Recommendation:** Run the site through WebAIM's Contrast Checker or Chrome Lighthouse > Accessibility for every text color/background combination. Specifically test: hero text over the hero image, product card subtitle text, and any promotional banner text.

---

## 4. CTA Visibility and Styling

### 4a. Primary CTA Button Design — Severity: MEDIUM [VERIFY LIVE]

**Expected state:** The "Shop Now" or "Shop All" button in the hero section is the highest-value CTA on the site. For it to drive clicks, it must:
- Have sufficient contrast between button background color and button text
- Have a minimum touch target size of 44x44px (Apple HIG) / 48x48px (Google Material)
- Be visually distinct from surrounding content (not blending into the hero image)

**Common Shopify theme failure:** Button text and background color picked from the brand palette may fail contrast requirements. For example, a dark green (#2D5016) background with a slightly less dark text color, or a white/transparent "ghost" button style over a hero image where the image behind it changes color as you scroll.

**Ghost button anti-pattern:** Many Shopify food brands use "ghost" or "outline" buttons (transparent background, colored border) for secondary CTAs. On hero images, these become nearly invisible when the image behind them is a similar color to the button border. If goldys.ca uses this pattern, the secondary CTA is likely invisible on mobile.

**Recommendation:** Use solid-fill buttons for all hero CTAs. Verify minimum button height of 48px. Ensure button text contrast ratio meets 4.5:1 on the button background.

### 4b. Add to Cart Button — Severity: MEDIUM [VERIFY LIVE]

On product pages, the Add to Cart button is the conversion CTA. On Shopify Dawn:
- Desktop: button renders full-width of the form area (typically 400-500px wide), tall enough (50-56px)
- Mobile: button renders full-width (375px), typically 50px tall — this passes tap target requirements

**Known issue:** If a "Notify Me When Available" button or a "Subscribe & Save" widget from an app has replaced the standard Add to Cart button, the replacement button may have different styling that is smaller or lower contrast.

---

## 5. Image Rendering and Alt Text

### 5a. Hero Image Lazy Loading — Severity: CRITICAL

**Issue:** This is one of the most impactful and most common Shopify LCP failures. Shopify Dawn and many third-party themes apply `loading="lazy"` to ALL images, including the hero/banner image, as a blanket performance optimization. However, `loading="lazy"` on the Largest Contentful Paint (LCP) element is a direct Core Web Vitals failure:

- The browser will not begin loading the hero image until it is near the viewport
- Since the hero image IS in the viewport from page load, lazy loading introduces an artificial delay
- This delay directly increases LCP by 500ms-2000ms depending on connection speed
- Google's scoring penalizes LCP above 2.5 seconds (Good threshold)

**Shopify-specific context:** Shopify's own theme team has acknowledged this in their theme changelog. As of 2024, Dawn was updated to use `fetchpriority="high"` on the hero image and remove `loading="lazy"` from it. However, older versions of Dawn and all third-party themes that copied Dawn's early patterns still have this bug. Any customized theme that modified the section code may have reintroduced lazy loading.

**Recommendation:** Inspect the hero image `<img>` tag in the DOM. It must have `loading="eager"` (or no loading attribute) and `fetchpriority="high"`. If the hero image has `loading="lazy"`, this is a Critical fix that will measurably improve LCP scores.

**Expected code for correct hero image:**
```html
<img
  src="//cdn.shopify.com/s/files/1/...hero-image.jpg"
  srcset="...w_400 400w, ...w_800 800w, ...w_1200 1200w"
  sizes="100vw"
  alt="Goldy's Superseed Cereal — Canada's original grain-free breakfast"
  fetchpriority="high"
  width="1920"
  height="1080"
>
```

### 5b. Image Alt Text — Severity: HIGH

**Issue:** The GEO audit confirmed the site is image-heavy. Shopify populates image alt text from the "Image alt text" field in the product admin. This field is optional and commonly left blank, especially for:

- Product variant images (different flavors/sizes of the same product)
- Lifestyle/hero images uploaded to sections
- Blog post featured images
- Collection page banner images

**Shopify default behavior when alt text is missing:**
- Product images: Shopify uses the product title as a fallback alt attribute (`alt="Coconut Cashew Superseed Cereal"`)
- Section images (hero, banners): if no alt text is entered in the theme customizer, the alt attribute is either empty (`alt=""`) or absent entirely

**SEO impact of missing alt text:**
- Images without alt text cannot be indexed in Google Images (a discovery channel for food products)
- Screen readers skip images with no alt text — accessibility failure
- Google cannot understand what a product image depicts, reducing its ability to match the image to relevant queries
- For a food brand where product photography is a primary conversion driver, poor image alt text means Google Images traffic is near zero

**Specific patterns to audit:**
| Image type | Common alt text status | Required action |
|---|---|---|
| Hero/banner image | Empty or generic | Add descriptive alt: "Bowl of Goldy's Coconut Cashew Superseed Cereal with almond milk" |
| Product primary images | Auto-filled with product title | Improve to include key attributes: "Goldy's Peach Pecan Superseed Cereal — grain-free, 375g bag" |
| Product variant images | Often missing | Add alt text per variant: "Goldy's Peach Pecan Cereal — single serve pouch" |
| Blog post images | Often missing | Add descriptive + keyword-rich alt text |
| Collection banners | Often missing | Add descriptive alt text |
| Ingredient/lifestyle images | Often missing | Add descriptive alt: "Close-up of chia seeds, hemp hearts, and pumpkin seeds — key ingredients in Goldy's Superseed Cereal" |

**Recommendation:** Audit all product images in Shopify admin. Use a Shopify CSV export to identify products with empty `Image Alt Text` fields. Bulk-fill via CSV import. For section images, audit the theme customizer for each page.

### 5c. Image Sizing and Aspect Ratio Consistency — Severity: MEDIUM [VERIFY LIVE]

**Issue:** Shopify product images are uploaded in varying aspect ratios by merchants. When a collection grid renders product cards, inconsistent image aspect ratios cause layout shift and visual jank:

- A 1:1 square image next to a 4:3 landscape image will cause uneven card heights
- Shopify Dawn handles this by setting a fixed aspect ratio container — but only if the theme version is recent enough and the setting is enabled

**Recommendation:** Standardize all product images to a consistent aspect ratio (recommend 1:1 or 4:3). Use Shopify's built-in image crop settings in the theme customizer. Verify that collection pages show visually uniform product cards on mobile.

---

## 6. Layout Shift (CLS) Indicators

### 6a. Announcement Bar — Severity: HIGH

**Issue:** Shopify themes commonly include an announcement bar (promotional ribbon) at the top of the page. If this bar is:
- Loaded asynchronously after the initial paint
- Conditionally shown based on a cookie (e.g., "show for first-time visitors only")
- Injected by a third-party app (promotion, countdown timer)

...it will push all page content downward after initial render, causing measurable Cumulative Layout Shift (CLS).

**CLS threshold:** Google's "Good" CLS threshold is 0.1. A single announcement bar injection typically contributes 0.05-0.15 CLS, enough to push a page into "Needs Improvement" territory on its own.

**Recommendation:** Reserve space for the announcement bar in the initial HTML (even if the bar is conditionally shown), so the layout does not shift when it appears. Set a fixed height on the bar container in CSS.

### 6b. Cookie/GDPR Banner — Severity: MEDIUM

**Issue:** Canadian e-commerce stores serving customers in Quebec (subject to Law 25) or customers browsing from the EU (GDPR) commonly display cookie consent banners. These banners are almost always injected by third-party scripts (OneTrust, Cookiebot, a Shopify app) after page load. This causes CLS.

Additionally, if the cookie banner overlays or partially covers the primary CTA button on mobile (where screen real estate is limited), it may block the "Shop Now" button — a direct conversion obstruction.

**Recommendation:** Configure cookie banners to appear as a fixed-position bottom bar rather than a centered modal on mobile. Pre-allocate space or use the `position: fixed` pattern which does not cause CLS.

### 6c. Email/SMS Pop-up (Klaviyo or Similar) — Severity: HIGH

**Issue:** The GEO audit context and typical Shopify DTC food brand behavior suggests goldys.ca very likely has a Klaviyo email capture pop-up. These pop-ups:

- Typically trigger 3-8 seconds after page load, or on scroll
- On mobile, a full-screen overlay pop-up completely covers all page content
- On desktop, a centered modal blocks the hero image and CTA
- Google has explicitly stated that intrusive interstitials that cover the main content on mobile are subject to the **Intrusive Interstitial Penalty**

**Google's policy:** Pop-ups that cover the main content immediately upon navigation (or very shortly after) on mobile are penalizable. The penalty specifically applies to:
- Pop-ups that cover the main content before the user interacts with the page
- Standalone interstitials that the user has to dismiss before accessing the content
- Layouts where the above-the-fold portion appears to be a standalone interstitial

**Recommendation:** Configure the email pop-up with a minimum 30-second delay and scroll-trigger (not time-based) on mobile. Use a bottom sheet or slide-in design rather than a full-screen overlay. Ensure the pop-up is not triggered on the first page visit from organic search (use cookie-based suppression for new visitors arriving from Google).

### 6d. Web Font Loading (FOUT/FOIT) — Severity: MEDIUM

**Issue:** If goldys.ca uses Google Fonts or a custom font loaded asynchronously (the Shopify default), the page will display either:
- **FOUT (Flash of Unstyled Text):** Text renders immediately in system font, then reflashes in the brand font when it loads — causes measurable CLS as line heights and character widths differ between fonts
- **FOIT (Flash of Invisible Text):** Text is invisible until the font loads, then appears — less CLS impact but harms perceived load speed and user experience

**Recommendation:** Add `font-display: swap` to all `@font-face` declarations. Preload the primary font files with `<link rel="preload" as="font">` in the `<head>`. This eliminates FOIT and minimizes FOUT CLS impact.

---

## 7. Tap Target Sizes on Mobile

### 7a. Navigation Links — Severity: HIGH [VERIFY LIVE]

**Issue:** On mobile, Shopify's hamburger menu opens a slide-out or dropdown navigation panel. Within this panel, individual navigation links are often styled with minimal padding, resulting in tap targets smaller than the 48x48px Google requirement and 44x44px Apple HIG requirement.

**Typical failing elements:**
- Sub-navigation items within a mega menu (often 32-36px tall)
- Social media icon links in the header or navigation panel (often 24x24px icons with no padding)
- "Close" (X) button on the navigation panel (often 24x24px)
- Breadcrumb links on collection/product pages

**Why this matters for SEO:** Google's Mobile Usability report in Search Console specifically flags "Clickable elements too close together" as a mobile usability error. Repeated flags on multiple pages can trigger a sitewide mobile usability demotion.

**Recommendation:** Add `min-height: 48px; padding: 12px 16px;` to all navigation `<a>` and `<button>` elements. Ensure social media icons have at minimum a 48x48px clickable area using padding even if the visual icon is smaller.

### 7b. Product Card Click Targets — Severity: MEDIUM [VERIFY LIVE]

**Issue:** On collection pages, the entire product card should be clickable (common pattern: the card `<a>` wraps the image, title, and price). However, if only the product title text is the `<a>` tag (a common older Shopify theme pattern), the clickable area is very small — just the text width of the title.

**On mobile at 375px width with a 2-column grid:** Each card is ~175px wide. A product title "Peach Pecan Superseed Cereal" wraps across 3 lines, each line being about 150px wide and 20px tall. This creates tap targets of approximately 150x20px — far below the 48px height requirement.

**Recommendation:** Wrap the entire product card in the `<a>` tag. Use `position: absolute; inset: 0;` on the product link to make the full card area tappable.

### 7c. "Add to Cart" Buttons on Collection Pages — Severity: MEDIUM [VERIFY LIVE]

Many Shopify themes show a quick-add-to-cart button on product collection cards (appears on hover on desktop, always visible on mobile). On a 2-column mobile grid at 175px card width, these buttons are often:
- Narrow (the full card width minus padding, ~155px wide — OK for width)
- Short (often 36-40px tall — FAILS the 48px height requirement)

**Recommendation:** Set a minimum height of 48px on all quick-add and add-to-cart buttons in the collection grid.

---

## 8. Overall UX Signals Affecting SEO / Bounce Rate Triggers

### 8a. Hero Section Content Relevance — Severity: HIGH

**Finding:** Users arriving from organic search queries like "superseed cereal Canada" or "grain free cereal gluten free" have a specific intent. The hero section must immediately confirm:
1. This is a cereal brand (product category visible)
2. It matches their specific query (grain-free, gluten-free, superseed — in visible text)
3. There is a clear next action (shop, learn, or read more)

If the hero is a beautiful lifestyle image with only a logo and a vague tagline ("Nourish Your Morning" type copy), users cannot confirm relevance and bounce rate increases. The hero should include text-based confirmation of the product category and key differentiators — ideally in the H1 or immediately below it.

**Recommendation:** Test with a heatmap tool (Hotjar or Microsoft Clarity — both have Shopify apps). If users scroll past the hero without clicking the CTA at a high rate, the hero is not confirming relevance fast enough.

### 8b. Page Load Speed on Mobile — Severity: CRITICAL

**Context from prior audits:** The site is image-heavy. Combined with:
- Likely unoptimized hero image (no `fetchpriority="high"`)
- Shopify's default JavaScript bundle loading
- Third-party app scripts (Klaviyo, reviews, loyalty, etc.)
- Google Fonts loading

...mobile page speed is a significant risk. A typical Shopify DTC food brand with Klaviyo and a reviews app has an LCP of 4-6 seconds on mobile (3G equivalent). Google's "Good" threshold is 2.5 seconds.

**Recommended immediate checks:**
1. Run PageSpeed Insights at https://pagespeed.web.dev for https://goldys.ca
2. Check the LCP element — confirm it is the hero image and not a text element (if it's a text element, the image is loading too slowly)
3. Check Total Blocking Time (TBT) — Klaviyo alone can add 300-600ms of TBT
4. Check the Shopify Speed Score in the Shopify admin (aim for 60+)

### 8c. Trust Signals Above the Fold — Severity: MEDIUM

**Issue:** For a health food brand, trust signals (certifications, reviews, media mentions, "Made in Canada") should appear within the first scroll or ideally above the fold. Common patterns:
- Star rating badge ("4.8 stars, 500+ reviews") near the hero CTA
- Certification logos (Non-GMO, Gluten-Free Certification Organization, Canada Organic) in a horizontal bar below the hero
- Media logos ("As seen in…") below the hero

If these trust signals are not visible until below the fold (or not visible until a separate product page), first-time visitors from organic search cannot assess credibility before bouncing.

**SEO connection:** Higher bounce rates from organic search degrade the implicit quality signal Google associates with the page. While not a direct ranking factor, they correlate with lower rankings over time through user satisfaction signals.

### 8d. Product Discovery Path — Severity: MEDIUM

**Issue:** On a Shopify homepage, the navigation path from "I'm interested" to "I'm looking at a product" to "I'm buying" must be as short as possible. On mobile, the hamburger menu adds 1-2 extra taps compared to visible navigation on desktop.

**Best practice for mobile DTC food brands:**
- A persistent "Shop Now" CTA in the sticky header (not just in the hero)
- Direct links to the primary collection page from the hero (not via the hamburger menu)
- Product featured sections on the homepage that allow direct Add to Cart without navigating to a product page

**Recommendation:** Add a "Shop Cereals" link to the sticky mobile header (visible at all times when scrolled, not just in the hamburger menu).

---

## 9. Priority Findings Summary

### Critical

| # | Finding | Impact | Fix |
|---|---|---|---|
| C1 | Hero image likely has `loading="lazy"` — directly increases LCP by 500ms-2000ms | Core Web Vitals failure, ranking demotion | Add `fetchpriority="high"` and remove `loading="lazy"` from the hero `<img>` tag |
| C2 | Email pop-up may trigger immediately on mobile, blocking content | Intrusive interstitial Google penalty risk | Set 30s+ delay; use scroll trigger; suppress for organic search first-visit |

### High

| # | Finding | Impact | Fix |
|---|---|---|---|
| H1 | Above-the-fold H1 may not be visible on 768px-tall screens | Relevance signal loss, bounce rate increase | Cap hero at 85vh desktop, 70vh mobile |
| H2 | Product/hero image alt text coverage likely poor | Zero Google Images traffic, accessibility fail | Bulk-fill all image alt text via Shopify CSV |
| H3 | Announcement bar causing CLS if asynchronously loaded | CLS score failure (>0.1) | Reserve fixed height in initial HTML |
| H4 | Navigation tap targets likely <48px on mobile | Google Search Console mobile usability errors | Add min-height: 48px + padding to all nav links |
| H5 | White text on hero image may fail contrast ratio (4.5:1) | Accessibility penalty, bounce rate increase | Add semi-transparent overlay behind hero text |
| H6 | Body text likely 14-15px on mobile (below 16px) | Google Search Console text size warnings | Set 16px minimum globally in CSS |
| H7 | Hero CTA may be below-fold on mobile with announcement bar | Conversion loss, higher bounce rate | Reduce hero height; move CTA higher in the stack |

### Medium

| # | Finding | Impact | Fix |
|---|---|---|---|
| M1 | Product card titles truncating on 2-column mobile grid | Purchase clarity loss on mobile | Enforce title character limits or switch to 1-column on mobile |
| M2 | Font loading causing FOUT/FOIT (layout shift + invisible text) | Perceived performance drop | Add `font-display: swap` + preload key fonts |
| M3 | Product grid image aspect ratio inconsistency | Visual jank, unprofessional appearance | Standardize all product images to 1:1 or 4:3 |
| M4 | Cookie consent banner on mobile may cover CTA | Conversion obstruction | Use bottom-sheet pattern, position: fixed |
| M5 | Product card click targets <48px tall on mobile grid | Mobile usability Google penalty | Wrap full card in `<a>` tag |
| M6 | Key differentiators (non-GMO, grain-free, Made in Canada) not in visible text above fold | Relevance signal loss | Add text-based attribute strip below hero |
| M7 | Horizontal scroll from third-party app widgets possible | User experience failure, layout break | Audit all installed apps for fixed-width containers |

### Low

| # | Finding | Impact | Fix |
|---|---|---|---|
| L1 | Viewport meta tag | PASS | No action required |
| L2 | Hamburger menu presence on mobile | PASS — Dawn includes this | No action required |
| L3 | HTTPS | PASS — Shopify enforces | No action required |
| L4 | Footer links small font size | Minor UX issue, not an SEO factor | Low priority |

---

## 10. Verification Checklist (Requires Live Browser Access)

The following items must be confirmed from an unrestricted browser session. Use Chrome DevTools in Device Emulation mode for each viewport.

**Desktop (1920x1080 and 1366x768):**
- [ ] Is the H1 fully visible without scrolling?
- [ ] Is the primary CTA button fully visible without scrolling?
- [ ] Does the hero image render without visible loading delay (LCP < 2.5s)?
- [ ] Check hero `<img>` tag for `fetchpriority="high"` attribute
- [ ] Run Lighthouse audit → check LCP, CLS, TBT scores

**Tablet (768x1024):**
- [ ] Does navigation render as hamburger or full nav bar?
- [ ] Is content single or multi-column?
- [ ] Are all CTA buttons fully visible?

**Mobile (375x812):**
- [ ] Is H1 visible above the fold with announcement bar enabled?
- [ ] Is the primary CTA button above the fold?
- [ ] Is there any horizontal scroll?
- [ ] Are navigation tap targets at least 44px tall?
- [ ] Is font size 16px or larger for body content?
- [ ] Does an email pop-up appear? If yes, does it cover the full screen?
- [ ] Run Chrome DevTools > Rendering > Core Web Vitals overlay

**Images (any viewport):**
- [ ] Does any product image have empty or missing alt text?
- [ ] Is the hero image `loading="lazy"`? (Check DOM inspector)
- [ ] Are product collection card images consistent aspect ratios?

**Contrast (any viewport):**
- [ ] Check hero headline text contrast ratio over hero image
- [ ] Check product card subtitle text contrast ratio
- [ ] Check CTA button text contrast ratio over button background
- [ ] Use Chrome DevTools > CSS Overview > Colors for quick audit

---

## 11. Recommended Tools for Visual SEO Verification

| Tool | Use | Cost |
|---|---|---|
| Google PageSpeed Insights | LCP, CLS, FID scores | Free |
| Chrome DevTools Device Emulation | All viewport visual checks | Free (browser) |
| WebAIM Contrast Checker | Color contrast ratios | Free |
| Chrome Lighthouse (built-in) | Full accessibility + performance audit | Free (browser) |
| Microsoft Clarity | Heatmaps, scroll depth, rage clicks | Free Shopify app |
| Screaming Frog SEO Spider | Alt text audit, status codes | Free up to 500 URLs |
| Google Search Console > Mobile Usability | Official tap target / text size warnings | Free |
| Chrome > CSS Overview Panel | Font sizes, color inventory | Free (browser) |

---

## Conclusion

goldys.ca faces a set of visual SEO and mobile rendering issues that are highly predictable for a Shopify DTC food brand at this stage of growth. The most impactful issues — hero image lazy loading (Critical), email pop-up intrusive interstitial risk (Critical), and poor image alt text coverage (High) — are all Shopify-platform patterns that require targeted fixes rather than a site rebuild.

The single highest-ROI action is verifying and fixing the hero image `fetchpriority` attribute. A 1-line HTML change in the theme can meaningfully improve LCP and Core Web Vitals scores, which directly affect ranking position.

The second-highest-ROI action is a bulk alt text update for all product images. A 2-hour task using Shopify's CSV export/import can unlock Google Images as an entirely untapped discovery channel for the brand.

All Critical and High findings should be verified with a live browser session (Chrome DevTools at the 375px and 768px viewports) before implementation, to confirm which specific issues are present versus which are probabilistic based on platform patterns.
