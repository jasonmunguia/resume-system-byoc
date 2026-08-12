"""The five gates a JD must pass before it may influence a keyword table.

Design rule: no gate models the CANDIDATE. Every gate filters on the JOB.
An earlier draft gated on "does the candidate meet 75% of these qualifications" (HHH
p.11) and that was circular — it filtered the input by the current resume, so
qualifications he has done but never written down would read as "not required"
instead of surfacing as gaps. Cut deliberately. Do not reintroduce it.
"""
import re
import json, os
from config import (FAMILIES, MAX_CONCENTRATION, TARGET_COMPANIES,
                    REPUTABLE_COMPANIES, DENY_COMPANIES, TIER_FILE)

# ---------------------------------------------------------------------------
# Stemming — so "Project Manager" on the whitelist matches "Project Management"
# in a posting title. A real stemmer (Porter) is overkill and drags a dependency
# in for ~25 whitelist entries; this handles the suffixes that actually collide
# in job titles.
# ---------------------------------------------------------------------------
_SUFFIXES = ("ements", "ement", "ments", "ment", "ings", "ing", "ions", "ion",
             "ants", "ant", "ers", "er", "ors", "or", "als", "al", "ics", "ic",
             "es", "s", "y")

def stem(word):
    """Reduce a word to a comparison stem. manager/management -> manag."""
    w = re.sub(r"[^a-z]", "", word.lower())
    changed = True
    while changed and len(w) > 4:
        changed = False
        for suf in _SUFFIXES:
            if w.endswith(suf) and len(w) - len(suf) >= 4:
                w = w[: -len(suf)]
                changed = True
                break
    return w.rstrip("e") if len(w) > 4 else w

def _stems(text):
    return [stem(t) for t in re.split(r"[^A-Za-z]+", text) if t]


# ---------------------------------------------------------------------------
# G1 — Good JD (HHH p.10): must carry a qualifications block.
# ---------------------------------------------------------------------------
def g1_good_jd(sections):
    if not sections.get("qual"):
        return False, "no qualifications/requirements block"
    return True, ""


# ---------------------------------------------------------------------------
# G2 — Title belongs to the family's whitelist, compared on stems.
# ---------------------------------------------------------------------------
def g2_title_in_family(title, fam):
    tstems = _stems(title)
    for entry in FAMILIES[fam]["titles"]:
        estems = _stems(entry)
        if estems and all(e in tstems for e in estems):
            return True, ""
    return False, f"title not in {fam} whitelist"


# ---------------------------------------------------------------------------
# G3' — Role nature. Rejects engineering IC roles wearing a business title
# (e.g. a "Special Projects Intern" whose duties are "write and maintain
# software that drives robot demonstrations"). Filters the job, not the person.
# ---------------------------------------------------------------------------
_ENG = re.compile(
    r"\bC\+\+|\bC#\b|\bJava\b|\bGolang\b|\bRust\b|\bCAD\b|SolidWorks|"
    r"firmware|embedded|PCB|circuit|soldering|mechanical engineering|"
    r"electrical engineering|control (?:logic|systems)|kinematic|"
    r"write and maintain software|software development life|algorithms and data|"
    r"computer science degree|degree in computer science|unit tests?\b|"
    r"CI/CD|kubernetes|docker\b", re.I)

_BIZ = re.compile(
    r"business|stakeholder|client|customer|strateg|market|revenue|"
    r"presentation|communicat|analys[ie]s|operations|commercial", re.I)

def g3_role_nature(sections, min_eng_hits=3):
    blob = " ".join(sections.get("qual", []) + sections.get("duty", []))
    eng = len(set(m.group(0).lower() for m in _ENG.finditer(blob)))
    biz = len(set(m.group(0).lower() for m in _BIZ.finditer(blob)))
    if eng >= min_eng_hits and eng > biz:
        return False, f"engineering IC role ({eng} eng vs {biz} biz markers)"
    return True, ""


# ---------------------------------------------------------------------------
# G4 — Seniority. Intern / co-op / new-grad only. A senior full-time JD asks
# for years of experience and P&L ownership; its qualifications would poison an
# intern keyword table.
# ---------------------------------------------------------------------------
_INTERN = re.compile(
    r"\bintern(?:ship)?\b|\bco-?op\b|new ?grad|university (?:program|recruit)|"
    r"campus|summer (?:analyst|associate)|fellowship|rotational|apprentice", re.I)

def g4_seniority(title, sections=None):
    if _INTERN.search(title):
        return True, ""
    blob = " ".join((sections or {}).get("qual", []))[:2000]
    if _INTERN.search(blob):
        return True, ""
    return False, "not an intern/co-op/new-grad posting"


# ---------------------------------------------------------------------------
# G5 — Concentration. Corpus-level, not per-JD. No single company may exceed
# MAX_CONCENTRATION of a family's corpus, so one employer's house style cannot
# masquerade as an industry pattern (Palantir was 25% of R3 in the v0 run).
# ---------------------------------------------------------------------------
def g5_concentration(docs, max_share=MAX_CONCENTRATION):
    """Trim to the cap. Cap is computed from the INPUT size and applied in one
    pass — iterating to a fixed point would shrink the corpus below the floor
    for small n, which costs more than the residual concentration."""
    if not docs:
        return [], []
    cap = max(1, int(len(docs) * max_share))
    kept, dropped, seen = [], [], {}
    for d in docs:
        c = d.get("company", "").strip().lower()
        seen[c] = seen.get(c, 0) + 1
        if seen[c] <= cap:
            kept.append(d)
        else:
            dropped.append((d, f"company over {max_share:.0%} cap (>{cap})"))
    return kept, dropped


# ---------------------------------------------------------------------------
# G6 - Segment floor. Optional (off unless enabled) because it is the one gate
# that encodes ambition rather than correctness: it asks "is this the kind of
# employer I am aiming at", which is a strategy choice, not a data-quality one.
# ---------------------------------------------------------------------------
def _load_tiers():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), TIER_FILE)  # legacy path
    if os.path.exists(p):
        try:
            return {k.lower() for k in json.load(open(p))}
        except Exception:
            return set()
    return set()

def _norm_co(name):
    """Company name -> token list, with legal/corporate suffixes stripped."""
    n = re.sub(r"[^a-z0-9 ]", " ", (name or "").lower())
    drop = {"inc", "llc", "ltd", "corp", "corporation", "company", "co",
            "group", "holdings", "technologies", "technology", "industries",
            "labs", "the", "and"}
    return [t for t in n.split() if t and t not in drop]


def g6_segment(company, allow=None, min_tier="reputable"):
    """Token-boundary match, NOT substring.

    Substring matching let 'meta' match 'AA Metals' and 'Metalinked', and
    'blackrock' match 'Blackrock Neurotech' — three long-tail companies admitted
    into a target-tier corpus by the one gate that exists to keep them out. An
    allowlist entry must match whole tokens: multi-word entries need all their
    tokens present, single-word entries need an exact token."""
    if allow is None:
        allow = TARGET_COMPANIES | _load_tiers()
        if min_tier == "reputable":
            allow = allow | REPUTABLE_COMPANIES
    if " ".join(_norm_co(company)) in {" ".join(_norm_co(d)) for d in DENY_COMPANIES}:
        return False, "name collides with a target-tier employer; different company"
    toks = _norm_co(company)
    if not toks:
        return False, "company below segment floor (not a target-tier employer)"
    tokset = set(toks)
    for entry in allow:
        etoks = _norm_co(entry)
        if not etoks:
            continue
        if all(e in tokset for e in etoks):
            return True, ""
    return False, "company below segment floor (not a target-tier employer)"


GATES_PER_JD = [
    ("G1 good-jd",   lambda d, fam: g1_good_jd(d["sections"])),
    ("G2 title",     lambda d, fam: g2_title_in_family(d["title"], fam)),
    ("G3 role",      lambda d, fam: g3_role_nature(d["sections"])),
    ("G4 seniority", lambda d, fam: g4_seniority(d["title"], d["sections"])),
]

def apply_gates(docs, fam, segment_floor=False):
    """Run G1-G4 (plus optional G6) per JD, then G5 across the survivors.
    Returns (kept, [(doc, gate_name, reason), ...])."""
    gates = list(GATES_PER_JD)
    if segment_floor:
        gates.append(("G6 segment", lambda d, fam: g6_segment(d.get("company"))))
    kept, rejected = [], []
    for d in docs:
        for name, fn in gates:
            ok, why = fn(d, fam)
            if not ok:
                rejected.append((d, name, why))
                break
        else:
            kept.append(d)
    kept, over = g5_concentration(kept)
    rejected += [(d, "G5 concentration", why) for d, why in over]
    return kept, rejected
