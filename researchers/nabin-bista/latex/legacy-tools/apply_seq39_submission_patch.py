from pathlib import Path
root=Path('/mnt/data/nabin_seq39')

def replace(path, old, new):
    p=root/path
    s=p.read_text()
    if old not in s:
        raise SystemExit(f'NOT FOUND in {path}: {old[:120]}')
    p.write_text(s.replace(old,new))

# Abstract
replace(Path('10_abstract.tex'),
"The latest nonlinear source reconciliation shows that the supplied pushover-capacity workbook gives distinct X- and Y-direction capacity histories for all four support conditions, while the separately supplied FEMA 356 demand-labelled displacement--base-force workbook reproduces the capacity-series data and therefore does not establish an independent performance point. The available fragility workbook contains twelve ground-motion result sets.",
"The latest nonlinear source reconciliation shows that the supplied pushover-capacity workbook gives distinct X- and Y-direction capacity histories for all four support conditions. A researcher-supplied performance-point summary is reported for the eight fixed/hard/medium/soft X- and Y-direction cases; however, the separately supplied FEMA 356 demand-labelled displacement--base-force workbook reproduces the capacity-series data and does not independently reconstruct those coordinates. The available fragility workbook contains twelve ground-motion result sets.")

# Methodology performance point text
replace(Path('23_methodology.tex'),
"Performance-point interpretation requires an independent demand representation in addition to the capacity curve. The supplied Chapter~4.9 displacement--base-force workbook labelled as FEMA~356 demand was therefore checked against the Chapter~4.8 capacity workbook. Its corresponding series reproduce the capacity data and do not constitute an independent demand curve. Accordingly, no numerical performance point is established or independently inferred from those duplicated series. FEMA~440 and ATC-40 remain relevant performance-based frameworks in the literature, but a numerical performance point is not reported without source-verified independent demand evidence.",
"Performance-point interpretation requires an independent demand representation in addition to the capacity curve. The supplied Chapter~4.9 displacement--base-force workbook labelled as FEMA~356 demand was checked against the Chapter~4.8 capacity workbook and its corresponding series reproduce the capacity data; consequently, that workbook alone cannot independently reconstruct a demand--capacity intersection. For the present submission revision, a separate researcher-supplied summary of eight performance-point coordinate pairs is reported in Chapter~4 exactly as supplied. Those coordinates are treated as source-provided results pending full provenance closeout rather than as values independently re-derived from the duplicated Chapter~4.9 demand-labelled workbook. FEMA~440 and ATC-40 remain the relevant performance-based context for the subsequent closeout check.")

replace(Path('23_methodology.tex'),
"Ground-motion inputs are screened first for explicit numerical provenance. Eleven supplied accelerograms state time in seconds and acceleration in units of $g$; for these records, the peak ground acceleration and time increment are retained directly from the supplied numerical series. Their source-derived acceleration--time-history plots are assembled in \\hyperref[app:verified_accelerograms]{Appendix~\\ref*{app:verified_accelerograms}} so that the input waveforms can be inspected without interrupting the main methodology. The Gorkha/Barpak record is not included in this verified-unit appendix set or in the verified-unit response-spectrum comparison because its time and acceleration units, recording station, and component have not yet been established from the available source provenance.",
"Ground-motion inputs are screened first for explicit numerical provenance. Eleven previously governed accelerograms state time in seconds and acceleration in units of $g$. In addition, the submission-stage workbook \\texttt{gorkha.xlsx} contains a THM station sheet (\\texttt{THM1505120705}) with time explicitly in seconds and three acceleration channels explicitly in cm/s$^2$ at a 0.01~s interval. The THM workbook is therefore admitted provisionally for the current PGA table and acceleration--time-history figure. The corresponding published THM raw DAT source and the previously governed sensor-correction chain are retained as separate provenance authorities that still require A9 closeout reconciliation \\cite{takai2016gorkha,shigefuji2022gorkha}. The source-derived acceleration--time-history plots are assembled in \\hyperref[app:verified_accelerograms]{Appendix~\\ref*{app:verified_accelerograms}}.")

# Insert old damage state table after fragility paragraph
needle="The reconciled fragility source workbook contains twelve ground-motion result sets for each of the fixed, hard-soil, medium-soil, and soft-soil models over analysed PGA ordinates from 0.1 to 0.5~$g$. The workbook applies drift thresholds of 0.5 percent for Operational (OP), 1.0 percent for Immediate Occupancy (IO), 1.5 percent for Damage Control (DC), 2.0 percent for Life Safety (LS), and 2.5 percent for Collapse Prevention (CP). These numerical thresholds are treated as adopted project-analysis thresholds rather than as verbatim FEMA 356 limits. FEMA 356 is cited for the broader performance-level framework \\cite{fema356}. For each support condition and damage state, the workbook reports twelve threshold-PGA estimates, their mean, standard deviation, and a final lognormal dispersion obtained by combining the calculated dispersion with an additional 0.4 uncertainty term. The workbook does not identify whether the nonlinear response series correspond to X or Y direction; accordingly, the reconciled fragility curves are reported without a directional label. The Barpark/Barpak-labelled record remains provenance-gated, so the twelve-record fragility assessment remains preliminary."
insert=needle+"\n\nFor continuity with the earlier methodology version, the inter-storey-drift performance-level screening bands used during fragility interpretation are retained in Table~\\ref{tab:legacy_isdr_performance_bands}. The FEMA performance-level names are retained as the project interpretation framework, while the numerical ISDR bands are treated as project screening limits rather than quoted verbatim as FEMA~356 component acceptance criteria \\cite{fema356}. These broader bands are distinct from the five OP/IO/DC/LS/CP thresholds used by the current twelve-record fragility workbook.\n\n\\begin{table}[htbp]\n\\caption{Inter-storey-drift performance-level screening bands retained from the earlier fragility methodology}\n\\label{tab:legacy_isdr_performance_bands}\n\\centering\n\\begin{tabular}{lc}\n\\hline\\hline\nPerformance level & Maximum ISDR \\\\ \\hline\nImmediate Occupancy (IO) & $\\leq 1.0\\%$ \\\\nLife Safety (LS) & $>1.0\\%$ to $\\leq 2.0\\%$ \\\\nCollapse Prevention (CP) & $>2.0\\%$ to $\\leq 4.0\\%$ \\\\nCollapse / Failure & $>4.0\\%$ \\\\ \\hline\\hline\n\\end{tabular}\n\\end{table}"
replace(Path('23_methodology.tex'),needle,insert)

replace(Path('23_methodology.tex'),
"The study is limited to one hospital prototype and the four support conditions considered. The foundation spring idealization does not replace a site-specific geotechnical investigation. The current fragility source workbook contains twelve ground-motion result sets, but its response direction is not identified in the workbook metadata and the Barpark/Barpak-labelled record remains source-provenance gated; the fragility results are therefore treated as preliminary. Some mean damage-state threshold PGAs exceed the directly analysed 0.1--0.5~$g$ intensity range and are interpreted as extrapolated threshold estimates. The separately supplied FEMA 356 demand-labelled displacement--base-force series reproduce the corresponding capacity-series data and therefore do not provide an independent demand curve or independently verified performance point. The reconciled pushover figures use only the supplied capacity rows and do not add graphical extrapolation.",
"The study is limited to one hospital prototype and the four support conditions considered. The foundation spring idealization does not replace a site-specific geotechnical investigation. The current fragility source workbook contains twelve ground-motion result sets, but its response direction is not identified in the workbook metadata and the Barpark/Barpak-labelled fragility series remains source-provenance gated; the fragility results are therefore treated as preliminary. Some mean damage-state threshold PGAs exceed the directly analysed 0.1--0.5~$g$ intensity range and are interpreted as extrapolated threshold estimates. The researcher-supplied performance-point coordinates reported in Chapter~4 have not yet been independently reconstructed from the duplicated Chapter~4.9 demand-labelled workbook and remain subject to provenance closeout. The THM Gorkha workbook is used provisionally for the current PGA/time-history presentation while its relationship to the published raw DAT and corrected canonical THM chain is retained as an explicit closeout item. The reconciled pushover figures use only the supplied capacity rows and do not add graphical extrapolation.")

# Results 4.9 rewrite
old="""\\section{Demand--Capacity and Performance-Point Status}
The latest source reconciliation does not establish an independent numerical performance point. The separately supplied Chapter~4.9 workbook labelled as FEMA~356 demand reproduces the Chapter~4.8 displacement--base-force capacity series for the corresponding support conditions, apart from a previously documented leading-zero formatting difference in the soft-Y series. It therefore cannot serve as an independent demand curve against which the capacity curve is intersected.

Accordingly, no capacity--demand intersection or numerical performance-point marker is added to the reconciled figures. Earlier spectral-coordinate demand--capacity graphics are not used as replacements for this missing evidence unless their generating model/version and an independent demand definition are reconciled to the latest capacity source. The present nonlinear-static interpretation is therefore limited to the source-verified capacity histories in Figure~\\ref{fig:pushover_4x1_latest}.
"""
new="""\\section{Demand--Capacity and Performance-Point Status}
A researcher-supplied performance-point summary was provided for the current submission revision and is reported in Table~\\ref{tab:performance_points_researcher}. The values are reproduced exactly as supplied; no numerical correction or rescaling has been applied. The separately supplied Chapter~4.9 workbook labelled as FEMA~356 demand still reproduces the Chapter~4.8 displacement--base-force capacity series and therefore does not independently reconstruct these points. The table is consequently treated as a source-provided result pending full provenance closeout, rather than as a performance point independently recalculated from the duplicated demand-labelled workbook.

\\begin{table}[htbp]
\\caption{Researcher-supplied performance-point coordinates for the four support conditions}
\\label{tab:performance_points_researcher}
\\centering
\\begin{tabular}{lcrr}
\\hline\\hline
Support type & Direction & Base shear (kN) & Displacement (m) \\\\ \\hline
Fixed & X & 16,337.028 & 0.120 \\\\nHard & X & 14,116.155 & 0.120 \\\\nMedium & X & 13,566.670 & 0.121 \\\\nSoft & X & 11,566.670 & 0.121 \\\\nFixed & Y & 17,911.160 & 0.135 \\\\nHard & Y & 15,987.832 & 0.155 \\\\nMedium & Y & 1,479.845 & 0.156 \\\\nSoft & Y & 1,294.845 & 0.156 \\\\ \\hline\\hline
\\end{tabular}
\\end{table}

Because the derivation chain for these coordinates is not yet reconciled to an independent demand representation, the points are not superimposed on Figure~\\ref{fig:pushover_4x1_latest} in this emergency submission patch. The numerical table is retained exactly as supplied so that the thesis records the researcher result without obscuring the outstanding provenance check.
"""
replace(Path('24_resultanddiscussion.tex'),old,new)

# Replace entire ground motion section intro + table/fig segment until PSA paragraph
p=root/'24_resultanddiscussion.tex'; s=p.read_text()
start=s.index('\\section{Ground-Motion Record Verification}')
end=s.index('Five-percent-damped pseudo-spectral acceleration spectra were derived',start)
newgm=r'''\section{Ground-Motion Record Verification}
Twelve supplied ground-motion records now have an explicit numerical time/acceleration source available for the current submission-stage presentation. Eleven previously governed accelerograms provide time in seconds and acceleration in units of $g$. The newly supplied \texttt{gorkha.xlsx} workbook includes the THM station sheet \texttt{THM1505120705}, with time in seconds and three acceleration channels in cm/s$^2$ sampled at $\Delta t=0.01$~s. The maximum absolute PGA across the three explicitly supplied THM channels is 0.1185~$g$ and is used as the Gorkha entry in Table~\ref{tab:gm_verified_records}. No orientation label is inferred from the workbook columns. The workbook is used provisionally for this submission-stage table and time-history figure, while the separate published THM raw DAT source and previously governed sensor-correction chain remain preserved for A9 closeout reconciliation \cite{takai2016gorkha,shigefuji2022gorkha}.

\begin{table}[htbp]
\caption{Supplied ground-motion records with explicit acceleration and time units used in the current submission-stage comparison}
\label{tab:gm_verified_records}
\centering
\small
\begin{tabular}{lrrp{5.0cm}}
\hline\hline
Record label & PGA ($g$) & $\Delta t$ (s) & Verification note \\ \hline
Chi-Chi & 0.3610 & 0.010 & Acceleration and time units verified in supplied record \\
Friuli & 0.3513 & 0.010 & Acceleration and time units verified in supplied record \\
Hollister & 0.1948 & 0.010 & Acceleration and time units verified in supplied record \\
Imperial Valley & 0.3152 & 0.010 & Acceleration and time units verified in supplied record \\
Kobe & 0.3447 & 0.010 & Acceleration and time units verified in supplied record \\
Kocaeli & 0.3490 & 0.010 & Acceleration and time units verified in supplied record \\
Landers & 0.7803 & 0.010 & Acceleration and time units verified in supplied record \\
Loma Prieta & 0.3674 & 0.010 & Acceleration and time units verified in supplied record \\
Northridge & 0.5683 & 0.010 & Acceleration and time units verified in supplied record \\
San Fernando & 0.02576 & 0.005 & Acceleration and time units verified in supplied record \\
Trinidad & 0.1936 & 0.010 & Acceleration and time units verified in supplied record \\
Gorkha (THM) & 0.1185 & 0.010 & \texttt{gorkha.xlsx}, THM sheet; maximum absolute PGA across three supplied channels; channel orientation not inferred \\ \hline\hline
\end{tabular}
\end{table}

The San Fernando PGA of 0.02576~$g$ is retained from the supplied accelerogram and is not replaced by a value from a different published San Fernando recording. Figure~\ref{fig:gm_verified_pga} compares the source-derived PGA values of all twelve records admitted to the current table.

\begin{figure}[htbp]
\centering
\includegraphics[width=0.94\textwidth]{figures/ch4/seq39/ground_motion_12eq_pga_with_gorkha_thm.png}
\caption{Source-derived PGA values of the twelve supplied records used in the current comparison, including the provisionally admitted Gorkha THM workbook record}
\label{fig:gm_verified_pga}
\end{figure}

Figure~\ref{fig:gorkha_thm_timehistory} shows the three acceleration channels supplied in the THM worksheet. The plot preserves the workbook units of cm/s$^2$ and does not infer component orientation.

\begin{figure}[p]
\centering
\includegraphics[width=0.96\textwidth]{figures/ch4/seq39/gorkha_thm_3channel_acceleration_time_history.png}
\caption{Acceleration time histories from the three explicitly supplied channels in the Gorkha THM worksheet (\texttt{THM1505120705}); component orientation is not inferred from the workbook}
\label{fig:gorkha_thm_timehistory}
\end{figure}

'''
p.write_text(s[:start]+newgm+s[end:])

# Replace PSA paragraph wording only
replace(Path('24_resultanddiscussion.tex'),
"Five-percent-damped pseudo-spectral acceleration spectra were derived for the same eleven verified-unit records using the governed response-spectrum calculation. Figure~\\ref{fig:gm_verified_psa} presents these spectra without a target spectrum, spectral matching, or an inferred Gorkha response spectrum. The corresponding source-derived acceleration--time-history plots are provided in \\hyperref[app:verified_accelerograms]{Appendix~\\ref*{app:verified_accelerograms}}. This distinction is retained because the unresolved Gorkha/Barpak source cannot yet be assigned a defensible verified-unit time-history or spectral series.",
"Five-percent-damped pseudo-spectral acceleration spectra in Figure~\\ref{fig:gm_verified_psa} remain the previously governed eleven-record comparison and are not silently regenerated in this emergency patch. The newly supplied Gorkha THM workbook is added to the PGA/time-history presentation, while integration of the published/corrected THM spectrum is left as an explicit A9 closeout item so the XLSX, raw DAT, and corrected canonical chain are not conflated. The acceleration--time-history plots are provided in \\hyperref[app:verified_accelerograms]{Appendix~\\ref*{app:verified_accelerograms}}.")
replace(Path('24_resultanddiscussion.tex'),
"\\caption{Five-percent-damped pseudo-spectral acceleration spectra of the eleven supplied accelerograms with verified time and acceleration units}",
"\\caption{Previously governed five-percent-damped pseudo-spectral acceleration spectra of the eleven-record comparison set; Gorkha THM spectral integration is retained for A9 closeout reconciliation}")

# Appendix intro + Gorkha figure
replace(Path('28_appendices.tex'),
"The following accelerograms are source-derived plots of the eleven supplied records for which time is explicitly given in seconds and acceleration is explicitly given in units of $g$. The plotting workflow converted the acceleration ordinates to m/s$^2$ using $g=9.81$ m/s$^2$ and annotated the source-derived positive and negative peaks. The Gorkha/Barpak source is not included because its time and acceleration units remain unresolved in the governed source provenance.",
"The following accelerograms document the eleven previously governed records plus the newly supplied Gorkha THM workbook record. The first eleven source-derived plots use the previously governed plotting workflow. For Gorkha, \\texttt{gorkha.xlsx} provides the THM station worksheet \\texttt{THM1505120705} with time in seconds and three acceleration channels in cm/s$^2$ at 0.01~s spacing. The Gorkha plot retains those workbook units and displays all three supplied channels without inferring their orientation. The published THM raw DAT and corrected canonical chain remain preserved separately for A9 closeout reconciliation.")
app=root/'28_appendices.tex'; s=app.read_text(); marker='\\end{myappendix}'
pos=s.rfind(marker)
gorkha_app=r'''
\begin{figure}[p]
\centering
\includegraphics[width=0.96\textwidth]{figures/appendix/ground_motion_time_histories/12_gorkha_thm__acceleration_time_history.png}
\caption{Gorkha earthquake THM worksheet acceleration time histories: three supplied channels from \texttt{gorkha.xlsx}; component orientation not inferred}
\label{fig:app_accel_12}
\end{figure}

'''
app.write_text(s[:pos]+gorkha_app+s[pos:])

# Conclusion consistency
replace(Path('25_conclusionandrecommendation.tex'),
"The source-reconciled SAP2000 pushover dataset provides the nonlinear static capacity component of the study. The latest Chapter~4.8 workbook is reported without graphical continuation beyond supplied rows. The separately supplied FEMA~356 demand-labelled displacement--base-force workbook reproduces the capacity series and therefore does not provide an independent basis for a numerical performance point.",
"The source-reconciled SAP2000 pushover dataset provides the nonlinear static capacity component of the study. The latest Chapter~4.8 workbook is reported without graphical continuation beyond supplied rows. A researcher-supplied summary provides eight fixed/hard/medium/soft X- and Y-direction performance-point coordinates and is tabulated exactly as supplied in Chapter~4. The separately supplied FEMA~356 demand-labelled displacement--base-force workbook reproduces the capacity series and therefore does not independently reconstruct those performance-point coordinates; their derivation remains a provenance closeout item.")
replace(Path('25_conclusionandrecommendation.tex'),
"For nonlinear static assessment, future interpretation would benefit from a directly documented FEMA 440 performance-point result or an explicitly defined calculation procedure. ATC-40 may be retained as a comparison, while the selected performance-interpretation method should remain consistent throughout the thesis.",
"For nonlinear static assessment, the researcher-supplied performance-point coordinates should be tied during closeout to a directly documented FEMA~440/ATC-40 calculation or exported analysis result so that their derivation can be reproduced. The selected performance-interpretation method should then remain consistent throughout the thesis.")
replace(Path('25_conclusionandrecommendation.tex'),
"The conclusions apply to the selected hospital prototype, the adopted foundation-spring idealization, and the analysed support conditions. The spring representation is not a substitute for a site-specific geotechnical investigation. The fragility assessment is derived from the available twelve-ground-motion source workbook, whose response direction is not identified and whose Barpark/Barpak-labelled record remains source-provenance gated; threshold PGAs above the directly analysed 0.1--0.5~$g$ range are extrapolated. The available demand-labelled displacement--base-force source is not independent of the capacity series, so no numerical performance point is established.",
"The conclusions apply to the selected hospital prototype, the adopted foundation-spring idealization, and the analysed support conditions. The spring representation is not a substitute for a site-specific geotechnical investigation. The fragility assessment is derived from the available twelve-ground-motion source workbook, whose response direction is not identified and whose Barpark/Barpak-labelled record remains source-provenance gated; threshold PGAs above the directly analysed 0.1--0.5~$g$ range are extrapolated. The reported performance-point coordinates are researcher-supplied and have not yet been independently reconstructed from the duplicated demand-labelled workbook. The Gorkha THM XLSX record is admitted provisionally for the current PGA/time-history presentation pending reconciliation with the separately preserved raw DAT and corrected canonical THM chain.")
replace(Path('25_conclusionandrecommendation.tex'),
"Future work should verify the directional identity of the twelve-ground-motion nonlinear response dataset, reconcile the Barpark/Barpak waveform provenance, and then regenerate any direction-specific fragility parameters from that verified basis. A separately documented independent demand curve or directly exported performance-point result would be required before adding a numerical performance point. Site-specific soil data, foundation-geometry sensitivity, and alternative foundation models may also be investigated to quantify uncertainty in the SSI spring representation and foundation settlement response.",
"Future work should verify the directional identity of the twelve-ground-motion nonlinear response dataset, reconcile the Barpark/Barpak fragility label, and complete the A9 source reconciliation between the provisionally used Gorkha THM XLSX workbook, the published THM raw DAT file, and the corrected canonical THM processing chain. The researcher-supplied performance-point coordinates should likewise be connected to a documented independent demand curve or directly exported performance-point result. Site-specific soil data, foundation-geometry sensitivity, and alternative foundation models may also be investigated to quantify uncertainty in the SSI spring representation and foundation settlement response.")

# BibTeX append if missing
bib=root/'27_reference.bib'; b=bib.read_text()
if 'takai2016gorkha' not in b:
    b += r'''

% =========================================================
% 9. 2015 Gorkha Kathmandu Valley strong-motion provenance
% =========================================================
@article{takai2016gorkha,
  author  = {Takai, Nobuo and Shigefuji, Michiko and Rajaure, Sudhir and Bijukchhen, Subeg and Ichiyanagi, Masayoshi and Dhital, Megh Raj and Sasatani, Tsutomu},
  title   = {Strong Ground Motion in the Kathmandu Valley during the 2015 Gorkha, Nepal, Earthquake},
  journal = {Earth, Planets and Space},
  volume  = {68},
  number  = {10},
  year    = {2016},
  doi     = {10.1186/s40623-016-0383-7}
}

@article{shigefuji2022gorkha,
  author  = {Shigefuji, Michiko and Takai, Nobuo and Bijukchhen, Subeg and Ichiyanagi, Masayoshi and Rajaure, Sudhir and Dhital, Megh Raj and Paudel, Lalu Prasad and Sasatani, Tsutomu},
  title   = {Strong Ground Motion Data of the 2015 Gorkha Nepal Earthquake Sequence in the Kathmandu Valley},
  journal = {Scientific Data},
  volume  = {9},
  number  = {513},
  year    = {2022},
  doi     = {10.1038/s41597-022-01634-6}
}
'''
    bib.write_text(b)

# Submission patch trace
(root/'SEQ39_SUBMISSION_PATCH_TRACE.md').write_text('''# SEQ39 submission patch trace\n\n- Restored the earlier ISDR performance-level screening table as a current methodology table, clearly separated from the five thresholds used by the current fragility workbook.\n- Added the researcher-supplied 8-row performance-point summary exactly as supplied. Medium-Y and Soft-Y base-shear values were not corrected or rescaled. Provenance reconstruction remains pending closeout.\n- Preserved and used `gorkha.xlsx` for the current Gorkha/THM PGA and time-history presentation. THM sheet: `THM1505120705`; explicit `Time [sec]` and `Acceleration [cm/sec2]`; dt=0.01 s; maximum absolute PGA across the three supplied channels = 0.118527 g. Component orientation was not inferred.\n- Separately preserved published raw DAT authority remains `THM001504250611__PUBLISHED_RAW_ORIGINAL.dat` (Drive ID 1OmBB5nK8NvGnu2CiJbjeI1T9cPRfuv5c).\n- Published/corrected THM source chain is not conflated with the XLSX in this emergency patch. Full A9 closeout/reconciliation remains explicitly pending.\n''')

# version history quick index
(root/'NABIN_LATEX_VERSION_HISTORY__SEQ39.md').write_text('''# Nabin Bista LaTeX/PDF version history - quick index\n\nDurable version history is maintained in the LaTeX lane Local Library and parent Nabin Local Library; immutable/reproducible bundles are kept under `10_LATEX_PARTWISE_ACTIVE/02_PART_BUILDS`, prior CURRENT PDFs under `99_SUPERSEDED_ARCHIVE`, and the legacy milestone under `98_ARCHIVE__LATEX_LEGACY__FROZEN`.\n\nKey milestones recovered in the current runtime:\n- v13 researcher-feedback baseline ZIP (immutable legacy baseline)\n- Part 01 / SEQ21 compiled integration\n- Part 02 / SEQ22 compiled debt-clear\n- Part 03 / SEQ27 source branch; SEQ28 compiled/promoted\n- Part 04A / SEQ30 nonlinear source reconciliation\n- SEQ31 reproducibility-code infrastructure\n- SEQ36 reproducibility debt clear\n- SEQ37 Part 04A compiled/promoted\n- SEQ38 submission-critical formatting fix compiled/promoted\n- SEQ39 current emergency submission patch: old ISDR table restoration + researcher-supplied performance-point table + provisional Gorkha THM XLSX inclusion\n\nStable current compiled PDF Drive ID: `199DQW3Qan-jOpkO2PL3v-uKI_qJ6lu93`.\nLaTeX sub-local registry Drive ID: `1U87TrBVm0pNVgmmsxIwOpkIZryjheupUoBRpC5Os-bQ`.\nParent Nabin Local Library Drive ID: `1G7LBXvuO2Q-WpOdidku9rkCa0Sj2yhv7lOIy_kNArjw`.\n''')
print('SEQ39 patch applied')
