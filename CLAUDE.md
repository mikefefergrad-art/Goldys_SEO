# Goldys SEO Project

## Setup

Claude SEO skill installed via:
```bash
curl -fsSL https://raw.githubusercontent.com/AgriciDaniel/claude-seo/main/install.sh | bash
```

Version: v1.4.0
Python deps: `~/.claude/skills/seo/.venv/`

## Usage

```
/seo audit https://goldys.com
/seo page https://goldys.com/some-page
/seo technical https://goldys.com
/seo content https://goldys.com
/seo schema https://goldys.com
/seo sitemap https://goldys.com
/seo images https://goldys.com
/seo geo https://goldys.com
```

## Available Skills

| Skill | Purpose |
|-------|---------|
| `/seo audit` | Full site audit with 7 parallel subagents |
| `/seo page` | Deep single-page analysis |
| `/seo technical` | Technical SEO (9 categories) |
| `/seo content` | E-E-A-T and content quality |
| `/seo schema` | Schema.org detection, validation, generation |
| `/seo sitemap` | XML sitemap analysis/generation |
| `/seo images` | Image optimization analysis |
| `/seo geo` | AI search / Generative Engine Optimization |
| `/seo plan` | Strategic SEO planning by industry |
| `/seo programmatic` | Programmatic SEO at scale |
| `/seo competitor-pages` | Competitor comparison pages |
| `/seo hreflang` | International SEO / hreflang audit |

## Source

Skill source: `./claude-seo/`
Documentation: `./claude-seo/docs/`
