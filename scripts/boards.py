"""Harvest full JD text straight from ATS public JSON APIs.

Greenhouse, Lever, and Ashby each publish an unauthenticated board API that
returns every posting WITH its full body. That is strictly better than fetching
and scraping career pages: no JS shells, no anti-bot, no sectionizer guessing
against nav chrome, and one request per company instead of one per posting.

Usage:
    python3 boards.py --family R2 --out urls_or_docs
"""
import argparse, html, json, os, re, ssl, sys, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import FAMILIES
from gates import g2_title_in_family, g4_seniority, g6_segment
from pipeline import sectionize

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE

# Board slugs for target-tier employers. Slug != company name, so this is a
# lookup table rather than something derivable.
BOARDS = {
    "greenhouse": [
        ("databricks", "Databricks"), ("stripe", "Stripe"), ("figma", "Figma"),
        ("andurilindustries", "Anduril"), ("spacex", "SpaceX"),
        ("vercel", "Vercel"), ("retool", "Retool"), ("samsara", "Samsara"),
        ("airtable", "Airtable"), ("robinhood", "Robinhood"),
        ("gitlab", "GitLab"), ("instacart", "Instacart"),
        ("affirm", "Affirm"), ("coinbase", "Coinbase"),
        ("appian", "Appian"), ("vardaspace", "Varda Space"),
        ("astranis", "Astranis"), ("figureai", "Figure AI"),
        ("cruise", "Cruise"), ("discord", "Discord"),
        ("doordash", "DoorDash"), ("flexport", "Flexport"),
    ],
    "lever": [
        ("palantir", "Palantir"), ("attentive", "Attentive"),
        ("mistral", "Mistral AI"),
    ],
    "ashby": [
        ("openai", "OpenAI"), ("claylabs", "Clay"), ("ramp", "Ramp"),
        ("linear", "Linear"), ("vanta", "Vanta"), ("deel", "Deel"),
        ("skydio", "Skydio"), ("saronic", "Saronic"), ("base-power", "Base Power"),
        ("mistral.ai", "Mistral AI"), ("cohere", "Cohere"), ("harvey", "Harvey"),
        ("abridge", "Abridge"), ("handshake", "Handshake"),
        ("airwallex", "Airwallex"), ("evenup", "EvenUp"),
        ("scaleai", "Scale AI"), ("notion", "Notion"), ("sierra", "Sierra"),
    ],
}

ENDPOINTS = {
    "greenhouse": "https://boards-api.greenhouse.io/v1/boards/{}/jobs?content=true",
    "lever":      "https://api.lever.co/v0/postings/{}?mode=json",
    "ashby":      "https://api.ashbyhq.com/posting-api/job-board/{}?includeCompensation=false",
}


def _get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout, context=_CTX) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def _strip(h):
    """HTML -> newline-preserving text. Block tags become newlines so the
    sectionizer can still see headings as their own lines."""
    if not h:
        return ""
    t = html.unescape(h)
    t = re.sub(r"(?i)</?(p|div|li|ul|ol|br|h[1-6]|tr|table)[^>]*>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    return re.sub(r"\n{2,}", "\n", t)


def harvest(kind, slug, company):
    """-> [{company,title,url,text}] for one board. Never raises."""
    try:
        data = _get(ENDPOINTS[kind].format(slug))
    except Exception as e:
        return [], f"{type(e).__name__}"
    out = []
    if kind == "greenhouse":
        for j in data.get("jobs", []):
            out.append({"company": company, "title": j.get("title", ""),
                        "url": j.get("absolute_url", ""),
                        "text": _strip(j.get("content", ""))})
    elif kind == "lever":
        for j in data if isinstance(data, list) else []:
            body = j.get("descriptionPlain", "") or _strip(j.get("description", ""))
            for lst in j.get("lists", []):
                body += "\n" + _strip(lst.get("text", "")) + "\n" + _strip(lst.get("content", ""))
            out.append({"company": company, "title": j.get("text", ""),
                        "url": j.get("hostedUrl", ""), "text": body})
    else:  # ashby
        for j in data.get("jobs", []):
            out.append({"company": company, "title": j.get("title", ""),
                        "url": j.get("jobUrl", "") or j.get("applyUrl", ""),
                        "text": j.get("descriptionPlain", "")
                                or _strip(j.get("descriptionHtml", ""))})
    return out, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True, choices=list(FAMILIES))
    ap.add_argument("--no-segment-floor", action="store_true")
    a = ap.parse_args()
    fam = a.family
    outdir = os.path.join(DATA, fam)
    os.makedirs(outdir, exist_ok=True)

    seen_board, kept, stats = set(), 0, {"boards": 0, "postings": 0, "title_ok": 0}
    for kind, boards in BOARDS.items():
        for slug, company in boards:
            if (kind, slug) in seen_board:
                continue
            seen_board.add((kind, slug))
            rows, err = harvest(kind, slug, company)
            if err:
                print(f"  --  {company:20} {kind:10} {err}")
                continue
            stats["boards"] += 1
            stats["postings"] += len(rows)
            hits = 0
            for r in rows:
                if not g2_title_in_family(r["title"], fam)[0]:
                    continue
                if not g4_seniority(r["title"], None)[0]:
                    continue
                if not a.no_segment_floor and not g6_segment(r["company"])[0]:
                    continue
                stats["title_ok"] += 1
                sec = sectionize(r["text"])
                if not sec["qual"]:
                    continue
                slugf = re.sub(r"[^A-Za-z0-9]+", "-", f"api-{company}-{r['title']}")[:95]
                json.dump({"company": company, "title": r["title"], "url": r["url"],
                           "method": f"api:{kind}", "raw_chars": len(r["text"]),
                           "sections": sec},
                          open(os.path.join(outdir, slugf + ".json"), "w"), indent=1)
                hits += 1; kept += 1
            if hits:
                print(f"  OK  {company:20} {kind:10} +{hits}")
    print(f"\n{stats['boards']} boards, {stats['postings']} postings, "
          f"{stats['title_ok']} passed title gates, {kept} written with quals")


if __name__ == "__main__":
    main()
