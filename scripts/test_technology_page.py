from pathlib import Path
import json, subprocess, sys, tempfile, unittest
ROOT=Path(__file__).resolve().parents[1]
class TechPageTests(unittest.TestCase):
    def test_registry_paths_exist(self):
        data=json.loads((ROOT/'controls/technology-stack.json').read_text())
        assert len(data['categories']) >= 5
        for item in data['categories']:
            self.assertTrue((ROOT/item['implementation']).is_file(), item)
            self.assertTrue((ROOT/item['validation']).is_file(), item)
    def test_generated_page_has_current_stack(self):
        with tempfile.TemporaryDirectory() as d:
            dest=Path(d)/'site-output'
            subprocess.run([sys.executable,str(ROOT/'scripts/build_site.py'),'--out',str(dest)],check=True,cwd=ROOT,capture_output=True)
            page=(dest/'technology/index.html').read_text()
            how=(dest/'how-to/index.html').read_text()
            assert 'ReportLab' in page and 'python-pptx' in page and 'XeLaTeX' in page
            assert 'technology/index.html' in how and 'TypeScript + PptxGenJS' not in how
if __name__=='__main__':unittest.main()
