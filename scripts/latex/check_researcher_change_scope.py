#!/usr/bin/env python3
"""Fail-closed changed-file ownership and pinned shared-style QA for thesis PRs.

Legacy branches are checked for cross-researcher scientific mixing without
retroactively renaming them. New thesis/ and template/ namespaces are strict.
"""
from __future__ import annotations
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THESIS = re.compile(r"^thesis/([a-z0-9-]+)/latex/seq([0-9]{3,})-[a-z0-9-]+$")
TEMPLATE = re.compile(r"^template/latex/v[0-9]+(?:[.-][0-9A-Za-z-]+)*$")
STY = "controls/latex/template/pumlsc-shared.sty"
REGISTRY = "registry/researcher-latex-sequences.json"
TOWER = "controls/latex/tower.json"
# Unambiguous historical namespaces; never infer 'safal/' ownership (two Safals).
LEGACY_OWNER_ALIASES = {"saugat": "saugat-paneru", "nabin": "nabin-bista"}


def out(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def changed(base: str, head: str) -> list[str]:
    return [s for s in out(["diff", "--name-only", "--diff-filter=ACMRT", base + "..." + head]).splitlines() if s]


def sources(files: list[str]) -> set[str]:
    return {match.group(1) for f in files
            if (match := re.match(r"^researchers/([^/]+)/latex/", f))}


def evaluate(branch: str, files: list[str], manifest: dict | None, style_sha: str | None) -> list[str]:
    errors: list[str] = []
    owners = sources(files)
    if len(owners) > 1:
        errors.append("CROSS_RESEARCHER_LATEX_EDIT: " + ", ".join(sorted(owners)))
    # Even a one-researcher PR must not silently include global LaTeX control edits.
    if owners and any(f.startswith("controls/latex/") for f in files):
        errors.append("SCIENTIFIC_AND_SHARED_CONTROL_MUTATION_REQUIRE_SEPARATE_PRS")
    alias = LEGACY_OWNER_ALIASES.get(branch.split("/", 1)[0])
    legacy_match = re.fullmatch(r"researcher/([a-z0-9-]+)/latex(?:/.*)?", branch)
    if legacy_match:
        alias = legacy_match.group(1)
    if alias and owners and owners != {alias}:
        errors.append("LEGACY_BRANCH_OWNER_MISMATCH: {} -> {}".format(branch, ", ".join(sorted(owners))))
    m = THESIS.fullmatch(branch)
    if m:
        slug, seq_text = m.groups()
        seq = int(seq_text)
        root = "researchers/{}/latex/".format(slug)
        bad = [f for f in files if not f.startswith(root)]
        if bad:
            errors.append("THESIS_BRANCH_OUTSIDE_OWNER_SCOPE: " + ", ".join(bad))
        if manifest is None:
            errors.append("MISSING_RESEARCHER_SEQUENCE_MANIFEST")
        else:
            if manifest.get("slug") != slug or manifest.get("sequence") != seq or manifest.get("branch") != branch:
                errors.append("MANIFEST_OWNER_SEQUENCE_BRANCH_MISMATCH")
            if manifest.get("style_path") != STY:
                errors.append("SHARED_TEMPLATE_PATH_MISMATCH")
            if manifest.get("style_blob_sha") != style_sha:
                errors.append("STYLE_SHA_DRIFT__PIN_UPDATE_AND_REGRESSION_REQUIRED")
            if manifest.get("status") not in ("RESERVED_SOURCE_ONLY", "EDITING", "QA_CANDIDATE", "MERGED", "RELEASED"):
                errors.append("UNKNOWN_MANIFEST_ADMISSION_STATE")
    elif TEMPLATE.fullmatch(branch):
        if owners:
            errors.append("GLOBAL_TEMPLATE_BRANCH_MUST_NOT_CHANGE_RESEARCHER_SCIENCE")
        allowed = ("controls/latex/", "scripts/latex/", "docs/", ".github/workflows/", "registry/latex-inheritance.json")
        bad = [f for f in files if not any(f.startswith(pre) for pre in allowed)]
        if bad:
            errors.append("GLOBAL_TEMPLATE_BRANCH_OUTSIDE_SCOPE: " + ", ".join(bad))
        if STY in files and ("controls/latex/change-register.json" not in files or TOWER not in files):
            errors.append("GLOBAL_TEMPLATE_AMENDMENT_AND_VERSION_REQUIRED")
    else:
        # Preserve older active workstreams, but never allow scientific mixing
        # or silent global .sty edits through an unscoped legacy branch.
        if STY in files:
            errors.append("UNSCOPED_GLOBAL_TEMPLATE_CHANGE_REQUIRES_TEMPLATE_BRANCH")
        if owners:
            print("LEGACY_LANE_WARNING: use thesis/<slug>/latex/seqNNN-topic for subsequent numbered revisions")
    for f in files:
        if f.endswith((".pdf", ".zip", ".ttf", ".otf", ".woff", ".woff2")) and f.startswith("researchers/"):
            errors.append("PRIVATE_BINARY_IN_PUBLIC_GIT: " + f)
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--branch", default=os.getenv("GITHUB_HEAD_REF") or os.getenv("GITHUB_REF_NAME", ""))
    parser.add_argument("--self-test", action="store_true")
    a = parser.parse_args()
    if a.self_test:
        correct = {
            "slug": "nabin-bista", "branch": "thesis/nabin-bista/latex/seq055-more-results",
            "sequence": 55, "style_path": STY, "style_blob_sha": "test", "status": "EDITING"
        }
        assert not evaluate(correct["branch"], ["researchers/nabin-bista/latex/versions/seq055.json"], correct, "test")
        assert evaluate(correct["branch"], ["researchers/saugat-paneru/latex/foo.tex"], correct, "test")
        assert evaluate(correct["branch"], ["researchers/nabin-bista/latex/foo.tex"], correct, "changed")
        assert evaluate("template/latex/v2.5.0", [STY], None, None)
        assert not evaluate("template/latex/v2.5.0", [STY, TOWER, "controls/latex/change-register.json"], None, None)
        assert evaluate("feature/mixed", ["researchers/nabin-bista/latex/a.tex", "researchers/saugat-paneru/latex/b.tex"], None, None)
        # A legacy researcher-named branch cannot change another person's source,
        # even if it changes only one researcher's directory.
        assert evaluate("saugat/editorial-m4", ["researchers/nabin-bista/latex/chapters/ch4.tex"], None, None)
        assert evaluate("nabin/ch4", ["researchers/saugat-paneru/latex/manuscript/main.tex"], None, None)
        assert evaluate("researcher/saugat-paneru/latex", ["researchers/nabin-bista/latex/chapters/ch4.tex"], None, None)
        assert not evaluate("saugat/editorial-m4", ["researchers/saugat-paneru/latex/manuscript/main.tex"], None, None)
        assert not evaluate("nabin/ch4", ["researchers/nabin-bista/latex/chapters/ch4.tex"], None, None)
        assert evaluate("saugat/editorial-m4", ["researchers/saugat-paneru/latex/chapters/ch4.tex", "controls/latex/core-rules.json"], None, None)
        print("LATEX_OWNERSHIP_SELF_TEST_PASS")
        return
    files = changed(a.base, a.head)
    m = THESIS.fullmatch(a.branch)
    manifest = None
    if m:
        slug, num = m.groups()
        path = ROOT / "researchers" / slug / "latex" / "versions" / ("seq" + num + ".json")
        if path.is_file():
            manifest = json.loads(path.read_text(encoding="utf-8"))
        else:
            # Sequence field is unpadded numeric; bootstrap paths always use 3 digits
            alt = ROOT / "researchers" / slug / "latex" / "versions" / ("seq{:03d}.json".format(int(num)))
            if alt.exists():
                manifest = json.loads(alt.read_text(encoding="utf-8"))
    style = out(["hash-object", STY])
    problems = evaluate(a.branch, files, manifest, style)
    if m:
        data = json.loads((ROOT / REGISTRY).read_text(encoding="utf-8"))
        if m.group(1) not in [x["slug"] for x in data["researchers"]]:
            problems.append("UNREGISTERED_RESEARCHER")
        row = next((x for x in data["researchers"] if x["slug"] == m.group(1)), None)
        if row is not None and not any(x["sequence"] == int(m.group(2)) and x["branch"] == a.branch for x in row["reservations"]):
            problems.append("SEQ_NOT_RESERVED_IN_CANONICAL_LEDGER")
    if TEMPLATE.fullmatch(a.branch) and STY in files:
        def git_json(ref: str, name: str):
            return json.loads(out(["show", ref + ":" + name]))
        before = git_json(a.base, TOWER)
        after = json.loads((ROOT / TOWER).read_text(encoding="utf-8"))
        def vtuple(v: str):
            m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", v)
            if not m:
                raise ValueError("Invalid template semantic version: " + v)
            return tuple(int(x) for x in m.groups())
        if vtuple(after["version"]) <= vtuple(before["version"]):
            problems.append("GLOBAL_TEMPLATE_SEMVER_NOT_INCREASED")
        old_register = git_json(a.base, "controls/latex/change-register.json")
        new_register = json.loads((ROOT / "controls/latex/change-register.json").read_text(encoding="utf-8"))
        if len(new_register["entries"]) <= len(old_register["entries"]) or not any(
            x.get("classification") == "GLOBAL_CANDIDATE"
            for x in new_register["entries"][len(old_register["entries"]):]
        ):
            problems.append("NO_NEW_GLOBAL_CANDIDATE_CHANGE_RECORD")
        # This is a source QA guard; actual A4/font/render parity must be
        # evidenced separately for each buildable researcher before promotion.
    if problems:
        print("LATEX_SCOPE_GATE_FAIL:\n- " + "\n- ".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print("LATEX_SCOPE_GATE_PASS {} files={} branch={}".format(len(owners := sources(files)), len(files), a.branch))


if __name__ == "__main__":
    main()
