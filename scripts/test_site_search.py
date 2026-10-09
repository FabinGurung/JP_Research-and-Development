#!/usr/bin/env python3
"""Small local tests for public-safe static catalogue."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from site_core import load
from site_search import build_index

class CatalogueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        researchers=load("registry/researchers.json")["researchers"]
        branches=load("registry/branch-inventory.json")
        websites=load("registry/websites.json")["websites"]
        cls.data=build_index(researchers,branches,websites)
    def test_all_researchers_and_handovers(self):
        e=self.data["entries"]
        self.assertEqual(sum(x["category"]=="Researchers" for x in e),11)
        self.assertEqual(sum(x["category"]=="Handovers" for x in e),11)
    def test_branch_history_from_snapshot(self):
        e=self.data["entries"]
        self.assertGreaterEqual(sum(x["category"]=="Git branches" for x in e),100)
        self.assertTrue(self.data["git_branch_observation_date"])
    def test_no_private_ids_or_science_bodies(self):
        for e in self.data["entries"]:
            self.assertEqual(set(e),{"category","title","description","url","keywords","status"})
            self.assertNotIn("drive_id",e)
            self.assertNotIn("full_text",e)
    def test_links_are_explicit(self):
        for e in self.data["entries"]:
            self.assertTrue(e["url"].startswith(("../","https://github.com/")))
    def test_no_scientific_approval_from_discovery(self):
        self.assertIn("never contains private thesis text",self.data["description"].lower())

if __name__=="__main__":
    unittest.main()
