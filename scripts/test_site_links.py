#!/usr/bin/env python3
"""Deterministic offline tests for generated-site link auditing."""
from __future__ import annotations
import tempfile
import unittest
from pathlib import Path

from validate_site_links import local_target, scan


class PortalLinkTests(unittest.TestCase):
    def test_parent_relative_and_directory_index(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            page = base / "researchers" / "fabin-gurung" / "index.html"
            page.parent.mkdir(parents=True)
            expected = base / "owner-prompts" / "index.html"
            self.assertEqual(
                local_target(base, page, "../../owner-prompts/"), expected.resolve()
            )

    def test_external_and_anchor_skipped(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            for value in ("https://drive.google.com/file/d/123", "#section", "mailto:hello@example.org"):
                self.assertIsNone(local_target(base, base / "index.html", value))

    def test_missing_local_link_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            (base / "index.html").write_text('<a href="missing/">Bad link</a>', encoding="utf-8")
            report = scan(base)
            self.assertEqual(report["state"], "FAIL")
            self.assertEqual(len(report["failed_links"]), 1)

    def test_legacy_unmodified(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            (base / "index.html").write_text("<p>Portal</p>", encoding="utf-8")
            old = base / "methodology-demo" / "index.html"
            old.parent.mkdir()
            old.write_text('<img src="missing.png">', encoding="utf-8")
            report = scan(base)
            self.assertEqual(report["state"], "PASS")
            self.assertEqual(report["pages_scanned"], 1)

    def test_portal_absolute_url(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            target = local_target(
                base, base / "index.html",
                "https://fabingurung.github.io/JP_Research-and-Development/owner-prompts/"
            )
            self.assertEqual(target, (base / "owner-prompts/index.html").resolve())


if __name__ == "__main__":
    unittest.main()
