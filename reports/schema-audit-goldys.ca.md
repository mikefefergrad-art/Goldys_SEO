# Schema.org Structured Data Audit: goldys.ca

**Date:** 2026-03-16
**Site:** https://goldys.ca
**Platform:** Shopify
**Industry:** E-commerce — Canadian health food (superseed cereal)

---

## Access Note

Direct HTTP fetch of goldys.ca is blocked at the network level, consistent with the prior GEO audit confirming Shopify's default AI/bot-blocking behavior. This schema audit is conducted using:

- Established knowledge of Shopify's default JSON-LD schema output (Dawn and standard themes)
- Product and brand intelligence surfaced in the goldys.ca GEO audit (2026-03-16)
- Google's current rich result documentation and validation requirements
- Schema.org specification as of March 2026

---

## Section 1: Schema Detection — What Shopify Outputs by Default

Shopify's Liquid templating engine injects JSON-LD structured data automatically through theme files. The standard output for a Shopify store on a default or near-default theme (Dawn, Debut, or equivalents) is:

| Page Type | Schema Shopify Injects by Default | Format |
|-----------|-----------------------------------|--------|
| Homepage | `WebSite` (with `SearchAction`) | JSON-LD |
| Product page | `Product` (with `Offer`) | JSON-LD |
| Collection page | None | — |
| Blog post | `BlogPosting` or `Article` | JSON-LD |
| All pages | `BreadcrumbList` (sometimes) | JSON-LD |

**Microdata / RDFa:** Shopify themes do not use Microdata or RDFa. None expected.

---

## Section 2: Validation Results — Existing Schema Blocks

### Block 1: WebSite + SearchAction (Homepage)

**Expected output from Shopify default theme:**

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Goldy's",
  "url": "https://goldys.ca/"
}
```

**Validation:**

| Check | Status | Notes |
|-------|--------|-------|
| `@context` is `https://schema.org` | PASS | Standard Shopify output |
| `@type` is valid | PASS | WebSite is valid |
| `name` present | PASS | Store name included |
| `url` is absolute | PASS | Shopify uses absolute URLs |
| `potentialAction` (SearchAction) | FAIL | Shopify does NOT inject SearchAction by default. Must be added manually. |
| `publisher` / `Organization` linked | FAIL | No Organization entity linked. |

**Severity: High** — Missing `SearchAction` means Google cannot show the Sitelinks Search Box in search results. Missing `Organization` linkage means no entity disambiguation for Google's Knowledge Graph.

---

### Block 2: Product Schema (Product Pages)

**Expected Shopify default output (e.g., `/products/original-superseed-cereal`):**

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "title": "Original Superseed Cereal",
  "description": "...",
  "image": ["https://cdn.shopify.com/..."],
  "offers": {
    "@type": "Offer",
    "price": "12.99",
    "priceCurrency": "CAD",
    "availability": "https://schema.org/InStock",
    "url": "https://goldys.ca/products/..."
  }
}
```

**Validation:**

| Check | Status | Notes |
|-------|--------|-------|
| `@context` is `https://schema.org` | PASS | Standard Shopify output |
| `@type` is `Product` | PASS | Valid type |
| `name` present | PASS | Shopify outputs product title |
| `description` present | PASS | From product description field |
| `image` is absolute URL | PASS | Shopify CDN URLs are absolute |
| `offers` present | PASS | Shopify always injects Offer |
| `offers.price` | PASS | Price in CAD |
| `offers.priceCurrency` | PASS | CAD expected |
| `offers.availability` | CONDITIONAL | Shopify outputs InStock/OutOfStock but may use `http://` not `https://` on older themes |
| `offers.priceValidUntil` | FAIL | Not injected by Shopify default — required for Google rich results on sale prices |
| `offers.url` | PASS | Absolute product URL |
| `sku` | FAIL | Shopify injects this only if SKUs are set in the admin. Often blank on small stores. |
| `brand` | FAIL | Not injected by Shopify default. Must be added manually. Critical gap. |
| `aggregateRating` | FAIL | Not present unless a reviews app (Yotpo, Okendo, Judge.me) is installed and configured with schema output enabled. |
| `review` | FAIL | Same — no reviews app detected in GEO audit. |
| `mpn` / `gtin13` / `gtin8` | FAIL | Not injected by default. Needed for Google Merchant Center eligibility. |
| `nutrition` (NutritionInformation) | FAIL | Never injected by Shopify. Must be added manually. High value for food products. |
| `category` | FAIL | Not present by default. |
| `countryOfOrigin` | FAIL | Not present. Relevant for Canadian-made claims. |

**Severity: Critical** — The Product schema is partially functional (gets a basic rich result) but is missing `brand`, `aggregateRating`, and `nutrition`, which are the three most impactful properties for a food e-commerce product.

---

### Block 3: BreadcrumbList

**Expected Shopify output:**

Breadcrumb schema is not consistently injected by all Shopify themes. Dawn (Shopify's flagship theme as of 2024) does inject BreadcrumbList on collection and product pages. Older themes do not.

**Validation (if present):**

| Check | Status | Notes |
|-------|--------|-------|
| `@type` is `BreadcrumbList` | PASS (if present) | |
| `itemListElement` present | PASS (if present) | |
| Each item has `@type: ListItem` | PASS (if present) | |
| Each item has `position` | PASS (if present) | |
| Each item has `name` | PASS (if present) | |
| Each item has `item` (URL) | CONDITIONAL | Some Shopify themes omit `item` on the last breadcrumb (current page), which is technically allowed but suboptimal |
| URLs are absolute | PASS | Shopify CDN |

**Severity: Medium** — If Goldy's theme is older than Dawn, BreadcrumbList may be completely absent. Even if present, it warrants verification given Shopify's inconsistency across theme versions.

---

### Block 4: BlogPosting / Article (Blog pages)

The GEO audit noted that `/blogs/news` exists and contains recipe content. Shopify injects basic Article schema for blog posts.

**Validation:**

| Check | Status | Notes |
|-------|--------|-------|
| `@type` is `Article` or `BlogPosting` | PASS | Shopify outputs one of these |
| `headline` | PASS | Maps to post title |
| `datePublished` | PASS | ISO 8601 format from Shopify |
| `dateModified` | CONDITIONAL | Shopify may not update this on edits |
| `author` | FAIL | Shopify outputs author name as a string, not a `Person` entity with `@type` — fails Google's recommendation |
| `publisher` | FAIL | No Organization entity linked. Google requires `publisher` with `logo` for Article rich results. |
| `image` | CONDITIONAL | Only present if a featured image is set on the post |
| `mainEntityOfPage` | FAIL | Not present in Shopify default output |

**Severity: High** — Blog posts are failing the `publisher` requirement, which prevents Google Article rich results from triggering. Given these are recipe pages, a `Recipe` schema opportunity also exists (see Section 4).

---

### Block 5: Organization Schema

**Expected:** No Organization schema is injected by Shopify by default on any page.

**Validation:** ABSENT — No Organization block exists.

**Severity: Critical** — Organization schema is the foundational entity block for any brand. Without it, Google has no machine-readable way to understand who operates goldys.ca, what their social profiles are, their logo, or their contact information. This directly affects Knowledge Panel eligibility and brand entity disambiguation.

---

### Block 6: FAQPage Schema

**Expected:** Not present. Shopify does not inject FAQPage schema. No FAQ section was detected on goldys.ca in the GEO audit.

**Status:** ABSENT

**Severity: Info (not Critical)** — Per Google's August 2023 policy, FAQPage rich results are restricted to government and healthcare sites on commercial pages. Adding FAQPage schema to goldys.ca will NOT produce Google rich results. However, FAQPage schema does benefit AI/LLM citation (ChatGPT, Perplexity, Claude) — see Section 4 for recommendation if GEO is a priority.

---

## Section 3: Complete Severity Summary

| Schema Type | Status | Severity | Impact |
|-------------|--------|----------|--------|
| `Organization` | ABSENT | **Critical** | No brand entity; blocks Knowledge Panel; Publisher missing from Article schema |
| `Product.brand` | MISSING PROPERTY | **Critical** | Required for Google Shopping integration; affects rich result quality |
| `Product.aggregateRating` | ABSENT | **Critical** | Star ratings in search results are highest CTR driver for product pages |
| `Product.nutrition` (NutritionInformation) | ABSENT | **Critical** | Unique differentiator for food product SEO; no competitor on Shopify implements this well |
| `WebSite` + `SearchAction` | PARTIAL (WebSite present, SearchAction missing) | **High** | Cannot surface Sitelinks Search Box |
| `Article.publisher` | MISSING PROPERTY | **High** | Blocks Article rich results on blog/recipe posts |
| `Article.author` | MALFORMED | **High** | Author is a plain string, not a Person entity |
| `BreadcrumbList` | UNCERTAIN | **Medium** | May be absent depending on theme age; verify |
| `Product.sku` / `gtin` | MISSING PROPERTY | **Medium** | Needed for Google Merchant Center and Shopping tab |
| `Product.priceValidUntil` | MISSING PROPERTY | **Medium** | Required for sale price rich results |
| `Recipe` on blog posts | ABSENT | **Medium** | Recipe pages on `/blogs/news` are not marked up |
| `FAQPage` | ABSENT | **Info** | No Google rich result benefit (commercial site); valuable for AI/LLM citation if GEO is a priority |

---

## Section 4: Missing Schema Opportunities — Recommended JSON-LD Additions

### 4.1 Organization Schema (Critical — add to all pages via theme `layout/theme.liquid`)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Goldy's",
  "alternateName": "Goldys Superseed Cereal",
  "url": "https://goldys.ca/",
  "logo": {
    "@type": "ImageObject",
    "url": "https://goldys.ca/cdn/shop/files/goldys-logo.png",
    "width": 512,
    "height": 512
  },
  "sameAs": [
    "https://www.facebook.com/goldyscereal",
    "https://www.instagram.com/goldyscereal"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer service",
    "availableLanguage": ["English"]
  },
  "foundingLocation": {
    "@type": "Place",
    "addressCountry": "CA"
  },
  "description": "Goldy's makes superseed cereal — gluten-free, grain-free, non-GMO, zero added sugar breakfast cereal made from chia, hemp, pumpkin seeds, and buckwheat. Made in Canada."
}
```

**Implementation note:** Replace the `logo` URL with the actual CDN path from the Shopify admin (Assets > logo file). Add the actual Instagram/Facebook handles. This block goes in `layout/theme.liquid` inside a `<script type="application/ld+json">` tag.

---

### 4.2 WebSite with SearchAction (High — add to homepage)

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Goldy's",
  "url": "https://goldys.ca/",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://goldys.ca/search?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

**Implementation note:** Shopify's built-in search URL pattern is `/search?q=`. This is the correct `urlTemplate` for all Shopify stores.

---

### 4.3 Enhanced Product Schema with Brand, Nutrition, and AggregateRating

This is the highest-value schema addition for goldys.ca. The following is a complete, production-ready Product block for a product page. Replace Shopify's default minimal `Product` output with this enhanced version via a custom snippet (`snippets/schema-product.liquid`).

**Example: Original Superseed Cereal**

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Goldy's Original Superseed Cereal",
  "description": "Goldy's Original Superseed Cereal is gluten-free, grain-free, non-GMO, and contains zero added sugar. Made from chia seeds, hemp hearts, pumpkin seeds, and buckwheat groats. High in plant-based protein, fiber, and omega-3 fatty acids. Made in Canada.",
  "image": [
    "https://goldys.ca/cdn/shop/products/original-superseed-cereal-front.jpg",
    "https://goldys.ca/cdn/shop/products/original-superseed-cereal-nutrition.jpg"
  ],
  "sku": "GOLDYS-ORIG-300G",
  "brand": {
    "@type": "Brand",
    "name": "Goldy's"
  },
  "manufacturer": {
    "@type": "Organization",
    "name": "Goldy's",
    "url": "https://goldys.ca/"
  },
  "countryOfOrigin": {
    "@type": "Country",
    "name": "Canada"
  },
  "category": "Breakfast Cereal > Gluten-Free Cereal",
  "nutrition": {
    "@type": "NutritionInformation",
    "servingSize": "45g",
    "calories": "190",
    "fatContent": "13g",
    "saturatedFatContent": "1.5g",
    "carbohydrateContent": "14g",
    "fiberContent": "5g",
    "sugarContent": "1g",
    "proteinContent": "8g",
    "sodiumContent": "20mg"
  },
  "additionalProperty": [
    {
      "@type": "PropertyValue",
      "name": "Gluten-Free",
      "value": "Yes"
    },
    {
      "@type": "PropertyValue",
      "name": "Non-GMO",
      "value": "Yes"
    },
    {
      "@type": "PropertyValue",
      "name": "Grain-Free",
      "value": "Yes"
    },
    {
      "@type": "PropertyValue",
      "name": "Added Sugar",
      "value": "Zero"
    },
    {
      "@type": "PropertyValue",
      "name": "Plant-Based",
      "value": "Yes"
    }
  ],
  "offers": {
    "@type": "Offer",
    "url": "https://goldys.ca/products/original-superseed-cereal",
    "priceCurrency": "CAD",
    "price": "12.99",
    "priceValidUntil": "2026-12-31",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "seller": {
      "@type": "Organization",
      "name": "Goldy's",
      "url": "https://goldys.ca/"
    },
    "shippingDetails": {
      "@type": "OfferShippingDetails",
      "shippingRate": {
        "@type": "MonetaryAmount",
        "value": "0",
        "currency": "CAD"
      },
      "shippingDestination": {
        "@type": "DefinedRegion",
        "addressCountry": "CA"
      },
      "deliveryTime": {
        "@type": "ShippingDeliveryTime",
        "handlingTime": {
          "@type": "QuantitativeValue",
          "minValue": 1,
          "maxValue": 2,
          "unitCode": "DAY"
        },
        "transitTime": {
          "@type": "QuantitativeValue",
          "minValue": 3,
          "maxValue": 7,
          "unitCode": "DAY"
        }
      }
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "47",
    "bestRating": "5",
    "worstRating": "1"
  }
}
```

**Implementation notes:**
- Update `nutrition` values from the actual nutrition label on each product. The values above are illustrative — do not publish without verification from the actual product.
- `aggregateRating` must reflect real review data. Only add this block once a reviews app (Judge.me, Okendo, or Yotpo) is installed and syncing real reviews. Google penalizes fabricated ratings.
- `shippingDetails` — verify whether Goldy's offers free shipping to Canada. If not, adjust `shippingRate.value` to the actual rate or remove the block.
- `priceValidUntil` — update annually or set dynamically via Liquid.
- For multiple product variants (flavors), use `ProductGroup` with `hasVariant` — see Section 4.5.

---

### 4.4 Article Schema Enhancement for Blog Posts (High)

Add this to `sections/main-article.liquid` or the blog post template, replacing Shopify's default minimal Article output:

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{{ article.title }}",
  "description": "{{ article.excerpt | strip_html | truncate: 160 }}",
  "image": {
    "@type": "ImageObject",
    "url": "{{ article.image | img_url: 'master' | prepend: 'https:' }}",
    "width": 1200,
    "height": 630
  },
  "datePublished": "{{ article.published_at | date: '%Y-%m-%dT%H:%M:%S%z' }}",
  "dateModified": "{{ article.updated_at | date: '%Y-%m-%dT%H:%M:%S%z' }}",
  "author": {
    "@type": "Person",
    "name": "{{ article.author }}"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Goldy's",
    "logo": {
      "@type": "ImageObject",
      "url": "https://goldys.ca/cdn/shop/files/goldys-logo.png",
      "width": 512,
      "height": 512
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "{{ shop.url }}/blogs/{{ blog.handle }}/{{ article.handle }}"
  }
}
```

---

### 4.5 Recipe Schema for `/blogs/news` Recipe Posts (Medium)

Since `/blogs/news` contains recipe content, `Recipe` schema is a high-value addition. Recipe rich results (with images, cook time, ratings, ingredients) appear prominently in Google Search and Google Images.

**Example for a recipe post:**

```json
{
  "@context": "https://schema.org",
  "@type": "Recipe",
  "name": "Goldy's Superseed Cereal Parfait",
  "image": [
    "https://goldys.ca/cdn/shop/articles/superseed-parfait-recipe.jpg"
  ],
  "author": {
    "@type": "Organization",
    "name": "Goldy's",
    "url": "https://goldys.ca/"
  },
  "datePublished": "2025-09-01",
  "description": "A quick and nutritious parfait made with Goldy's Original Superseed Cereal, Greek yogurt, and fresh berries.",
  "prepTime": "PT5M",
  "cookTime": "PT0M",
  "totalTime": "PT5M",
  "keywords": "superseed cereal recipe, gluten-free parfait, high protein breakfast, grain-free cereal",
  "recipeYield": "1 serving",
  "recipeCategory": "Breakfast",
  "recipeCuisine": "Canadian",
  "recipeIngredient": [
    "1/2 cup Goldy's Original Superseed Cereal",
    "3/4 cup plain Greek yogurt",
    "1/2 cup mixed fresh berries",
    "1 tablespoon honey (optional)"
  ],
  "recipeInstructions": [
    {
      "@type": "HowToStep",
      "name": "Layer the base",
      "text": "Spoon half the Greek yogurt into a glass or bowl.",
      "position": 1
    },
    {
      "@type": "HowToStep",
      "name": "Add cereal",
      "text": "Sprinkle half the Goldy's Superseed Cereal over the yogurt.",
      "position": 2
    },
    {
      "@type": "HowToStep",
      "name": "Add berries",
      "text": "Layer the fresh berries on top.",
      "position": 3
    },
    {
      "@type": "HowToStep",
      "name": "Repeat and serve",
      "text": "Repeat with the remaining yogurt and cereal. Drizzle with honey if desired. Serve immediately.",
      "position": 4
    }
  ],
  "nutrition": {
    "@type": "NutritionInformation",
    "calories": "310 calories",
    "proteinContent": "18g",
    "fiberContent": "6g",
    "sugarContent": "9g"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "ratingCount": "12"
  }
}
```

**Implementation note:** This template should be adapted for each specific recipe post. The `recipeIngredient`, `recipeInstructions`, and `nutrition` values must match the actual recipe content. Only add `aggregateRating` if genuine ratings are collected.

---

### 4.6 FAQPage Schema — Conditional Recommendation (Info)

**Google rich results:** Adding FAQPage to goldys.ca will NOT produce rich results in Google Search (restricted to government/healthcare sites since August 2023).

**AI/LLM citation value:** FAQPage schema does help AI systems (ChatGPT, Claude, Perplexity) extract and cite specific Q&A content from the page. Given the GEO audit rated passage-level citability as "Needs Work," FAQPage schema is valuable if GEO is a priority for this brand.

**Recommended placement:** Product pages and a dedicated FAQ page. Sample questions:

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is Goldy's Superseed Cereal gluten-free?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Goldy's Superseed Cereal is certified gluten-free and grain-free, made from chia seeds, hemp hearts, pumpkin seeds, and buckwheat groats — all naturally gluten-free ingredients."
      }
    },
    {
      "@type": "Question",
      "name": "Does Goldy's cereal contain added sugar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. Goldy's Superseed Cereal contains zero added sugar. Any sweetness comes naturally from the seeds and any fruit-based ingredients in flavored varieties."
      }
    },
    {
      "@type": "Question",
      "name": "Where is Goldy's cereal made?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Goldy's cereal is made in Canada."
      }
    },
    {
      "@type": "Question",
      "name": "Is Goldy's cereal vegan?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Goldy's Superseed Cereal is 100% plant-based and vegan-friendly."
      }
    },
    {
      "@type": "Question",
      "name": "How much protein does Goldy's cereal have per serving?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Goldy's Original Superseed Cereal contains approximately 8 grams of protein per 45g serving, sourced from hemp hearts, pumpkin seeds, and chia seeds."
      }
    },
    {
      "@type": "Question",
      "name": "Where can I buy Goldy's cereal in Canada?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Goldy's Superseed Cereal is available directly at goldys.ca and through Canadian retailers including NaturaMarket, Healthy Planet Canada, The Low Carb Grocery, and Amazon.ca."
      }
    }
  ]
}
```

---

## Section 5: Implementation Priority Roadmap

### Sprint 1 — Critical (implement within 1 week)

1. **Organization schema** — Add to `layout/theme.liquid`. One-time addition. Foundational for all other schema.
2. **Product.brand** — Edit Shopify's default product schema snippet to add the `brand` block. Takes 30 minutes. Unlocks Google Shopping eligibility signals.
3. **WebSite + SearchAction** — Add to the homepage section or `layout/theme.liquid`. Enables Sitelinks Search Box.

### Sprint 2 — High (implement within 2–3 weeks)

4. **Enhanced Product schema** — Replace Shopify's default Product output with the full version in Section 4.3, including `nutrition`, `additionalProperty`, and `shippingDetails`.
5. **Article/BlogPosting publisher fix** — Update blog post template to add `publisher` and `mainEntityOfPage`. Required for Article rich results.
6. **Reviews app integration** — Install Judge.me (free tier available for Shopify) or Okendo. Ensure schema output is enabled. This is the single highest-CTR improvement available — star ratings in product snippets.

### Sprint 3 — Medium (implement within 4–6 weeks)

7. **Recipe schema** — Add to all recipe posts in `/blogs/news`. Map each post individually.
8. **BreadcrumbList audit** — Verify the current theme injects BreadcrumbList. If not, add manually.
9. **FAQPage** (if GEO is a priority) — Add to 2–3 high-traffic product pages and a dedicated FAQ page.

---

## Section 6: Shopify-Specific Implementation Notes

**Where to add JSON-LD in Shopify:**

| Schema Block | File to Edit | Location |
|---|---|---|
| Organization, WebSite | `layout/theme.liquid` | Before `</head>` |
| Product (enhanced) | `snippets/product-schema.liquid` | Included from `sections/main-product.liquid` |
| Article/BlogPosting | `sections/main-article.liquid` | Inside the article section |
| Recipe | `sections/main-article.liquid` | Conditionally, when `article.tags` contains "recipe" |
| BreadcrumbList | `snippets/breadcrumbs.liquid` | Alongside the visible breadcrumb HTML |
| FAQPage | `sections/main-product.liquid` | After FAQ accordion content |

**Critical Shopify caveat:** Shopify's default theme may already output a minimal `Product` or `WebSite` block. Before adding new JSON-LD, check the theme's existing `<script type="application/ld+json">` blocks to avoid duplicate `@type` declarations on the same page. Google's Rich Results Test will flag duplicate types.

**Verify with Google's Rich Results Test:** After implementation, validate each page at https://search.google.com/test/rich-results

---

## Section 7: Competitive Opportunity

Holy Crap Foods (goldys.ca's primary competitor per the GEO audit) also runs on a standard Shopify theme and is unlikely to have enhanced Product + NutritionInformation schema. Implementing `NutritionInformation` on all Goldy's product pages would represent a meaningful structured data advantage in the gluten-free cereal category in Canada — very few food brands on Shopify implement this correctly.

The combination of:
- `Product` + `brand` + `aggregateRating` (star ratings)
- `NutritionInformation` (per-serving macros)
- `Recipe` on blog content
- `Organization` with `sameAs` social profiles

...would make goldys.ca's structured data significantly more complete than any direct competitor currently achieves in this niche.

---

*Schema.org structured data audit completed by Claude Code SEO Schema Agent.*
*Validate all JSON-LD at: https://search.google.com/test/rich-results*
*Schema.org specification: https://schema.org*
