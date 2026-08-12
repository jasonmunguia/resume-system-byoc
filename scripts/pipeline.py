"""Fetch -> section -> gate -> tally. The measurement half of the system."""
import json, os, re, collections, warnings
warnings.filterwarnings("ignore")

from config import LEXICON, FAMILIES, FLOOR, LEAD_WEIGHT
from gates import apply_gates, _stems, stem

COMPILED = {k: re.compile(v, re.I) for k, v in LEXICON.items()}

# --- fetching ---------------------------------------------------------------
_AGGREGATORS = ("jobright.ai", "speedrun-talent-network.com", "simplify.jobs",
                "glassdoor.com", "ziprecruiter.com")
_CANONICAL = ("greenhouse.io", "ashbyhq.com", "lever.co", "myworkdayjobs.com",
              "oraclecloud.com", "amazon.jobs", "apple.com")

def url_rank(u):
    """Lower is better. Aggregators re-post the same role with thinner text."""
    if any(a in u for a in _AGGREGATORS): return 3
    if any(c in u for c in _CANONICAL):   return 0
    return 1

_SHELL = re.compile(r"(enable javascript|loading\.\.\.|you need to enable)", re.I)

def has_jd_signal(text):
    """Does this text actually contain a job posting, or just site chrome?

    Length is NOT a proxy for content. A Greenhouse/Workday embed that loads the
    posting via JS still returns 12k+ characters of navigation menu, which sails
    past any character threshold while containing no job at all. This silently
    poisoned the first corpus and hit big companies hardest, because they are the
    ones with heavy site chrome. Require an actual qualifications or duties
    heading before trusting a fast fetch."""
    for line in text.split("\n"):
        l = line.strip()
        if len(l) < 90 and (QUAL_H.match(l) or DUTY_H.match(l)):
            return True
    return False


def fetch(url, timeout=30):
    """Fast HTTP first; escalate to a real browser when that returns a JS shell
    OR a page with no job-posting signal. Most boards serve static HTML — always
    paying browser cost would make a 15-JD run ~10x slower for no gain."""
    from scrapling.fetchers import Fetcher, DynamicFetcher
    try:
        p = Fetcher.get(url, stealthy_headers=True, timeout=timeout)
        t = p.get_all_text(ignore_tags=("script", "style"))
        if (len(t.strip()) > 1200 and not _SHELL.search(t[:600])
                and has_jd_signal(t)):
            return t, "get"
    except Exception:
        pass
    try:
        p = DynamicFetcher.fetch(url, headless=True, network_idle=True,
                                 timeout=timeout * 1500)
        return p.get_all_text(ignore_tags=("script", "style")), "dynamic"
    except Exception as e:
        return "", f"FAIL:{type(e).__name__}"


# --- sectioning (HHH p.10 heading library) ----------------------------------
QUAL_H = re.compile(r"^\s*(required|preferred|basic|minimum|desired|key)?\s*"
    r"(qualifications?|requirements?|skills? (?:and|&) (?:experience|qualifications?)|"
    r"must[- ]haves?|need to have|nice[- ]to[- ]have|what we(?:'|’)?re looking for|"
    r"what we are looking for|we would love to meet you if|you might be a great fit if|"
    r"who you are|about you|what you(?:'|’)?ll need|what you need|"
    r"you(?:'|’)?ll be a great fit|ideal candidate|our ideal candidate|"
    r"skills? (?:you|we)|experience (?:you|we)|what you bring|you have|"
    # Palantir and peers head their qualifications "What We Value" / "What We
    # Require". Missing these dropped 32 otherwise-valid GTM postings.
    r"what we (?:value|require|need|look for|expect)|what we(?:'|’)?d love|"
    r"what you(?:'|’)?ll bring|minimum requirements?|basic requirements?|"
    r"qualifications? we|desired skills?|required skills?)\s*:?\s*$", re.I)

DUTY_H = re.compile(r"^\s*(what you(?:'|’)?ll do|what you(?:'|’)?ll be doing|"
    r"(?:core|key|primary|main|your)? ?responsibilities|what we do|"
    r"the role|your (?:role|impact)|day[- ]to[- ]day|"
    r"in this role|what to expect|the opportunity|you will|core duties|"
    r"a day in the life|what the job (?:involves|entails))\s*:?\s*$", re.I)

STOP_H = re.compile(r"^\s*(benefits?|perks?|compensation|pay (?:range|transparency)|salary|"
    r"about (?:us|the (?:company|team))|equal (?:employment )?opportunity|"
    r"eeo|e-verify|our (?:commitment|values|culture)|tools and resources|"
    r"why (?:join|work)|privacy|accommodations?|legal|how to apply|"
    r"itar|export control|total rewards|what we(?:'|’)?re about|"
    r"a world[- ]changing company|life at |offer deadline|to apply)\b", re.I)

def sectionize(text):
    mode, out = None, {"qual": [], "duty": []}
    for raw in text.split("\n"):
        l = raw.strip()
        if not l:
            continue
        short = len(l) < 90
        if short and STOP_H.match(l):
            mode = None; continue
        if short and QUAL_H.match(l):
            mode = "qual"; continue
        if short and DUTY_H.match(l):
            mode = "duty"; continue
        if short and mode and l.endswith(":") and re.match(r"^[A-Z][A-Za-z’'&/,\- ]{3,60}:$", l):
            mode = None; continue
        if mode and len(l) > 25:
            out[mode].append(l)
    return out


# --- tallying ---------------------------------------------------------------
def is_lead(title, fam):
    lead = _stems(FAMILIES[fam]["lead"])
    t = _stems(title)
    return bool(lead) and all(s in t for s in lead)

def tally(docs, fam):
    """Document frequency, with lead-title JDs weighted. Returns rows sorted by
    demand = qual_weighted*2 + duty_weighted (qualifications count double,
    per HHH p.9 which says duties are not the signal)."""
    rows = {}
    for k, rx in COMPILED.items():
        q = d = 0
        q_src = []
        for doc in docs:
            w = LEAD_WEIGHT if is_lead(doc["title"], fam) else 1
            if rx.search(" \n".join(doc["sections"]["qual"])):
                q += w; q_src.append(doc["company"])
            if rx.search(" \n".join(doc["sections"]["duty"])):
                d += w
        rows[k] = {"qual": q, "duty": d, "demand": q * 2 + d, "sources": q_src}
    return dict(sorted(rows.items(), key=lambda x: -x[1]["demand"]))


def duty_verbs(docs, limit=8):
    """Verbatim duty lines, for the inception layer: mirror their noun-verb
    pair and keep your own number."""
    out = []
    for doc in docs:
        lines = [re.sub(r"\s+", " ", l) for l in doc["sections"]["duty"]
                 if 25 < len(l) < 240]
        if lines:
            out.append({"company": doc["company"], "title": doc["title"],
                        "lines": lines[:limit]})
    return out


def dedupe(docs):
    """Same company + same role = one posting, however many URLs point at it.

    Merging corpora from different runs (or an ATS that exposes a role at both
    boards.greenhouse.io and job-boards.greenhouse.io) yields literal duplicates.
    Left in, they double-count every qualification in that JD and quietly inflate
    demand for whatever that one employer happens to emphasise. Keep the copy
    with the most qualification lines."""
    best = {}
    for d in docs:
        co = re.sub(r"\b(inc|llc|ltd|corp|company|technologies|industries|group|space|ai)\b",
                    "", (d.get("company") or "").lower())
        co = re.sub(r"[^a-z]", "", co)
        ti = re.sub(r"[^a-z]", "", (d.get("title") or "").lower())[:40]
        k = (co, ti)
        if k not in best or len(d["sections"]["qual"]) > len(best[k]["sections"]["qual"]):
            best[k] = d
    return list(best.values())


def run_family(fam, raw_docs, segment_floor=False):
    """raw_docs: [{company,title,url,sections}] already fetched+sectioned.
    Returns a report dict. Enforces the floor — below it, no ranked table."""
    raw_docs = dedupe(raw_docs)
    kept, rejected = apply_gates(raw_docs, fam, segment_floor=segment_floor)
    employers = sorted({(d.get("company") or "").strip() for d in kept})
    rep = {
        "family": fam, "name": FAMILIES[fam]["name"], "lead": FAMILIES[fam]["lead"],
        "n": len(kept), "floor": FLOOR,
        "employers": len(employers),
        # G5 caps any single company's SHARE, but a corpus can still clear the
        # floor from very few employers. Diversity is a separate axis and is
        # surfaced rather than silently trimmed — trimming to force it would
        # push a thin family back below the floor, trading a stated weakness
        # for a missing table.
        "narrow": len(employers) < 6,
        "sufficient": len(kept) >= FLOOR,
        "kept": [{"company": d["company"], "title": d["title"], "url": d.get("url", ""),
                  "lead": is_lead(d["title"], fam)} for d in kept],
        "rejected": [{"company": d["company"], "title": d["title"],
                      "gate": g, "reason": why} for d, g, why in rejected],
    }
    if rep["sufficient"]:
        rep["table"] = tally(kept, fam)
        rep["duties"] = duty_verbs(kept)
    else:
        rep["table"] = None
        rep["message"] = (f"INSUFFICIENT CORPUS: n={len(kept)}, floor={FLOOR}. "
                          f"Need {FLOOR - len(kept)} more qualifying JDs. "
                          f"No ranked table emitted.")
    return rep
