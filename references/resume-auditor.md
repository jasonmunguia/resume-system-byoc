# Sub-skill 4 — Resume Auditor

**Input:** the finished tailored resume + the supplied qualifications.
**Output:** a coverage verdict and a ranked keep/cut list.

Runs once every experience is complete. Audits against **only the supplied
qualifications** — not against general resume advice, and not against what would
be impressive in the abstract.

## The eight checks

**1. Qualification coverage.** For every supplied qualification: where is it
proven, how strong is that evidence, is it repeated more than it needs to be, is
there a gap?

**2. Burger / hot dog.** Which bullets are role-relevant evidence, and which
occupy space mainly because they are impressive?

**3. Stranger audit.** Which bullets still require insider knowledge for a
critical causal link?

**4. Redundancy.** Where does the page prove the same thing more than once? Two
strong bullets proving one qualification is a worse portfolio than two adequate
bullets proving two.

**5. Impact density.** Which bullets consume page space out of proportion to
their evidence value?

**6. Role narrative.** After a 20-second read, what kind of candidate does the
reader believe this is — and does that match the supplied role? This is the check
that catches a resume every individual bullet passes.

**7. Weak links.** Which supplied qualification is least convincingly proven?
That is the next thing to fix.

**8. Bullet ranking.** Every bullet gets exactly one label:

| Label | Meaning |
|---|---|
| **ESSENTIAL** | Proves a top qualification, nothing else proves it as well |
| **STRONG** | Proves a real qualification with credible evidence |
| **REPLACEABLE** | Adequate, but a better burger exists in the inventory |
| **REMOVE** | Hot dog, redundant, or fails the stranger test |

## Coverage table

Report as a grid, not prose:

```
| Supplied qualification | Proven where | Strength | Verdict |
|---|---|---|---|
| Stakeholder management | Northwind b2, Meridian b3 | strong | covered |
| Problem solving        | —                      | none   | GAP    |
| Teamwork               | Kestrel b1 (implicit)   | weak   | thin   |
```

Three verdicts only: **covered · thin · GAP**. A qualification proven only
implicitly is *thin*, not covered — screeners do not infer.

## The role-narrative check, expanded

The single most useful question in the audit, because it is invisible at the
bullet level:

> Read only the finished page. Describe the candidate in one sentence. Now read
> the supplied qualifications. Do they describe the same person?

A measured example from this system's own first run: a resume where **8 of 14
bullets carried sales/GTM signal** read as a GTM candidate — while the target
family's qualification blocks mentioned sales/GTM near the bottom of the ranking.
Every bullet was individually good. The portfolio was aimed at a different job.

## Automated support and its limits

`scripts/chart.py` runs the mechanical part: which concepts each bullet matches,
which supplied qualifications have zero bullets, which are over-covered, and
which bullets carry no dominant signal.

> ⚠️ It measures **relevance only** — one of the six terms in evidence value.
> Strength, credibility, specificity, comprehension, and differentiation are
> human judgment. A bullet the script marks "covered" can still be thin under
> the stranger test. Never report the script's output as the audit.

## Output contract

1. Coverage table (covered / thin / GAP per supplied qualification)
2. Bullet ranking (ESSENTIAL / STRONG / REPLACEABLE / REMOVE)
3. Weakest link and the specific next action
4. Role-narrative verdict in one sentence
