#!/usr/bin/env python3
"""Validate enrollment and supplied PRIVATE release receipts; never certify science.

This does not fetch providers, convert manuscripts, render pages or manufacture QA.
Receipt PASS means internally consistent supplied evidence, not independently true.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTROL = "controls/academic-writing/research-deliverables.json"
ENROLLMENT = "registry/researcher-deliverables.json"
STATES = {"NOT_DISCOVERED", "IDENTIFIED", "CANDIDATE", "VERIFIED", "SUBMISSION_READY"}
HASH64 = re.compile(r"^[a-f0-9]{64}$")
HASH40 = re.compile(r"^[a-f0-9]{40}$")


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def require(value, message):
    if not value:
        raise ValueError(message)


def check_enrollment(root=ROOT):
    contract = load(root / CONTROL)
    owners = load(root / "registry/researchers.json")["researchers"]
    rows = load(root / ENROLLMENT)["researchers"]
    identities = [(x["researcher_id"], x["slug"]) for x in rows]
    require(len(identities) == len(set(identities)), "duplicate deliverable owner")
    require(set(identities) == {(x["researcher_id"], x["slug"]) for x in owners}, "owner enrollment drift")
    family = load(root / "controls/academic-writing/tower.json")
    require(family["deliverable_contract"] == CONTROL, "family routing missing")
    require(contract["authority"] == "controls/academic-writing/tower.json", "duplicate authority")
    for key in ("format_authority", "semantic_authority", "presentation_authority", "git_drive_authority", "receipt_schema", "read_first", "validator", "resume_prompt"):
        require((root / contract[key]).is_file(), "missing dependency: " + key)
    require(load(root / "controls/latex/tower.json")["deliverable_contract"] == CONTROL, "LaTeX routing missing")
    require(load(root / "controls/presentation/tower.json")["deliverable_contract"] == CONTROL, "presentation routing missing")
    roles = set(contract["roles"])
    for row in rows:
        require(row["contract"] == CONTROL, "owner contract mismatch")
        owner = next(x for x in owners if x["researcher_id"] == row["researcher_id"])
        require(owner["governance"].get("deliverable_contract") == CONTROL, "owner entrypoint delivery routing absent")
        require(set(row["roles"]) == roles, "owner role inventory incomplete")
        # Public inventory is discovery metadata; it cannot release a private artifact.
        for role, value in row["roles"].items():
            require(value["assessment"] == "UNVERIFIED", "public enrollment must not certify " + role)
        require(row["release_receipt"] is None, "private receipt must not be embedded in public enrollment")
    return len(rows)


def validate_receipt(m, contract, owners):
    """Fail closed on contradictory receipts; caller still must inspect evidence."""
    require(isinstance(m, dict), "receipt must be an object")
    require(m.get("schema_version") == "1.0.0", "unknown schema")
    owner = (m.get("researcher_id"), m.get("slug"))
    require(owner in {(x["researcher_id"], x["slug"]) for x in owners}, "unregistered owner")
    require(isinstance(m.get("scientific_revision"), str) and m["scientific_revision"].strip(), "missing scientific revision")
    for key, pattern in (("source_tree_sha256", HASH64), ("source_commit_sha", HASH40), ("style_blob_sha", HASH40)):
        require(isinstance(m.get(key), str) and pattern.fullmatch(m[key]), "invalid " + key)
    require(type(m.get("bundle_ready")) is bool, "bundle_ready must be boolean")
    artifacts = m.get("artifacts")
    require(isinstance(artifacts, list) and all(isinstance(a, dict) for a in artifacts), "missing artifacts")
    indexed = {a.get("role"): a for a in artifacts}
    require(len(indexed) == len(artifacts) and set(indexed) == set(contract["roles"]), "missing/duplicate/unknown artifact role")
    native_ids = []
    protected_paths = set()
    for role, a in indexed.items():
        require(a.get("researcher_id") == owner[0], "cross-owner artifact")
        require(a.get("state") in STATES, "unknown artifact state")
        require(isinstance(a.get("checks"), dict), "checks must be an object")
        path = a.get("git_path")
        if path:
            require(isinstance(path, str) and ".." not in Path(path).parts and path.startswith("researchers/" + owner[1] + "/"), "cross-owner or non-owner source path")
            require(path not in protected_paths, "same source path assigned to different roles")
            protected_paths.add(path)
        provider = a.get("provider_file_id")
        if provider:
            require(isinstance(provider, str), "provider identity must be a string")
            native_ids.append(provider)
        if a["state"] != "NOT_DISCOVERED":
            require(path or provider, "identified artifact needs an actual pointer")
        if a["state"] in {"CANDIDATE", "VERIFIED", "SUBMISSION_READY"}:
            require(isinstance(a.get("artifact_sha256"), str) and HASH64.fullmatch(a["artifact_sha256"]), "missing candidate artifact digest")
            if role in contract["submission_bundle_roles"] + contract.get("optional_submission_roles", []) + contract["presentation_roles"]:
                require(a.get("scientific_revision") == m["scientific_revision"] and a.get("source_tree_sha256") == m["source_tree_sha256"], "stale thesis source binding")
                require(a.get("style_blob_sha") == m["style_blob_sha"], "stale artifact template pin")
        ready = a["state"] == "SUBMISSION_READY"
        if ready:
            require(role not in contract["working_roles"], "working record cannot be submitted as manuscript")
            require(role != "presentation_source", "presentation source is a build input, not a submission manuscript")
        if a["state"] in {"VERIFIED", "SUBMISSION_READY"}:
            # VERIFIED means the role's supplied evidence is complete, not just inventoried.
            for gate in contract["roles"][role].get("gates", []):
                c = a["checks"].get(gate, {})
                require(isinstance(c, dict) and c.get("status") == "PASS", "unpassed gate: " + role + "/" + gate)
                require(all(isinstance(c.get(k), str) and c[k].strip() for k in ("evidence_ref", "executed_at")), "missing executed evidence: " + gate)
                require(c.get("subject_sha256") == a["artifact_sha256"] and c.get("source_tree_sha256") == m["source_tree_sha256"], "stale receipt: " + gate)
                require(c.get("style_blob_sha") == m["style_blob_sha"], "stale receipt template pin: " + gate)
            if provider:
                require(isinstance(a.get("provider_revision"), str) and a["provider_revision"].strip(), "missing provider revision")
            if "provider_readback" in contract["roles"][role].get("gates", []):
                c = a["checks"]["provider_readback"]
                require(provider and c.get("provider_file_id") == provider and c.get("provider_revision") == a["provider_revision"], "readback identity/revision mismatch")
            if role == "submission_google_doc":
                require(isinstance(a.get("native_digest_method"), str) and a["native_digest_method"].strip(), "native content digest method missing")
                ref_pdf = indexed["submission_pdf"].get("artifact_sha256")
                require(ref_pdf and a.get("reference_pdf_sha256") == ref_pdf, "Doc compared to wrong thesis PDF")
                require(isinstance(a.get("export_pdf_sha256"), str) and HASH64.fullmatch(a["export_pdf_sha256"]), "Doc exported PDF missing")
                for gate in ("content_parity", "equation_table_figure_parity", "exact_font_and_format", "pagination_parity", "full_page_visual_qa"):
                    c = a["checks"][gate]
                    require(c.get("export_pdf_sha256") == a["export_pdf_sha256"] and c.get("reference_pdf_sha256") == ref_pdf and c.get("provider_revision") == a["provider_revision"], "stale Doc parity evidence")
                require(type(a.get("page_count")) is int and a["page_count"] > 0 and a["page_count"] == indexed["submission_pdf"].get("page_count"), "pagination mismatch")
    require(len(native_ids) == len(set(native_ids)), "submission, audit, discussion and other roles must not alias the same provider file")
    if m["bundle_ready"]:
        require(all(indexed[r]["state"] == "SUBMISSION_READY" for r in contract["submission_bundle_roles"]), "incomplete required LaTeX/PDF bundle")
    events = m.get("version_events")
    require(isinstance(events, list), "version_events must be an array")
    changed = m.get("changed_roles")
    require(isinstance(changed, list) and len(changed) == len(set(changed)) and set(changed) <= set(indexed), "invalid changed role list")
    require(set(changed) == {e.get("subject") for e in events if isinstance(e, dict)}, "changed artifacts require matching version events")
    ordinals = {}
    for event in events:
        require(isinstance(event, dict) and event.get("researcher_id") == owner[0], "cross-owner version event")
        require(event.get("kind") in {"CREATE", "MUTATE", "RESTORE"}, "unknown version event")
        require(event.get("subject") in indexed, "unknown version subject")
        require(all(isinstance(event.get(k), str) and event[k].strip() for k in ("live_id_after", "restore_target", "post_ref", "history_ref", "what", "why", "readback_ref")), "incomplete version event")
        live = event["live_id_after"]
        require(event["restore_target"] == live, "restore must target same live identity")
        require(live == (indexed[event["subject"]].get("provider_file_id") or indexed[event["subject"]].get("git_path")), "version event does not identify owner artifact")
        n = event.get("snapshot_ordinal")
        require(type(n) is int and n > ordinals.get(event["subject"], 0), "snapshot ordinal reuse/out of order")
        ordinals[event["subject"]] = n
        if event["kind"] == "CREATE":
            require(event.get("live_id_before") is None and event.get("pre_ref") is None, "new subject has no fictional PRE")
        else:
            require(event.get("live_id_before") == live and isinstance(event.get("pre_ref"), str) and event["pre_ref"].strip(), "same live ID and PRE required")
        require(event.get("pre_ref") != event["post_ref"] and live not in {event.get("pre_ref"), event["post_ref"]}, "archive must not be live object or alias PRE/POST")
    return True


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, help="PRIVATE owner receipt; never upload real evidence to public CI")
    args = p.parse_args()
    try:
        count = check_enrollment()
        if args.manifest:
            validate_receipt(load(args.manifest), load(ROOT / CONTROL), load(ROOT / "registry/researchers.json")["researchers"])
            print("RECEIPT_CONSISTENT_ONLY__PROVIDER_AND_SCIENTIFIC_EVIDENCE_NOT_INDEPENDENTLY_CERTIFIED")
        else:
            print(f"DELIVERABLE_CONTRACT_PASS {count} owners; no conversion, provider execution or submission certification")
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as e:
        raise SystemExit("DELIVERABLE_HOLD: " + str(e)) from e


if __name__ == "__main__":
    main()
