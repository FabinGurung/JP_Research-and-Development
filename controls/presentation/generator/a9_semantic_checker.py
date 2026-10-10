"""A9 scientific semantic/evidence gate for researcher-specific presentations.

This checks machine-verifiable provenance linkages and explicit admission states.
It cannot determine whether a published scientific assertion is true; that
requires human/supervisor review and source examination.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

_ALLOWED_TYPES = {"BACKGROUND", "METHOD", "OBSERVATION", "RESULT", "INTERPRETATION", "RECOMMENDATION", "LIMITATION", "NON_SCIENTIFIC"}
_ADMITTED = {"ADMITTED_CURRENT", "APPROVED_CURRENT"}
_FORBIDDEN = {"REJECTED", "SUPERSEDED", "CANDIDATE", "UNVERIFIED", "NOT_ADMITTED", "PRIVATE_ONLY"}
_RESULT_TITLES = re.compile(r"\b(results?|findings?|observed rework|case study|impact|quantitative|rankings?|conclusion|recommendations?)\b", re.I)
_QUANTIFIED = re.compile(r"(?:\d+(?:\.\d+)?\s*%|\b\d+(?:\.\d+)?\s*(?:days?|weeks?|months?|NPR|Rs\.|rupees|respondents?|cases?|hours?)\b)", re.I)
_CLIENT_FORBIDDEN = re.compile(r"\b(?:ChatGPT|OpenAI|AI[- ]generated|machine[- ]generated|source[- ]lock|control[- ]tower|QA[- ]PASS|checkpoint|Drive ID)\b", re.I)


def check_semantics(content: dict, evidence_map: dict | None, *, mode: str = "researcher") -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    if mode == "fixture":
        return {"ok": True, "mode": "fixture", "errors": [], "warnings": ["Fixture only: researcher scientific evidence not assessed"]}
    if not isinstance(content, dict):
        return {"ok": False, "mode": mode, "errors": ["content must be a JSON object"], "warnings": []}
    if not isinstance(evidence_map, dict):
        return {"ok": False, "mode": mode, "errors": ["researcher build requires a structured admitted evidence_map"], "warnings": []}
    project_id = (content.get("metadata") or {}).get("project_id")
    if not isinstance(project_id, str) or not project_id.strip():
        errors.append("metadata.project_id is required for a researcher build")
    if evidence_map.get("project_id") != project_id:
        errors.append("evidence_map.project_id must match content.metadata.project_id")
    if not evidence_map.get("source_commit"):
        errors.append("evidence_map.source_commit must identify an explicit current source commit")
    if not evidence_map.get("source_manifest_id"):
        errors.append("evidence_map.source_manifest_id is required")
    records = evidence_map.get("sources")
    if not isinstance(records, list):
        errors.append("evidence_map.sources must be an array")
        records = []
    source_by_id = {}
    for i, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"sources[{i}] must be an object")
            continue
        sid = record.get("source_id")
        if not sid or not isinstance(sid, str) or sid in source_by_id:
            errors.append(f"sources[{i}] has missing/duplicate source_id")
            continue
        source_by_id[sid] = record
        status = record.get("admission_status")
        if status not in _ADMITTED and status not in _FORBIDDEN:
            errors.append(f"source {sid} has missing/unknown admission_status")
    from a9_literature_table import validate_literature
    literature = validate_literature(content, evidence_map)
    errors.extend(literature["errors"])
    warnings.extend(literature["warnings"])
    from a9_methodology_flow import validate_methodology
    methodology = validate_methodology(content, evidence_map)
    errors.extend(methodology["errors"])
    warnings.extend(methodology["warnings"])
    for i, slide in enumerate(content.get("slides") or [], 1):
        if not isinstance(slide, dict):
            errors.append(f"slide {i} must be an object")
            continue
        kind = slide.get("scientific_role")
        text = " ".join([str(slide.get(x, "")) for x in ("title", "subtitle", "caption")] +
                        [str(x) for x in slide.get("bullets", [])])
        if kind not in _ALLOWED_TYPES:
            errors.append(f"slide {i} requires scientific_role in {_ALLOWED_TYPES}")
            continue
        if content.get("metadata", {}).get("client_facing", True) and _CLIENT_FORBIDDEN.search(text):
            errors.append(f"slide {i} contains internal/machine-control wording")
        if slide.get("type") in {"literature_table", "methodology_flow"}:
            # Per-row cited references, source admission and project relevance are
            # checked by the literature handler; no redundant slide-level source IDs.
            continue
        refs = slide.get("evidence_refs") or []
        if not isinstance(refs, list):
            errors.append(f"slide {i} evidence_refs must be an array")
            refs = []
        if kind in {"BACKGROUND", "OBSERVATION", "RESULT", "INTERPRETATION", "RECOMMENDATION"} and not refs:
            errors.append(f"slide {i} ({kind}) requires admitted source evidence_refs")
        if (_RESULT_TITLES.search(str(slide.get("title", ""))) or _QUANTIFIED.search(text)) and kind in {"NON_SCIENTIFIC", "METHOD"}:
            warnings.append(f"slide {i} has a results/quantity cue; independently inspect its scientific_role and evidence")
        for sid in refs:
            src = source_by_id.get(sid)
            if src is None:
                errors.append(f"slide {i} references unregistered source {sid}")
            elif src.get("admission_status") not in _ADMITTED:
                errors.append(f"slide {i} references non-admitted source {sid} ({src.get('admission_status')})")
        if kind in {"OBSERVATION", "RESULT", "INTERPRETATION"} and not slide.get("admission_decision_id"):
            errors.append(f"slide {i} ({kind}) requires admitted case/result admission_decision_id")
        if kind == "RECOMMENDATION" and not slide.get("recommendation_basis"):
            errors.append(f"slide {i} recommendation needs explicit basis")
    return {"ok": not errors, "mode": mode, "errors": errors, "warnings": warnings,
            "registered_sources": len(source_by_id), "slide_count": len(content.get("slides") or [])}


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--content", required=True)
    ap.add_argument("--evidence-map", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    content = json.loads(Path(args.content).read_text(encoding="utf-8"))
    evidence = json.loads(Path(args.evidence_map).read_text(encoding="utf-8"))
    report = check_semantics(content, evidence)
    Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
