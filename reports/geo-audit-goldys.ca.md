# AI Search Readiness & GEO Audit: goldys.ca

**Date:** 2026-03-16

## Executive Summary

Goldy's has solid brand presence across Canadian health food retail channels, but significant gaps exist in AI search readiness. The site is likely blocking AI crawlers by default (Shopify's standard behavior), has no llms.txt file, and lacks the structured content needed for AI citation.

---

## Summary Scorecard

| Area | Rating | Key Issue |
|------|--------|-----------|
| **AI Crawler Access** | **CRITICAL** | Shopify default blocks GPTBot, ClaudeBot, PerplexityBot |
| **llms.txt** | **CRITICAL** | File does not exist |
| **Brand Mention Signals** | **GOOD** | Strong retail partner presence; weak editorial/authority signals |
| **Passage-Level Citability** | **NEEDS WORK** | No specific nutritional stats in crawlable text; no FAQ schema; image-heavy |
| **AI Overview Presence** | **NEEDS WORK** | Not appearing in AI Overviews; invisible for broad category queries |
| **Knowledge Panel** | **NEEDS WORK** | No Wikipedia, Wikidata, or Crunchbase presence to trigger a panel |

---

## 1. AI Crawler Access — Rating: CRITICAL

**Shopify blocks AI crawlers by default.** Fetch attempts to goldys.ca pages returned **403 Forbidden** errors, consistent with Shopify's documented default behavior of blocking non-browser user agents.

Key findings:
- Shopify updated its default `robots.txt` to block GPTBot, ClaudeBot, PerplexityBot, and other AI crawlers without notifying most merchants.
- ClaudeBot is blocked by ~69% of sites; GPTBot by ~62%. Unless Goldy's has proactively customized their `robots.txt.liquid` template, all major AI crawlers are almost certainly blocked.
- **Impact**: When users ask ChatGPT, Claude, or Perplexity "what's a good superseed cereal in Canada?", the AI cannot crawl goldys.ca to get current product/pricing info. It must rely entirely on third-party retailer pages (NaturaMarket, Amazon.ca, etc.).

**Fix**: Create a `robots.txt.liquid` file in the Shopify theme that explicitly allows AI search/retrieval bots (GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot, Claude-SearchBot, PerplexityBot) while optionally continuing to block training-only bots.

---

## 2. llms.txt File — Rating: CRITICAL

**No llms.txt file exists.** There is no evidence of a `goldys.ca/llms.txt` file on the domain.

An llms.txt file would provide AI systems with a structured, markdown-formatted summary of the brand, products, nutritional claims, and key pages — making it far easier for LLMs to accurately represent Goldy's in responses.

---

## 3. Brand Mention Signals — Rating: GOOD

This is Goldy's strongest area. The brand has a healthy distribution of third-party mentions across the Canadian web:

- **Retail partners citing the brand**: NaturaMarket, The Low Carb Grocery, Healthy Planet Canada, Mindful Snacks, Coco Market, Molly's Market, Natural Food Mart, Amazon.ca
- **Distribution/wholesale**: LCG Foods has a dedicated [brand story page](https://www.lcgfoods.com/page/87/goldy-s-brand-story-lcg-foods)
- **Canadian-made directories**: [MadeInCA](https://madeinca.ca/cereal-oatmeal-goldys/) lists the brand
- **Social presence**: Facebook page exists (goldyscereal)
- **Competitive visibility**: For the query "best superseed cereal Canada", Goldy's appeared as the **#1 result** and also at positions #4 and #5 via retailer pages.

**Gap**: No Wikipedia page, no Crunchbase profile, no LinkedIn company page found, and no independent blog reviews or press coverage surfaced. Holy Crap Foods, a direct competitor, has stronger editorial/media presence.

---

## 4. Passage-Level Citability — Rating: NEEDS WORK

AI systems cite content that contains **specific, quotable claims with numbers**.

**What works:**
- Clear ingredient lists (chia, hemp, pumpkin seeds, buckwheat)
- Strong attribute claims (Non-GMO, gluten-free, grain-free, zero added sugar, plant-based)
- Flavor variety is well-documented

**What's missing:**
- **No specific nutritional numbers appear in crawlable text.** No exact per-serving values for protein, fiber, calories, or omega-3s in text form. AI systems need numbers to cite: "12g of protein per serving" or "5x more fiber than regular cereal" are the kinds of claims that get pulled into AI Overviews.
- **No FAQ schema** detected on the site.
- **No comparison data** (e.g., "vs traditional cereal, Goldy's has X% more protein")
- **No informational blog content** with citable claims. The `/blogs/news` section appears to be recipes, not informational content.
- Content appears to be heavily image-based (typical of Shopify stores), which AI crawlers cannot parse.

---

## 5. AI Overview Presence — Rating: NEEDS WORK

**No evidence that Goldy's appears in Google AI Overviews.** However, for the query "best superseed cereal Canada", Goldy's dominates organic results (positions #1, #4, #5), which means it has the **potential** to appear in AI Overviews if on-page content is improved for citability.

For the broader query "gluten free cereal Canada", Goldy's does **not** appear. Results are dominated by larger brands (Cheerios, Chex, Nature's Path, Holy Crap) and major retailers (Amazon.ca, Well.ca).

---

## 6. Knowledge Panel — Rating: NEEDS WORK

**No Google Knowledge Panel exists for Goldy's.** There is no Wikipedia page, no Wikidata entry, and no Crunchbase profile — all of which are primary sources Google uses to generate Knowledge Panels.

Without a Knowledge Panel, AI systems have lower confidence in the brand as a distinct entity, reducing the likelihood of being cited in generative responses.

---

## Priority Recommendations

### Immediate Actions
1. **Customize `robots.txt.liquid`** in the Shopify theme to unblock AI search bots (GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot, Claude-SearchBot, PerplexityBot)
2. **Create an `llms.txt` file** with brand summary, product lines, nutritional claims, and key URLs

### Short-term Actions
3. **Add specific, citable nutritional statistics** to product page text (not just images of nutrition labels)
4. **Implement FAQ schema** on product and collection pages

### Medium-term Actions
5. **Create a Wikidata entry** and pursue a Wikipedia stub
6. **Pursue independent editorial coverage** (blog reviews, press mentions, "best of" lists)
7. **Develop informational blog content** targeting broad queries like "best gluten free cereal Canada" with comparison tables and citable data points

---

## References

- [Sobefy - Shopify robots.txt AI Agent Guide](https://www.sobefy.com/blog/shopify-robots-txt-how-to-allow-ai-agents-to-crawl-your-store-for-better-seo-and-discovery)
- [Inflow - Shopify's Hidden AI Bot Blocking](https://www.inflowinventory.com/blog/shopifys-ai-bot-blocking/)
- [Shopify Dev - Customize robots.txt](https://shopify.dev/docs/storefronts/themes/seo/robots-txt)
- [LCG Foods - Goldy's Brand Story](https://www.lcgfoods.com/page/87/goldy-s-brand-story-lcg-foods)
- [MadeInCA - Goldy's](https://madeinca.ca/cereal-oatmeal-goldys/)
- [NaturaMarket - Goldy's](https://naturamarket.ca/brands/goldys.html)
- [llmstxt.org - The llms.txt Standard](https://llmstxt.org/)
- [Amazon.ca - Goldy's Peach Pecan](https://www.amazon.ca/Goldys-Sugar-Fiber-Superseed-Cereal/dp/B0C9JWFXXP)
