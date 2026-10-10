"""Researcher-neutral literature matrix normalizer and machine-verifiable evidence guardrails.

The paper's finding and its applicability are distinct author-supplied statements.
Validation verifies provenance *links and formatting*; not the truth of research claims.
"""
from __future__ import annotations
from copy import deepcopy
import re
from typing import Any

LITERATURE_TYPE = "literature_table"
RELEVANCE_KINDS = {"METHOD", "CONTEXT", "TECHNICAL_BASIS", "COMPARISON", "LIMITATION", "RESEARCH_GAP"}
SOURCE_KINDS = {"PEER_REVIEWED", "THESIS", "CODE", "STANDARD", "GUIDELINE", "MANUFACTURER", "OTHER"}
ADMITTED = {"ADMITTED_CURRENT", "APPROVED_CURRENT"}


def _txt(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _table_refs(content: dict) -> tuple[dict, list[str]]:
    errors = []
    raw = content.get("literature_references", [])
    if not isinstance(raw, list):
        return {}, ["literature_references must be an array"]
    refs = {}
    for index, ref in enumerate(raw, 1):
        if not isinstance(ref, dict):
            errors.append(f"literature_references[{index}] must be an object")
            continue
        key = _txt(ref.get("reference_id"))
        if not key or key in refs:
            errors.append(f"literature_references[{index}] missing/duplicate reference_id")
            continue
        refs[key] = ref
        for field in ("authors", "title", "source_id", "bibliography_key"):
            if not _txt(ref.get(field)):
                errors.append(f"literature reference {key} requires {field}")
        year = ref.get("year")
        if not isinstance(year, int) or isinstance(year, bool) or year < 1500 or year > 2100:
            errors.append(f"literature reference {key} requires a valid year")
        if ref.get("source_kind") not in SOURCE_KINDS:
            errors.append(f"literature reference {key} has missing/invalid source_kind")
    return refs, errors


def validate_literature(content: dict, evidence_map: dict | None, *, fixture: bool = False) -> dict:
    """Fail-closed per-row source admission and citation/relevance linkage checks."""
    slides = content.get("slides") or []
    lit_slides = [(i, slide) for i, slide in enumerate(slides, 1)
                  if isinstance(slide, dict) and slide.get("type") == LITERATURE_TYPE]
    if not lit_slides:
        return {"ok": True, "errors": [], "warnings": [], "table_count": 0, "entry_count": 0}
    refs, errors = _table_refs(content)
    warnings = []
    sources = {}
    if not fixture:
        if not isinstance(evidence_map, dict):
            errors.append("literature table requires current project admitted evidence_map")
        else:
            sources = {r.get("source_id"): r for r in evidence_map.get("sources", [])
                       if isinstance(r, dict) and isinstance(r.get("source_id"), str)}
    count = 0
    for index, slide in lit_slides:
        ncol = slide.get("columns", 3)
        if ncol not in (3, 4) or isinstance(ncol, bool):
            errors.append(f"slide {index}: columns must be 3 or 4")
            ncol = 3
        maxrows = slide.get("max_rows_per_slide", 3)
        if not isinstance(maxrows, int) or isinstance(maxrows, bool) or not 1 <= maxrows <= 3:
            errors.append(f"slide {index}: max_rows_per_slide must be between 1 and 3")
        rows = slide.get("rows")
        if not isinstance(rows, list) or not rows:
            errors.append(f"slide {index}: literature table rows must be nonempty array")
            continue
        used = set()
        for j, row in enumerate(rows, 1):
            count += 1
            prefix = f"slide {index} literature row {j}"
            if not isinstance(row, dict):
                errors.append(f"{prefix}: not an object")
                continue
            ref_id = _txt(row.get("reference_id"))
            if not ref_id:
                errors.append(f"{prefix}: reference_id is required")
            if ref_id in used:
                errors.append(f"{prefix}: duplicate reference_id on same literature slide")
            used.add(ref_id)
            ref = refs.get(ref_id)
            if ref is None:
                errors.append(f"{prefix}: unregistered reference_id {ref_id}")
            if row.get("relevance_type") not in RELEVANCE_KINDS:
                errors.append(f"{prefix}: invalid/missing relevance_type")
            for field, limit in (("key_finding", 145 if ncol == 3 else 120),
                                 ("project_relevance", 145 if ncol == 3 else 110)):
                val = _txt(row.get(field))
                if not val or len(val) > limit:
                    errors.append(f"{prefix}: {field} required, <= {limit} characters")
            if ncol == 4:
                detail = _txt(row.get("method_or_limitation"))
                if not detail or len(detail) > 95:
                    errors.append(f"{prefix}: fourth-column method_or_limitation required, <= 95 characters")
            if not _txt(row.get("finding_locator")):
                errors.append(f"{prefix}: exact source finding_locator required")
            # Research relevance is *not* a finding from the cited paper.
            # Must link a manuscript scope/objective/gap explicitly, without claiming local results.
            if not _txt(row.get("relevance_basis")):
                errors.append(f"{prefix}: relevance_basis must identify project objective/section")
            for field in ("key_finding", "project_relevance", "method_or_limitation"):
                val = _txt(row.get(field))
                if re.search(r"\b(proven in (our|this) study|confirmed local caus(e|es)|our data prove)\b",val,re.I):
                    errors.append(f"{prefix}: unsubstantiated local-proof expression in {field}")
            if ref and not fixture:
                sid = ref.get("source_id")
                source = sources.get(sid)
                if source is None:
                    errors.append(f"{prefix}: source_id {sid} absent from evidence_map")
                elif source.get("admission_status") not in ADMITTED:
                    errors.append(f"{prefix}: source_id {sid} not admitted ({source.get('admission_status')})")
            if ref:
                if len(_txt(ref.get("authors"))) > 72:
                    errors.append(f"{prefix}: authors too long for presentation; use cited short author label")
                if ref.get("source_kind") in {"CODE", "STANDARD", "GUIDELINE", "MANUFACTURER"}:
                    warnings.append(f"{prefix}: technical-source row, do not attribute empirical findings to a code/product guide")
    return {"ok": not errors, "errors": errors, "warnings": warnings,
            "table_count": len(lit_slides), "entry_count": count}


def expand_literature_tables(content: dict) -> dict:
    """Deterministically turn N literature entries into bounded 4:3 editable page tables."""
    copy = deepcopy(content)
    refs = {r["reference_id"]: r for r in copy.get("literature_references", [])}
    expanded = []
    for slide in copy.get("slides", []):
        if slide.get("type") != LITERATURE_TYPE:
            expanded.append(slide)
            continue
        rows = slide["rows"]
        chunk_size = slide.get("max_rows_per_slide", 3)
        parts = [rows[i:i+chunk_size] for i in range(0, len(rows), chunk_size)]
        for chunk_index, subset in enumerate(parts, 1):
            item = {k:v for k,v in slide.items() if k != "rows"}
            item["rows"] = [dict(row, author_year=f"{refs[row['reference_id']]['authors']} ({refs[row['reference_id']]['year']})") for row in subset]
            item["page_in_section"] = chunk_index
            item["page_total"] = len(parts)
            if len(parts) > 1:
                item["title"] = f"{slide.get('title', 'Literature Review')} ({chunk_index}/{len(parts)})"
            expanded.append(item)
    copy["slides"] = expanded
    return copy
