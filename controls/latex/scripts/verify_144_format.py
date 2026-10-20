#!/usr/bin/env python3
"""Repeatable technical evidence check for the enumerated PU 144-rule audit.

Never labels a thesis "144/144 certified" from compiler exit or PDF geometry
alone. Unknown/partial rules remain open and user-reported university acceptance
is different from an independently evidenced university certificate.

Usage:
  python controls/latex/scripts/verify_144_format.py \
    controls/latex/audits/PU144_RSH002_CP114_v2_5_RC1_20261020.json \
    --pdf /private/path/candidate.pdf --output qa_evidence.json

Requires PyMuPDF only when --pdf is supplied.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path
import re


def verify_inventory(audit: dict) -> tuple[list[str], dict]:
    issues = []
    rules = audit.get("entries", [])
    ids = [r.get("number") for r in rules]
    expected = set(range(1, 146)) - {76}
    if len(rules) != 144 or len(set(ids)) != 144 or set(ids) != expected:
        issues.append("Rule cardinality/identifier mismatch: original source has 144 IDs, excluding 076")
    recomputed = dict(collections.Counter(r.get("assessment") for r in rules))
    if recomputed != audit.get("summary"):
        issues.append("Rule status counts differ from the per-rule entries")
    if audit.get("all_rules_fully_certified") is not False:
        issues.append("Unjustified all-rules-certified flag; independent 144/144 evidence absent")
    for rule in rules:
        if not rule.get("approved_rule") or not rule.get("evidence_note"):
            issues.append(f"Missing source rule/evidence note: {rule.get('id')}")
    return issues, recomputed


def verify_pdf(path: Path) -> dict:
    import fitz

    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    document = fitz.open(path)
    counts = collections.Counter()
    all_pages_a4 = True
    linebreaks = []
    all_page_font_names = set()
    image_occurrences = 0
    for i, page in enumerate(document):
        all_pages_a4 &= abs(page.rect.width - 595.28) < 0.6 and abs(page.rect.height - 841.89) < 0.6
        raw = page.get_text()
        for m in re.finditer(r"\w+-\n\w+", raw):
            linebreaks.append({"page": i + 1, "sample": m.group(0)})
        image_occurrences += len(page.get_images())
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    counts[str(round(span["size"], 1))] += len(span["text"])
                    all_page_font_names.add(span["font"])
    return {
        "sha256": h.hexdigest(),
        "size_bytes": path.stat().st_size,
        "page_count": len(document),
        "all_pages_a4": bool(all_pages_a4),
        "lineend_hyphen_candidates": linebreaks,
        "lineend_hyphen_count": len(linebreaks),
        "image_occurrences": image_occurrences,
        "observed_fonts": sorted(all_page_font_names),
        "text_glyph_size_counts": dict(counts),
        "non_tnr_fonts_may_belong_to_embedded_figures": True,
        "human_visual_certification": "NOT_DERIVED_FROM_THIS_CHECKER",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit", type=Path, help="Full, rule-by-rule v2.5 audit JSON")
    parser.add_argument("--pdf", type=Path, help="Target compiled PDF")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    audit = json.loads(args.audit.read_text(encoding="utf-8"))
    issues, groups = verify_inventory(audit)
    observations = verify_pdf(args.pdf) if args.pdf else None
    if observations:
        desired = audit["candidate"].get("local_pdf_sha256")
        if desired and observations["sha256"] != desired:
            issues.append("PDF SHA256 differs from frozen audited candidate")
        if not observations["all_pages_a4"]:
            issues.append("At least one PDF page is not A4")
        if observations["page_count"] != 115:
            issues.append("Page count differs from recorded 115-page CP114 candidate")
    result = {
        "status": "FAIL_INVENTORY_OR_INPUT" if issues else "PASS_TECHNICAL_INVENTORY_ONLY",
        "all_144_rules_certified": False,
        "inventory_count": len(audit.get("entries", [])),
        "group_counts": groups,
        "open_or_partial_rules": sum(v for k, v in groups.items() if k != "TECHNICALLY_VERIFIED"),
        "university_signed_certificate_checked": False,
        "scientific_release_unchanged": True,
        "pdf_observations": observations,
        "errors": issues,
    }
    output = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)
    return 2 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
