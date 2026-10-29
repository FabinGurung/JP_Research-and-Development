from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

outdir = Path(__file__).parent / 'figures' / 'ch3'
outdir.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(8.1, 9.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 13)
ax.axis('off')

# Academic monochrome palette
box_face = '#f7f7f7'
branch_face = '#eeeeee'
edge = '#222222'
text = '#111111'


def box(x, y, w, h, s, fs=9.5, face=box_face, lw=1.15):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle='round,pad=0.025,rounding_size=0.08',
                       linewidth=lw, edgecolor=edge, facecolor=face)
    ax.add_patch(p)
    ax.text(x+w/2, y+h/2, s, ha='center', va='center', fontsize=fs,
            color=text, wrap=True, linespacing=1.15)
    return p


def arrow(x1, y1, x2, y2, lw=1.2):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2), arrowstyle='-|>',
                                 mutation_scale=12, linewidth=lw,
                                 color=edge, shrinkA=1.5, shrinkB=1.5))

# Top sequence
box(1.3, 11.65, 7.4, 0.75, 'Define hospital prototype, structural system, loading,\nand NBC 105:2025 seismic parameters', fs=9.4)
box(1.3, 10.35, 7.4, 0.75, 'Establish four support conditions:\nFixed base + hard-, medium-, and soft-soil SSI models', fs=9.4)
box(1.3, 9.05, 7.4, 0.75, 'Derive and assign foundation translational, rocking,\nand torsional spring stiffnesses using Gazetas formulation', fs=9.2)
arrow(5,11.65,5,11.10)
arrow(5,10.35,5,9.80)

# Branching analyses
box(0.35, 7.15, 2.8, 1.1, 'ETABS linear analyses\nModal + response spectrum\n+ settlement/member response', fs=8.8, face=branch_face)
box(3.60, 7.15, 2.8, 1.1, 'SAP2000 nonlinear static\npushover analyses\nin X and Y directions', fs=8.8, face=branch_face)
box(6.85, 7.15, 2.8, 1.1, 'Ground-motion verification\nand nonlinear time-history /\nfragility processing', fs=8.7, face=branch_face)
# fork from common model
arrow(5,9.05,1.75,8.25)
arrow(5,9.05,5.00,8.25)
arrow(5,9.05,8.25,8.25)

# Outputs
box(0.35, 5.25, 2.8, 1.15, 'Extract EDPs:\nperiod, displacement, drift,\nshear, settlement, forces', fs=8.65)
box(3.60, 5.25, 2.8, 1.15, 'Evaluate capacity curves\nand reported FEMA 356\nperformance coordinates', fs=8.65)
box(6.85, 5.25, 2.8, 1.15, 'Apply adopted damage-state\nthresholds and estimate\npreliminary fragility', fs=8.65)
arrow(1.75,7.15,1.75,6.40)
arrow(5.00,7.15,5.00,6.40)
arrow(8.25,7.15,8.25,6.40)

# Merge and interpretation
box(1.3, 3.45, 7.4, 0.9, 'Compare fixed and flexible support conditions across verified\nlinear, foundation, nonlinear-capacity, and fragility response measures', fs=9.15)
box(1.3, 1.95, 7.4, 0.82, 'Synthesize soil-structure interaction effects and identify\nresponse trends, limitations, and engineering implications', fs=9.15)
box(1.3, 0.55, 7.4, 0.75, 'Conclusions and recommendations for the selected hospital prototype', fs=9.3)
arrow(1.75,5.25,3.5,4.35)
arrow(5.00,5.25,5.00,4.35)
arrow(8.25,5.25,6.5,4.35)
arrow(5,3.45,5,2.77)
arrow(5,1.95,5,1.30)

fig.tight_layout(pad=0.25)
fig.savefig(outdir/'research_workflow_seq44.pdf', bbox_inches='tight')
fig.savefig(outdir/'research_workflow_seq44.png', dpi=300, bbox_inches='tight')
plt.close(fig)
