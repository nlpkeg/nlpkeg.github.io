#!/usr/bin/env python3
"""
NLPKE@CASIA publication crawler.

Pulls the full publication list of the group's faculty from DBLP (the most
reliable structured source — it carries official venue links), deduplicates
across coauthors, merges arXiv preprints into their published version, picks
the best link per the rule "main-conference page > arXiv > journal", and
writes src/data/publications.json (consumed by the site's publications page).

Usage:
    python3 scripts/fetch_publications.py            # incremental: add new papers, keep existing
    python3 scripts/fetch_publications.py --refresh  # rebuild the whole file from DBLP

Only standard library is used. No PDFs are downloaded — links only.

NOTE on identity: the group is identified by its members' CASIA emails
(nlpr.ia.ac.cn / ia.ac.cn). DBLP does not index by email, so each author is
configured with their email (for the record) AND their DBLP PID, which is the
stable handle the crawler actually queries. Resolve a PID once from
https://dblp.org/search/author/api?q=<name>&format=json and paste it below.
"""

from __future__ import annotations
import argparse
import json
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

# ----------------------------------------------------------------------------
# CONFIG — edit here. One entry per group member. `pid` is the DBLP person id
# (the part after /pid/ in the DBLP URL). `email` is the CASIA identity anchor.
# To add a new member later: add a row and re-run (incremental by default).
# ----------------------------------------------------------------------------
AUTHORS = [
    {"name_zh": "赵军",   "name_en": "Jun Zhao",     "email": "jzhao@nlpr.ia.ac.cn",       "pid": "47/2026-1"},
    {"name_zh": "刘康",   "name_en": "Kang Liu",     "email": "kliu@nlpr.ia.ac.cn",        "pid": "42/4903"},
    {"name_zh": "何世柱", "name_en": "Shizhu He",    "email": "shizhu.he@nlpr.ia.ac.cn",   "pid": "136/8650"},
    {"name_zh": "曹鹏飞", "name_en": "Pengfei Cao",  "email": "pengfei.cao@nlpr.ia.ac.cn", "pid": "182/7941"},
    {"name_zh": "金卓然", "name_en": "Zhuoran Jin",  "email": "",                          "pid": "320/9888"},
    {"name_zh": "陈玉博", "name_en": "Yubo Chen",    "email": "yubo.chen@nlpr.ia.ac.cn",   "pid": "90/7879"},
    {"name_zh": "张元哲", "name_en": "Yuanzhe Zhang","email": "yzzhang@nlpr.ia.ac.cn",     "pid": "141/4448"},
    {"name_zh": "郭少茹", "name_en": "Shaoru Guo",   "email": "",                          "pid": "190/7914"},
]

OUTPUT = Path(__file__).resolve().parent.parent / "src" / "data" / "publications.json"
DBLP_PID_XML = "https://dblp.org/pid/{pid}.xml"
REQUEST_DELAY = 2.0  # be polite to DBLP
USER_AGENT = "NLPKE-site-pub-crawler/1.0 (research group website; contact jzhao@nlpr.ia.ac.cn)"

# Hosts that serve the open, official "main conference" version (preferred).
OPEN_VENUE_HOSTS = (
    "aclanthology.org", "aclweb.org", "openreview.net", "ojs.aaai.org",
    "aaai.org", "proceedings.mlr.press", "proceedings.neurips.cc",
    "papers.nips.cc", "jmlr.org", "openaccess.thecvf.com",
)
# Paywalled / journal hosts (last resort).
JOURNAL_HOSTS = ("ieeexplore.ieee.org", "dl.acm.org", "link.springer.com", "sciencedirect.com", "onlinelibrary.wiley.com")

ARXIV_ID_RE = re.compile(r"(\d{4}\.\d{4,5})")

# Homonym defense: DBLP person profiles for common names (Pengfei Cao, Kang Liu,
# Jun Zhao, ...) get contaminated with same-name authors from other fields
# (image encryption, bioinformatics, blockchain, ...). A paper is accepted as
# the group's only if it has >=2 distinct configured members as coauthors
# (two homonyms co-authoring is vanishingly rare), OR exactly one member at a
# strict NLP venue (pure-NLP venues almost never collide with the homonyms).
CORE_NAMES = [a["name_en"] for a in AUTHORS]
STRICT_NLP_VENUES = (
    "acl", "emnlp", "naacl", "coling", "tacl", "computational linguistics",
    "comput. linguist", "findings",
)


def group_author_count(authors_str: str) -> int:
    return sum(1 for n in CORE_NAMES if n in authors_str)


def is_strict_nlp(venue: str) -> bool:
    vl = venue.lower()
    return any(k in vl for k in STRICT_NLP_VENUES)


def is_group_paper(entry: dict) -> bool:
    n = group_author_count(entry["authors"])
    return n >= 2 or (n == 1 and is_strict_nlp(entry["venue"]))


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", t.lower())


def clean_authors(names: list[str]) -> str:
    # DBLP appends a homonym suffix like "Jun Zhao 0001" — strip the trailing digits.
    out = [re.sub(r"\s+\d{4}$", "", n).strip() for n in names]
    return ", ".join(out)


def clean_venue(raw: str, year: str) -> str:
    if not raw:
        return year
    v = re.sub(r"\s*\(\d+\)\s*$", "", raw).strip()  # drop "ACL (1)" volume markers
    return f"{v} {year}".strip()


def normalize_arxiv(url: str) -> str | None:
    if "arxiv.org" in url:
        return url
    if "10.48550/arXiv." in url or "arxiv" in url.lower():
        m = ARXIV_ID_RE.search(url)
        if m:
            return f"https://arxiv.org/abs/{m.group(1)}"
    return None


def classify_links(ees: list[str]) -> dict:
    """Return {paper, arxiv} following: main-conf official > arXiv > journal."""
    arxiv = None
    open_venue = None
    journal = None
    for url in ees:
        ax = normalize_arxiv(url)
        if ax:
            arxiv = arxiv or ax
            continue
        host = url.split("/")[2] if "://" in url else url
        if any(h in host for h in OPEN_VENUE_HOSTS):
            open_venue = open_venue or url
        elif any(h in host for h in JOURNAL_HOSTS) or "doi.org" in host:
            journal = journal or url
        else:
            journal = journal or url  # unknown host → treat as fallback
    links = {}
    paper = open_venue or journal  # official page (open preferred, journal last)
    if paper:
        links["paper"] = paper
    if arxiv:
        links["arxiv"] = arxiv
    return links


def parse_person(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    pubs = []
    for r in root.findall("r"):
        for el in r:  # one publication element per <r>
            tag = el.tag
            if tag not in ("inproceedings", "article", "incollection"):
                continue
            key = el.get("key", "")
            title_el = el.find("title")
            if title_el is None or not (title_el.text or "".join(title_el.itertext())):
                continue
            title = "".join(title_el.itertext()).strip().rstrip(".")
            year = (el.findtext("year") or "").strip()
            if not year:
                continue
            authors = [a.text for a in el.findall("author") if a.text]
            venue_raw = el.findtext("booktitle") or el.findtext("journal") or ""
            ees = [e.text for e in el.findall("ee") if e.text]
            pubs.append({
                "key": key,
                "title": title,
                "authors": authors,
                "year": int(year),
                "venue_raw": venue_raw,
                "ees": ees,
                "is_corr": key.startswith("journals/corr"),
            })
    return pubs


def build_entries(raw_pubs: list[dict]) -> list[dict]:
    # Dedupe by DBLP key (identical across coauthors).
    by_key: dict[str, dict] = {}
    for p in raw_pubs:
        by_key.setdefault(p["key"], p)

    published = [p for p in by_key.values() if not p["is_corr"]]
    corr = [p for p in by_key.values() if p["is_corr"]]

    pub_by_title = {norm_title(p["title"]): p for p in published}

    entries: dict[str, dict] = {}

    def to_entry(p: dict, venue_override: str | None = None) -> dict:
        links = classify_links(p["ees"])
        return {
            "id": p["key"].replace("/", "-"),
            "dblpKey": p["key"],
            "title": p["title"],
            "authors": clean_authors(p["authors"]),
            "venue": venue_override or clean_venue(p["venue_raw"], str(p["year"])),
            "year": p["year"],
            "links": links,
        }

    for p in published:
        entries[p["key"]] = to_entry(p)

    # Merge arXiv preprints: attach arxiv link to the matching published paper,
    # else keep the preprint as a standalone entry.
    for c in corr:
        match = pub_by_title.get(norm_title(c["title"]))
        c_arxiv = classify_links(c["ees"]).get("arxiv")
        if match and c_arxiv:
            entries[match["key"]]["links"].setdefault("arxiv", c_arxiv)
        elif not match:
            entries[c["key"]] = to_entry(c, venue_override=f"arXiv {c['year']}")

    return list(entries.values())


def load_existing() -> list[dict]:
    if OUTPUT.exists():
        try:
            return json.loads(OUTPUT.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="rebuild from scratch (default: incremental append)")
    args = ap.parse_args()

    all_raw: list[dict] = []
    for a in AUTHORS:
        url = DBLP_PID_XML.format(pid=a["pid"])
        print(f"[dblp] {a['name_en']} ({a['pid']}) ...", flush=True)
        try:
            all_raw.extend(parse_person(fetch(url)))
        except Exception as e:
            print(f"  !! failed for {a['name_en']}: {e}", file=sys.stderr)
        time.sleep(REQUEST_DELAY)

    crawled_all = build_entries(all_raw)
    crawled = [e for e in crawled_all if is_group_paper(e)]
    print(f"[crawl] {len(crawled_all)} unique after dedup → {len(crawled)} after homonym filter")

    if args.refresh:
        merged = {e["id"]: e for e in crawled}
    else:
        merged = {e["id"]: e for e in load_existing()}
        added = 0
        for e in crawled:
            if e["id"] not in merged:
                merged[e["id"]] = e
                added += 1
        print(f"[merge] incremental: +{added} new (kept {len(merged) - added} existing)")

    out = sorted(merged.values(), key=lambda e: (-e["year"], e["title"].lower()))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[done] wrote {len(out)} entries → {OUTPUT.relative_to(OUTPUT.parent.parent.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
