# Academic thesis presentation control — A9 / PU MSc

**Review candidate, not current production authority.** This is the single R&D academic presentation implementation, beneath the existing [presentation control wrapper](../presentation.control.json); it is not an Enterprise template or a second control tower.

## Authority
- Drive READ FIRST v2.2: https://docs.google.com/document/d/1uEw_cnlq75uMER3U6Z-njFKDXf1kFfz8bghM3k4dQ2g/edit
- Drive A9 presentation tower v2.2: https://docs.google.com/document/d/1i2YO58HJ1WVsYnBDP0a0ZJg-29VOPccPnWiWit08ofM/edit
- Drive rules: https://docs.google.com/spreadsheets/d/1q9gz1e8sdJkOo8U-ZpvglDOqHVw1N2_N3TkVqy6JCiY/edit
- Drive canonical generator v2.1 SHA-256: `fce6266ed54e724ce049909051f110bd0d99ea638cda65979cc1528f9da4d6b4`
- Drive v2.2 semantic extension candidate: https://drive.google.com/drive/folders/1OOFFnJVQKYEt9IIqGQV1C4uIOV5HVTBf

## Code
`generator/` preserves the verified Python/ReportLab/python-pptx engine and adds an **unpromoted semantic/provenance gate**. Do not silently port it to PptxGenJS. The code and synthetic test fixture contain no researcher photographs, licensed Times New Roman font files, or scientific findings.

## Validation
```bash
cd controls/presentation/generator
pip install -r requirements.lock.txt
python -m unittest -v test_a9_semantic_checker.py
python smoke_test.py
```
The smoke command is *fixture only*. Researcher builds require `--evidence-map`, a current source manifest and source commit, and admitted slide-level evidence. A missing evidence map fails closed. Production requires separately verified exact Times New Roman, structural QA and a real per-page visual inspection; this candidate does not assert those gates have passed.

## Researcher inheritance
Every researcher can reference the same presentation generator and rules; only project-local structured content, evidence/admission IDs, metadata and private assets differ. Do not insert Safal scientific details or private photographs into shared source. Neither this PR nor the synthetic smoke test approves Safal v1.12 as scientific-final.

## Promotion hold
The existing Drive v2.2 control remains active. Merge only after independent code review, GitHub Actions readback, Drive migration/release decision and website QA. The live site and researcher-specific new presentation are deliberately *not* declared finished on this review branch.
