# Sub-skill 2 — Evidence Mapper

**Input:** supplied qualifications (from `qualification-finder`, or handed over
directly) + the master experience inventory.
**Output:** a qualification↔evidence map and a resume-level allocation plan.

Runs *before* any sentence is written. Skipping straight from qualifications to
prose is the most common failure in the whole system.

## The central reframe

A bullet is not a sentence. It is a **compressed argument supported by
evidence**, and the implicit claim is always: *here is evidence I already possess
a qualification this role requires.*

So the opening question is never *how do I make this sound impressive?* It is:

> **Which supplied qualification does this accomplishment prove, and what is the
> strongest evidence inside it?**

## The resume is a portfolio, not a list

Do not optimize bullets independently. If a role wants seven qualifications, the
goal is not seven bullets each proving all seven — it is an allocation where the
*finished page collectively* proves all seven as strongly as possible.

For every candidate bullet ask: **what does this add that the others do not
already prove?** Two individually excellent bullets can be a poor pair.

## Burger vs. Hot Dog

- **Burger** — directly relevant evidence for a supplied qualification.
- **Hot dog** — impressive, but not what this role is measuring.

The test is not *is this impressive?* It is: **does this materially increase the
recruiter's confidence that I can do THIS job?** A spectacular hot dog can
deserve less space than a modest burger.

```
EVIDENCE VALUE ≈ relevance × strength × credibility
                 × specificity × comprehension × differentiation
```

Roughly multiplicative, so any near-zero term sinks the whole bullet: a huge
result with no relevance is weak; perfect relevance with no proof is weak; an
impressive accomplishment nobody understands is weak.

> ⚠️ The automated bullet audit in `scripts/chart.py` measures **relevance
> only** — it regex-matches concepts against bullet text. Treat its output as
> the first term of six, never as evidence value. Strength, credibility,
> specificity, comprehension, and differentiation are judgment calls.

## Classify every accomplishment

| Class | Meaning | Action |
|---|---|---|
| **COMPLETE** | Developed bullet, evidence intact | Ready to allocate |
| **PROMISING BUT INCOMPLETE** | Real accomplishment, missing a key fact | Interrogate before writing |
| **SCRATCHPAD** | Memory placeholder — *"Waddle, Avea"*, *"Add corp relations role"* | Never treat as style; extract the lead |

**Scratchpad entries are not drafts and not a style signal.** They are memory
placeholders. When one appears: establish what's known, why it might matter for
the supplied qualifications, what the highest-value missing facts are — then
ask, then write. Developed bullets are the only reliable evidence of intended
style.

## Phase 1 — Qualification ↔ Evidence map

Do **not** re-derive qualifications if they were supplied. Take them as the
working target.

For each meaningful accomplishment, record: qualifications it could prove ·
strongest relevant signal · strength of evidence · quantified outcome · useful
scale · important stakeholder · mechanism · missing information · redundancy
with other accomplishments.

## Phase 2 — Allocation

Before writing anything, decide:

- Which experiences deserve the most space **for this role**?
- Which supplied qualifications are already strongly covered?
- Which are weakly covered?
- Which accomplishments are redundant with each other?
- Which impressive accomplishments are actually hot dogs?
- Which lesser-known accomplishments are stronger burgers?

Then assign each experience a job, and each bullet inside it a *distinct*
evidentiary job. A worked shape:

```
Experience: <company>
  Bullet 1 → strategic judgment
  Bullet 2 → stakeholder management + executive communication
  Bullet 3 → technical execution + quantified commercial impact
```

**Never keep a bullet just because a previous resume version had it.** Different
target roles allocate space differently.

## Same facts, different resume

Facts stay fixed. Framing changes. One accomplishment legitimately reads several
ways depending on what was supplied:

> 150+ customer interviews → *analytical research and problem diagnosis* ·
> *customer discovery and product sense* · *market validation before
> commercialization*

Reorder and emphasize true facts. Never invent new ones.

## Avoid repeated underlying behaviour

Experience sets accumulate recurring patterns — customer discovery, product
feedback, executive communication, AI automation, engineering coordination. If
every bullet reads *gathered feedback → recommendations → increased X*, the
portfolio proves one thing several times. Assign different evidentiary jobs
deliberately.

## Hand-off

Output of this sub-skill, per experience: the qualifications it should prove,
the ranked accomplishments, the missing facts worth asking about, the
recommended bullet count, and each bullet's assigned job. That is the input to
`bullet-creator.md`.
