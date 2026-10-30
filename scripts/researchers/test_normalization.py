#!/usr/bin/env python3
"""Small dependency-free folder planner invariants; no Drive writes."""
import importlib.util
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"scripts/researchers"))
from normalize import load,validate,plan,handover
class FolderTests(unittest.TestCase):
    def setUp(self):
        self.reg=load(ROOT/"registry/researcher-folder-roles.json")
        self.people=load(ROOT/"registry/researchers.json")["researchers"]
    def test_live_registry(self):
        self.assertEqual(validate(self.reg,self.people),[])
        self.assertEqual(len(self.reg["records"]),len(self.people))
    def test_root_hold(self):
        thapa=next(x for x in self.reg["records"] if x["researcher_id"]=="RSH-004")
        self.assertIsNone(thapa["existing_project_root_drive_id"])
        self.assertEqual(len(plan(thapa)["reuse"]),0)
        self.assertIn("DO NOT CREATE",handover(thapa))
    def test_project_root_lease(self):
        fake=json.loads(json.dumps(self.reg))
        fake["records"][0]["existing_project_root_drive_id"]="INVENTED"
        self.assertTrue(validate(fake,self.people))
    def test_no_auto_mutation(self):
        for p in self.reg["records"]:
            self.assertEqual(plan(p)["action"],"NO_CENTRAL_MUTATIONS")
            for r in p["roles"]:
                is_authorized_new_role=(p["researcher_id"]=="RSH-012" and r["logical_role"] in ("00_PROJECT_CONTROL","01_SOURCE_ORIGINALS","03_PDF_BUILDS"))
                self.assertEqual(r["physical_mutation_performed"],is_authorized_new_role)
    def test_legacy_alias_kept(self):
        k=next(x for x in self.reg["records"] if x["researcher_id"]=="RSH-009")
        self.assertTrue(any(x["current_name"]=="01_ACTIVE_LATEX_PROJECT" for x in plan(k)["alias_review"]))
if __name__=="__main__":
    unittest.main()
