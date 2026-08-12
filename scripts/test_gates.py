"""Gate tests. Every case is a real posting from the v0 run, with the verdict
we decided it should get. Run: python3 -m pytest test_gates.py -q
"""
import pytest
from gates import (stem, g1_good_jd, g2_title_in_family, g3_role_nature,
                   g4_seniority, g5_concentration, apply_gates)


# --- stemming: the bug that false-rejected Astranis in v0 -------------------
@pytest.mark.parametrize("a,b", [
    ("manager", "management"),      # Project Manager <-> Project Management
    ("operations", "operational"),
    ("strategy", "strategic"),
    ("consulting", "consultant"),
    ("development", "developer"),
    ("solutions", "solution"),
])
def test_stem_collapses_variants(a, b):
    assert stem(a) == stem(b), f"{a}->{stem(a)} != {b}->{stem(b)}"


def test_stem_keeps_distinct_words_apart():
    assert stem("product") != stem("project")
    assert stem("sales") != stem("solutions")


# --- G1 ---------------------------------------------------------------------
def test_g1_rejects_jd_with_no_qualifications_block():
    ok, why = g1_good_jd({"qual": [], "duty": ["You will do things"]})
    assert not ok and "qualification" in why


def test_g1_passes_jd_with_qualifications():
    ok, _ = g1_good_jd({"qual": ["Pursuing a Bachelor's degree"], "duty": []})
    assert ok


# --- G2: the v0 false reject, and the true rejects --------------------------
def test_g2_astranis_technical_project_management_now_passes():
    """v0 bug: whitelist said 'project manager', title said 'Project
    Management'. Substring matching missed it; stems catch it."""
    ok, _ = g2_title_in_family("Technical Project Management Intern (Fall 2026)", "R1")
    assert ok


@pytest.mark.parametrize("title,fam", [
    ("Member Experience Intern", "R3"),          # customer support
    ("American Tech Fellowship", "R3"),          # unpaid virtual training
    ("Neurodivergent Fellowship", "R3"),
    ("Recruiting Operations Internship", "R1"),  # HR ops
])
def test_g2_rejects_off_family_titles(title, fam):
    ok, _ = g2_title_in_family(title, fam)
    assert not ok


@pytest.mark.parametrize("title,fam", [
    ("Business Analyst Intern", "R1"),
    ("Associate Consultant Intern", "R1"),
    ("Supply Chain Internship - Spring 2027", "R1"),
    ("Product Manager Intern", "R2"),
    ("Associate Product Manager Intern (APM)", "R2"),
    ("Deployment Strategist, Internship - US Government", "R3"),
    ("Business Development Intern", "R3"),
])
def test_g2_accepts_in_family_titles(title, fam):
    ok, why = g2_title_in_family(title, fam)
    assert ok, why


# --- G3': engineering IC wearing a business title ---------------------------
def test_g3_rejects_figure_ai_special_projects():
    """Real v0 leak: title is on the R1 whitelist, job is robotics software."""
    s = {"qual": ["Pursuing a degree in computer science",
                  "Experience with C++ and embedded systems"],
         "duty": ["Write and maintain software that drives robot demonstrations",
                  "Test behaviors on hardware and debug control logic in the lab"]}
    ok, why = g3_role_nature(s)
    assert not ok and "engineering" in why


def test_g3_keeps_technical_business_roles():
    """Appian Associate Consultant mentions technical work but is a business role."""
    s = {"qual": ["Aptitude for analyzing business strategies",
                  "Exceptional verbal and written communication skills",
                  "Experience with relational databases such as SQL"],
         "duty": ["Partner with our customer success team and clients to analyze "
                  "business strategies and model critical workflows"]}
    ok, why = g3_role_nature(s)
    assert ok, why


# --- G4: seniority ----------------------------------------------------------
@pytest.mark.parametrize("title", [
    "New Geography and International Growth Lead",
    "Commercial, International Subscriber Growth, Apple Music",
    "International Strategy & Operations Lead",
])
def test_g4_rejects_senior_fulltime(title):
    ok, _ = g4_seniority(title, {"qual": []})
    assert not ok


@pytest.mark.parametrize("title", [
    "Business Analyst Intern",
    "2026 Supply Chain Intern/Co-op",
    "Campus Undergraduate Summer Internship Program",
    "Product Management Intern (Summer 2027)",
])
def test_g4_accepts_intern_level(title):
    ok, _ = g4_seniority(title, {"qual": []})
    assert ok


# --- G5: concentration ------------------------------------------------------
def test_g5_caps_palantir_at_20_percent():
    """v0: Palantir was 3 of 12 R3 JDs (25%). At n=12 the cap is 2."""
    docs = [{"company": "Palantir"}] * 3 + [{"company": f"Co{i}"} for i in range(9)]
    kept, dropped = g5_concentration(docs)
    assert sum(1 for d in kept if d["company"] == "Palantir") == 2
    assert len(dropped) == 1


def test_g5_never_empties_a_small_corpus():
    kept, _ = g5_concentration([{"company": "Solo"}] * 3)
    assert len(kept) >= 1


# --- integration ------------------------------------------------------------
def test_apply_gates_reports_the_failing_gate():
    docs = [
        {"company": "McKinsey", "title": "Business Analyst Intern",
         "sections": {"qual": ["Strong analytical and communication skills"], "duty": []}},
        {"company": "Base Power", "title": "Member Experience Intern",
         "sections": {"qual": ["Strong attention to detail"], "duty": []}},
        {"company": "Ghost", "title": "Business Analyst Intern",
         "sections": {"qual": [], "duty": ["stuff"]}},
    ]
    kept, rejected = apply_gates(docs, "R1")
    assert [d["company"] for d in kept] == ["McKinsey"]
    by_co = {d["company"]: gate for d, gate, _ in rejected}
    assert by_co["Ghost"].startswith("G1")
    assert by_co["Base Power"].startswith("G2")


# --- G6: segment floor ------------------------------------------------------
from gates import g6_segment

@pytest.mark.parametrize("company", [
    "Kirat Plastics Pvt. Ltd.", "South Carolina Department of Commerce",
    "Good People Only", "Vital Lyfe", "Evaro Italia",
])
def test_g6_rejects_long_tail(company):
    """These all passed G1-G5 honestly on the ungated run and diluted the
    corpus to 6-19% target-tier."""
    ok, why = g6_segment(company)
    assert not ok and "segment floor" in why


@pytest.mark.parametrize("company", [
    "McKinsey & Company", "Capital One", "Databricks", "Palantir",
    "American Express", "Appian", "Mistral AI", "SpaceX",
])
def test_g6_accepts_target_tier(company):
    ok, why = g6_segment(company)
    assert ok, why


def test_g6_off_by_default_in_apply_gates():
    """Segment floor encodes ambition, not correctness — it must be opt-in."""
    docs = [{"company": "Kirat Plastics Pvt. Ltd.", "title": "Business Analyst Intern",
             "sections": {"qual": ["Strong communication skills"], "duty": []}}]
    kept, _ = apply_gates(docs, "R1")
    assert len(kept) == 1
    kept, rejected = apply_gates(docs, "R1", segment_floor=True)
    assert len(kept) == 0 and rejected[0][1].startswith("G6")


# --- fetch content validation ----------------------------------------------
from pipeline import has_jd_signal

def test_nav_chrome_is_not_mistaken_for_a_job_posting():
    """The v1 bug: Databricks returned 12,273 chars of pure site navigation and
    the length threshold accepted it, so the browser escalation never fired."""
    nav = "\n".join(["Why Databricks", "Discover", "For App Developers",
                     "Lakehouse Architecture", "Customers", "Partner Program",
                     "Pricing", "Open Source", "Financial Services"] * 40)
    assert not has_jd_signal(nav)


def test_real_posting_is_recognized():
    jd = "\n".join(["Product Manager Intern", "Responsibilities",
                    "Own the agile backlog for an engineering squad",
                    "Required Qualifications",
                    "Pursuing a Bachelor's degree with a strong academic record"])
    assert has_jd_signal(jd)


# --- dedupe -----------------------------------------------------------------
from pipeline import dedupe

def test_dedupe_collapses_same_role_across_corpora():
    """Merging two runs produced SpaceX x3 and Varda x3 of one posting each."""
    docs = [
        {"company": "Varda Space", "title": "Supply Chain Internship - Spring 2027",
         "sections": {"qual": ["a"], "duty": []}},
        {"company": "Varda Space Industries", "title": "Supply Chain Internship - Spring 2027",
         "sections": {"qual": ["a", "b", "c"], "duty": []}},
        {"company": "Appian", "title": "Associate Consultant Intern",
         "sections": {"qual": ["x"], "duty": []}},
    ]
    out = dedupe(docs)
    assert len(out) == 2
    varda = [d for d in out if "Varda" in d["company"]][0]
    assert len(varda["sections"]["qual"]) == 3, "should keep the richer copy"


@pytest.mark.parametrize("company", [
    "AA Metals, Inc",        # matched 'meta' as a substring
    "Metalinked",            # matched 'meta'
    "Applied Materials",     # guard the substring class generally
])
def test_g6_substring_false_positives_are_rejected(company):
    ok, _ = g6_segment(company)
    assert not ok, f"{company} must not clear the segment floor"


def test_g6_still_accepts_real_names_with_suffixes():
    for c in ["Palantir Technologies", "Databricks, Inc.", "McKinsey & Company",
              "Varda Space Industries", "Mistral AI"]:
        ok, why = g6_segment(c)
        assert ok, f"{c}: {why}"


def test_g6_denylist_separates_colliding_names():
    """BlackRock (asset manager) is a target; Blackrock Neurotech is an
    unrelated medical-device company. No string rule separates them."""
    ok, why = g6_segment("Blackrock Neurotech")
    assert not ok and "different company" in why
    assert g6_segment("BlackRock")[0]


def test_g6_reputable_band_is_admitted_by_default():
    """the tier rubric scores "well-known corporates" 4/5 — legitimate resume
    employers, so legitimate corpus material. The floor excludes the 1-2/5 band."""
    for c in ["Campbell Soup", "Deloitte", "Kearney", "Bosch", "Uline", "TikTok"]:
        assert g6_segment(c)[0], c


def test_g6_elite_only_mode_is_stricter():
    assert g6_segment("Campbell Soup", min_tier="elite")[0] is False
    assert g6_segment("McKinsey & Company", min_tier="elite")[0] is True


# --- sectionizer heading coverage -------------------------------------------
from pipeline import sectionize

def test_palantir_what_we_value_require_headings():
    """Palantir heads qualifications 'What We Value' / 'What We Require'. Missing
    these dropped 32 GTM postings that had passed every gate."""
    jd = "\n".join([
        "A World-Changing Company",
        "The Role",
        "Build and deliver demos to new and existing customers today",
        "What We Value",
        "Adaptive and introspective; willing to learn, teach, lead and follow",
        "What We Require",
        "Must be graduating in 2026 or 2027 with a bachelors degree",
    ])
    sec = sectionize(jd)
    assert sec["qual"], "qualifications block must be found"
    assert any("Adaptive" in q for q in sec["qual"])
    assert any("graduating" in q for q in sec["qual"])
    assert any("demos" in d for d in sec["duty"])


def test_core_responsibilities_variant_is_duties():
    sec = sectionize("Core Responsibilities\nOwn the agile backlog for a squad today")
    assert sec["duty"] and not sec["qual"]
