from __future__ import annotations
import unittest
from a9_semantic_checker import check_semantics

META={"project_id":"TEST-001","client_facing": True}
MAP={"project_id":"TEST-001","source_commit":"deadbeef", "source_manifest_id":"DRIVE-EXAMPLE",
     "sources":[{"source_id":"S1", "admission_status":"ADMITTED_CURRENT"},
                {"source_id":"P1", "admission_status":"CANDIDATE"}]}

class SemanticGateTests(unittest.TestCase):
    def test_admitted_observation(self):
        slides=[{"type":"bullets","title":"Site observations","scientific_role":"OBSERVATION",
                 "evidence_refs":["S1"],"admission_decision_id":"DEC-1", "bullets":["Observed joint"]}]
        self.assertTrue(check_semantics({"metadata":META,"slides":slides},MAP)["ok"])
    def test_reject_candidate_photo(self):
        slides=[{"title":"Results","scientific_role":"RESULT", "evidence_refs":["P1"],
                "admission_decision_id":"DEC-1"}]
        self.assertFalse(check_semantics({"metadata":META,"slides":slides},MAP)["ok"])
    def test_reject_unmapped_result(self):
        slides=[{"title":"Results","scientific_role":"RESULT", "evidence_refs":[],
                "admission_decision_id":"DEC-1"}]
        self.assertFalse(check_semantics({"metadata":META,"slides":slides},MAP)["ok"])
    def test_reject_project_mismatch(self):
        self.assertFalse(check_semantics({"metadata":{"project_id":"OTHER"},"slides":[]},MAP)["ok"])
    def test_reject_internal_terms(self):
        slides=[{"title":"OpenAI checkpoint","scientific_role":"NON_SCIENTIFIC"}]
        self.assertFalse(check_semantics({"metadata":META,"slides":slides},MAP)["ok"])
    def test_fixture_is_not_researcher_pass(self):
        x=check_semantics({},None,mode="fixture")
        self.assertTrue(x["ok"])
        self.assertEqual(x["mode"],"fixture")
    def test_no_evidence_map_fails_closed(self):
        self.assertFalse(check_semantics({"metadata":META,"slides":[]},None)["ok"])

if __name__ == '__main__': unittest.main()
