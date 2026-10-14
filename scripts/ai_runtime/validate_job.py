#!/usr/bin/env python3
"""Validate versioned, public-safe AI job envelopes without executing them.

A request fingerprint is deterministic *only* for identical canonical request
bytes. This tool cannot attest live Drive evidence, facts or human approvals.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SHA40 = re.compile(r"^[a-f0-9]{40}$")
SHA64 = re.compile(r"^[a-f0-9]{64}$")
JOB = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$")
ACTIONS = {"READ", "DRAFT", "WRITE_PRIVATE", "RELEASE"}
MODES = {"VALIDATE", "DRAFT", "EXECUTE"}

def canonical_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def validate(doc):
    if not isinstance(doc, dict):
        raise ValueError("Job must be a JSON object")
    required = {"job_id", "family_id", "task_type_id", "mode", "engine_commit", "sources", "output_kinds", "inputs"}
    optional = {"authorized_actions", "approval_ref", "runtime_digest"}
    if set(doc) - (required | optional) or required - set(doc):
        raise ValueError("Unknown or missing job-envelope keys")
    if not isinstance(doc["job_id"], str) or not JOB.fullmatch(doc["job_id"]):
        raise ValueError("Invalid job_id")
    router = json.loads((ROOT / "controls/family-router.v0.1.json").read_text(encoding="utf-8"))
    family = doc["family_id"]
    if family not in router["families"]:
        raise ValueError("Unknown family")
    task = doc["task_type_id"]
    if family == "enterprise":
        canonical = json.loads((ROOT / "registry/enterprise-document-types.json").read_text(encoding="utf-8"))["types"]
        valid = {c["id"] for c in canonical}
    else:
        valid = {"thesis", "manuscript", "presentation", "discussion", "research-website", "source-audit", "research-record"}
    if task not in valid:
        raise ValueError("Unregistered task type for family")
    mode = doc["mode"]
    if mode not in MODES or not isinstance(doc["engine_commit"], str) or not SHA40.fullmatch(doc["engine_commit"]):
        raise ValueError("Invalid execution mode or unpinned engine commit")
    if not isinstance(doc["inputs"], dict) or not isinstance(doc["output_kinds"], list) or not doc["output_kinds"]:
        raise ValueError("Missing typed input or output expectations")
    if not all(isinstance(kind, str) and kind.strip() for kind in doc["output_kinds"]):
        raise ValueError("Malformed output kind")
    sources = doc["sources"]
    if not isinstance(sources, list):
        raise ValueError("Source references must be a list")
    for src in sources:
        if not isinstance(src, dict) or set(src) != {"authority", "source_id", "sha256", "revision"}:
            raise ValueError("Unrecognized evidence structure")
        if src["authority"] not in {"DRIVE_PRIVATE", "GIT_PUBLIC", "AUTHORIZED_OTHER"}:
            raise ValueError("Unknown evidence authority")
        if not isinstance(src["source_id"], str) or not src["source_id"] or not isinstance(src["revision"], str) or not src["revision"]:
            raise ValueError("Missing evidence IDs and versions")
        if not isinstance(src["sha256"], str) or not SHA64.fullmatch(src["sha256"]):
            raise ValueError("Source hash required for reproducibility")
    actions = doc.get("authorized_actions", [])
    if not isinstance(actions, list) or len(set(actions)) != len(actions) or set(actions) - ACTIONS:
        raise ValueError("Unsupported or repeated permissions")
    if mode == "EXECUTE":
        if not sources or "WRITE_PRIVATE" not in actions or not doc.get("approval_ref"):
            raise ValueError("Private execution requires immutable sources, scoped write authorization and approval")
        digest = doc.get("runtime_digest")
        if not isinstance(digest, str) or not SHA64.fullmatch(digest):
            raise ValueError("Pinned runtime image/toolchain digest is mandatory for EXECUTE")
    if mode != "EXECUTE" and ("WRITE_PRIVATE" in actions or "RELEASE" in actions):
        raise ValueError("Read/preview jobs cannot request side-effecting permissions")
    fingerprint = hashlib.sha256(b"A9_AI_JOB_V0.1\n" + canonical_bytes(doc)).hexdigest()
    return {"job_id": doc["job_id"], "family_id": family,
            "task_type_id": task, "request_sha256": fingerprint,
            "envelope_validation": "PASS", "source_contents_verified": False,
            "result_status": "HOLD_LIVE_SOURCE_AND_QA",
            "execute_performed": False}

def selftest():
    sample = json.loads((ROOT / "examples/ai-runtime/public-safe-demo-request.json").read_text(encoding="utf-8"))
    a = validate(sample); b = validate(dict(reversed(list(sample.items()))))
    assert a["request_sha256"] == b["request_sha256"], "Canonical key order differs"
    assert a["source_contents_verified"] is False
    bad = json.loads(json.dumps(sample))
    bad["task_type_id"] = "unknown"
    try: validate(bad)
    except ValueError: pass
    else: raise AssertionError("Unregistered template accepted")
    bad = json.loads(json.dumps(sample))
    bad["mode"] = "EXECUTE"
    try: validate(bad)
    except ValueError: pass
    else: raise AssertionError("Unapproved execution accepted")
    bad = json.loads(json.dumps(sample))
    bad["inputs"]["fixture_only"] = False
    assert validate(bad)["request_sha256"] != a["request_sha256"]
    print("PASS family routing, canonical SHA-256, task registration, fail-closed execute gate")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        selftest()
    elif args.data:
        print(json.dumps(validate(json.loads(args.data.read_text(encoding="utf-8"))), indent=2))
    else:
        ap.error("Provide --data or --self-test")
