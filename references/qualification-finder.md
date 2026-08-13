# Sub-skill 1 — Keyword Engine

**Input:** a job family (a set of related titles you'll apply to with one resume)
plus a candidate pool of postings.
**Output:** a ranked qualification table with provenance, and verbatim duty
language for the inception layer.

## Why this exists

A resume written from memory optimizes for what you remember doing. A resume
written from a measured corpus optimizes for what employers actually screen on.
Those differ more than people expect — in the first real run, the candidate's
resume spent 8 of 14 bullets on Sales/GTM signal, and Sales/GTM appeared in
**zero of ten** Strategy/Business-Analyst qualification blocks.

## Procedure

### 1. Define the family
A family is the set of titles one resume will serve. Give it a **lead title** —
the one you'll mass-apply to. Lead-title JDs are weighted 2× because the resume
aims at that title first and the tail titles second.

Family unit vs. per-title unit: HHH prescribes 10–15 JDs *per job title*. That
assumes one resume per title. If you're building N resumes for N families, the
family is the correct unit — but weight the lead title so the centroid doesn't
drift toward the tail.

### 2. Pre-filter on title (free)
G2 and G4 read only the posting title. Run them before any network call.

### 3. Fetch
HTTP first, escalate to a real browser only on a JS shell. Prefer canonical ATS
hosts (Greenhouse, Ashby, Lever, Workday, company career sites) over aggregators
— aggregators re-post the same role with thinner text and often no
qualifications block at all.

### 4. Sectionize
Split each JD into `QUALIFICATIONS` and `DUTIES`, discarding benefits, EEO,
compensation, and About-Us.

Qualification headings vary widely. The library covers: Requirements ·
Qualifications (Required / Preferred / Basic / Minimum / Desired) · Must Have ·
Need to Have · Nice to Have · What We're Looking For · We Would Love To Meet You
If · You Might Be a Great Fit If · Who You Are · About You · What You'll Need ·
Ideal Candidate · What You Bring.

**Keep duties even though HHH says to ignore them.** HHH p.9 says duties don't
matter for the resume. That's right for *keyword counting* and wrong for
*bullet writing* — duty language is the raw material for inception (see
`bullet-writer.md`). Count them separately at half weight rather than choosing.

### 5. Gate
G1 → G2 → G3′ → G4 per JD, then G5 across survivors. Record every rejection with
its gate and reason; the rejection list is as informative as the corpus.

### 6. Tally
Document frequency per concept. `demand = qual×2 + duty`. Qualifications count
double because that's the section the screener is actually checking against.

### 7. Enforce the floor
Below 10 → no table, print what's missing and how many more are needed.

## Reading the output

- **Top 5 are robust.** Large effects survive an imperfect corpus.
- **Below ~#5, or demand ≤6, is noise** at n=10–15. Don't build strategy on rank
  ordering down there.
- **A qualification appearing in all families** belongs in the first half of page
  one on every resume (HHH p.27).
- **Duty verbs are not for counting.** They're vocabulary for stage 2.

## Optional output — deriving a job-cycle view

The ranked trait table says WHICH qualifications to prove. It doesn't say WHAT
KIND of activity proves each one — that's a different, complementary view,
rendered by `scripts/chart.py`'s `job_cycle_block()` when a family has an entry
in `JOB_CYCLES`. R1 (Strategy/Business Analyst) has one; other families don't
yet.

A job cycle is a hand-curated sequence of 5–7 stages that most postings in a
family functionally imply, even though no single posting states it as a
checklist. It exists because a trait like "Problem solving" or "Cross-functional
partnering" is an abstraction — a candidate reading it can't immediately picture
what activity would prove it. A stage phrased as "diagnose the real problem, not
what you're told is wrong" is concrete enough to recognize in your own
experience; the trait name alone isn't.

### How to derive one for a new family

1. Read the family's `duties` corpus — the "what you'll do" sections captured
   alongside qualifications (see Procedure above). Look for a recurring
   **functional sequence**, not identical wording — different postings
   describe the same underlying stage in different words.
2. Name each stage as a **verb phrase** ("Diagnose the real problem," not
   "Problem diagnosis"). It should read as something you *did*.
3. Write one or two sentences per stage on what it's *for* — why the step
   exists, what skipping it costs.
4. Map each stage to the **one** trait from the ranked table it most directly
   evidences. A stage maps to a trait, not the reverse — don't force every
   high-demand trait into the cycle if it doesn't correspond to a discrete
   step.
5. **Hand-pick 1–2 real, verbatim quotes per stage. Do not regex-select them.**
   Auto-classifying "which stage does this duty line belong to" is unreliable
   in the same way the qualification lexicon itself needed four rounds of
   false-positive/negative fixes in one session (Stakeholder management missed
   "presented X to the CTO," Communication missed past tense, Leadership missed
   the bare verb "led," Coachability couldn't tell mentoring others from being
   mentored — see `scripts/config.py`'s inline comments for the specifics).
   Detecting *whether* a line contains a concept is hard enough with regex;
   detecting *which step of a multi-stage process* it describes requires
   understanding the line's role in a sequence, which is a different and
   harder problem. Curate by reading.
6. If a trait runs through every stage rather than belonging to one step (R1's
   example: Coachability — being mentored isn't a discrete phase, it's a
   constant background condition across an internship), file it as the cycle's
   **undercurrent** instead of forcing it into the numbered sequence.
7. Add the entry to `JOB_CYCLES` in `scripts/chart.py`, following the existing
   `"R1"` structure exactly. `job_cycle_block()` already renders any family
   with an entry — no code changes needed beyond adding the data. A family
   without an entry gets an explicit "not yet curated" note pointing back here,
   not silence.

## Failure modes seen in practice

| Symptom | Cause | Fix |
|---|---|---|
| Table skews toward one industry's tooling | Corpus drawn from a source tuned to a different goal | Source postings for *this* purpose; don't reuse a job-alert pipeline as a keyword corpus |
| One employer dominates | No concentration cap | G5 |
| Engineering skills rank high in a business family | Title collision — same title, different job | G3′ |
| Senior-role requirements appear in an intern table | No seniority gate | G4 |
| Corpus shrinks unexpectedly | Substring title matching missing morphological variants | Stem comparison |

## A caution on corpus sourcing

A job-discovery pipeline built to surface *openings* is not a keyword corpus.
It's tuned to a person's alert preferences, so its composition reflects those
preferences, not the labor market for a title. Using one as a keyword source
imports its bias wholesale. Source the corpus for this task, and use the
discovery pipeline for what it's good at: applying fast (HHH p.30–32).
