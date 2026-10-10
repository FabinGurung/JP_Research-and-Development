#!/usr/bin/env python3
"""Advisory, read-only semantic lint of LaTeX prose from the ONE shared R&D tower.

No automatic rewriting, scientific certification, cross-researcher content transfer or
private image access. --fail-on-warning is an opt-in reviewer gate.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = "controls/latex/authorial-voice-policy.json"
SELF_REFERENCE = re.compile(
    r"\bthe researcher\s+(?:report(?:s|ed)?|state(?:s|d)?|observ(?:e|ed|es)|"
    r"identif(?:y|ied|ies)|describ(?:e|ed|es)|supervis(?:e|ed|es)|"
    r"perform(?:s|ed)?|not(?:e|ed|es)|was|is)\b", re.I
)
ADMIN_VOICE = re.compile(r"\b(?:researcher-reported|researcher-identified|practitioner-supplied)\b", re.I)
PHOTO_ID = re.compile(r"\b[A-Z][A-Z0-9_-]*PHOTO-[A-Z0-9_-]{2,}\b")
CASE_ID = re.compile(r"\b(?:W0[1-9]|CASE-[A-Z0-9-]{3,}|A9-[A-Z0-9-]{3,})\b")
PRIVATE_ARG = re.compile(
    r"\\(?:includegraphics|input|label|ref|pageref|addbibresource|url)"
    r"(?:\[[^\]]*\])?\{[^{}]*\}"
)
FILE_TEST = re.compile(r"\\IfFileExists\{[^{}]*\}")
COMMENT = re.compile(r"(?<!\\)%.*$")

def visible_line(line: str) -> str:
    """Keep probable visible wording; exclude TeX paths, refs, and comments."""
    s = COMMENT.sub("", line)
    s = FILE_TEST.sub(" ", s)
    s = PRIVATE_ARG.sub(" ", s)
    # Image path arguments must not be interpreted as printed captions.
    s = re.sub(r"private_photos/[A-Za-z0-9_.-]+", " ", s)
    return s

def inspect_text(content: str, path: str = "<sample>") -> list[dict]:
    out = []
    patterns = (
        ("STUDENT_SELF_THIRD_PERSON_REVIEW", SELF_REFERENCE),
        ("ADMINISTRATIVE_PROSE_REVIEW", ADMIN_VOICE),
        ("PRINTED_PHOTO_IDENTIFIER_REVIEW", PHOTO_ID),
        ("INTERNAL_CASE_CODE_REVIEW", CASE_ID),
    )
    for lineno, line in enumerate(content.splitlines(), 1):
        shown = visible_line(line)
        for rule, pattern in patterns:
            for hit in pattern.finditer(shown):
                out.append({"file": path, "line": lineno, "rule": rule,
                            "sample": hit.group(0), "level": "REVIEW"})
    return out

def sources(root: Path, researcher: str | None) -> list[Path]:
    base = root / "researchers"
    if researcher:
        slug = researcher.lower()
        registry = json.loads((root / "registry/researchers.json").read_text(encoding="utf-8"))
        found = next((row for row in registry["researchers"]
                      if slug in (row["slug"], row["researcher_id"].lower())), None)
        if found is None:
            raise ValueError("Unknown researcher; select a registered RSH identifier or slug")
        folders = [base / found["slug"]]
    else:
        folders = sorted(p for p in base.iterdir() if p.is_dir())
    files = []
    for folder in folders:
        manuscript = folder / "latex/manuscript"
        for section in ("chapters", "appendices"):
            files.extend(sorted((manuscript / section).glob("*.tex")))
        abstract = manuscript / "frontmatter/abstract.tex"
        if abstract.is_file():
            files.append(abstract)
    return files

def self_test() -> None:
    samples = [
        (r"The researcher observed the wall.", "STUDENT_SELF_THIRD_PERSON_REVIEW", True),
        (r"The report contains practitioner-supplied descriptions.", "ADMINISTRATIVE_PROSE_REVIEW", True),
        (r"\caption{SAFAL-PHOTO-W02B-01}", "PRINTED_PHOTO_IDENTIFIER_REVIEW", True),
        (r"\includegraphics{private_photos/SAFAL-PHOTO-W01-01.jpg}", "PRINTED_PHOTO_IDENTIFIER_REVIEW", False),
        (r"\IfFileExists{private_photos/SAFAL-PHOTO-W01-01.jpg}{\includegraphics{private_photos/SAFAL-PHOTO-W01-01.jpg}}{}", "PRINTED_PHOTO_IDENTIFIER_REVIEW", False),
        ("I observed the wall during my visit.", "STUDENT_SELF_THIRD_PERSON_REVIEW", False),
        ("% The researcher observed; invisible TeX comment", "STUDENT_SELF_THIRD_PERSON_REVIEW", False),
        (r"\caption{Door-threshold waterproofing during repair}", "PRINTED_PHOTO_IDENTIFIER_REVIEW", False),
    ]
    for text, rule, expected in samples:
        found = any(item["rule"] == rule for item in inspect_text(text))
        if found != expected:
            raise AssertionError(f"{rule} expected={expected} found={found}: {text}")
    print(f"SEMANTIC SELF-TEST PASS ({len(samples)} cases; advisory/no source edits)")

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--researcher", help="RSH identifier or registered researcher slug")
    p.add_argument("--json", action="store_true", help="Emit only machine-readable JSON")
    p.add_argument("--fail-on-warning", action="store_true", help="Opt-in review gate; not default CI")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return 0
    root = args.root.resolve()
    policy = json.loads((root / CONFIG).read_text(encoding="utf-8"))
    if policy.get("canonical_owner") != "controls/latex/tower.json":
        raise ValueError("Competing semantic control tower")
    findings = []
    for path in sources(root, args.researcher):
        findings.extend(inspect_text(path.read_text(encoding="utf-8"),
                                     path.relative_to(root).as_posix()))
    result = {
        "policy_id": policy["policy_id"],
        "mode": "ADVISORY_REVIEW_ONLY",
        "source_files_scanned": len(sources(root, args.researcher)),
        "warning_count": len(findings),
        "findings": findings,
        "scientific_approval": "NOT_TESTED",
        "automatic_text_edits": False,
    }
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"SEMANTIC SOURCE QA: {result['source_files_scanned']} files, "
              f"{len(findings)} advisory warnings")
        for hit in findings:
            print(f"{hit['file']}:{hit['line']} {hit['rule']}: {hit['sample']}")
        print("Warnings need human contextual review; they are NOT proof of fabrication.")
    return 1 if args.fail_on_warning and findings else 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError) as err:
        print(f"SEMANTIC POLICY ERROR: {err}", file=sys.stderr)
        sys.exit(2)
