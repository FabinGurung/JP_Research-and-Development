#!/usr/bin/env python3
"""One-repository per-researcher LaTeX sequence reservation. No science/PDF mutation.

Dry-run/check modes use only local files. --reserve opens a ledger-only PR.
--finalize bootstraps only an accepted reservation from canonical main.
Neither writes directly to main or force-pushes.
"""
from __future__ import annotations
import argparse
import base64
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
LEDGER = "registry/researcher-latex-sequences.json"
STYLE = "controls/latex/template/pumlsc-shared.sty"
TOWER = "controls/latex/tower.json"
TOPIC_RE = re.compile(r"[^a-z0-9]+")
BRANCH_RE = re.compile(r"^thesis/([a-z0-9-]+)/latex/seq([0-9]{3,})-([a-z0-9-]+)$")


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def normalize_topic(topic: str) -> str:
    value = TOPIC_RE.sub("-", topic.strip().lower()).strip("-")[:48].strip("-")
    if not value:
        raise ValueError("Topic must contain at least one alphanumeric character")
    return value


def validate(data: dict, enrolled: list[dict]) -> None:
    if data.get("id") != "RD-RESEARCHER-LATEX-SEQUENCE-REGISTER-001":
        raise ValueError("Wrong sequence register authority")
    rows = data.get("researchers")
    if not isinstance(rows, list):
        raise ValueError("Researcher rows absent")
    identities = [(r["researcher_id"], r["slug"]) for r in rows]
    expected = [(r["researcher_id"], r["slug"]) for r in enrolled]
    if len(identities) != len(set(identities)) or set(identities) != set(expected):
        raise ValueError("Sequence register differs from authoritative researcher enrollment")
    for row in rows:
        base = row["baseline"]
        floor = base["last_historical_sequence"]
        if floor is not None and (type(floor) is not int or floor < 0):
            raise ValueError("Invalid verified historical floor")
        if floor is None and base["status"] != "BASELINE_VERIFICATION_REQUIRED":
            raise ValueError("Unknown baseline must be held")
        if floor is not None and (base["status"] != "VERIFIED_CURRENT_REPOSITORY" or not base["source_path"]):
            raise ValueError("Verified baseline must cite source")
        # Existing release records produced outside the allocator are not reservations.
        # They still consume their sequence numbers; preserve the original historical floor.
        observed = row.get("observed_out_of_band_versions", [])
        if not isinstance(observed, list):
            raise ValueError("Malformed out-of-band version register for " + row["slug"])
        observed_nums = set()
        for recorded in observed:
            number = recorded.get("sequence")
            path = recorded.get("source_path", "")
            prefix = "researchers/{}/latex/releases/SEQ{:03d}".format(row["slug"], number) if type(number) is int and number > 0 else ""
            if (type(number) is not int or number <= (floor or 0)
                    or number in observed_nums or not path.startswith(prefix)
                    or recorded.get("status") != "EXISTING_GIT_RELEASE_RECORD__NOT_ALLOCATOR_RESERVED"
                    or not (ROOT / path).is_file()):
                raise ValueError("Invalid or unsupported observed release for " + row["slug"])
            observed_nums.add(number)
        if observed != sorted(observed, key=lambda x: x["sequence"]):
            raise ValueError("Observed releases must be in ascending sequence")
        used, maxval = set(), max([floor or 0, *observed_nums])
        for entry in row["reservations"]:
            seq = entry["sequence"]
            if type(seq) is not int or seq <= (floor or 0) or seq in used or seq in observed_nums:
                raise ValueError("Duplicate/invalid reserved sequence for " + row["slug"])
            used.add(seq)
            maxval = max(maxval, seq)
            if entry["status"] not in ("RESERVED", "EDITING", "MERGED", "RELEASED", "ABANDONED", "HOLD"):
                raise ValueError("Unrecognized sequence status")
            if not BRANCH_RE.fullmatch(entry["branch"]):
                raise ValueError("Invalid branch in registry")
            match = BRANCH_RE.fullmatch(entry["branch"])
            if match.group(1) != row["slug"] or int(match.group(2)) != seq:
                raise ValueError("Branch/owner/sequence mismatch")
        if row["reservations"] != sorted(row["reservations"], key=lambda x: x["sequence"]):
            raise ValueError("Reservations not in append order")


def plan(data: dict, slug: str, topic: str) -> dict:
    row = next((x for x in data["researchers"] if x["slug"] == slug), None)
    if not row:
        raise ValueError("Unregistered researcher: " + slug)
    floor = row["baseline"]["last_historical_sequence"]
    if floor is None:
        raise ValueError("HOLD_BASELINE_VERIFICATION_REQUIRED for " + slug)
    used = [x["sequence"] for x in row["reservations"]]
    observed = [x["sequence"] for x in row.get("observed_out_of_band_versions", [])]
    number = max([floor] + used + observed) + 1
    branch = "thesis/{}/latex/seq{:03d}-{}".format(slug, number, normalize_topic(topic))
    return {"researcher_id": row["researcher_id"], "slug": slug, "sequence": number, "branch": branch}


def remote_release_highwater(tree: dict, slug: str) -> int:
    """Inspect a real Git tree without inventing sequence allocations."""
    if tree.get("truncated") or not isinstance(tree.get("tree"), list):
        raise RuntimeError("REMOTE_TREE_INCOMPLETE__NO_SEQUENCE_RESERVATION")
    prefix = "researchers/{}/latex/".format(slug)
    numbers = [0]
    for entry in tree["tree"]:
        path = entry.get("path", "")
        if not path.startswith(prefix) or entry.get("type") != "blob":
            continue
        tail = path[len(prefix):]
        match = re.match(r"(?:releases/SEQ|versions/seq)([0-9]{3,})(?:[^0-9].*)?$", tail)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers)


def verify_remote_releases_reconciled(tree: dict, row: dict) -> None:
    remote_floor = remote_release_highwater(tree, row["slug"])
    ledger_floor = max([row["baseline"]["last_historical_sequence"] or 0]
                       + [x["sequence"] for x in row.get("observed_out_of_band_versions", [])]
                       + [x["sequence"] for x in row["reservations"]])
    if remote_floor > ledger_floor:
        raise RuntimeError(
            "UNREGISTERED_REMOTE_RELEASE_SEQ_{:03d}__RECONCILE_BEFORE_RESERVING".format(remote_floor)
        )


class Github:
    def __init__(self):
        self.repo = os.environ.get("GITHUB_REPOSITORY", "")
        self.token = os.environ.get("GH_TOKEN", "")
        if not self.repo or not self.token:
            raise RuntimeError("GITHUB_REPOSITORY and GH_TOKEN required")
        self.base = "https://api.github.com/repos/" + self.repo

    def api(self, method: str, path: str, body: dict | None = None):
        payload = json.dumps(body).encode() if body is not None else None
        req = Request(self.base + path, data=payload, method=method)
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("Authorization", "Bearer " + self.token)
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        if payload is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with urlopen(req, timeout=30) as response:
                return json.load(response), response.status
        except HTTPError as e:
            data = e.read().decode(errors="replace")[:1200]
            if e.code in (404, 409, 422):
                return {"error": data}, e.code
            raise RuntimeError("GitHub HTTP {}: {}".format(e.code, data)) from e

    def file(self, path: str, ref: str):
        data, status = self.api("GET", "/contents/{}?ref={}".format(quote(path), quote(ref)))
        if status != 200 or not isinstance(data, dict):
            raise RuntimeError("GitHub file read failed: " + path + " " + str(status))
        return data, base64.b64decode(data["content"]).decode("utf-8")

    def main_sha(self) -> str:
        a, code = self.api("GET", "/branches/main")
        if code != 200:
            raise RuntimeError("Cannot read main")
        return a["commit"]["sha"]


def require_action():
    if os.getenv("GITHUB_ACTIONS") != "true" or os.getenv("GITHUB_REF") != "refs/heads/main":
        raise RuntimeError("Reservation must run via authorized GitHub Actions from main")


def reservation_delta(before: dict, after: dict, request_branch: str) -> None:
    """Exactly one next-number append; all previous history and policy immutable."""
    import copy
    expected = copy.deepcopy(before)
    additions = []
    for old, new in zip(before["researchers"], after["researchers"]):
        if len(new["reservations"]) == len(old["reservations"]) + 1:
            item = new["reservations"][-1]
            match = BRANCH_RE.fullmatch(item.get("branch", ""))
            if match is None:
                raise ValueError("Malformed reservation branch")
            candidate = plan(before, old["slug"], match.group(3))
            if any(item.get(k) != v for k, v in candidate.items()):
                raise ValueError("Reservation is not the next canonical sequence")
            if item.get("status") != "RESERVED" or not item.get("request_key"):
                raise ValueError("New reservation must have RESERVED state and request key")
            if request_branch != "reservation/latex/" + item["request_key"].replace(":", "-"):
                raise ValueError("Reservation branch/request key mismatch")
            expected["researchers"][before["researchers"].index(old)]["reservations"].append(item)
            additions.append(item)
    if len(additions) != 1 or after != expected:
        raise ValueError("Reservation PR must append exactly one entry without changing history")


def reserve(slug: str, topic: str, make_pr: bool) -> None:
    require_action()
    gh = Github()
    key = "gha:" + os.environ["GITHUB_RUN_ID"]
    request_branch = "reservation/latex/" + key.replace(":", "-")
    current_main = gh.main_sha()
    obj, original = gh.file(LEDGER, current_main)
    data = json.loads(original)
    _, enrolled_text = gh.file("registry/researchers.json", current_main)
    enrolled = json.loads(enrolled_text)["researchers"]
    validate(data, enrolled)
    row = next((x for x in data["researchers"] if x["slug"] == slug), None)
    if row is None:
        raise RuntimeError("Unregistered researcher")
    tree, code = gh.api("GET", "/git/trees/" + current_main + "?recursive=1")
    if code != 200:
        raise RuntimeError("CANNOT_VERIFY_CURRENT_MAIN_RELEASE_TREE")
    verify_remote_releases_reconciled(tree, row)
    info = plan(data, slug, topic)
    _, status = gh.api("GET", "/git/ref/heads/" + quote(info["branch"], safe="/"))
    if status != 404:
        raise RuntimeError("Researcher branch collision or uniqueness unavailable")
    template, _ = gh.file(STYLE, current_main)
    item = {**info, "status": "RESERVED", "request_key": key,
            "created_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "main_sha_at_reservation": current_main, "template_sha": template["sha"],
            "note": "Reservation effective only after this PR merges; no science/PDF change"}
    row["reservations"].append(item)
    validate(data, enrolled)
    reservation_delta(json.loads(original), data, request_branch)
    branch, code = gh.api("GET", "/git/ref/heads/" + quote(request_branch, safe="/"))
    if code == 404:
        branch, code = gh.api("POST", "/git/refs", {"ref": "refs/heads/" + request_branch, "sha": current_main})
        if code != 201:
            raise RuntimeError("Cannot create reservation proposal branch")
        result, code = gh.api("PUT", "/contents/" + quote(LEDGER), {
            "message": "reserve(latex): propose " + info["branch"],
            "content": base64.b64encode((json.dumps(data, indent=2) + "\n").encode()).decode(),
            "sha": obj["sha"], "branch": request_branch})
        if code not in (200, 201):
            raise RuntimeError("Reservation proposal write failed; retry/reconcile branch: " + str(result))
    elif code == 200:
        _, existing_text = gh.file(LEDGER, request_branch)
        existing_data = json.loads(existing_text)
        reservation_delta(json.loads(original), existing_data, request_branch)
        existing = next(x for x in existing_data["researchers"] if x["slug"] == slug)["reservations"][-1]
        if existing["request_key"] != key or existing["branch"] != info["branch"]:
            raise RuntimeError("Existing request differs; reconcile instead of overwriting")
    else:
        raise RuntimeError("Cannot verify proposal branch")
    prs, code = gh.api("GET", "/pulls?state=open&head=" + quote(gh.repo.split('/')[0] + ':' + request_branch))
    if code != 200:
        raise RuntimeError("Cannot inspect existing reservation PR")
    if prs:
        print("RESERVATION_PR " + prs[0]["html_url"])
        return
    result, code = gh.api("POST", "/pulls", {
        "title": "Reserve " + info["branch"], "head": request_branch, "base": "main",
        "body": "Ledger-only reservation proposal. Merge only through required validate on current main. Then run finalize with request key `" + key + "`. This PR does not admit science, create a researcher branch or promote CURRENT."})
    if code != 201:
        raise RuntimeError("Reservation PR creation failed: " + str(result))
    print("RESERVATION_PR " + result["html_url"] + " REQUEST_KEY=" + key)


def finalize(slug: str, key: str, make_pr: bool) -> None:
    require_action()
    gh = Github()
    starting_sha = gh.main_sha()
    _, text = gh.file(LEDGER, starting_sha)
    data = json.loads(text)
    _, enrolled = gh.file("registry/researchers.json", starting_sha)
    validate(data, json.loads(enrolled)["researchers"])
    row = next((x for x in data["researchers"] if x["slug"] == slug), None)
    info = next((x for x in (row or {}).get("reservations", []) if x["request_key"] == key), None)
    if info is None or info["status"] != "RESERVED":
        raise RuntimeError("No accepted RESERVED entry for this owner/request on canonical main")
    branch = info["branch"]
    branch_ref, bstatus = gh.api("GET", "/git/ref/heads/" + quote(branch, safe="/"))
    if bstatus == 404:
        branch_ref, bstatus = gh.api("POST", "/git/refs", {"ref": "refs/heads/" + branch, "sha": starting_sha})
        if bstatus != 201:
            raise RuntimeError("Sequence reserved but branch creation failed; manual recovery required: " + str(branch_ref))
    if bstatus not in (200, 201):
        raise RuntimeError("Cannot verify researcher branch: " + str(branch_ref))

    template, _ = gh.file(STYLE, branch)
    tower_obj, tower_text = gh.file(TOWER, branch)
    tower = json.loads(tower_text)
    manifest_path = "researchers/{}/latex/versions/seq{:03d}.json".format(slug, info["sequence"])
    manifest = {
        "schema_version": "1.0.0", "researcher_id": info["researcher_id"], "slug": slug,
        "lane": "latex", "sequence": info["sequence"], "status": "RESERVED_SOURCE_ONLY",
        "scientific_checkpoint": None, "scientific_admission": "NOT_INFERRED",
        "branch": branch, "branch_base_sha": branch_ref["object"]["sha"],
        "style_path": STYLE, "style_blob_sha": template["sha"],
        "style_version": tower["version"], "style_source_commit": branch_ref["object"]["sha"],
        "source_post_sha": None, "pdf_drive_id": None, "pdf_sha256": None,
        "source_zip_drive_id": None, "source_zip_sha256": None,
        "approval": None, "request_key": key
    }
    existing, st = gh.api("GET", "/contents/{}?ref={}".format(quote(manifest_path), quote(branch)))
    if st == 404:
        result, status = gh.api("PUT", "/contents/" + quote(manifest_path), {
            "message": "thesis({}): initialize seq{:03d} pinned shared template manifest".format(slug, info["sequence"]),
            "content": base64.b64encode((json.dumps(manifest, indent=2) + "\n").encode()).decode(),
            "branch": branch
        })
        if status != 201:
            raise RuntimeError("Reserved/branch created but manifest write failed: " + str(result))
    elif st == 200:
        _, old = gh.file(manifest_path, branch)
        existing_manifest = json.loads(old)
        for field in ("request_key", "slug", "sequence", "branch", "style_blob_sha"):
            if existing_manifest.get(field) != manifest[field]:
                raise RuntimeError("Manifest collision or template drift: " + field)
    else:
        raise RuntimeError("Cannot check manifest")
    print("BRANCH_READY " + branch + " STYLE_PIN=" + template["sha"])
    if make_pr:
        result, code = gh.api("POST", "/pulls", {
            "title": "Draft: {} LaTeX sequence {:03d} — {}".format(slug, info["sequence"], normalize_topic(topic)),
            "head": branch, "base": "main", "draft": True,
            "body": "Sequence reserved by the R&D Memory Wall allocator. Researcher-only source branch; shared template pinned. Scientific admission, build, Drive PDF and release require separate evidence. Do not merge this placeholder PR as a scientific result."
        })
        if code == 201:
            print("DRAFT_PR " + result["html_url"])
        elif code == 422:
            print("PR_ALREADY_EXISTS_OR_UNAVAILABLE " + str(result)[:200])
        else:
            raise RuntimeError("Branch exists but PR creation failed: " + str(result))


def self_test() -> None:
    registered = load("registry/researchers.json")["researchers"]
    data = load(LEDGER)
    validate(data, registered)
    for slug in ("saugat-paneru", "nabin-bista"):
        row = next(x for x in data["researchers"] if x["slug"] == slug)
        highest = max([row["baseline"]["last_historical_sequence"]] +
                      [v["sequence"] for v in row["reservations"]] +
                      [v["sequence"] for v in row.get("observed_out_of_band_versions", [])])
        assert plan(data, slug, "unit test")["sequence"] == highest + 1
    nabin = next(x for x in data["researchers"] if x["slug"] == "nabin-bista")
    assert [x["sequence"] for x in nabin.get("observed_out_of_band_versions", [])] == [55, 56, 57]
    assert plan(data, "nabin-bista", "safe preview")["sequence"] == 58
    mock_tree = {"truncated": False, "tree": [
        {"path": "researchers/nabin-bista/latex/releases/SEQ055_EXAMPLE.md", "type": "blob"},
        {"path": "researchers/nabin-bista/latex/releases/SEQ056_EXAMPLE.md", "type": "blob"},
        {"path": "researchers/nabin-bista/latex/releases/SEQ057_EXAMPLE.md", "type": "blob"},
        {"path": "researchers/saugat-paneru/latex/releases/SEQ999_OTHER_RESEARCHER.md", "type": "blob"}]}
    assert remote_release_highwater(mock_tree, "nabin-bista") == 57
    verify_remote_releases_reconciled(mock_tree, nabin)
    assert remote_release_highwater(mock_tree, "saugat-paneru") == 999
    stale = {"truncated": False, "tree": mock_tree["tree"] + [
        {"path": "researchers/nabin-bista/latex/releases/SEQ058_UNREGISTERED.md", "type": "blob"}]}
    try:
        verify_remote_releases_reconciled(stale, nabin)
    except RuntimeError as exc:
        assert "UNREGISTERED_REMOTE_RELEASE_SEQ_058" in str(exc)
    else:
        raise AssertionError("Unregistered existing release must block reservation")
    contaminated = json.loads(json.dumps(data))
    bad_row = next(x for x in contaminated["researchers"] if x["slug"] == "nabin-bista")
    bad_row["reservations"].append({
        "sequence": 56, "status": "RESERVED", "branch": "thesis/nabin-bista/latex/seq056-illegal"
    })
    try:
        validate(contaminated, registered)
    except ValueError:
        pass
    else:
        raise AssertionError("Duplicate Nabin seq056 must fail validation")
    assert remote_release_highwater({"truncated": False, "tree": []}, "nabin-bista") == 0
    try:
        remote_release_highwater({"truncated": True, "tree": []}, "nabin-bista")
    except RuntimeError:
        pass
    else:
        raise AssertionError("Truncated Git tree must block allocation")
    unknowns = [r["slug"] for r in data["researchers"]
                if r["baseline"]["last_historical_sequence"] is None]
    if unknowns:
        try:
            plan(data, unknowns[0], "new")
        except ValueError as e:
            assert "HOLD_BASELINE_VERIFICATION_REQUIRED" in str(e)
        else:
            raise AssertionError("Unverified researcher must be held")
    clone = json.loads(json.dumps(data))
    r = next(x for x in clone["researchers"] if x["slug"] == "nabin-bista")
    example = plan(clone, "nabin-bista", "Test")
    r["reservations"].append({**example, "status": "RESERVED", "request_key": "unit-test"})
    validate(clone, registered)
    assert plan(clone, "nabin-bista", "Next")["sequence"] == example["sequence"] + 1
    r["reservations"].append({**example, "status": "RESERVED", "request_key": "duplicate"})
    try:
        validate(clone, registered)
    except ValueError:
        pass
    else:
        raise AssertionError("Duplicate number not detected")
    print("SEQUENCE_ALLOCATOR_SELF_TEST_PASS")


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--self-test", action="store_true")
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--reserve", action="store_true")
    g.add_argument("--finalize", action="store_true")
    p.add_argument("--request-key")
    p.add_argument("--slug")
    p.add_argument("--topic")
    p.add_argument("--create-pr", action="store_true")
    a = p.parse_args()
    if a.self_test:
        self_test()
    elif a.check:
        validate(load(LEDGER), load("registry/researchers.json")["researchers"])
        print("SEQUENCE_REGISTRY_PASS")
    elif a.dry_run:
        validate(load(LEDGER), load("registry/researchers.json")["researchers"])
        print(json.dumps(plan(load(LEDGER), a.slug or "", a.topic or "")))
    elif a.finalize:
        if not a.slug or not a.request_key:
            p.error("--finalize requires --slug and --request-key")
        finalize(a.slug, a.request_key, a.create_pr)
    else:
        if not a.slug or not a.topic:
            p.error("--reserve requires --slug and --topic")
        reserve(a.slug, a.topic, a.create_pr)


if __name__ == "__main__":
    try:
        main()
    except (KeyError, ValueError, RuntimeError) as exc:
        sys.exit("FAIL_CLOSED: " + str(exc))
