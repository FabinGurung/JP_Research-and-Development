#!/usr/bin/env python3
"""Synthetic-only release guard tests. No real researcher numbers or provider writes."""
import copy
import unittest
from validate_deliverables import CONTROL, ROOT, load, validate_receipt, check_enrollment

C = load(ROOT / CONTROL)
OWNERS = [{"researcher_id": "FIXTURE-OWNER", "slug": "fixture-owner"}]


def fixture():
    m = dict(schema_version="1.0.0", researcher_id="FIXTURE-OWNER", slug="fixture-owner",
             scientific_revision="SYNTHETIC-NOT-A-SCIENTIFIC-CP", source_tree_sha256="a"*64,
             source_commit_sha="b"*40, style_blob_sha="c"*40, bundle_ready=True,
             artifacts=[], changed_roles=[], version_events=[])
    for i, role in enumerate(C["roles"]):
        ready = role in C["submission_bundle_roles"]
        a = dict(role=role, researcher_id=m["researcher_id"], state="SUBMISSION_READY" if ready else "IDENTIFIED",
                 artifact_sha256=f"{i+1:064x}", scientific_revision=m["scientific_revision"],
                 source_tree_sha256=m["source_tree_sha256"], provider_file_id="FIXTURE-ONLY-"+role,
                 provider_revision="FIXTURE-REVISION", style_blob_sha=m["style_blob_sha"], checks={})
        if ready:
            for gate in C["roles"][role]["gates"]:
                a["checks"][gate] = dict(status="PASS", evidence_ref="synthetic://not-provider-evidence/"+gate,
                    executed_at="SYNTHETIC-TEST-ONLY", subject_sha256=a["artifact_sha256"],
                    source_tree_sha256=m["source_tree_sha256"], provider_file_id=a["provider_file_id"],
                    provider_revision=a["provider_revision"], style_blob_sha=m["style_blob_sha"])
        m["artifacts"].append(a)
    pdf = next(a for a in m["artifacts"] if a["role"] == "submission_pdf")
    doc = next(a for a in m["artifacts"] if a["role"] == "submission_google_doc")
    pdf["page_count"] = doc["page_count"] = 2
    doc["reference_pdf_sha256"] = pdf["artifact_sha256"]
    doc["export_pdf_sha256"] = "d"*64
    doc["native_digest_method"] = "SYNTHETIC-ONLY-normalization-v1"
    for gate in ("content_parity", "equation_table_figure_parity", "exact_font_and_format", "pagination_parity", "full_page_visual_qa"):
        doc["checks"][gate].update(reference_pdf_sha256=pdf["artifact_sha256"], export_pdf_sha256=doc["export_pdf_sha256"])
    return m


class DeliverableTests(unittest.TestCase):
    def setUp(self):
        self.m = fixture()

    def artifact(self, role):
        return next(a for a in self.m["artifacts"] if a["role"] == role)

    def reject(self):
        with self.assertRaises(ValueError):
            validate_receipt(self.m, C, OWNERS)

    def test_complete_synthetic_receipt_is_consistent_only(self):
        self.assertTrue(validate_receipt(self.m, C, OWNERS))

    def test_live_enrollment(self):
        self.assertEqual(check_enrollment(), len(load(ROOT / "registry/researchers.json")["researchers"]))

    def test_missing_role(self):
        self.m["artifacts"].pop(); self.reject()

    def test_cross_researcher(self):
        self.m["artifacts"][0]["researcher_id"] = "OTHER"; self.reject()

    def test_cross_owner_source_path(self):
        self.artifact("submission_latex")["git_path"] = "researchers/other/latex/main.tex"; self.reject()

    def test_audit_cannot_be_submission_doc(self):
        self.artifact("audit_google_doc")["provider_file_id"] = self.artifact("submission_google_doc")["provider_file_id"]
        self.reject()

    def test_missing_executed_evidence(self):
        self.artifact("submission_google_doc")["checks"]["content_parity"]["evidence_ref"] = ""; self.reject()

    def test_stale_source(self):
        self.artifact("submission_google_doc")["source_tree_sha256"] = "e"*64; self.reject()

    def test_changed_template_invalidates_receipt(self):
        self.m["style_blob_sha"] = "e"*40; self.reject()

    def test_fallback_font_not_production(self):
        self.artifact("submission_pdf")["checks"]["exact_font_and_format"]["status"] = "NOT_RUN"; self.reject()

    def test_stale_export(self):
        self.artifact("submission_google_doc")["export_pdf_sha256"] = "e"*64; self.reject()

    def test_different_page_count(self):
        self.artifact("submission_google_doc")["page_count"] = 3; self.reject()

    def test_native_digest_method_required(self):
        self.artifact("submission_google_doc").pop("native_digest_method"); self.reject()

    def test_readback_revision_changed(self):
        self.artifact("submission_pdf")["provider_revision"] = "NEW-REVISION"; self.reject()

    def test_working_doc_not_submit_ready(self):
        self.artifact("discussion_google_doc")["state"] = "SUBMISSION_READY"; self.reject()

    def test_partial_bundle_not_ready(self):
        self.artifact("submission_google_doc")["state"] = "CANDIDATE"; self.reject()

    def test_missing_prepost(self):
        self.m["changed_roles"] = ["submission_google_doc"]; self.reject()

    def event(self):
        live = self.artifact("submission_google_doc")["provider_file_id"]
        e = dict(kind="MUTATE", subject="submission_google_doc", researcher_id=self.m["researcher_id"],
                 live_id_before=live, live_id_after=live, restore_target=live, snapshot_ordinal=1,
                 pre_ref="synthetic://PRE", post_ref="synthetic://POST", history_ref="synthetic://history",
                 what="Synthetic edit", why="Test only", readback_ref="synthetic://readback")
        self.m["changed_roles"] = ["submission_google_doc"]
        self.m["version_events"] = [e]
        return e

    def test_same_live_identity(self):
        self.event(); self.assertTrue(validate_receipt(self.m, C, OWNERS))

    def test_replaced_live_id(self):
        self.event()["live_id_before"] = "OLD-LIVE-ID"; self.reject()

    def test_restore_into_archive_forbidden(self):
        self.event()["restore_target"] = "ARCHIVE-ID"; self.reject()

    def test_reused_snapshot_ordinal(self):
        e = self.event(); self.m["version_events"].append(copy.deepcopy(e)); self.reject()

    def test_initial_creation_has_no_fictional_pre(self):
        e = self.event(); e.update(kind="CREATE", live_id_before=None, pre_ref=None)
        self.assertTrue(validate_receipt(self.m, C, OWNERS))
        e["pre_ref"] = "MADE-UP-PRE"; self.reject()


if __name__ == "__main__":
    unittest.main()
