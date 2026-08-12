---
name: resume-system
description: CAPABILITY: builds a role-targeted resume backward from employer demand rather than from memory — measures which qualifications a job family actually screens on (10-15 gated job descriptions, ranked by document frequency), maps a master experience inventory against those qualifications, allocates evidence across the page as a portfolio rather than optimizing bullets independently, writes each bullet with the architecture that surfaces its strongest relevant signal, and audits the finished resume for coverage, redundancy, and role narrative. Applies named tests: Burger vs. Hot Dog, Stranger, Primary Signal, Causality, Interview Defensibility. Displaces writing bullets from memory, generic 'action verb + metric' advice, single-formula bullet templates, and per-job manual tailoring. Use when writing or rewriting a resume or specific bullets, targeting a new role or job family, deciding what to cut when bullets exceed slots, developing a scratchpad note into a real bullet, tailoring for a specific posting, diagnosing why a resume gets no interviews, or asking which qualifications a resume fails to prove.
---

# Resume System

A resume's only job is to prove you meet the minimum qualifications for one job
title. This system measures what those qualifications actually are, then spends
each bullet slot deliberately against them.

Four sub-skills, run in order:

| # | Sub-skill | Input → Output |
|---|---|---|
| 1 | **qualification-finder** — `references/qualification-finder.md` | Job family + target companies → ranked qualification table + verbatim duty language |
| 2 | **evidence-mapper** — `references/evidence-mapper.md` | Qualifications + master experience inventory → qualification↔evidence map + allocation plan |
| 3 | **bullet-creator** — `references/bullet-creator.md` | Allocation plan → finished bullets, one experience at a time |
| 4 | **resume-auditor** — `references/resume-auditor.md` | Finished resume + qualifications → coverage verdict + keep/cut ranking |

**Stage 1 is skippable. Stage 2 is not.** When qualifications arrive already
supplied — a competency map, a hiring-signal list, a parsed JD — take them as the
working target and start at stage 2. Do **not** re-derive them. But never jump
from qualifications straight to prose: stage 2 is where a resume stops being a
list of accomplishments and becomes a portfolio of evidence.

The HHH qualification skeleton — `references/hhh-framework.md` — sits under all
four. The Business Analyst Intern slide is canonical and must never be rewritten;
new roles are derived by holding its risk-removal buckets fixed and swapping only
the tool-stack bullet.

## The core rule

The resume does not answer *"what are the coolest things I've done?"*

It answers: **"what concrete evidence most efficiently proves I already
demonstrate the behaviors this employer is trying to hire?"**

## The named tests

Applied consistently across stages 2–4; each is defined in its sub-skill.

| Test | Asks | Defined in |
|---|---|---|
| **Burger vs. Hot Dog** | Relevant evidence, or merely impressive? | evidence-mapper |
| **Evidence Allocation** | What does this bullet add that the others don't? | evidence-mapper |
| **Primary Signal** | What single thing should the reader remember? | bullet-creator |
| **Stranger Test** | Does an outsider follow it without insider context? | bullet-creator |
| **Causality Test** | Is the causal verb defensible? | bullet-creator |
| **Interview Defensibility** | Does every claim survive "tell me more"? | bullet-creator |
| **Role Narrative** | Does the whole page read as this candidate? | resume-auditor |

## Collaboration contract

Work **one experience at a time**. Ask for missing facts rather than writing
around them. Offer alternatives only on a genuine strategic tradeoff, never as
synonym variants. Never regenerate a finished resume wholesale — the allocation
decisions belong to the person whose experience it is.

Evidence arrives in three states, and they are not interchangeable: **complete
bullets**, **promising but incomplete accomplishments**, and **scratchpad
placeholders** (*"Waddle, Avea"*, *"Add corp relations role"*). Scratchpad
fragments are memory notes, never a style signal and never a draft.

## Method provenance

Derived from *How to Get a Job* (the Headless Headhunter), plus corrections
learned by running it wrong first.

**Take the method, not the formatting.** HHH mandates Arial, 1.5 line spacing,
and permits multiple pages. That guidance targets **corporate mass-apply** —
recruiter-screened job boards, first-come-first-served in the ATS. Campus
recruiting and consulting/APM programs are a different funnel: GPA screens,
resume drops, cohort comparison, often read by an alum of your own school. A
dense one-page resume that already produced interviews should not be reformatted
to satisfy a rulebook written for a different channel — that introduces a
variable you cannot attribute if results drop.

Keep from HHH: keyword harvesting (p.10–11), the qualification skeleton, and
apply-fast (p.30–32).

**Superseded:** HHH's fixed *What → How → Result/Reason* bullet formula (p.24–26)
is now **one of five conditional architectures** in `bullet-creator.md`, not the
only shape. It remains a sound default for high-volume corporate applications;
for competitive campus and consulting programs, architecture should follow the
evidence.

## The non-negotiables

**1. The floor is real.** Below 10 qualifying JDs, emit
`INSUFFICIENT CORPUS: n=X, need Y more` and **no ranked table**. A table built
from 6 JDs looks identical to one built from 15 — that is the failure the reader
cannot catch by reading. Never round a thin corpus up to an answer.

**2. No gate may model the candidate.** Every filter judges the *job*, never the
person. An early version gated on "does the candidate meet 75% of these
qualifications" (HHH p.11) and it was circular: it filtered the input by the
current resume, so qualifications the person had done but never written down
read as "not required" instead of surfacing as gaps. That single gate would have
suppressed the most valuable finding of the first run. Do not reintroduce it.

**3. Count documents, not mentions.** A JD saying "stakeholder" six times is one
JD asking for stakeholder management. Raw-frequency counting rewards verbose
postings.

**4. One PRIMARY signal per bullet.** A bullet with no dominant signal proves
nothing — three things half-proven. Secondary signals may ride along if they
don't dilute the primary. The rule is one *purpose*, not one detectable concept;
do not chase a literal match count. See `bullet-creator.md`.

**5. Measurement ranks capability; the skeleton ranks risk.** Where a measured
corpus and the HHH skeleton disagree about a risk-removal bucket (coachability,
teamwork), the skeleton wins — JDs under-state what every employer assumes.

**6. Report the corpus with the table.** Every ranked output ships with which
JDs produced it and which were rejected at which gate. A number without
provenance cannot be audited.

## The six gates

Applied in order. G2 and G4 need only the posting title, so run them *before*
fetching — on a real board that drops ~90% of candidates for free.

| Gate | Rule | Catches |
|---|---|---|
| **G1** Good-JD | Has a Qualifications/Requirements block (HHH p.10) | Postings that are all marketing copy |
| **G2** Title-in-family | Title matches the family whitelist, compared on **stems** | "Member Experience Intern" filed under GTM |
| **G3′** Role-nature | Qualifications not majority hard-engineering IC | "Special Projects Intern" whose duties are robotics software |
| **G4** Seniority | Intern / co-op / new-grad only | Senior roles whose "8 years experience" poisons an intern table |
| **G5** Concentration | No single company >20% of a corpus | One employer's house style masquerading as an industry pattern |
| **G6** Segment floor *(opt-in)* | Company clears a target-tier allowlist, matched on **whole tokens** | Long-tail employers padding a corpus to the floor |

G6 is opt-in because it encodes *ambition*, not correctness: "is this the kind of
employer I'm aiming at" is a strategy call. Turn it on for an aim-high corpus —
a resume built for McKinsey clears Campbell Soup, never the reverse.

Token matching, not substring: `meta` otherwise matches *AA Metals* and
*Metalinked*, and `blackrock` matches *Blackrock Neurotech* — three long-tail
firms admitted by the one gate meant to exclude them. Genuine name collisions
between distinct companies need `DENY_COMPANIES`; no string rule separates them.

Stem comparison matters: a whitelist entry `project manager` must match a
posting titled `Technical Project Management Intern`. Substring matching misses
this and silently shrinks the corpus.

## Usage

```bash
cd scripts
python3 -m pytest test_gates.py -q            # 55 tests, run after any gate edit

# urls file lines:  URL | Company | Title
python3 run.py fetch  --family R1 --urls urls_R1.txt
python3 run.py report --all --segment-floor   # aim-high corpus; exit 2 if below floor
python3 chart.py                              # the artifact you write from
```

Families, title whitelists, the qualification lexicon, and the thresholds all
live in `scripts/config.py`. Nothing is hardcoded in the pipeline — adding a job
family means adding a dict entry, not editing logic.

`run.py report` **exits 2** when any family is below the floor, so it can gate a
downstream step rather than quietly emitting a thin table.

## Files

```
scripts/config.py    families, title whitelists, 31-concept lexicon, thresholds
scripts/gates.py     G1–G6 + the stemmer and company normaliser
scripts/pipeline.py  fetch (HTTP → browser escalation), sectionize, tally
scripts/run.py       CLI: fetch / report
scripts/chart.py     the per-family traits/qualifications chart
scripts/test_gates.py 55 tests, every case a real posting from a prior run
data/<family>/       cached JD JSON — re-runs are free
references/qualification-finder.md   sub-skill 1 — measure demand
references/evidence-mapper.md        sub-skill 2 — match + allocate evidence
references/bullet-creator.md         sub-skill 3 — write, test, compress
references/resume-auditor.md         sub-skill 4 — audit the finished page
references/hhh-framework.md          the canonical qualification skeleton
```
