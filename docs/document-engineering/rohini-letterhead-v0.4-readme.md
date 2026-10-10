# Branded enterprise contract source – work branch v0.4

This is a reusable LaTeX layout, not a published Radha Roka agreement.
The business-facing PDF must be compiled in an authorized private work folder
with project-specific `contract-content.tex`, `company-brand.tex` and
`assets/rohini-logo.jpg`. None of those private sources or branding binaries
are committed to the public repository.

## Rohini company branding authority
- Company originals root: https://drive.google.com/drive/folders/1sA55AmDWiP2ZTp_Iw6OoCGi4ud4acEI9
- Letterhead Google Doc: https://docs.google.com/document/d/1Yp3-Sn0AKYHZ8TQAVxX0D1Q6wQT8CK0UJ4iqn2bAcEk/edit
- Embedded logo Google Doc: https://docs.google.com/document/d/1qZGmgf9GwNeDXBjPOgrgfOoLFy5VKRJrXcKEvJ8LAb4/edit
- Approved rendition is resolved from that source into a private Drive branding asset folder.
- Both originals are imported Google Docs; byte-identical original DOCX preservation has not been demonstrated.

## Versioning
- Immutable starting-point branch: `snapshot/enterprise-radha-roka-v0.3-20261011`
- Work branch: `work/enterprise-radha-roka-v0.4-branded-20261011`
- The shared `main` branch has not been renamed or force-updated.
- Radha Roka v0.3 documents are preserved in their existing Rohini Drive project directory.

## Layout and release rules
A4 document: left/right 24 mm, top/bottom 25 mm, header/footer within
the page boundary. Private branding fields are injected by the profile file.
The original 1,135 square-foot house-area statement is removed from v0.4.
All project-specific scope and the 57,50,000 NPR lump sum remain in private
contract-content.tex and must not enter public Git history.
Contract is still a DRAFT requiring confirmed address, dates, taxes,
payment terms, specifications and approval before signature.

To compile locally: `latexmk -pdf -no-shell-escape client-contract-simple-lumpsum-letterhead.tex`
