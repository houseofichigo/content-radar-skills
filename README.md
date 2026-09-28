# Content Radar Skills

A seven-skill, industry-agnostic content intelligence suite for discovering trends, monitoring competitors, finding responsible news hooks, generating channel-specific ideas, and producing SEO/AEO/GEO-ready content briefs.

## Skills

| Skill | Purpose |
|---|---|
| `content-radar-setup` | Builds and confirms the shared brand `profile.md`. |
| `content-radar` | Orchestrates the complete weekly sweep and content plan. |
| `trend-radar` | Finds and ranks timely themes from open sources. |
| `newsjacking` | Finds current events the brand can responsibly address. |
| `competitor-scan` | Maps competitor activity, white space, and replicable wins. |
| `content-ideas` | Produces one on-brand idea per channel. |
| `seo-aeo-geo` | Creates answer-first content for search and AI citation. |

The skills remain separate Agent Skills and share one user-approved `profile.md`; the suite repository does not merge them into one oversized instruction file.

## Install

Install the suite and select all seven skills:

```bash
npx skills add houseofichigo/content-radar-skills --skill '*'
```

Install one skill instead:

```bash
npx skills add houseofichigo/content-radar-skills --skill trend-radar
```

Use `--agent codex`, `--agent claude-code`, or another supported agent identifier when targeting a specific host. Add `-g` for a user-level installation.

After installation, run `content-radar-setup` first. It uses its bundled profile template, asks the user to confirm discovered topics and competitors, and saves the approved `profile.md` in the active project—not inside the installed skill.

## Distributions

- `dist/<skill-name>.zip`: one portable upload package per skill.
- `dist/content-radar-skills.zip`: the full seven-skill bundle plus shared profile resources. This is a suite archive, not a single-skill upload.

## Repository layout

```text
skills/                 Seven independently discoverable skills
resources/              Shared blank profile template
dist/                   Seven skill ZIPs plus the suite bundle
scripts/                Deterministic validation and packaging
tests/                  Suite layout and distribution checks
```

## Validate

```bash
python3 scripts/validate_suite.py
python3 scripts/build_dist.py --check
python3 -m unittest discover -s tests -v
```

Validation checks structure, cross-host rules, and deterministic distributions. It does not prove runtime behavior, source availability, or the truth of future web results.

## Licence

Released under the [MIT License](LICENSE). Each portable skill package includes the licence text.
