# Resume System — keyword corpus → assigned bullets

Self-contained. Paste into any assistant to give it this capability. No scripts
required; everything below is executable by hand or by code.

---

## What this replaces

Writing resume bullets from memory. Memory optimizes for what you remember
doing; screeners select on what they were told to look for. Those diverge. In
the first real run of this system the candidate's resume spent **8 of 14 bullets
on Sales/GTM signal**, and Sales/GTM appeared in **0 of 10** Strategy/Business
Analyst qualification blocks — an entire resume aimed slightly off-target,
invisible without counting.

## Four stages

1. **qualification-finder** — measure what a job family actually screens on.
2. **evidence-mapper** — match a master experience inventory to those qualifications and allocate evidence across the page.
3. **bullet-creator** — write each bullet with the architecture that surfaces its strongest relevant signal.
4. **resume-auditor** — audit the finished page against the supplied qualifications.

**Stage 1 is skippable. Stage 2 is not.** If qualifications are supplied — a
competency map, hiring-signal list, or parsed JD — take them as the working
target and start at stage 2. Do not re-derive them. But never jump from
qualifications straight to prose.

## The core rule

The resume does not answer *"what are the coolest things I've done?"*

It answers: **"what concrete evidence most efficiently proves I already
demonstrate the behaviors this employer is trying to hire?"**

---

# Stage 1 — qualification-finder

## Definitions

- **Family** — the set of job titles one resume will serve. Give each a **lead
  title**: the one you'll mass-apply to. Lead-title JDs count **2×**.
- **Good JD** — a posting containing an actual Qualifications/Requirements
  section. Postings without one are unusable.
- **Document frequency** — how many JDs mention a concept. *Not* raw mentions. A
  JD saying "stakeholder" six times is one JD asking for stakeholder management.

## Corpus rules

- **10–15 qualifying JDs per family.** 10 is a hard floor.
- **Source the corpus for this task.** A job-alert pipeline built to surface
  *openings* is tuned to someone's alert preferences, not to the labor market for
  a title. Reusing one as a keyword corpus imports its bias wholesale.
- **Prefer canonical postings** (Greenhouse, Ashby, Lever, Workday, company
  career pages) over aggregators, which re-post thinner text and often drop the
  qualifications block entirely.

## The six gates

Every gate judges **the job**, never the candidate. G2 and G4 need only the
title — run them before fetching anything.

| Gate | Rule | Catches |
|---|---|---|
| **G1** Good-JD | Has a Qualifications/Requirements block | All-marketing postings |
| **G2** Title-in-family | Title matches family whitelist, compared on **stems** | "Member Experience Intern" filed under GTM |
| **G3′** Role-nature | Qualifications not majority hard-engineering IC | "Special Projects Intern" whose duties are robotics software |
| **G4** Seniority | Intern / co-op / new-grad only | Senior JDs whose "8 years experience" poisons an intern table |
| **G5** Concentration | No single company >20% of the corpus | One employer's house style read as an industry pattern |
| **G6** Segment floor *(opt-in)* | Company clears a target-tier allowlist, matched on **whole tokens** | Long-tail employers padding a corpus up to the floor |

**On G6 — aim high, miss low.** A resume built to satisfy the hardest employers
clears the easier ones with minor tweaking; the reverse never happens. So when
the goal is top-tier roles, the target-tier corpus is the BASE, not a tailoring
layer. It stays opt-in because it encodes ambition rather than correctness.

Match on whole tokens, never substrings: `meta` otherwise matches *AA Metals* and
*Metalinked*, `blackrock` matches *Blackrock Neurotech*. Distinct companies that
genuinely share a name need an explicit denylist — no string rule separates
BlackRock the asset manager from Blackrock Neurotech.

**Stem, don't substring.** A whitelist entry `project manager` must match a
posting titled `Technical Project Management Intern`. Collapse: manager/management,
operations/operational, strategy/strategic, consulting/consultant,
development/developer, solutions/solution.

### The gate that was cut, and why

An earlier version included HHH's rule: *only use JDs you meet 75% of the
qualifications for.* **Remove it.** It filters the input by the current resume,
so qualifications the candidate has done but never written down read as "not
required" rather than surfacing as gaps. It suppresses precisely what the system
exists to find. Any gate that references the candidate is the same bug wearing a
different name.

## The HHH qualification skeleton

The Business Analyst Intern example is **canonical**. Do not rewrite it; read the
pattern off it and apply that pattern to new roles.

> - Degree
> - Basic knowledge of (Tableau, Power BI, communicate and influence, Microsoft
>   Windows and Office, including Word, PowerPoint, Advanced Excel, and Outlook),
>   Deadlines, and organizational skills.
> - Ability to work with others
> - Takes direction and criticism

Four bullets; only one is about the job.

| # | Bucket | Function | Varies by role? |
|---|---|---|---|
| 1 | Credential — Degree | Threshold check | No |
| 2 | Tool stack + core ability + self-management | The actual role | **Yes — the only one that swaps** |
| 3 | Collaboration — works with others | Risk removal | No |
| 4 | Coachability — takes direction and criticism | Risk removal | No |

**Three of four bullets are risk removal.** For an intern requisition the manager
is not asking *is this person exceptional* — they are asking *will this be a bad
hire*, and would rather hire nobody than badly. Derive a new role by holding 1,
3, 4 fixed and swapping only bucket 2's tool stack and core ability:

- BA → *communicate and influence*
- PM → *prioritize and influence without authority* (Jira, roadmapping, SQL, dashboards)
- GTM → *communicate value and handle objections* (CRM, prospecting tools)

**Measurement ranks capability; the skeleton ranks risk.** Coachability scores
demand 2–4 in every measured corpus because JDs rarely write it down — yet HHH
gives it a quarter of the canonical list. Where the two disagree on a
risk-removal bucket, the skeleton wins: postings under-state what everyone
assumes.

## Sectioning

Split each JD into **QUALIFICATIONS** and **DUTIES**; discard benefits, EEO,
compensation, About-Us, perks, legal.

Qualification headings to recognize: Requirements · Qualifications (Required /
Preferred / Basic / Minimum / Desired) · Must Have · Need to Have · Nice to Have ·
What We're Looking For · We Would Love To Meet You If · You Might Be a Great Fit
If · Who You Are · About You · What You'll Need · Ideal Candidate · What You Bring.

Duty headings: What You'll Do · Responsibilities · The Role · Your Impact ·
Day-to-Day · In This Role · A Day in the Life · You Will.

**Keep duties.** Counting-wise they're weak signal — but they are the raw
vocabulary for inception in stage 2. Count them at half weight rather than
discarding.

## Scoring

```
demand = (qualification_frequency × 2) + duty_frequency
```
Qualifications count double: that's the section the screener checks against.

## The floor

Below 10 qualifying JDs, output exactly this and **no ranked table**:

```
INSUFFICIENT CORPUS: n=<X>, floor=10. Need <Y> more qualifying JDs.
```

A table built from 6 JDs is visually identical to one built from 15. That is the
failure a reader cannot catch by reading. Never round a thin corpus up.

## Reading the result

- Top ~5 are robust — large effects survive an imperfect corpus.
- Below ~#5, or demand ≤6, is noise at n=10–15. Don't build strategy there.
- A qualification ranking high in *every* family belongs in the first half of
  page one on all resumes.
- Always ship the corpus list and the rejection list with the table. A number
  without provenance can't be audited.

## Qualification lexicon

Concept → phrasings to match (case-insensitive regex).

```
Communication (written & verbal)   communicat|verbal and written|articulate|present(ing)? to
Stakeholder management             stakeholder|senior leader|executive (audience|presence)|client relationship|C-suite
Influence / persuasion             influenc|persuas|buy-in|drive alignment|build consensus|negotiat
Analytical skills                  analytical|analysis|analyz|quantitative|data-driven
Problem solving                    problem-solv|solve complex|structured thinking|first principles|troubleshoot
Leadership / initiative            leadership|self-start|take initiative|ownership|owner mentality|player-coach
Teamwork / collaboration           teamwork|collaborat|work (well )?(with|across) (others|teams)|team player
Excel / spreadsheet modeling       excel|spreadsheet|pivot table|vlookup|financial model
SQL                                sql|relational database|querying
Python / scripting                 python|scripting
Data visualization                 tableau|power ?bi|looker|data visuali[sz]|dashboard
PowerPoint / storytelling          powerpoint|slide|deck|presentation skills|storytell|narrative
AI / LLM fluency                   \bAI\b|LLM|generative ai|machine learning|prompt engineering
Cross-functional partnering        cross-functional|partner with (engineering|sales|product|design)|matrix
Ambiguity / fast-paced             ambigu|fast-paced|rapidly changing|scrappy|startup environment|calm under pressure
Prioritization / time management   priorit|time management|competing (demands|priorities)|manage multiple|deadline
Attention to detail                attention to detail|detail-oriented|meticulous|accuracy|rigor
Project / program management       project manage|program manage|PMP|scrum|agile|sprint|roadmap|backlog
Process improvement                process improv|continuous improv|operational excellence|six sigma|lean|streamlin|efficien
Metrics / KPIs                     KPI|metric|measur(e|ing) (success|impact)|OKR|key results
Business acumen / strategy         business acumen|commercial acumen|business strategy|strategic thinking|market (analysis|research)
Customer / client-facing           customer-facing|client-facing|customer success|voice of the customer|user research|customer obsess
Curiosity / learning agility       curious|curiosity|eager to learn|learning agility|growth mindset|intellectual
Bias for action / results          bias for action|results-(driven|oriented)|deliver results|get things done|execution
Written documentation              document(ation)?|write (clear|concise)|technical writing|memo|spec(ification)?s
Financial / P&L                    P&L|forecast|budget|revenue|pricing|unit economics|financial analysis
Supply chain / logistics           supply chain|logistics|procure|inventory|vendor|supplier|sourcing
Sales / pipeline / GTM             sales|pipeline|quota|prospect|lead gen|go-to-market|GTM|business development
Product sense / user empathy       product sense|user (empathy|needs)|customer problem|product intuition|user experience
Technical aptitude                 technical (aptitude|background|concepts|specification)|engineering (background|team)|API
Coachability                       takes? (direction|feedback)|receptive to feedback|open to criticism|mentorship|coachab
```

Extend per domain. Keep concepts at the level a bullet can prove — "Excel" is
provable, "excellence" is not.

---

# Stage 2 — evidence-mapper

## A bullet is a compressed argument

Not a sentence. The implicit claim is always: *here is evidence I already possess
a qualification this role requires.* So the opening question is never *how do I
make this sound impressive?* but **which supplied qualification does this prove,
and what is the strongest evidence inside it?**

## The resume is a portfolio, not a list

Do not optimize bullets independently. If a role wants seven qualifications, the
goal is not seven bullets each proving all seven — it is an allocation where the
finished page *collectively* proves all seven. For every bullet ask: **what does
this add that the others do not already prove?** Two excellent bullets can be a
poor pair.

## Burger vs. Hot Dog

- **Burger** — directly relevant evidence for a supplied qualification.
- **Hot dog** — impressive, but not what this role measures.

Not *is this impressive?* but **does this materially increase the recruiter's
confidence that I can do THIS job?** A spectacular hot dog can deserve less space
than a modest burger.

```
EVIDENCE VALUE ≈ relevance × strength × credibility
                 × specificity × comprehension × differentiation
```

Roughly multiplicative, so any near-zero term sinks the bullet: a huge result
with no relevance is weak; perfect relevance with no proof is weak; an impressive
accomplishment nobody understands is weak.

## Three evidence states — not interchangeable

| State | Meaning | Action |
|---|---|---|
| **COMPLETE** | Developed bullet, evidence intact | Ready to allocate |
| **PROMISING BUT INCOMPLETE** | Real accomplishment, missing a key fact | Interrogate before writing |
| **SCRATCHPAD** | Memory placeholder — *"Waddle, Avea"* | Extract the lead; never a style signal |

Scratchpad fragments are not drafts. Establish what is known, why it might matter
for the supplied qualifications, what facts are missing — then ask, then write.

## Allocation

Before writing anything: which experiences deserve space *for this role*? Which
qualifications are already strongly covered, which weakly? Which accomplishments
are redundant? Which impressive ones are hot dogs? Which obscure ones are strong
burgers?

Then give each experience a job and each bullet inside it a **distinct**
evidentiary job:

```
Experience: <company>
  Bullet 1 → strategic judgment
  Bullet 2 → stakeholder management + executive communication
  Bullet 3 → technical execution + quantified commercial impact
```

Never keep a bullet just because a previous resume version had it.

## Same facts, different resume

Facts stay fixed; framing changes. *150+ customer interviews* legitimately reads
as analytical research, or customer discovery, or market validation — depending
on what was supplied. Reorder and emphasize true facts. Never invent new ones.

---

# Stage 3 — bullet-creator

Work **one experience at a time**. Never regenerate a whole resume in one pass.

## Primary signal

Name the **PRIMARY SIGNAL** (the one thing the reader should remember) and any
**SECONDARY SIGNALS** that ride along without diluting it. This sets word order —
first words are premium real estate.

> The rule is one *purpose*, not one detectable concept. A bullet may evidence
> several qualifications if one clearly dominates. The failure mode is a bullet
> with **no dominant signal** — three things half-proven.

## Content components

Ownership · Action · Insight · Mechanism · Scale · Stakeholder · Artifact ·
Decision · Outcome · Purpose/Function. Pick a subset; no bullet needs all.

## There is no universal formula

Do not enforce *always lead with the metric* or any single template. Architecture
follows evidence. Uniform reasoning is the goal; uniform syntax is not — variation
strengthens a page because different bullets surface different evidence types.

**1 — Result first.** `RESULT → HOW/WHY → SCALE`
When the metric is exceptional, maps directly to the qualification, reads
instantly, and causality is defensible. Do not result-front merely because a
number exists.

**2 — Ownership / trust first.** `OWNED X → SCOPE/STAKEHOLDER → ACTION → OUTCOME`
When what you were entrusted with is itself the evidence: senior responsibility,
stakeholder caliber, decision authority. For a stakeholder qualification this can
beat leading with the metric.

**3 — Build / artifact first.** `BUILT X → WHAT IT DID → HOW USED → OUTCOME`
For technical fluency, analytics, automation, product, data. Never stop at *"built
an AI system that does X"* — who used it, at what scale, what changed?

**4 — Insight / diagnosis first.** `IDENTIFIED X → EVIDENCE → ACTION → OUTCOME`
For strategy, problem solving, product sense, ambiguity. Says *I determined what
should be done*, not *I executed instructions*.

**5 — Execution / deal first.** `NEGOTIATED/CLOSED/LAUNCHED → WITH WHOM → HOW → OUTCOME`
For GTM, sales, BD, partnerships, deployment, commercialization.

**Selection rule:** whichever is strongest *and* most relevant leads.

## Mechanism usually earns its space

> "Raised $550K." — proves outcome.
> "Raised $550K after identifying a stronger use case, validating demand through
> 150+ prospective-customer interviews, and influencing a product pivot." — also
> proves research, analysis, customer discovery, judgment, influence.

Ask: does explaining *how* add evidence for a supplied qualification? If yes,
keep it.

## Function vs. intent vs. outcome

**Function** (what it actually did) is often essential to comprehension.
**Intent** alone is weak — *"built AI system to increase sales"* states a goal.
**Outcome** is strongest — *"...increasing sales 15%."*

Include purpose when it makes the mechanism understandable, proves a
qualification, or explains why an obscure action mattered.

## Activity is not automatically evidence

Calls, meetings, emails, decks, workshops are usually *channels*. Compress unless
the channel proves the qualification. Related: *"created a PowerPoint"* is an
artifact; *"presented recommendations that changed a decision"* is organizational
influence.

## The four tests

**Stranger Test.** Must land for a reader who never met you, never heard of the
company, doesn't know the product or internal vocabulary, and is scanning. They
should get: what you did · what you owned · the problem · scale and with whom ·
how · what decision changed · the result · why it matters. **No critical causal
link may depend on insider knowledge.**
*Do not over-correct* — if the header reads **Northwind — AI Video Intelligence
Startup**, write *"trained their teams"*, not *"trained their teams on Northwind"*.
Sufficient information, not redundant information.

**Causality Test.** Direct attribution: *increased, reduced, generated, closed,
cut, tripled*. Shared or indirect: *contributed to, helped drive, supported,
informed*. Truth that survives an interview beats a verb that collapses.

**Personal-Ownership Test.** Separate company outcome, team outcome, your
contribution. Don't imply sole ownership of a team result; don't weaken real
ownership with *"helped"*. Strongest accurate claim.

**Interview-Defensibility Test.** Survives: *What exactly did you do? How? What
made it difficult? How was the metric calculated? How much is attributable to
you? Who decided? Why did it work? What alternatives were considered?*

## Metrics

Pick the metric that best proves the *supplied qualification* — do not reflexively
prefer revenue. Commercial · Operations · Product · Technical · People/scale.

## Mirror concepts, not labels

**Mirror their action vocabulary, never their trait vocabulary.**
*"Scoped engagements in new industries"* — their verb-noun for something you did ✅
*"Demonstrated stakeholder management"* — their label for a trait ❌
**Their noun, your number; never their adjective.**

Translate terminology only when it describes the same thing. Determine what a
*"product refinement memo"* actually contained before renaming it a *spec*.

## Ask before writing around a gap

If an accomplishment looks relevant but incomplete, interrogate it. Ask only what
materially improves relevance, evidence, specificity, credibility, scale,
mechanism, or impact: *What changed afterward? Who used it, how many? Who was the
decision maker? What was your personal role? How was the metric measured? What
decision did your analysis change?*

## Compression order

1. low-value procedural channels · 2. context the header already supplies ·
3. filler adjectives · 4. repeated explanations · 5. connectors (*"then"*) ·
6. excess company examples · 7. secondary mechanism · 8. secondary signal

Preserve: primary evidence · primary signal · causal mechanism · important scale ·
decision maker · outcome · stranger comprehension · **grammar**. Never produce
malformed English to save a line.

## Showing drafts

No synonym variants. Alternatives only on a real strategic tradeoff — *Version A
leads with revenue because the commercial result is strongest; Version B leads
with Fortune 500 ownership because the stakeholder qualification is strongest.*
Explain the tradeoff, then recommend one.

## Voice

The strongest bullets read like **miniature causal case studies**: what I did +
how it worked + who/what scale + what decision changed + measurable result. The
characteristic is **high information density, visible causality, personal
agency** — not a rigid formula. **Role relevance outranks persona.**

---

# Stage 4 — resume-auditor

Audit against **only the supplied qualifications**.

**1. Coverage.** Per qualification: proven where, how strongly, over-repeated, or
missing?
**2. Burger / hot dog.** Which bullets earn their space by relevance?
**3. Stranger audit.** Which still need insider knowledge?
**4. Redundancy.** Where is the same thing proven twice?
**5. Impact density.** Which bullets cost more space than their evidence value?
**6. Role narrative.** After a 20-second read, what candidate does the reader
believe this is — and does it match the role? *This is the check that catches a
resume every individual bullet passes.*
**7. Weak links.** Which qualification is least convincingly proven?
**8. Bullet ranking.** ESSENTIAL · STRONG · REPLACEABLE · REMOVE

Report coverage as a grid with three verdicts only — **covered · thin · GAP**. A
qualification proven only implicitly is *thin*: screeners do not infer.

# Method vs. formatting

This method derives from *How to Get a Job* (the Headless Headhunter).

**Take the method, not the formatting.** HHH mandates Arial, 1.5 line spacing,
and permits multiple pages — guidance aimed at **corporate mass-apply**:
recruiter-screened job boards, first-come-first-served in the applicant tracking
system. **Campus recruiting and consulting/APM programs are a different funnel**
— GPA screens, resume drops, cohort comparison, often read by an alum of your own
school.

A dense one-page resume that already produces interviews should not be
reformatted to satisfy a rulebook written for another channel. That introduces a
variable you can't attribute if results drop.

Keep from HHH: keyword harvesting, What/How/Result bullets, and apply-fast —
most applicant tracking systems sort by application order, so speed is a real
edge.

# Non-negotiables

1. Below the floor, emit no ranked table.
2. No gate may model the candidate.
3. Count documents, not mentions.
4. One PRIMARY signal per bullet — one purpose, not one detectable concept.
5. Measurement ranks capability; the HHH skeleton ranks risk.
6. Ship the corpus and rejection list with every table.
7. Optimize the portfolio, never the bullet in isolation.
8. Ask for missing facts; never write around them.
9. One experience at a time — allocation decisions belong to the person.
