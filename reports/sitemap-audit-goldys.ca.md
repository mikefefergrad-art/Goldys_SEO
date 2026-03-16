# XML Sitemap Audit: goldys.ca

**Date:** 2026-03-16
**Platform:** Shopify (confirmed)
**Store type:** Canadian e-commerce, health food / superseed cereal

---

## Fetch Status

Direct HTTP access to goldys.ca is blocked by the sandbox egress proxy (403 host_not_allowed). All findings below are based on:
- Shopify's documented and deterministic sitemap generation behavior (all Shopify stores produce sitemaps in identical structural patterns)
- The GEO audit previously run against goldys.ca (confirmed live Shopify store, robots.txt behavior, blog section at /blogs/news)
- Shopify platform documentation and known version-specific issues as of March 2026

Items that require live verification are explicitly marked **[VERIFY LIVE]**.

---

## Summary Scorecard

| Check | Severity | Status |
|-------|----------|--------|
| Sitemap existence at /sitemap.xml | Low | PASS — Shopify auto-generates (confirmed pattern) |
| Sitemap index structure | Low | PASS — Shopify generates sitemapindex by default |
| XML format validity | Low | PASS — Shopify output is always well-formed |
| URL count per file (<50,000) | Low | PASS — small store, well under limit |
| HTTPS-only URLs | Low | PASS — Shopify enforces HTTPS |
| Deprecated tags (priority, changefreq) | Info | PRESENT — Shopify injects both into all sitemaps |
| Identical lastmod dates | Medium | LIKELY ISSUE — Shopify uses product updated_at, not publish date |
| Sitemap referenced in robots.txt | Low | PASS — Shopify auto-injects Sitemap: directive |
| Non-canonical URLs in sitemap | High | LIKELY ISSUE — variant URLs, tagged collections [VERIFY LIVE] |
| Noindexed URLs in sitemap | High | LIKELY ISSUE — Shopify known bug with /password page [VERIFY LIVE] |
| Redirected URLs in sitemap | Medium | LIKELY ISSUE — if old URLs were ever changed [VERIFY LIVE] |
| Blog posts covered | Medium | LIKELY PARTIAL — /blogs/news/ posts included, but recipe-heavy |
| Product pages covered | Low | PASS — all published products auto-included |
| Collection pages covered | Low | PASS — all published collections auto-included |
| Static pages covered | Low | PASS — all published pages auto-included |
| AI crawler access affecting sitemap crawl | Critical | FAIL — robots.txt blocks Googlebot-extended, AI bots |

---

## 1. Sitemap Existence and Structure

### 1a. /sitemap.xml

**Severity: Low (PASS)**

Shopify auto-generates a sitemap index at `/sitemap.xml` for all stores. There is no configuration required and it cannot be disabled through the admin. The file is always a sitemapindex document (not a flat urlset), even for small stores.

Expected structure Shopify generates:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://goldys.ca/sitemap_products_1.xml</loc>
    <lastmod>2026-03-16T00:00:00-05:00</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://goldys.ca/sitemap_collections_1.xml</loc>
    <lastmod>2026-03-16T00:00:00-05:00</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://goldys.ca/sitemap_pages_1.xml</loc>
    <lastmod>2026-03-16T00:00:00-05:00</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://goldys.ca/sitemap_blogs_1.xml</loc>
    <lastmod>2026-03-16T00:00:00-05:00</lastmod>
  </sitemap>
</sitemapindex>
```

### 1b. /sitemap_index.xml

**Severity: Low (N/A)**

Shopify does not generate a file at `/sitemap_index.xml`. The canonical index location is `/sitemap.xml`. Any request to `/sitemap_index.xml` will return a 404. This is expected and not a defect.

---

## 2. XML Format Validity

**Severity: Low (PASS)**

Shopify's sitemap generation is handled server-side by Shopify's platform code (not theme code). Output is always:
- Valid UTF-8 encoded XML
- Well-formed with correct namespace declarations (`http://www.sitemaps.org/schemas/sitemap/0.9`)
- Properly escaped special characters in URLs
- Correctly structured sitemapindex and urlset documents

No format defects are expected.

---

## 3. Deprecated Tags: priority and changefreq

**Severity: Info**

**Issue:** Shopify injects both `<priority>` and `<changefreq>` tags into every URL entry in every sub-sitemap. Example of what Shopify generates:

```xml
<url>
  <loc>https://goldys.ca/products/superseed-cereal-original</loc>
  <lastmod>2026-03-10T12:00:00-05:00</lastmod>
  <changefreq>daily</changefreq>
  <priority>0.8</priority>
</url>
```

**Why this matters:** Google has explicitly stated it ignores both `<priority>` and `<changefreq>`. These tags have been ignored since at least 2022. Bing also ignores them. They add byte bloat to every URL entry without providing any ranking or crawl benefit.

**Fix:** Shopify does not allow merchants to remove these tags via the admin. The only fix is a custom sitemap implementation via a Liquid template (advanced). For a store of goldys.ca's likely size, this is low priority — the bloat is negligible. Log it and move on.

**Action required:** None unless you move to a headless or custom sitemap approach.

---

## 4. URL Coverage

### 4a. Products

**Severity: Low (PASS)**

All published products are auto-included in `/sitemap_products_1.xml`. Shopify paginates at 5,000 products per file, generating `sitemap_products_2.xml` etc. as needed. For a specialty food brand like goldys.ca, the product catalog is almost certainly under 100 SKUs, meaning a single file.

**Known Shopify coverage gap:** Product variant URLs (e.g., `/products/superseed-cereal?variant=12345678`) are NOT included in the sitemap. Only the canonical product URL is included. This is correct behavior.

### 4b. Collections

**Severity: Low (PASS)**

All published collections are included in `/sitemap_collections_1.xml`.

**Known Shopify coverage gap — VERIFY LIVE [Medium]:** Shopify includes tagged collection URLs (e.g., `/collections/all/gluten-free`) in some configurations. These are filtered/tag pages, not canonical collections, and should NOT be in the sitemap. If any apps or theme customizations have created tagged collection URLs, check whether they appear.

### 4c. Blog Posts

**Severity: Medium (PARTIAL)**

The GEO audit confirmed a blog section at `/blogs/news`. Shopify auto-includes all published blog posts in `/sitemap_blogs_1.xml`.

**Coverage gap to verify [VERIFY LIVE]:**
- Are all blog posts published (not draft)? Draft posts are excluded from the sitemap correctly, but sometimes posts are accidentally left in draft status.
- The GEO audit noted the blog appears to be recipe-focused rather than informational. Recipe posts may have thin content and be candidates for noindex, in which case they should also be removed from the sitemap (see Section 6).

### 4d. Static Pages

**Severity: Low (PASS)**

All published pages (About, Contact, FAQ, etc.) are included in `/sitemap_pages_1.xml`.

**Known Shopify bug — VERIFY LIVE [High]:** Shopify has a documented historical bug where the `/password` page (the store password/coming soon page) appears in sitemaps when it should not. If the store was ever password-protected during development, confirm the password page is not present.

---

## 5. lastmod Dates

**Severity: Medium**

**Issue:** Shopify uses the `updated_at` timestamp from its database for `<lastmod>`. This creates two problems:

**Problem A — App-triggered mass updates:** Many Shopify apps (inventory sync, pricing apps, review apps, translation apps) touch product records as part of their operation, causing `updated_at` to be refreshed even when no meaningful content change occurred. This means `<lastmod>` for most products will reflect the last time an app ran, not the last time the page content changed. Google uses lastmod as a crawl priority signal; inaccurate lastmod reduces its value.

**Problem B — All products showing today's date [VERIFY LIVE]:** If any bulk operation (price import, inventory sync, tag update) was recently run across all products, the entire product sitemap will show the same `lastmod` date — a red flag to Google indicating the dates are not trustworthy. Check whether all `<lastmod>` values in `/sitemap_products_1.xml` are identical.

**Fix:** This is a platform limitation. You cannot override lastmod in Shopify's native sitemap. The workaround is a custom sitemap Liquid template that queries Metafields for a manually set "content last updated" date. Medium effort, medium payoff.

---

## 6. Non-Canonical and Noindexed URLs

**Severity: High**

### 6a. Non-canonical URLs

**[VERIFY LIVE]** Shopify can include non-canonical URLs in sitemaps in specific scenarios:

- **Duplicate collection pages:** If the store has both `/collections/all` and a custom collection covering the same products, both may be sitemapped. Only the intended canonical should be present.
- **Localization URLs:** If Shopify Markets is enabled with country-specific URLs (e.g., `/en-ca/products/...`) or subdomain/subfolder international routing, both the root and localized URLs may appear. The localized versions need hreflang handling; being in the sitemap without hreflang is a medium issue.
- **Legacy redirect sources:** If any product or page URLs were changed in the Shopify admin (handle change), the old URL now 301-redirects to the new URL. If Shopify's cache has not been invalidated, old URLs occasionally persist in the sitemap temporarily. [VERIFY LIVE: check all sitemap URLs return 200, not 301/302.]

### 6b. Noindexed URLs

**[VERIFY LIVE]** Shopify does not automatically exclude noindexed pages from the sitemap. Any page with a noindex meta tag or X-Robots-Tag header that also remains published will appear in the sitemap. This is a direct contradiction — the sitemap tells Google "please index this" while the noindex tag tells Google "do not index this." Google will respect noindex but the conflicting signal wastes crawl budget and causes Search Console warnings.

Check for:
- Pages with noindex added via theme settings or an SEO app that are still published
- Any "coming soon" or placeholder collection pages
- Any policy pages (privacy, terms) that may have been noindexed to avoid duplicate content flags

---

## 7. Redirected URLs in Sitemap

**Severity: Medium [VERIFY LIVE]**

If any of the following events occurred, redirected URLs may exist in the sitemap:
- Product handle (slug) was changed in the Shopify admin
- Collection handle was changed
- A page was renamed
- An app migration moved URLs to new paths

Shopify creates automatic 301 redirects when handles change, but the old URL can remain in the sitemap until the sitemap cache regenerates (typically within 24-48 hours, but occasionally longer).

**How to verify:** Crawl all URLs from the sitemaps with a tool like Screaming Frog and filter for 3xx responses.

---

## 8. Shopify-Specific Sitemap Issues

### 8a. robots.txt Sitemap Declaration

**Severity: Low (PASS)**

Shopify automatically adds `Sitemap: https://goldys.ca/sitemap.xml` to the robots.txt file. This is handled at the platform level and requires no action.

### 8b. AI Crawler Access (Critical — Affects Sitemap Crawl Utility)

**Severity: Critical**

The GEO audit confirmed that Shopify's default robots.txt blocks AI crawlers. This affects sitemap utility because:
- If Googlebot (standard web crawler) is allowed but AI-extended crawlers are blocked, Google's AI features (AI Overviews, Search Generative Experience) cannot crawl pages to feature them
- More importantly for sitemap health: if the store's robots.txt disallows any significant crawler, those crawlers cannot even fetch the sitemap to discover what to crawl

The sitemap itself may be technically correct, but its reach is artificially reduced by the robots.txt policy. Refer to the GEO audit report for the specific robots.txt fix required.

### 8c. Shopify Markets / International URLs

**Severity: Medium [VERIFY LIVE]**

If goldys.ca uses Shopify Markets for international routing (e.g., serving US customers at goldys.ca/en-us/ or on a separate domain), the sitemap configuration needs review:
- Each market's URLs should appear in a sitemap served from that market's domain/subfolder
- hreflang annotations must link the variants together
- Without hreflang, having the same product at two URLs in two sitemaps creates duplicate content risk

Given that this is a Canadian brand (goldys.ca .ca domain), Markets may be configured. [VERIFY LIVE: check whether /en-ca/ or /en/ subfolders exist.]

### 8d. Image Sitemap

**Severity: Low (Info)**

Shopify does NOT generate an image sitemap or include `<image:image>` extensions in product sitemaps. For a food brand where product photography drives conversions and Google Images can be a discovery channel, this is a missed opportunity.

Google can discover product images through standard crawling of product pages, so this is not a blocking issue. But an image sitemap would improve image indexing speed.

**Fix:** A custom image sitemap can be generated via a Liquid template or a third-party Shopify sitemap app.

### 8e. Video Sitemap

**Severity: Low (Info)**

No Shopify store generates a video sitemap by default. If goldys.ca embeds any product demo videos or recipe videos (common for food brands), these are not discoverable via sitemap. Low priority unless video SEO is a specific goal.

---

## 9. URL Count Estimate

**Severity: Low (PASS)**

For a specialty Canadian health food brand selling superseed cereals, the URL count is estimated as:

| Content type | Estimated count |
|---|---|
| Products | 10-30 |
| Collections | 5-15 |
| Pages (static) | 5-10 |
| Blog posts | 10-50 |
| **Total** | **30-105** |

This is far below the 50,000 URL per-file limit. No sitemap index splitting is required beyond Shopify's default segmentation by content type.

[VERIFY LIVE: confirm actual counts from sitemap_products_1.xml, sitemap_collections_1.xml, sitemap_pages_1.xml, sitemap_blogs_1.xml]

---

## 10. Priority Recommendations

### Critical

1. **Fix robots.txt to unblock AI crawlers** (see GEO audit) — the sitemap is only as useful as the crawlers that can access it. This does not change the sitemap XML but directly impacts what Google can do with sitemap-discovered URLs.

### High

2. **Audit for noindexed pages appearing in sitemap** — pull the sitemap, render each URL with a headless browser or a tool like Screaming Frog, and check the meta robots tag. Remove any noindexed pages from the Shopify published state or suppress them with an SEO app that also removes them from the sitemap.

3. **Check for redirect URLs in sitemap** — run a status code check on all sitemap URLs. Any 3xx must be updated to the final destination URL, which means changing the handle back or updating Shopify's URL structure.

### Medium

4. **Audit tagged collection URLs** — confirm that filter/tag URLs like `/collections/all/gluten-free` are not present in the collections sitemap. If they are, these are non-canonical and should be excluded.

5. **Investigate lastmod date accuracy** — if all products share the same lastmod, document this for Google Search Console. Consider whether a custom sitemap template is worth the development cost to implement accurate content-change dates.

6. **Verify Shopify Markets configuration** — if multiple market subfolders exist, ensure each has a properly configured sitemap and that hreflang is in place.

### Low / Info

7. **Remove priority and changefreq** (optional) — only worth pursuing as part of a custom sitemap implementation for other reasons. Not worth standalone development effort.

8. **Consider an image sitemap extension** — particularly valuable for product photography on a food brand where visual search (Google Images, Google Lens) can drive discovery. A third-party Shopify sitemap app can add this without custom development.

---

## Verification Checklist

The following items require live access to confirm. Use Screaming Frog, Google Search Console, or a direct browser/curl session from an unrestricted network:

- [ ] Fetch https://goldys.ca/sitemap.xml — confirm sitemapindex structure
- [ ] Fetch each sub-sitemap — confirm URL counts per content type
- [ ] Check all lastmod dates — are any identical across all products?
- [ ] Confirm /password page is absent from sitemap_pages_1.xml
- [ ] Run status code check on all sitemap URLs — flag any 3xx or 4xx
- [ ] Check meta robots on all sitemapped pages — flag any noindex
- [ ] Confirm whether /en-ca/ or other Markets subfolders exist
- [ ] Check Google Search Console > Sitemaps report for submitted sitemaps and indexing errors
- [ ] Check robots.txt for Sitemap: directive and AI bot rules

---

## Conclusion

goldys.ca's sitemap infrastructure is structurally sound by virtue of Shopify's platform handling — the XML will be well-formed, HTTPS-only, and properly referenced in robots.txt. The critical issues are not in the sitemap file itself but in the surrounding ecosystem: AI crawlers being blocked reduces the effective reach of correctly sitemapped URLs, and the potential presence of noindexed or redirected URLs in the sitemap creates contradictory signals for Google.

The most actionable immediate step is fixing the robots.txt AI crawler policy (covered in the GEO audit), followed by a live verification sweep of all sitemap URLs for status codes and noindex conflicts. The deprecated priority/changefreq tags are cosmetic and can be deferred.
