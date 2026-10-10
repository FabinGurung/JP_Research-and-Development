#!/usr/bin/env python3
"""Advisory content lint for student-facing TeX; never changes scientific prose."""
import argparse
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CONTROL = REPO / "controls/latex/authorial-voice-policy.json"
PHOTO_PATTERN = re.compile(r"\b[A-Z][A-Z0-9-]*PHOTO-[A-Z0-9-]+\b")
TECH_CODE = re.compile(r"\\bW0[1-9]\\b")
STUDENT_AS_THIRD_PERSON = re.compile(r"\\bthe researcher\\s+(?:reports?|states?|identified|observed|examined|described|found|did|used)\\b", re.I)
ADMIN = re.compile(r"\\b(?:researcher-reported|researcher-identified)\\b", re.I)


def visible_text(tex: str) -> str:
    """Remove comments, TeX graphics args and refs, preserving paragraph text."""
    cleaned = []
    for raw in tex.splitlines():
        # Treat unescaped '%' as start of comment.
        line = re.split(r"(?<!\\)%", raw, maxsplit=1)[0]
        # Internal private photo paths are not text printed on a typeset page.
        line = re.sub(r"private_photos/[A-Za-z0-9_.-]+", "", line)
        line = re.sub(r"\\(?:includegraphics|IfFileExists|label|ref|pageref|input|addbibresource)(?:\\[[^\\]]*\\])?(?:\\{[^{}]*\\})+", " ", line)
        cleaned.append(line)
    return "\n".join(cleaned)


def analyze(path: Path) -> list[dict]:
    text = visible_text(path.read_text(encoding="utf-8"))
    findings = []
    for label, pattern in (("SELF_THIRD_PERSON", STUDENT_AS_THIRD_PERSON),
                           ("INTERNAL_PHOTO_ID", PHOTO_PATTERN),
                           ("INTERNAL_CASE_CODE", TECH_CODE),
                           ("ADMIN_VOICE", ADMIN)):
        for hit in pattern.finditer(text):
            findings.append({"rule": label, "line": text.count("\n", 0, hit.start())+1, "sample": hit.group(0)})
    return findings


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=REPO)
    p.add_argument("--researcher", default=None, help="Optional researcher slug")
    p.add_argument("--fail-on-warning", action="store_true")
    args = p.parse_args()
    cfg = json.loads((args.root / "controls/latex/authorial-voice-policy.json").read_text())
    if cfg["status"].startswith("PROPOSED"):
        print("NOTICE: shared semantic guardrail is a PR proposal, not yet a canonical rule.")
    root = args.root / "researchers"
    projects = [root / args.researcher] if args.researcher else [r for r in root.iterdir() if r.is_dir()]
    report = {}
    for project in projects:
        manuscript = project / "latex/manuscript"
        if not manuscript.exists(): continue
        results={}
        for sub in ("chapters","appendices"):
            for source in (manuscript / sub).glob("*.tex"):
                if found := analyze(source): results[str(source.relative_to(args.root))]=found
        abstract=manuscript/"frontmatter/abstract.tex"
        if abstract.exists():
            if found := analyze(abstract):results[str(abstract.relative_to(args.root))]=found
        if results:report[project.name]=results
    print(json.dumps(report,indent=2))
    n=sum(len(f) for r in report.values() for f in r.values())
    print(f"Authorial-voice warnings: {n}; advisory only unless --fail-on-warning is set.")
    return 1 if n and args.fail_on_warning else 0


if __name__ == "__main__":
    raise SystemExit(main())
