# Construction Works Agreement — Three-Document Delivery Standard

**Shared enterprise document-engineering guidance.** Applies to future projects using the approved v3 `client-contract` template. This is a *semantic companion*, not a replacement for the immutable, approved `templates/enterprise/v3/client-contract.tex` layout.

## Deliverables — A, B and C

| No. | Document | Contents and responsibility | QA |
|---|---|---|---|
| **A** | Construction Works Agreement | Legal parties; defined work scope and exclusions; milestone/NPR schedule; certification and payment terms; warranties/defects; variation orders; signature area; **explicit references** to B and C. | Independently compiled PDF and editable project-specific LaTeX source; amounts total correctly; no false signature/approval claims. |
| **B** | Drawings / original technical source | Referenced **architectural and structural original PDFs**, preserved as-received; can be multiple discipline files with separate identity. Register file name, owner/source provider, version/date, page/sheet references, approval state. | No source modification; page citations valid; drawn work is not assumed commercially included solely because it appears. |
| **C** | Materials and Workmanship Schedule | Explicit products, accepted alternatives, material grades, specifications, workmanship, testing, brands/manufacturers and who supplies/installs each item. | Distinguish candidate from accepted; written bilateral approval; conflict/VO tracking. |

**Default:** deliver three logical documents as three separately navigable resources; **do not concatenate drawings into Agreement A**. If B consists of multiple original PDFs, keep each file separate and use a single indexed drawing register. PDF merging is an optional explicit client request only, and never changes original source bytes.

## Agreement A citation pattern

“Appendix A — Drawing Register: see `[drawing title]`, `[source version]`, architectural sheets/pages `[range]` and structural sheets/pages `[range]` in the separately supplied Document B (`[authorized resource link]`). Materials shall follow the separately agreed Document C, revision `[version]`. **Neither reference itself proves that an as-received technical source is approved or executed**.”

The private registry tracks stable provider file IDs, source hash, page count, drawing/sheet codes, signatures where verified, and independently approved versions. Reference legal, engineering and commercial facts separately. No private client agreements or source drawings belong in public Pages, Actions artifacts or public Git.

## Minimum material record for C

Every material entry must have:
- `material/category` and intended location/work item
- `proposed brand/manufacturer` **or “to be jointly selected”**; a local supplier is not automatically an approved brand
- `profile/product and technical specification` (grade, size, thickness, finish and suitable performance tests where applicable)
- `source type`: original client agreement, technical drawing, independently verified specification, or candidate/market research
- `commercial status`: candidate / mutually agreed / signed approved / superseded
- `equivalent substitution rule`, written consent and sample approval
- `procurement/installation responsibility`, inspection and warranty requirements
- `source citation` (document/revision/page) and `changes/VO` as needed.

Do not silently inherit historical clients' brand choices, material exclusions, quantities or contractual rates.

### uPVC windows/doors — example candidate specification for Pokhara projects

**Example only:** uPVC framed windows/doors, rather than aluminium. The user-originated older Overleaf agreements describe an **88 mm uPVC section and 5 mm glass**. This is a historical candidate, **not a manufacturer-verified system or an issued specification for every project**.

For site-specific procurement, require a mutually approved **manufacturer + named series/model** whose shop drawings show the actual frame/sash geometry (including whether “88 mm” refers to a frame dimension or a system class), internal reinforcement, glazing support and compatibility. Specify:
1. UV-stable uPVC colour/finish; sliding, casement, fixed or ventilation configuration per approved opening schedule.
2. Frame and sash profile sections documented by manufacturer and compatible with as-built openings; **88 mm** is an initial reference only, not an unverified universal requirement.
3. **5 mm clear float glass as the historical single-glazing baseline**, subject to glazing-size, safety-glass location, wind/impact or acoustics requirements; specify toughened/laminated/IGU glass wherever the approved design requires it.
4. Suitable corrosion-resistant reinforcement/hardware, multi-point locks or sliding locks as relevant, hinges/rollers, handles, gaskets, weatherstrips, glazing beads and insect mesh where scheduled.
5. Drainage/weep holes, properly sloped sills and weatherproof frame-to-wall sealants for local monsoon rain and external exposure; installation must be plumb, level and securely anchored to the substrate.
6. On-site measurements, submittals/samples, leakage/operation checks, maintenance instructions, warranties and written approval of proposed equivalents before supply.

No specific brand is prescribed by the shared template. For projects in Pokhara, local procurement candidates can be identified through current provider research; a supplier's location does **not** verify an exact profile size, manufacturer warranty or equivalent quality.

## Project creation procedure

1. Resolve active Drive project identity, legal parties, current original documents, existing source/manifests and authoritative site-specific scope.
2. Locate historical original Overleaf .tex and approved v3 reusable template; classify their material language as **historical candidates** until adopted by this project's client and contractor.
3. Create/revise **Agreement A** source and PDF; reference B and C, do not embed their bytes by default.
4. Register **Drawing Set B** with exact IDs, filenames, versions, page/sheet mapping and signature state. Link the existing originals; do not rename or overwrite them.
5. Create/revise **Materials C** including names, grades, alternatives, supply, responsibilities and explicit pending items; do not invent paint brands, steel grade, VO rates or product certificates.
6. Validate sums, references, filenames, rendering, source integrity, future version restoration and approval boundaries.
7. Save editable LaTeX in the **project-owned private Drive** and public-safe reusable code in Git, each under its correct authority; verify provider readback.
8. Expose only authorized links in navigation/Pages. An online link is not a permission grant. **Stop** on unresolved privacy or signatures.
9. For revisions, retain **one live Drive file ID per subject**. Use a versioned PRE archive copy in the dedicated project archive before material changes and POST after readback where the governing Drive library policy requires it; retain append-only version history. Git-managed shared template revisions use commit history and reviewed PRs, not routine Drive snapshots.

## Do not

- Merge A/B/C into one huge PDF without explicit request.
- Treat “drawn” as “commercially included” or “source received” as “approved/signed.”
- Put a prior client's approved materials straight into another client agreement.
- Claim uPVC brand, 88 mm system, glass safety classification or fixed contract price without evidence.
- Modify the immutable approved v3 `client-contract.tex` or its exact blob digest without an explicit new approved template release.
- Expose client information, payments or private source links on public Pages.
- Put machine codes or internal DRAFT/AUDIT labels in a client-facing agreement; preserve those in private version metadata.
