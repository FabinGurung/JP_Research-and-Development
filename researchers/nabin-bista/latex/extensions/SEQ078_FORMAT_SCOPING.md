# Nabin SEQ078 owner-only layout exception

Authority: RD-LTX-CHG-124 / RD-LTX-EXT-NABIN-001; PU-FMT-003, -031, -036, -040 and -121.

Official PU source rule remains top=2.5 cm. User explicitly directs Nabin-only top=1.33 in (33.782 mm), which is NOT certified as official parity. No other researcher or central style receives this automatically.

The actual formatting code is limited to the owner manuscript modules (main.tex, Table 3.2 block in 23_methodology.tex, float modules in 24_resultanddiscussion.tex and 29_additional_researcher_data_seq050.tex). The global pumlsc-shared.sty is not copied or modified. All 88 figure IDs and Table 3.2 scientific cells are retained; no scientific recalculation. SEQ077 remains immutable in A7 000021 PRE and will only be advanced after a separately verified PDF/source promotion.

The user phrase 'no spacing' is implemented as conservative nonzero 4–8 pt caption/float gaps so captions never collide with figures or prose. A global compact-float macro requires its own cross-researcher regression and rule parity assessment before it may enter the shared template.
