from __future__ import annotations
import copy
import unittest
from a9_literature_table import validate_literature, expand_literature_tables
from a9_semantic_checker import check_semantics
from a9_presentation_validator import validate_content


def case(n=5, columns=3):
    refs=[{"reference_id":f"TEST-{i}","authors":f"Example Researcher {i}","year":2020+i,
           "title":f"Fictional test fixture only {i}","source_id":f"SRC-{i}",
           "bibliography_key":f"test{i}","source_kind":"PEER_REVIEWED"} for i in range(n)]
    rows=[{"reference_id":f"TEST-{i}","key_finding":"Synthetic fixture finding for renderer testing only.",
           "project_relevance":"Illustrates a source-linked methodological comparison, not a field finding.",
           "finding_locator":"synthetic fixture / paragraph 1","relevance_basis":"synthetic test objective 1",
           "relevance_type":"METHOD","method_or_limitation":"Sample size is not real; test fixture only."} for i in range(n)]
    content={"metadata":{"project_id":"SYNTHETIC-ONLY","client_facing":True},
             "literature_references":refs,
             "slides":[{"type":"literature_table","title":"Literature Review", "scientific_role":"BACKGROUND",
                       "columns":columns,"max_rows_per_slide":3,"rows":rows}]}
    map_={"project_id":"SYNTHETIC-ONLY","source_commit":"abcdef123","source_manifest_id":"FIXTURE-ONLY",
          "sources":[{"source_id":f"SRC-{i}","admission_status":"ADMITTED_CURRENT"} for i in range(n)]}
    return content,map_

class LiteratureTests(unittest.TestCase):
    def test_three_columns(self):
        c,m=case();self.assertTrue(check_semantics(c,m)["ok"])
    def test_four_columns(self):
        c,m=case(columns=4);self.assertTrue(check_semantics(c,m)["ok"])
    def test_missing_source_is_blocker(self):
        c,m=case();m["sources"][0]["admission_status"]="CANDIDATE"
        self.assertFalse(check_semantics(c,m)["ok"])
    def test_missing_finding_locator_is_blocker(self):
        c,m=case();del c["slides"][0]["rows"][0]["finding_locator"]
        self.assertFalse(check_semantics(c,m)["ok"])
    def test_missing_relevance_basis_is_blocker(self):
        c,m=case();del c["slides"][0]["rows"][0]["relevance_basis"]
        self.assertFalse(check_semantics(c,m)["ok"])
    def test_unknown_reference_is_blocker(self):
        c,m=case();c["slides"][0]["rows"][0]["reference_id"]="HALLUCINATED"
        self.assertFalse(check_semantics(c,m)["ok"])
    def test_missing_fourth_column_is_blocker(self):
        c,m=case(columns=4);del c["slides"][0]["rows"][0]["method_or_limitation"]
        self.assertFalse(check_semantics(c,m)["ok"])
    def test_relevance_cannot_claim_local_proof(self):
        c,m=case();c["slides"][0]["rows"][0]["project_relevance"]="This study proves confirmed local causes."
        self.assertFalse(check_semantics(c,m)["ok"])
    def test_paginate_no_truncation(self):
        c,m=case(7);ex=expand_literature_tables(c)
        self.assertEqual(len(ex["slides"]),3)
        self.assertEqual(sum(len(s["rows"]) for s in ex["slides"]),7)
        self.assertEqual(ex["slides"][0]["title"],"Literature Review (1/3)")
        self.assertEqual(ex["slides"][2]["rows"][0]["author_year"],"Example Researcher 6 (2026)")
    def test_without_evidence_map_is_blocker(self):
        c,m=case();self.assertFalse(validate_literature(c,None)["ok"])
    def test_tech_source_warning(self):
        c,m=case();c["literature_references"][0]["source_kind"]="GUIDELINE"
        q=validate_literature(c,m)
        self.assertTrue(q["ok"]);self.assertTrue(q["warnings"])
    def test_no_literature_preserves_legacy(self):
        self.assertTrue(validate_literature({"slides":[{"type":"bullets"}]},None)["ok"])

if __name__=="__main__": unittest.main()
