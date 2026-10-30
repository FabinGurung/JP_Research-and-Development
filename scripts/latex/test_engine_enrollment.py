#!/usr/bin/env python3
"""Mutation regressions: enrollment must fail rather than accept stale routing."""
import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
import check_engine_enrollment as enrollment
import check_authorial_voice as voice


class EnrollmentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        # Copy only public governance fixtures, never original research binaries.
        for path in ['registry', 'controls/latex']:
            shutil.copytree(enrollment.ROOT / path, self.root / path)
        self.people = json.loads((self.root / 'registry/researchers.json').read_text())['researchers']
        for row in self.people:
            src = enrollment.ROOT / row['governance']['read_first']
            dst = self.root / row['governance']['read_first']
            dst.parent.mkdir(parents=True)
            shutil.copy(src, dst)
        for entry in json.loads((self.root / 'controls/latex/extension-registry.json').read_text())['registered']:
            dst = self.root / entry['path']; dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(enrollment.ROOT / entry['path'], dst)
        dst = self.root / 'researchers/safal-dawadi/latex/control.json'
        shutil.copy(enrollment.ROOT / dst.relative_to(self.root), dst)

    def check(self):
        with contextlib.redirect_stdout(io.StringIO()):
            enrollment.check(self.root)

    def mutate(self, path, fn):
        p = self.root / path; data = json.loads(p.read_text()); fn(data)
        p.write_text(json.dumps(data))

    def test_all_owners_valid(self):
        self.check()

    def test_each_owner_missing_entrypoint_or_evidence_contract_rejected(self):
        for row in self.people:
            with self.subTest(owner=row['slug']):
                p = self.root / row['governance']['read_first']; before = p.read_text()
                p.unlink()
                with self.assertRaises(AssertionError): self.check()
                p.write_text(before.replace(enrollment.EVIDENCE_MARKER, ''))
                with self.assertRaises(AssertionError): self.check()
                p.write_text(before)

    def test_stale_policy_rejected(self):
        self.mutate('registry/latex-inheritance.json', lambda d: d['researchers'][0].update(semantic_policy_version='0.0.0'))
        with self.assertRaises(AssertionError): self.check()

    def test_duplicate_inheritance_rejected(self):
        self.mutate('registry/latex-inheritance.json', lambda d: d['researchers'].append(d['researchers'][0]))
        with self.assertRaises(AssertionError): self.check()

    def test_cross_owner_build_routing_rejected(self):
        self.mutate('registry/latex-build-profiles.json', lambda d: d['profiles'][0].update(source_root='researchers/nabin-bista/latex/manuscript'))
        with self.assertRaises(AssertionError): self.check()

    def test_cross_owner_extension_rejected(self):
        self.mutate('controls/latex/extension-registry.json', lambda d: d['registered'][0].update(owner='safal-thapa'))
        with self.assertRaises(AssertionError): self.check()

    def test_missing_shared_dependency_rejected(self):
        (self.root / 'controls/latex/qa-contract.json').unlink()
        with self.assertRaises(AssertionError): self.check()

    def test_missing_required_rule_rejected(self):
        self.mutate('controls/latex/authorial-voice-policy.json', lambda d: d.update(rules=[r for r in d['rules'] if r['id'] != 'RD-LTX-SEM-002']))
        with self.assertRaises(AssertionError): self.check()

    def test_flat_and_nested_prose_scanned_without_extensions(self):
        base = self.root / 'researchers/nabin-bista/latex/manuscript'
        (base / 'nested').mkdir(parents=True)
        (base / '16_introduction.tex').write_text('Actual research prose.')
        (base / 'nested/chapter.tex').write_text('Material limitations remain.')
        ext = base.parent / 'extensions'; ext.mkdir()
        (ext / 'adapter.tex').write_text('% formatting only')
        files = voice.sources(self.root, 'nabin-bista')
        self.assertEqual(len(files), 2)
        self.assertTrue(all(base in f.parents for f in files))


if __name__ == '__main__':
    unittest.main()
