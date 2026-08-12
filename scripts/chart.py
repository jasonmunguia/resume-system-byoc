"""Emit the per-family chart: traits to prove, tools to list, duty language.

This is the artifact a person actually writes from. The raw demand ranking is an
intermediate; this splits it by how each qualification gets SPENT on the page.
"""
import json, os, re, sys, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import LEXICON, KIND, ANCHORS, FAMILIES
from pipeline import COMPILED

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

# Master experience inventory lives in context/ — see scripts/context.py for the
# BYOC boundary. Only COMPLETE bullets are auditable; incomplete and scratchpad
# entries are leads, and scoring them would report a placeholder as coverage.
import context as _ctx

BULLETS = _ctx.load_inventory()


def audit_bullets():
    """Which qualification(s) each bullet currently signals."""
    rows, cover = [], collections.Counter()
    for org, b in BULLETS:
        hits = [k for k, rx in COMPILED.items() if rx.search(b)]
        rows.append((org, b, hits))
        for h in hits:
            cover[h] += 1
    return rows, cover


def chart(rep, cover, top=16):
    fam, L = rep["family"], []
    L.append(f"### {rep['family']} — {rep['name']}")
    if not rep["sufficient"]:
        L += ["", f"> ⚠️ {rep['message']}", ""]
        return "\n".join(L)
    n = rep["n"]
    lead = sum(1 for k in rep["kept"] if k["lead"])
    L += ["", f"*({n} JDs across {rep.get('employers', '?')} employers · lead title "
          f"**`{rep['lead']}`**, {lead} of {n}, weighted 2\u00d7)*", ""]
    if rep.get("narrow"):
        L += [f"> \u26a0\ufe0f Only {rep['employers']} distinct employers — treat the ordering "
              f"as indicative. One firm's house style carries more weight than it should.", ""]

    srcs = ", ".join(f"{d['company']} {d['title'][:34]}" for d in rep.get("duties", [])[:5])
    if srcs:
        L += [f"*Duty language from: {srcs}*", ""]

    tbl = rep["table"]

    # A duty sentence usually satisfies several regexes ("collaborative
    # partnerships ... align on priorities and execution" hits teamwork,
    # prioritization, leadership and bias-for-action). Quoting it four times
    # makes the table look full while carrying one sentence of information, so
    # each line is spent once — claimed by the highest-demand trait, since
    # rows are walked in demand order.
    used_lines = set()

    def their_words(concept, limit=2):
        """Duty lines from the corpus that carry this concept, attributed.

        Auto-matched rather than hand-picked: the same regex that scores the
        concept selects the sentences, so column 2 can never drift from the
        ranking in column 1."""
        rx = COMPILED[concept]
        picks = []
        for d in rep.get("duties", []):
            for line in d["lines"]:
                key = line.strip()[:80]
                if key in used_lines or not rx.search(line):
                    continue
                used_lines.add(key)
                txt = line.strip().rstrip(".")
                if len(txt) > 155:
                    txt = txt[:152].rsplit(" ", 1)[0] + "…"
                picks.append(f'{d["company"]}: *"{txt}"*')
                break
            if len(picks) >= limit:
                break
        return " · ".join(picks)

    def mine(concept, limit=1):
        """Bullets already carrying this concept — the inception starting point."""
        out = []
        for org, b in BULLETS:
            if COMPILED[concept].search(b):
                frag = b[:110].rsplit(" ", 1)[0] + "…"
                out.append(f"**{org}**: {frag}")
            if len(out) >= limit:
                break
        return " · ".join(out)

    def block(kind, header, note):
        rows = [(k, v) for k, v in tbl.items()
                if KIND.get(k) == kind and v["demand"] > 0][:top]
        if not rows:
            return []
        out = ["", f"#### {header}", ""]
        if note:
            out += [f"*{note}*", ""]
        out += ["| Trait / Qualification | Their day-to-day, their words | Your inception mirror |",
                "|---|---|---|"]
        for k, v in rows:
            star = "⭐" if k in ANCHORS else ""
            c = cover.get(k, 0)
            state = "**GAP**" if c == 0 else (f"×{c}" + (" over" if c >= 4 else ""))
            theirs = their_words(k) or "*(not phrased as a duty in this corpus)*"
            ours = mine(k) or "— **write this one**"
            out.append(f"| **{k}**{star}<br>*({v['demand']}, {state})* | {theirs} | {ours} |")
        return out + [""]

    L += block("trait", "Traits / Qualifications to prove — one per bullet",
               "⭐ = anchor trait (context/anchors.json) · format: (demand, your coverage) · "
               "rule: their noun, your number")
    L += block("domain", "Domain signal — prove in a bullet, this family only", "")
    L += block("tool", "Hard qualifications — Skills line only",
               "Earns a bullet only if the bullet shows it doing something (HHH p.24)")
    return "\n".join(L)


if __name__ == "__main__":
    reports = json.load(open(os.path.join(DATA, "_report.json")))
    rows, cover = audit_bullets()
    out = []
    # A high match count is a PROMPT to check for a dominant signal, not a
    # verdict. The rule is one primary signal per bullet, not one detectable
    # concept — secondary signals are fine when they don't dilute the primary.
    # Regex matching cannot see dominance, so the label must not claim it does.
    many = [(o, h) for o, b, h in rows if len(h) > 2]
    blank = [o for o, b, h in rows if not h]
    out.append(f"*Bullet audit: {len(BULLETS)} bullets · {len(many)} match 3+ concepts "
               f"(check each has a dominant signal) · {len(blank)} signalling nothing · "
               f"relevance only — 1 of 6 evidence-value terms*\n")
    for fam in FAMILIES:            # whatever families context defines, not a fixed three
        if fam in reports:
            out.append(chart(reports[fam], cover))
    md = "\n\n---\n\n".join(out)
    p = os.path.join(DATA, "charts.md")
    open(p, "w").write(md)
    print(md)
