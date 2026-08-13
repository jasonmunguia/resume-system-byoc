"""Families, title whitelists, and the qualification lexicon.

Everything a human would tune lives here. The pipeline reads it; it never
hardcodes a title or a keyword.
"""

# ---------------------------------------------------------------------------
# Resume families. Titles come from your context/families.json.
# `lead` is the mass-apply title — JDs matching it are weighted heavier because
# the resume is aimed at that title first and the tail titles second.
# ---------------------------------------------------------------------------
FAMILIES = {
    "R1": {
        "name": "Strategy / Business Analyst",
        "lead": "business analyst",
        "titles": [
            "business analyst", "strategy intern", "strategy analyst",
            "strategy and operations", "strategy & operations",
            "strategy and analytics", "corporate strategy", "business strategy",
            "consultant intern", "consulting intern", "associate consultant",
            "summer associate", "chief of staff", "founders associate",
            "founder's associate", "founders office", "founder's office",
            "business operations", "bizops", "special projects",
            "strategic initiatives", "operations intern", "program manager",
            "project manager", "supply chain", "strategic finance",
        ],
    },
    "R2": {
        "name": "Product",
        "lead": "product manager",
        "titles": [
            "product manager", "product management", "associate product manager",
            "apm intern", "product intern", "technical product",
            "technical program", "product development", "associate product builder",
            "product operations", "product analyst", "product strategy",
            "rotational product", "product owner", "growth product",
            "product research", "digital product", "platform product",
        ],
    },
    "R3": {
        "name": "GTM / Commercial",
        "lead": "business development",
        "titles": [
            "go-to-market", "gtm strategy", "gtm intern", "business development",
            "bd intern", "partnerships", "strategic partnerships", "growth intern",
            "growth strategy", "growth operations", "revenue operations",
            "revops", "sales strategy", "sales operations", "commercial intern",
            "commercial strategy", "capture intern", "deployment strategist",
            "forward deployed", "implementation strategist",
            "implementation consultant", "solutions intern", "solutions consultant",
            "customer success", "field operations",
        ],
    },
}

# ---------------------------------------------------------------------------
# Qualification lexicon: concept -> regex of the ways JDs phrase it.
# Counted as DOCUMENT FREQUENCY (how many JDs mention it), never raw hits.
# ---------------------------------------------------------------------------
LEXICON = {
    # the seven anchors from context/anchors.json
    # v1 required "presenting"/"present" immediately adjacent to "to" and missed
    # the past tense entirely. Real resume phrasing puts the object in between
    # ("presented RECOMMENDATIONS to the CTO"), so this under-reported the #1
    # highest-demand R1 trait on a resume that has real evidence for it.
    "Communication (written & verbal)": r"communicat|verbal and written|written and verbal|articulate|"
                                        r"present(?:ed|ing)?\b.{0,60}\bto\b|\bbriefed\b",
    # Resumes name the PERSON, postings name the ABSTRACTION. An early version
    # matched only "stakeholder"/"senior leader" and so missed "presented to the
    # CTO", "marketing leaders", and "executives from X" — the three most common
    # ways a bullet actually expresses this. It under-reported the trait in every
    # run until a real resume exposed it.
    "Stakeholder management":           r"stakeholder|senior leader(?:ship)?|executive|C-suite|\b(?:CTO|CEO|CFO|COO|CMO|CIO|VP)\b|"
                                        r"client relationship|decision[- ]maker|founders?\b|partners?\b|"
                                        r"(?:marketing|business|department|functional|industry|team) leaders?\b|leaders? at\b",
    "Influence / persuasion":           r"influenc|persuas|buy[- ]in|drive alignment|build consensus|negotiat",
    "Analytical skills":                r"analytical|analysis|analyz|quantitative|data[- ]driven",
    "Problem solving":                  r"problem[- ]solv|solve complex|structured thinking|first principles|troubleshoot",
    # "led"/"leading" as verbs are the most common way bullets actually express
    # this trait ("led networking workshops"), but the noun-only regex missed
    # them. Guard against "led to" (a causal connector, not a leadership claim,
    # e.g. "which led to a 15% increase") with a negative lookahead.
    "Leadership / initiative":          r"leadership|self[- ]start|take initiative|ownership|owner mentality|"
                                        r"drive projects|player[- ]coach|\bled\b(?!\s+to\b)|\bleading\b(?!\s+to\b)",
    "Teamwork / collaboration":         r"teamwork|collaborat|work (?:well )?(?:with|across) (?:others|teams)|team player",
    # tools
    "Excel / spreadsheet modeling":     r"\bexcel\b|spreadsheet|pivot table|vlookup|financial model",
    "SQL":                              r"\bsql\b|relational database|querying",
    "Python / scripting":               r"\bpython\b|scripting",
    "Data visualization (Tableau/PBI)": r"tableau|power ?bi|looker|data visuali[sz]|dashboard",
    "PowerPoint / storytelling":        r"powerpoint|slide|deck|present(?:ation)? skills|storytell|narrative",
    "AI / LLM fluency":                 r"\bAI\b|\bLLM|generative ai|machine learning|prompt engineering",
    # ways of working
    "Cross-functional partnering":      r"cross[- ]functional|partner with (?:engineering|sales|product|design)|matrix",
    "Ambiguity / fast-paced":           r"ambigu|fast[- ]paced|rapidly changing|scrappy|startup environment|calm under pressure",
    "Prioritization / time management": r"priorit|time management|competing (?:demands|priorities)|manage multiple|deadline",
    "Attention to detail":              r"attention to detail|detail[- ]oriented|meticulous|accuracy|rigor",
    "Project / program management":     r"project manage|program manage|\bPMP\b|scrum|agile|sprint|roadmap|timeline|backlog",
    "Process improvement":              r"process improv|continuous improv|operational excellence|six sigma|\blean\b|streamlin|efficien",
    "Metrics / KPIs":                   r"\bKPI|metric|measur(?:e|ing) (?:success|impact)|\bOKR|track performance|key results",
    "Business acumen / strategy":       r"business acumen|commercial acumen|business strategy|strategic thinking|market (?:analysis|research)",
    "Customer / client-facing":         r"customer[- ]facing|client[- ]facing|customer success|voice of (?:the )?customer|user research|customer obsess",
    "Curiosity / learning agility":     r"curious|curiosity|eager to learn|learning agility|growth mindset|intellectual",
    "Bias for action / results":        r"bias for action|results[- ](?:driven|oriented)|deliver results|get things done|execution",
    "Written documentation":            r"document(?:ation)?|write (?:clear|concise)|technical writing|memo|spec(?:ification)?s",
    "Financial / P&L":                  r"\bP&L\b|forecast|budget|revenue|pricing|unit economics|financial analysis",
    "Supply chain / logistics":         r"supply chain|logistics|procure|inventory|vendor|supplier|sourcing",
    "Sales / pipeline / GTM":           r"\bsales\b|pipeline|quota|prospect|lead gen|go[- ]to[- ]market|\bGTM\b|business development",
    "Product sense / user empathy":     r"product sense|user (?:empathy|needs)|customer problem|product intuition|user experience",
    "Technical aptitude":               r"technical (?:aptitude|background|concepts|specification)|engineering (?:background|team)|\bAPI\b",
    # "Mentor" is directionally ambiguous — "created a mentor ecosystem" means
    # the candidate mentors OTHERS (a leadership act), not that the candidate
    # takes direction from someone else (what this trait actually measures, per
    # HHH's own bucket 4: "takes direction and criticism"). A bare "mentor" or
    # "mentorship" match can't tell those apart, so only match constructions
    # where direction is unambiguous — the candidate is the one BEING mentored.
    "Coachability":                     r"takes? (?:direction|feedback)|receptive to feedback|open to criticism|"
                                        r"coachab|under (?:the )?mentorship|received mentorship|mentored by|"
                                        r"with mentorship from",
}

# ---------------------------------------------------------------------------
# Gate thresholds
# ---------------------------------------------------------------------------
FLOOR = 10          # refuse to emit a ranked table below this many JDs
TARGET = 15         # stop fetching once we have this many
MAX_CONCENTRATION = 0.20   # no single company may exceed this share of a corpus
LEAD_WEIGHT = 2     # JDs matching the family's lead title count this many times


# ---------------------------------------------------------------------------
# G6 — Segment floor.
# G1-G5 catch CATEGORY error (wrong title, wrong seniority, engineering role
# wearing a business title). They do not catch SEGMENT error: a South Carolina
# Dept. of Commerce "Business Development Intern" is a genuine BD internship and
# passes every other gate, but its qualifications say nothing about what the
# target employers screen for. Without this gate a corpus reaches the floor by
# diluting with the long tail — measured at 6%/19%/12% target-tier on the first
# ungated run.
#
# `tiers.json` (optional, from an external tiering source) is merged with this
# list at load time.
# ---------------------------------------------------------------------------
TARGET_COMPANIES = {
    # consulting
    "mckinsey", "bain", "bcg", "boston consulting", "deloitte", "accenture",
    "ey-parthenon", "oliver wyman", "kearney", "l.e.k.", "roland berger",
    # tech / product
    "google", "meta", "microsoft", "amazon", "apple", "linkedin", "salesforce",
    "databricks", "snowflake", "stripe", "figma", "notion", "airtable", "uber",
    "lyft", "doordash", "instacart", "atlassian", "workday", "servicenow",
    "adobe", "intuit", "nvidia", "openai", "anthropic", "mistral", "scale ai",
    # fintech / financial
    "capital one", "american express", "goldman sachs", "jpmorgan", "morgan stanley",
    "blackrock", "visa", "mastercard", "paypal", "block", "ramp", "brex", "plaid",
    # defense / hard tech
    "palantir", "anduril", "spacex", "skydio", "figure", "shield ai", "saronic",
    "astranis", "varda", "applied intuition", "relativity space",
    # high-growth startups
    "clay", "rippling", "deel", "vanta", "retool", "linear", "vercel", "appian",
}

# Distinct companies whose names collide with an allowlist entry. String rules
# cannot separate these — BlackRock (asset manager) vs. Blackrock Neurotech
# (medical devices) share a token and are unrelated firms. Explicit and small by
# design; if this list grows past ~20 the allowlist itself is too loose.
DENY_COMPANIES = {
    "blackrock neurotech",
}

# 4/5 band from an employer-quality rubric (see context/tiers.json):
# "Big 4 for Consulting, mid-tier banks, well-known corporates." These are
# legitimate resume employers and their JDs are legitimate corpus material.
# The floor exists to exclude the 1-2/5 band (unknown local shops, staffing
# fronts, tiny agencies), NOT to exclude everyone below MBB.
REPUTABLE_COMPANIES = {
    # Big 4 + consulting
    "deloitte", "pwc", "pricewaterhousecoopers", "kpmg", "ernst young", "ey",
    "kearney", "alixpartners", "huron", "zs associates", "slalom", "west monroe",
    # banks / financial
    "wells fargo", "citi", "citigroup", "us bank", "pnc", "truist", "fifth third",
    "northern trust", "state street", "bny mellon", "nasdaq", "fidelity",
    "charles schwab", "synchrony", "discover", "gemini",
    # well-known corporates
    "campbell soup", "general mills", "kraft heinz", "pepsico", "conagra",
    "johnson johnson", "procter gamble", "unilever", "nestle", "mars",
    "bosch", "siemens", "honeywell", "ge vernova", "general electric", "abb",
    "schneider electric", "emerson", "eaton", "rockwell automation", "signify",
    "toshiba", "panasonic", "sony", "lg", "samsung", "philips",
    "john deere", "caterpillar", "cummins", "3m", "dow", "dupont", "huntsman",
    "boeing", "lockheed martin", "northrop grumman", "rtx", "raytheon", "l3harris",
    "ford", "general motors", "toyota", "rivian", "volkswagen", "vertiv",
    "target", "costco", "kroger", "nike", "starbucks", "marriott", "delta",
    "united airlines", "fedex", "ups", "uline", "grainger", "rockwool",
    "accuweather", "nielsen", "s&p global", "moodys", "verisk",
    "oracle", "sap", "ibm", "cisco", "dell", "hp", "hpe", "qualcomm", "intel",
    "texas instruments", "analog devices", "infineon", "nxp", "micron",
    "tiktok", "bytedance", "celonis", "nice", "submittable", "nelnet",
    "crane", "curtiss wright", "jm family", "marmon", "copart", "plymouth rock",
}

TIER_FILE = "tiers.json"   # optional: {"company name": "T1"|"T2"|...}


# ---------------------------------------------------------------------------
# Concept kind. Drives how a qualification is spent on the page:
#   trait  -> PROVEN in a bullet (one per bullet slot)
#   tool   -> LISTED in the Skills line; only earns a bullet if a bullet shows
#             it doing something (HHH p.24 — show HOW the keyword was used)
#   domain -> subject-matter signal; proven in a bullet, but only for the
#             family that asks for it
# ---------------------------------------------------------------------------
KIND = {
    "Communication (written & verbal)": "trait",
    "Stakeholder management":           "trait",
    "Influence / persuasion":           "trait",
    "Analytical skills":                "trait",
    "Problem solving":                  "trait",
    "Leadership / initiative":          "trait",
    "Teamwork / collaboration":         "trait",
    "Cross-functional partnering":      "trait",
    "Ambiguity / fast-paced":           "trait",
    "Prioritization / time management": "trait",
    "Attention to detail":              "trait",
    "Process improvement":              "trait",
    "Metrics / KPIs":                   "trait",
    "Business acumen / strategy":       "trait",
    "Customer / client-facing":         "trait",
    "Curiosity / learning agility":     "trait",
    "Bias for action / results":        "trait",
    "Written documentation":            "trait",
    "Coachability":                     "trait",
    "Product sense / user empathy":     "trait",
    "Project / program management":     "trait",
    "Excel / spreadsheet modeling":     "tool",
    "SQL":                              "tool",
    "Python / scripting":               "tool",
    "Data visualization (Tableau/PBI)": "tool",
    "PowerPoint / storytelling":        "tool",
    "AI / LLM fluency":                 "tool",
    "Technical aptitude":               "tool",
    "Sales / pipeline / GTM":           "domain",
    "Supply chain / logistics":         "domain",
    "Financial / P&L":                  "domain",
}

# Anchor traits context/anchors.json names as the BA target set.
# Flagged in output so a measured ranking never silently drops one he decided
# matters — measurement informs the list, it does not overrule him.
ANCHORS = {
    "Influence / persuasion", "Analytical skills", "Leadership / initiative",
    "Communication (written & verbal)", "Stakeholder management",
    "Problem solving", "Teamwork / collaboration",
}


# ---------------------------------------------------------------------------
# BYOC overrides. Anything in context/ wins over the defaults above, so a user
# can retarget the whole system — different job families, different anchor
# traits, different employer tiers — without editing this file.
# ---------------------------------------------------------------------------
import context as _ctx

_fam = _ctx.load("families")
if _fam and _fam.get("families"):
    FAMILIES = _fam["families"]

_anc = _ctx.load("anchors")
if _anc and _anc.get("anchors"):
    ANCHORS = set(_anc["anchors"])

_tiers = _ctx.load("tiers")
if _tiers:
    TARGET_COMPANIES = set(_tiers.get("elite", TARGET_COMPANIES))
    REPUTABLE_COMPANIES = set(_tiers.get("reputable", REPUTABLE_COMPANIES))
    DENY_COMPANIES = set(_tiers.get("deny", DENY_COMPANIES))
