# E-E-A-T and Content Quality Audit: goldys.ca

**Audit Date:** 2026-03-16
**Framework:** September 2025 QRG + December 2025 Core Update
**Site Type:** Canadian Shopify e-commerce — superseed cereal

---

## Overall Content Quality Score: 34/100

Strong off-site brand signals but critically thin on-site content — a pattern common in Shopify stores that rely on visual design over crawlable text.

---

## E-E-A-T Breakdown

| Factor | Weight | Score | Weighted | Key Signals |
|--------|--------|-------|----------|-------------|
| Experience | 20% | 9/20 | 1.8/20 | No founder story in crawlable text; no first-person narrative |
| Expertise | 25% | 8/25 | 2.0/25 | No author bylines; no nutritional expert attribution; ingredient claims not backed by sources |
| Authoritativeness | 25% | 14/25 | 3.5/25 | Strong retail distribution; #1 organic for "best superseed cereal Canada"; weak editorial presence |
| Trustworthiness | 30% | 11/30 | 2.75/30 | Shopify HTTPS; known retailer relationships; no visible contact info; no content dates |

**Composite E-E-A-T Score: 34/100 (Weak — Significant Gaps)**

---

## Page-Level Findings

### 1. Homepage — CRITICAL

No crawlable H1, H2, or H3 text detected. Page title returned empty — a critical on-page SEO failure. No meta description. Brand tagline, value proposition, and product descriptions appear to exist only within rendered JavaScript or image files. Against a 500-word minimum floor for homepages, estimated crawlable content: ~0 words.

**Missing:**
- Crawlable brand positioning statement above the fold
- Primary keyword in H1 (e.g., "Superseed Cereal, Made in Canada")
- Core differentiators in bullet text (not image text)
- Short founder/origin summary with link to About page

### 2. Product Pages — HIGH

Nutritional statistics — the most citable, rankable content asset a food brand has — do not appear in crawlable text. Nutrition facts are presented as images of labels.

| Element | Status | Severity |
|---------|--------|----------|
| Per-serving protein (g) in text | Missing | Critical |
| Per-serving fiber (g) in text | Missing | Critical |
| Calorie count in text | Missing | Critical |
| Omega-3 content in text | Missing | High |
| Ingredient list in HTML text | Likely image-only | High |
| Allergen statement in text | Unknown | High |
| Certifications in text | Unclear | Medium |
| Customer review schema | Not confirmed | Medium |
| Comparison vs. traditional cereal | Absent | Medium |

Estimated crawlable words per product page: ~50–100 (against 400-word minimum).

### 3. Blog / Recipe Content (/blogs/news) — HIGH

Blog contains primarily recipes, not informational content — a strategic content error:
- Recipes don't capture mid-funnel queries ("is superseed cereal healthy", "best high-protein breakfast cereal Canada")
- No author bylines detected (anonymously published — penalized under December 2025 standards)
- No publication dates confirmed visible
- No external citations or source links
- No "first-hand experience" signals

**Missing blog content types:**
1. Informational: "What is a superseed?" / "Health benefits of chia seeds for breakfast"
2. Comparison: "Superseed cereal vs. oatmeal: nutrition comparison"
3. Brand story: "How Goldy's was founded in Canada"
4. Category authority: "Complete guide to gluten-free cereals in Canada"

### 4. Author Signals — CRITICAL

- No author bylines on any blog post or content page
- No founder name attributed to content (founder context exists on LCG Foods off-site only)
- No nutritional expert or dietitian attribution for health claims
- December 2025 QRG "penalized anonymous or generic authorship even for non-YMYL content"

### 5. Trust Signals / About Page — HIGH

| Trust Element | Present | Notes |
|---------------|---------|-------|
| HTTPS | Yes | Shopify default |
| Physical address | Not confirmed | |
| Phone/email contact | Not confirmed | |
| Privacy/refund policy | Likely (Shopify default) | Not confirmed in crawl |
| Customer reviews with dates | Not confirmed | |
| Certification authority names | Not confirmed | |
| Founder identity | Off-site only (LCG Foods) | |
| Years in business | Not found | |

**What is known from third-party sources:** LCG Foods hosts a "Goldy's Brand Story" page. Brand is listed in MadeInCA directory. Carried by NaturaMarket, Healthy Planet, Low Carb Grocery, Amazon.ca.

### 6. Thin Content Detection — CRITICAL

| Page Type | Min Words | Est. Crawlable Words | Gap |
|-----------|-----------|----------------------|-----|
| Homepage | 500 | ~0 | -500 |
| Product pages | 400 | ~50–100 | -300 to -350 |
| Blog posts | 1,500 | ~300–600 (est.) | -900 to -1,200 |
| Collection pages | 300 | ~0 | -300 |
| About page | 500 | Unknown, likely thin | -200 to -500 |

### 7. AI Citation Readiness — 12/100

| Citability Factor | Status | Score |
|-------------------|--------|-------|
| Specific nutritional stats in crawlable text | Missing | 0/15 |
| FAQ schema markup | Not detected | 0/15 |
| Clear quotable claims with numbers | Missing | 0/15 |
| Structured ingredient/benefit text | Missing | 2/10 |
| Answer-first formatting | Missing | 0/10 |
| Comparison tables vs. competitors | Missing | 0/10 |
| Author/brand entity markup (schema) | Not confirmed | 2/10 |
| Heading hierarchy for AI parsing | Not detected | 0/10 |
| Content freshness signals (dates) | Not detected | 4/5 |
| AI crawler access (robots.txt) | Blocked | 0/5 |

---

## Severity-Ranked Findings

| # | Finding | Severity | Effort |
|---|---------|----------|--------|
| 1 | No crawlable title tag, meta description, or H1 on homepage | CRITICAL | Low |
| 2 | Zero author attribution across all content | CRITICAL | Medium |
| 3 | Nutritional statistics locked in images, not crawlable text | CRITICAL | Low |
| 4 | AI crawlers blocked (Shopify default robots.txt) | CRITICAL | Low |
| 5 | Blog contains only recipes — no informational authority content | HIGH | High |
| 6 | No founder story / About page content in crawlable HTML | HIGH | Medium |
| 7 | Product pages below 400-word content floor | HIGH | Medium |
| 8 | No FAQ schema on product or category pages | HIGH | Low |
| 9 | No visible certification authority names (e.g., Non-GMO Project) | HIGH | Low |
| 10 | Collection pages return no crawlable content | HIGH | Medium |
| 11 | No comparison content vs. traditional cereal | MEDIUM | Medium |
| 12 | No publication dates on blog content | MEDIUM | Low |
| 13 | No Wikipedia / Wikidata / Crunchbase entity presence | MEDIUM | Medium |
| 14 | Blog section named "News" but contains recipes | MEDIUM | Low |
| 15 | No internal linking strategy detectable | MEDIUM | Medium |
| 16 | No press/media coverage linked from site | LOW | High |
| 17 | No LinkedIn company page found | LOW | Low |

---

## Prioritized Recommendations

### Immediate (Week 1–2)

1. **Fix title tag and meta description** — Shopify theme settings edit. Homepage title: "Goldy's — Superseed Cereal | Gluten-Free, Grain-Free, Made in Canada"
2. **Add nutritional stats as crawlable text on every product page** — Beneath the label image, add HTML text with exact per-serving values: protein, fiber, calories, omega-3. ~15 min per product.
3. **Customize robots.txt.liquid to allow AI search bots** — Allow GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot, Claude-SearchBot, PerplexityBot
4. **Add author byline to all blog posts** — Attribute to founder by name; create a simple author bio page
5. **Add publication dates to all blog posts** — Theme setting or minor template edit

### Short-Term (Month 1)

6. **Rewrite the About page as a founder story** — 600–800 words of crawlable HTML. Bring the LCG Foods brand story on-site.
7. **Add FAQ schema to product pages** — 5–7 Q&A per product (gluten-free?, protein per serving?, where to buy?, keto-friendly?)
8. **Expand each product page to 400+ words** — Benefits with numbers → ingredient spotlight → serving suggestions → certifications
9. **Create 3 informational blog articles** (1,500+ words each, author-attributed, dated):
   - "Superseed Cereal: What It Is and Why It's Different From Regular Cereal"
   - "High Protein Gluten-Free Cereal: A Canadian Guide"
   - "Health Benefits of Chia, Hemp, and Pumpkin Seeds for Breakfast"

### Medium-Term (Months 2–3)

10. **Create Wikidata entity** for the brand to support Knowledge Panel generation
11. **Build topical content clusters** — 10–15 posts around "Superseed Cereals," "Gluten-Free Breakfast Canada," "Plant-Based Protein Breakfast"
12. **Pursue independent editorial coverage** — Canadian health food blogs, registered dietitian sites, "best of" lists

---

## Competitor Context

**Holy Crap Foods** (direct Canadian competitor) shows stronger E-E-A-T: named founders with editorial presence, independent press coverage, informational blog content, specific nutritional claims in text, customer testimonials. Goldy's currently outranks Holy Crap on "best superseed cereal Canada" but that ranking rests on off-site signals — fragile without on-site content improvement.
