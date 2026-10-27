#!/usr/bin/env python3
"""Validate private client-contract manifests using public-safe generic rules.

Only synthetic fixtures are used for CI. Private project data is passed locally
to --instance when authorized, never committed to a public repository.
"""
import argparse
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "schemas/enterprise/client-contract-instance.schema.json"


def validate(instance: dict, schema_path: Path = SCHEMA_PATH):
    from jsonschema import Draft202012Validator
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda e: list(map(str,e.absolute_path)))
    if errors:
        raise ValueError("Invalid contract instance: " + "; ".join(e.message for e in errors[:4]))
    # Semantic checks not expressed by JSON Schema.
    milestones = instance["milestones"]
    if sorted(x["sequence"] for x in milestones) != list(range(1, len(milestones) + 1)):
        raise ValueError("Milestone sequences must be consecutive and unique")
    value = instance.get("contract_value_npr")
    if value is not None and sum(x["amount_npr"] for x in milestones) != value:
        raise ValueError("Milestone NPR amounts do not reconcile to the base contract")
    if any(x["approval_status"] == "PROPOSED_UNPRICED" and x["amount_npr"] is not None
           for x in instance["variation_orders"]):
        raise ValueError("Unpriced variation has a numeric amount")
    sources = {x["source_ref"]: x for x in instance.get("source_documents", [])}
    if len(sources) != len(instance.get("source_documents", [])):
        raise ValueError("Duplicate original source references")
    cited = set()
    for citation in instance.get("source_citations", []):
        if citation["citation_id"] in cited:
            raise ValueError("Duplicate source citation id")
        cited.add(citation["citation_id"])
        source = sources.get(citation["source_ref"])
        if not source:
            raise ValueError("Citation refers to absent source")
        if citation["first_page"] > citation["last_page"] or citation["last_page"] > source["page_count"]:
            raise ValueError("Citation pages outside original source")
    attachment = instance.get("attachment_bundle", {})
    if attachment.get("method") == "PDF_APPEND_AS_RECEIVED":
        expected = sum(x["page_count"] for x in sources.values() if x["usage"] == "CONTRACT_ATTACHMENT")
        if attachment["appended_pages"] != expected:
            raise ValueError("Source appendix page count mismatch")
        if attachment.get("combined_pages") is not None and attachment.get("contract_pages") is not None:
            if attachment["combined_pages"] != attachment["contract_pages"] + attachment["appended_pages"]:
                raise ValueError("Combined PDF page count mismatch")
    delivery = instance.get("client_delivery", {})
    if delivery:
        basename = delivery["basename"].upper()
        if "DRAFT" in basename or "AUDIT" in basename:
            raise ValueError("Internal labels belong in a separate audit/status file")
        if instance["draft_state"] != "EXECUTED_WITH_EVIDENCE" and delivery["contract_execution_status"] != "FOR_REVIEW_NOT_EXECUTED":
            raise ValueError("Unsigned document must visibly disclose unexecuted status")
    if instance.get("publication", {}).get("private_pdf_in_public_repo") is not False:
        raise ValueError("Private PDF publication forbidden")
    return {"status": "PASS", "milestones": len(milestones), "source_citations": len(cited),
            "source_appendix_pages": attachment.get("appended_pages", 0)}


def synthetic_fixture():
    return {
      "project": {"project_id": "EXAMPLE-001", "organization_id": "EXAMPLE-ORG", "company_project_code": "EXAMPLE-CODE"},
      "source_control": {"canonical_template_git_blob": "a"*40, "private_source_provider": "GOOGLE_DRIVE", "private_source_revision": "v0.1"},
      "publication": {"is_public": False, "private_pdf_in_public_repo": False, "site_link_visibility": "HOLD"},
      "contract_value_npr": 1000,
      "milestones": [{"sequence": 1,"description": "Fictional milestone A","percentage_display": "40","amount_npr": 400},
                     {"sequence": 2,"description": "Fictional milestone B","percentage_display": "60","amount_npr": 600}],
      "contract_drawings": [{"discipline": "ARCHITECTURAL","source_available": True,"approval_status": "AVAILABLE_AS_RECEIVED_NOT_SIGNED","source_provider": "GOOGLE_DRIVE"}],
      "source_documents": [{"source_ref": "SRC-A","source_provider": "GOOGLE_DRIVE","sha256": "b"*64,"page_count": 3,"approval_status": "AS_RECEIVED_UNVERIFIED","usage": "CONTRACT_ATTACHMENT","original_bytes_preserved": True}],
      "source_citations": [{"citation_id": "SRC-01","source_ref": "SRC-A","first_page": 1,"last_page": 3,"contract_scope_key": "example","assertion_type": "SOURCE_FACT"}],
      "attachment_bundle": {"method": "PDF_APPEND_AS_RECEIVED", "originals_unchanged": True,"appended_pages": 3,"contract_pages": 2,"combined_pages": 5},
      "variation_orders": [{"id": "VO-01","description": "Fictional unpriced substitution","approval_status": "PROPOSED_UNPRICED","amount_npr": None}],
      "client_delivery": {"basename": "Example_Construction_Agreement_v0.1.pdf","contract_execution_status": "FOR_REVIEW_NOT_EXECUTED","internal_audit_separate": True},
      "draft_state": "DRAFT_NOT_EXECUTED"
    }


def self_test():
    x=synthetic_fixture()
    assert validate(x)["status"] == "PASS"
    for edit in ("wrong_sum", "invalid_pages", "priced_unapproved", "bad_basename", "wrong_appended"):
        bad=copy.deepcopy(x)
        if edit == "wrong_sum": bad["contract_value_npr"] = 1001
        if edit == "invalid_pages": bad["source_citations"][0]["last_page"] = 4
        if edit == "priced_unapproved": bad["variation_orders"][0]["amount_npr"] = 1
        if edit == "bad_basename": bad["client_delivery"]["basename"] = "Example_DRAFT_v0.1.pdf"
        if edit == "wrong_appended": bad["attachment_bundle"]["appended_pages"] = 2
        try:
            validate(bad)
        except ValueError:
            continue
        raise AssertionError(f"Expected semantic failure: {edit}")
    print("PASS generic private-contract evidence schema, original source references and crosschecks")


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--instance", type=Path)
    args=parser.parse_args()
    if args.self_test:
        self_test()
    elif args.instance:
        print(json.dumps(validate(json.loads(args.instance.read_text())), indent=2))
    else:
        parser.error("Provide --self-test or --instance PRIVATE.json")
