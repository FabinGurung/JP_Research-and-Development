"""SEQ040: repeat existing CP112 values with exact 12pt TNR plot labels.
The PDF/ZIP production build uses privately installed Times New Roman fonts;
their binary files must not be distributed through GitHub or source ZIP.
"""
from pathlib import Path
import ast
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[1]
for face in ('times.ttf', 'timesbd.ttf', 'timesi.ttf', 'timesbi.ttf'):
    font = Path('/mnt/data') / face
    if font.exists():
        fm.fontManager.addfont(str(font))
if not any('Times New Roman' in face.name for face in fm.fontManager.ttflist):
    raise RuntimeError('Exact Times New Roman required for SEQ040 production graphs')
plt.rcParams.update({
    'font.family': 'Times New Roman', 'font.size': 12,
    'axes.labelsize': 12, 'xtick.labelsize': 12, 'ytick.labelsize': 12,
    'legend.fontsize': 12, 'pdf.fonttype': 42, 'ps.fonttype': 42
})

source = ast.parse((ROOT / 'scripts/generate_cp112_figures.py').read_text())
values = {}
for stmt in source.body:
    if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
        key = stmt.targets[0].id
        if key in ('drift_profiles', 'models', 'gii', 'max_drift', 'cmcr', 'peak_push', 'pp_disp', 'pp_shear'):
            values[key] = ast.literal_eval(stmt.value)
models = values['models']
assert models == ['Regular', 'L', 'L1', 'L2', 'T', 'U', 'Non-Parallel']
markers = ['o', 's', '^', 'D', 'v', 'P', 'X']
colors = ['#222222', '#23548b', '#9a4a20', '#6f5886', '#2f7b57', '#b13d52', '#8a6b26']
output = ROOT / 'figures/ch4/seq040_generated'
output.mkdir(parents=True, exist_ok=True)

# Drift: same original storey values, visual zero anchor, no intrusive caption note.
fig, ax = plt.subplots(figsize=(6.35, 4.25))
for i, (name, (x, y)) in enumerate(values['drift_profiles'].items()):
    ax.plot([0] + list(x), [0, 3, 6, 9, 12],
            marker=markers[i], lw=1.5, ms=5.4, label=name)
ax.set_xlabel('ULS inter-storey drift ratio, X direction', labelpad=4)
ax.set_ylabel('Elevation (m)')
ax.set_xlim(0, .006)
ax.set_ylim(0, 12.8)
ax.set_yticks([0, 3, 6, 9, 12], ['Base', 'Story 1', 'Story 2', 'Story 3', 'Stair cover'])
ax.grid(True, ls=':', alpha=.32)
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(.5, .99),
           ncol=4, frameon=False, fontsize=11.5, handletextpad=.4, columnspacing=.9)
fig.subplots_adjust(left=.20, right=.90, top=.81, bottom=.18)
fig.savefig(output / 'uls_drift_profile_X_12pt.pdf')
plt.close(fig)

# Figure 4.36 four response panels, with the matching categorical symbols/colors.
for stem, axis_label, data in [
    ('gii_max_drift', 'Maximum ULS drift ratio', values['max_drift']),
    ('gii_cmcr', 'CM–CR separation (m)', values['cmcr']),
    ('gii_peak_pushover', 'Peak pushover shear (kN)', values['peak_push']),
    ('gii_pp_displacement', 'PP roof displacement (mm)', values['pp_disp']),
]:
    fig, ax = plt.subplots(figsize=(3.25, 2.48))
    for i, (name, g, val) in enumerate(zip(models, values['gii'], data)):
        ax.scatter(g, val, s=58, marker=markers[i], facecolor=colors[i],
                   edgecolor='black', linewidths=.7, zorder=3)
    ax.set_xlabel('GII (%)')
    ax.set_ylabel(axis_label, labelpad=2)
    ax.set_xlim(-2.5, 36.6)
    ax.set_xticks([0, 10, 20, 30])
    ax.grid(True, ls=':', alpha=.25)
    lo, hi = min(data), max(data)
    pad = max((hi - lo) * .13, abs(hi) * .005)
    ax.set_ylim(lo - pad, hi + pad)
    fig.subplots_adjust(left=.27, right=.98, top=.95, bottom=.24)
    fig.savefig(output / (stem + '_12pt.pdf'))
    plt.close(fig)
legend_handles = [
    Line2D([0], [0], marker=markers[i], markersize=7, linestyle='',
           markerfacecolor=colors[i], markeredgecolor='black', label=name)
    for i, name in enumerate(models)
]
fig, ax = plt.subplots(figsize=(6.2, .88))
ax.axis('off')
fig.legend(handles=legend_handles, loc='center', ncol=4, frameon=False,
           fontsize=12, handlelength=1.3, columnspacing=1.4)
fig.savefig(output / 'gii_category_legend_12pt.pdf', bbox_inches='tight', pad_inches=.02)
plt.close(fig)

# Figure 4.37, same model/category annotation style as Figure 4.36.
fig, ax = plt.subplots(figsize=(5.35, 4.25))
for i, (name, g, val) in enumerate(zip(models, values['gii'], values['pp_shear'])):
    ax.scatter(g, val, marker=markers[i], s=72, facecolor=colors[i],
               edgecolor='black', linewidths=.75, zorder=3, label=name)
ax.set_xlabel('Geometric Irregularity Index (%)')
ax.set_ylabel('Performance-point base shear (kN)')
ax.set_xlim(-2.5, 36.5)
ax.set_xticks([0, 10, 20, 30])
ax.set_ylim(328, 475)
ax.grid(True, ls=':', alpha=.3)
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(.5, .02),
           ncol=4, fontsize=12, frameon=False, handletextpad=.5, columnspacing=.8)
fig.subplots_adjust(left=.16, right=.97, top=.96, bottom=.40)
fig.savefig(output / 'gii_pp_shear_consistent_marker_12pt.pdf')
plt.close(fig)
print('Generated 7 vector PDFs with exact 12pt TNR and unchanged source values')
