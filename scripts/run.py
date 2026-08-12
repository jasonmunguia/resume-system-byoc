"""CLI. Usage:

  python3 run.py fetch  --family R1 --urls urls_r1.txt   # fetch + cache + gate
  python3 run.py report --family R1                      # print the table
  python3 run.py report --all --md report.md             # all three, markdown

urls file: one URL per line, optional "  # Company | Title" comment ignored.
Cache lives in ../data/<family>/ so re-runs are free.
"""
import argparse, json, os, sys, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import FAMILIES, FLOOR
from pipeline import fetch, sectionize, run_family, url_rank
from gates import g2_title_in_family, g4_seniority

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def _slug(u):
    return re.sub(r"[^A-Za-z0-9]+", "-", u)[-90:]


def cmd_fetch(args):
    fam = args.family
    out = os.path.join(DATA, fam)
    os.makedirs(out, exist_ok=True)
    # urls file lines: URL | Company | Title      (blank lines and # ignored)
    rows = []
    for line in open(args.urls):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            print(f"  SKIP    malformed line (need 'URL | Company | Title'): {line[:60]}")
            continue
        rows.append({"url": parts[0], "company": parts[1], "title": parts[2]})
    # Pre-filter: G2 (title in family) and G4 (intern level) need only the
    # title, so run them BEFORE spending a network round-trip on each URL.
    # On the v0 corpus this drops ~90% of candidates for free.
    pre, skipped = [], 0
    for r in rows:
        ok2, _ = g2_title_in_family(r["title"], fam)
        ok4, _ = g4_seniority(r["title"], None)
        if ok2 and ok4:
            pre.append(r)
        else:
            skipped += 1

    seen, uniq = set(), []
    for r in sorted(pre, key=lambda r: url_rank(r["url"])):
        key = (r["company"].lower(), r["title"].lower())
        if key in seen:
            continue
        seen.add(key); uniq.append(r)

    # Fetch a headroom multiple of TARGET — G1/G3 still cull, and dead links
    # are common on aggregated boards.
    if args.limit:
        uniq = uniq[: args.limit]
    print(f"{fam}: {len(rows)} candidates -> {len(pre)} pass title gates "
          f"({skipped} skipped pre-fetch) -> {len(uniq)} unique to fetch\n")
    for r in uniq:
        p = os.path.join(out, _slug(r["url"]) + ".json")
        if os.path.exists(p) and not args.refresh:
            print(f"  cached  {r['company'][:20]:22} {r['title'][:44]}"); continue
        txt, how = fetch(r["url"])
        if len(txt) < 1200:
            print(f"  THIN    {r['company'][:20]:22} {r['title'][:40]} [{how}]")
            continue
        sec = sectionize(txt)
        json.dump({**r, "raw_chars": len(txt), "method": how, "sections": sec},
                  open(p, "w"), indent=1)
        print(f"  OK  q={len(sec['qual']):2} d={len(sec['duty']):2}  "
              f"{r['company'][:20]:22} {r['title'][:40]} [{how}]")


def _load(fam):
    d = os.path.join(DATA, fam)
    if not os.path.isdir(d):
        return []
    docs = []
    for f in sorted(os.listdir(d)):
        if f.endswith(".json") and not f.startswith("_"):
            docs.append(json.load(open(os.path.join(d, f))))
    return docs


def _md(rep):
    L = [f"## {rep['family']} — {rep['name']}", ""]
    if not rep["sufficient"]:
        L += [f"> ⚠️ **{rep['message']}**", ""]
    else:
        L += [f"*n={rep['n']} JDs · floor={rep['floor']} · lead title: "
              f"`{rep['lead']}` (weighted {2}x)*", "",
              "| # | Qualification | Demand | Qual | Duty |",
              "|---|---|---|---|---|"]
        for i, (k, v) in enumerate(rep["table"].items(), 1):
            if v["demand"] == 0:
                continue
            L.append(f"| {i} | {k} | {v['demand']} | {v['qual']} | {v['duty']} |")
        L += ["", "### Day-to-day duty language (for inception bullets)", ""]
        for d in rep.get("duties", []):
            L.append(f"**{d['company']} — {d['title']}**")
            L += [f"- {x}" for x in d["lines"]]
            L.append("")
    L += ["<details><summary>Corpus & rejections</summary>", ""]
    L += [f"- ✅ {k['company']} — {k['title']}" + (" *(lead)*" if k["lead"] else "")
          for k in rep["kept"]]
    L += [f"- ❌ {r['company']} — {r['title']} → **{r['gate']}**: {r['reason']}"
          for r in rep["rejected"]]
    L += ["", "</details>", ""]
    return "\n".join(L)


def cmd_report(args):
    fams = list(FAMILIES) if args.all else [args.family]
    chunks, reports = [], {}
    for fam in fams:
        docs = [d for d in _load(fam) if d.get("sections")]
        rep = run_family(fam, docs, segment_floor=args.segment_floor)
        reports[fam] = rep
        chunks.append(_md(rep))
        status = "OK" if rep["sufficient"] else "INSUFFICIENT"
        print(f"{fam}: n={rep['n']:2} ({status}), {len(rep['rejected'])} rejected",
              file=sys.stderr)
    md = "\n".join(chunks)
    if args.md:
        open(args.md, "w").write(md)
        print(f"\nwrote {args.md}", file=sys.stderr)
    else:
        print(md)
    json.dump(reports, open(os.path.join(DATA, "_report.json"), "w"), indent=1)
    return 0 if all(r["sufficient"] for r in reports.values()) else 2


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch");  f.add_argument("--family", required=True, choices=list(FAMILIES))
    f.add_argument("--urls", required=True); f.add_argument("--refresh", action="store_true")
    f.add_argument("--limit", type=int, default=40)
    r = sub.add_parser("report"); r.add_argument("--family", choices=list(FAMILIES))
    r.add_argument("--all", action="store_true"); r.add_argument("--md")
    r.add_argument("--segment-floor", action="store_true", dest="segment_floor")
    a = ap.parse_args()
    sys.exit(cmd_fetch(a) or 0 if a.cmd == "fetch" else cmd_report(a))
