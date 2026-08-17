# resume-system

A Claude Code skill that builds a role-targeted resume **backward from employer
demand** instead of forward from memory.

Built by [Jason Munguia](https://github.com/jasonmunguia). Apache-2.0 — free to use, fork and build on, **with credit**.


Memory optimizes for what you remember doing. Screeners select on what they were
told to look for. Those diverge, and the gap is invisible without counting — in
this system's first real run, a resume spent **8 of 14 bullets on sales/GTM
signal** while Sales/GTM ranked *last of 28* in the qualification blocks of the
job family it was aimed at.

## Four sub-skills

| # | Sub-skill | Input → Output |
|---|---|---|
| 1 | `qualification-finder` | Job family + target companies → ranked qualification table + verbatim duty language |
| 2 | `evidence-mapper` | Qualifications + experience inventory → evidence map + allocation plan |
| 3 | `bullet-creator` | Allocation plan → finished bullets, one experience at a time |
| 4 | `resume-auditor` | Finished resume → coverage verdict + keep/cut ranking |

**Stage 1 is skippable. Stage 2 is not.** If qualifications arrive already
supplied, start at stage 2 — but never jump from qualifications to prose.

Full method: [`SKILL.md`](SKILL.md). Single-file version for pasting into any
assistant: [`PORTABLE.md`](PORTABLE.md).

## Quick start

```bash
pip install "scrapling[all]>=0.4.9"      # only stage 1 needs it
cd scripts
python3 -m pytest test_gates.py -q       # 59 tests

# Stage 1a — harvest from ATS public JSON APIs (fastest, full posting bodies)
python3 boards.py --family R1

# Stage 1b — or fetch specific URLs:  "URL | Company | Title" per line
python3 run.py fetch --family R1 --urls my_urls.txt

# Rank. --segment-floor restricts to target-tier employers. Exit 2 if below floor.
python3 run.py report --all --segment-floor

# Stage 2-4 input: the chart you write from
cp ../context/master_experience.example.json ../context/master_experience.json
python3 chart.py
```

## Why it refuses to answer sometimes

Below **10 qualifying job descriptions** a family emits
`INSUFFICIENT CORPUS: n=X, need Y more` and **no ranked table**.

A table built from 6 postings looks identical to one built from 15. That is the
failure a reader cannot catch by reading, so the system declines rather than
rounding a thin corpus up to an answer. `run.py report` exits **2** so it can
gate a downstream step.

## The six gates

Every gate judges the **job**, never the candidate.

| Gate | Rule |
|---|---|
| G1 Good-JD | Has a Qualifications/Requirements block |
| G2 Title-in-family | Title matches the family whitelist, compared on **stems** |
| G3′ Role-nature | Qualifications not majority hard-engineering IC |
| G4 Seniority | Intern / co-op / new-grad only |
| G5 Concentration | No single company >20% of a corpus |
| G6 Segment floor *(opt-in)* | Company clears a tier allowlist, matched on **whole tokens** |

An early version included the source method's rule *"only use JDs you meet 75% of
the qualifications for."* **It was cut and must not return.** It filters the input
by the current resume, so qualifications you have done but never written down read
as *not required* rather than surfacing as gaps — suppressing exactly what the
system exists to find. Any gate referencing the candidate is that bug renamed.

## Named tests

`Burger vs. Hot Dog` · `Evidence Allocation` · `Primary Signal` · `Stranger Test`
· `Causality Test` · `Interview Defensibility` · `Role Narrative`

Defined in `references/`.

## Configuration

Method-level knobs live in [`scripts/config.py`](scripts/config.py) — the
31-concept qualification lexicon, trait/tool/domain classification, and the
thresholds (floor, target, concentration cap, lead weight).

Anything specific to *a person or a market* lives in `context/` and overrides
the shipped defaults — see below. Adding a fourth job family is a JSON entry,
not a code change.

## Bring your own context

Everything in `scripts/` is method and works unchanged for anyone. Everything in
[`context/`](context/) is you — your experience, your target market, your
judgment. Copy any `*.example.json` to the same name without `.example`:

| File | Holds | Kind |
|---|---|---|
| `master_experience.json` | Your bullets and scratchpad leads | **Personal** — gitignored |
| `families.json` | Job families + title whitelists, one per resume | Market |
| `anchors.json` | Traits you've decided matter regardless of measurement | Judgment |
| `tiers.json` | Employer allowlists for the segment floor | Ambition |

All optional — examples are the fallback, so a fresh clone runs immediately. See
[`context/README.md`](context/README.md).

The inventory holds three evidence states — `complete`, `incomplete`,
`scratchpad`. Only `complete` bullets are audited; scoring a placeholder would
report it as resume coverage.

## Known limits

- The automated audit regex-matches concepts, which measures **relevance only** —
  one of six terms in evidence value. Strength, credibility, specificity,
  comprehension, and differentiation are human judgment.
- G5 caps a single company's *share*, but a corpus can still clear the floor from
  few employers. Distinct-employer count is reported; below 6 it warns rather
  than trimming, since trimming would push thin families back under the floor.
- Business internships at elite employers are seasonally scarce. A sweep of
  11,435 postings across 38 target-tier boards found 204 intern-level roles,
  overwhelmingly engineering.

## Provenance

Method derived from *How to Get a Job* (the Headless Headhunter), plus
corrections learned by running it wrong first. **Take the method, not the
formatting** — its Arial / 1.5-spacing / multi-page rules target high-volume
corporate applications through job boards, a different funnel from campus
recruiting. Its fixed *What → How → Result* bullet formula is retained as one of
five conditional architectures rather than the only shape.

Downstream evidence-selection and bullet-construction logic contributed via a
separate review process and reconciled in `references/`.
