from __future__ import annotations
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT / p).read_text(encoding="utf-8"))

class GitDriveAuthorityTests(unittest.TestCase):
    def test_single_scoped_git_authority(self):
        p=load("controls/git-drive-authority.json")
        self.assertEqual(p["authority"]["github"], "GIT_COMMITS_BRANCHES_PULL_REQUESTS_TAGS_RELEASES_CI_AND_APPROVED_MILESTONE_HISTORY")
        self.assertEqual(p["status"], "ACTIVE_SCOPE_LIMITED_CUTOVER")
        self.assertIn("Google Drive", (ROOT/"docs/GIT_DRIVE_AUTHORITY_READ_FIRST.md").read_text())
    def test_legacy_numbers_preserved_no_auto_ack(self):
        p=load("controls/git-drive-authority.json")
        b=load("registry/legacy-a9-ledger-index.json")
        self.assertEqual((b["local"]["last_local_seq"],b["main"]["last_ack_cursor"]),(20,5))
        self.assertEqual((b["unacknowledged"]["from_seq"],b["unacknowledged"]["to_seq"]),(6,20))
        self.assertTrue(p["safal_dawadi"]["future_local_seq_creation"].startswith("DISABLED"))
        self.assertFalse(b["scientific_approval_changed"])
    def test_not_two_version_systems(self):
        r=load("controls/repository.control.json")
        x=load("controls/presentation.control.json")
        t=load("controls/presentation/tower.json")
        self.assertEqual(r["version_authority_policy"],"controls/git-drive-authority.json")
        self.assertEqual(x["version_control_policy"],"controls/git-drive-authority.json")
        self.assertEqual(t["version_control_authority"],"GITHUB")
        self.assertNotIn("PptxGenJS",r["presentation_default"])
        self.assertIn("python-pptx",r["presentation_default"])
        self.assertTrue((ROOT/"researchers/safal-dawadi/presentation/GOVERNANCE_READ_FIRST.md").is_file())
    def test_both_location_traces(self):
        m=load("registry/migrations/git-drive-authority-20261011.json")
        self.assertTrue(m["decision_drive_doc_id"])
        self.assertEqual(len(m["pre_copies"]),6)
        self.assertFalse(m["no_deletions"] is False)
if __name__=="__main__":unittest.main()
