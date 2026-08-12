# context/ — Bring Your Own Context

Everything in `scripts/` is **method** and works unchanged for anyone.
Everything here is **you**: your experience, your target market, your judgment
about what matters. The split is what lets the code be shared without shipping
someone's resume.

Copy any `*.example.json` to the same name without `.example` and edit it. Every
file is optional — the examples are the fallback, so a fresh clone runs before
you have written anything.

| File | What it holds | Kind of thing |
|---|---|---|
| `master_experience.json` | Your bullets and scratchpad leads | **Personal** — gitignored |
| `families.json` | Job families + title whitelists, one per resume | Market |
| `anchors.json` | Traits you've decided matter regardless of measurement | Judgment |
| `tiers.json` | Employer allowlists for the opt-in segment floor (G6) | Ambition |

## master_experience.json

The inventory holds three states, and they are **not** interchangeable:

```json
{"bullets": [
  {"org": "Acme",     "text": "Built X that did Y, cutting Z by 40%", "state": "complete"},
  {"org": "Acme",     "text": "Ran pricing analysis before the raise", "state": "incomplete"},
  {"org": "Sidework", "text": "Waddle, Avea",                          "state": "scratchpad"}
]}
```

- **complete** — a developed bullet with its evidence intact. Only these are audited.
- **incomplete** — a real accomplishment missing a key fact. Interrogate it before writing.
- **scratchpad** — a memory placeholder. Never a draft, never a style signal.

Scoring the last two would report a placeholder as resume coverage, so the
auditor ignores them by design. Write leads down anyway — that is what the field
is for.

## families.json

One entry per resume you intend to maintain. `lead` is the title you'll
mass-apply to; JDs matching it count double, so the ranking centers on your
actual target rather than drifting toward the tail titles.

```json
{"families": {"R1": {"name": "Strategy / Business Analyst",
                     "lead": "business analyst",
                     "titles": ["business analyst", "strategy intern", "..."]}}}
```

Titles are matched on **stems**, so `project manager` catches *Technical Project
Management Intern*.

## anchors.json

Traits you've decided matter, independent of what any corpus measures. They're
starred in the chart so a measured ranking never silently drops one.

This exists because measurement and judgment answer different questions.
Coachability scores near the bottom of every corpus — postings rarely write it
down — while the underlying hiring model treats it as a quarter of what an
intern is screened on. **Measurement ranks capability; your anchors rank what
you know to be true anyway.**

## tiers.json

Drives the opt-in `--segment-floor`. Three bands:

- **elite** — the aim-high set.
- **reputable** — still legitimate resume employers. Present because the floor
  exists to exclude unknown local shops, *not* everyone below the top tier.
- **deny** — names that collide with an allowlist entry but are different
  companies. No string rule separates an asset manager from an unrelated
  medical-device firm sharing its name.

Matching is on **whole tokens**, never substrings — otherwise `meta` matches
*AA Metals*.
