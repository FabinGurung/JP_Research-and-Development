# CP112 Supervisor-Correction Matrix — 2026-10-04 NPT

Authority: supervisor correction annex ANNEX_S01 + live CP111 + governed Saugat data sources.
Rule: implement supported corrections; leave unsupported fields explicit; do not import cross-researcher values.

| ID | Supervisor correction | Status in CP112 candidate | Authority / note |
|---|---|---|---|
| C1 | Strengthen research gap | IMPLEMENTED | Ch1 contribution/problem framing + Ch2 gap wording |
| C2 | Add study contribution/novelty | IMPLEMENTED | New Contribution of the Study section |
| C3 | Match RQs/objectives and trace to Ch4/Ch5 | IMPLEMENTED | Six matched RQs/objectives + Ch4 traceability + six objective-aligned conclusions |
| C4 | Nepal seismic-zone map | IMPLEMENTED | Exact image extracted from official NBC 105:2025 source |
| C5 | NBC 205 evolution diagram | IMPLEMENTED | TikZ source; cited code authority is NBC 205:1994, followed by Draft Final 2012 and NBC 205:2024. Supervisor note said 1995; source authority retained as 1994. |
| C6 | Strengthen Ch2 research gap | IMPLEMENTED | Bounded to literature reviewed in thesis |
| C7 | Pushover/hinge/performance-point concepts | IMPLEMENTED | TikZ conceptual figure, cited ATC/FEMA/ASCE |
| C8 | Complete model table | IMPLEMENTED | Seven models, storeys, plan area, GII, features |
| C9 | Floor-plan figures for the seven building configurations | IMPLEMENTED | Seven verified one-page Saugat plan PDFs embedded as vector figure inputs; SHA-256 list retained |
| C10 | GII schematic and geometry table | IMPLEMENTED | GII formula + area/Rx/Ry/aspect/theta table |
| C11 | Material/section/load tables | IMPLEMENTED | Recovered seven-model E2K source set |
| C12 | NBC 105:2025 response-spectrum figure | IMPLEMENTED | Exact official Figure 4-2 source extract |
| C13 | Modal results T1/T2/T3/X/Y participation | IMPLEMENTED | Seven latest Saugat model-specific modal-participation workbooks provide T1/T2/T3, UX/UY and cumulative SumUX/SumUY values. The printed comparison uses the matched Soil C, Z=0.40 blocks. |
| C14 | Explain pushover procedure | PARTIAL, FAIL-CLOSED | X/Y curves/PP supported; exact control node, target displacement, steps, gravity sequence not exposed in governed source |
| C15 | Explain hinge modeling | PARTIAL, FAIL-CLOSED | Final-step X/Y image set supported; exact member-level hinge assignment/P-M2-M3 metadata not uniformly exposed |
| C16 | Modal results before shear/drift | IMPLEMENTED | New Ch4 modal section before seven-model response |
| C17 | Storey shear X/Y summary | PARTIAL, FAIL-CLOSED | EQx table implemented; governed EQy shear source not found, Y left unreported |
| C18 | Complete drift profiles | IMPLEMENTED | Seven models, X/Y, Story1–Story4, Soil C Z=0.40 |
| C19 | Percentage change from Regular | IMPLEMENTED | EQx shear, governing drift, CM-CR, peak pushover, PP displacement |
| C20 | Detailed CM-CR table and explanation | IMPLEMENTED | Governing CM-X/Y, CR-X/Y, deltas, resultant |
| C21 | Pushover summary table | IMPLEMENTED | Peak and PP response for all seven |
| C22 | PP comparison graphs | IMPLEMENTED | Seven-model PP shear and displacement plots |
| C23 | Hinge summary table | PARTIAL, FAIL-CLOSED | Evidence-status table; member-level critical hinge fields not invented from screenshots |
| C24 | GII vs five responses | IMPLEMENTED | All seven models |
| C25 | Highlight same-GII/different response | IMPLEMENTED | L/U and L1/L2/T discussion + plots |
| C26 | Critical discussion after major results | IMPLEMENTED | Added source-supported comparative interpretation |
| C27 | Final summary table | IMPLEMENTED | Seven-model evidence summary |
| C28 | Conclusions according to objectives | IMPLEMENTED | Six objective-aligned conclusions |
| C29 | Visual QA | DEFERRED TO USER | Explicit user instruction; no PASS claimed |
| C30 | XeLaTeX/Biber compile + machine QA | IMPLEMENTED | Exact Times New Roman production build; 112 A4 pages; 0 TeX errors; 0 undefined citations; 0 undefined references; 0 overfull h/v boxes; 0 oversized-float warnings; PDF not post-edited |

Scientific/source debts retained: Regular Type-C Z=0.30 EQx force-scale provenance; EQy shear source; member-level hinge and detailed pushover-setup fields that remain unsupported by retained source records.
