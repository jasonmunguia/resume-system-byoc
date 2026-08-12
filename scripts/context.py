"""The BYOC boundary — Bring Your Own Context.

Everything about a *particular person and their target market* lives in
`context/`. Everything in `scripts/` is method and should work unchanged for
anyone. Keeping the two separable is what lets the same codebase ship publicly
without shipping someone's resume, and lets a user swap in their own job
families and employer tiers without editing code.

Each loader falls back to the shipped default, so a fresh clone runs before the
user has written any context at all.

    context/master_experience.json   your bullets + scratchpad leads   (personal)
    context/families.json            job families and title whitelists (market)
    context/anchors.json             traits you've decided matter      (judgment)
    context/tiers.json               employer tier allowlists          (ambition)
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTEXT = os.path.join(ROOT, "context")


def path(name):
    return os.path.join(CONTEXT, name)


def load(name, default=None, quiet=True):
    """Read context/<name>.json, else context/<name>.example.json, else default.

    A malformed context file is a hard error, not a silent fallback: dropping
    back to defaults would run the whole pipeline against the wrong market and
    report it as if nothing were wrong."""
    real = path(f"{name}.json")
    example = path(f"{name}.example.json")
    for p, kind in ((real, "context"), (example, "example")):
        if os.path.exists(p):
            try:
                data = json.load(open(p))
            except json.JSONDecodeError as e:
                raise SystemExit(f"{p} is not valid JSON: {e}")
            if not quiet:
                print(f"  [{kind}] {os.path.relpath(p, ROOT)}")
            return data
    return default


def load_inventory():
    """Master experience inventory -> [(org, text)] of COMPLETE bullets only.

    The other two states are leads, not evidence. Scoring a scratchpad
    placeholder would report it as resume coverage."""
    data = load("master_experience", default={"bullets": []})
    return [(r["org"], r["text"]) for r in data.get("bullets", [])
            if r.get("state", "complete") == "complete"]


def inventory_states():
    """-> {state: count}. Surfaces how much of the inventory is still leads."""
    data = load("master_experience", default={"bullets": []})
    out = {}
    for r in data.get("bullets", []):
        s = r.get("state", "complete")
        out[s] = out.get(s, 0) + 1
    return out
