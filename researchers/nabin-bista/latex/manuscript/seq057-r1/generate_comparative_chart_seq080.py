#!/usr/bin/env python3
"""Recreate Figure 4.36 from explicitly cited published and thesis results.

Poudel & Chaulagain (2024), DOI 10.1016/j.rineng.2024.102161:
reported nonlinear-soft percentages relative to fixed-base response for
Gorkha, Northridge, and San Fernando seismic records (six-model averages).
Nabin Bista, LATEX_SEQ079, Table 4.14: six block-specific percentage changes.
The other cited study (Dhakal & Chaulagain 2023) gives no numerical effect
sizes in the accessible abstract; it is deliberately NOT plotted.
The two plotted studies use different seismic analysis methods and buildings.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
values = [85.35, 88.68, 65.38, 86.8, 30.8, 7.5, 17.0, 22.4, 16.8]
labels = [
    "Poudel\nGorkha", "Poudel\nNorthridge", "Poudel\nSan Fernando",
    "Hospital\nBlock 1", "Hospital\nBlock 2", "Hospital\nBlock 3",
    "Hospital\nBlock 4", "Hospital\nBlock 5", "Hospital\nBlock 6",
]
fig, ax = plt.subplots(figsize=(9.0, 3.45))
ax.bar(range(len(values)), values, width=0.66)
ax.set_ylabel("Increase over fixed support (%)")
ax.set_xticks(range(len(values)))
ax.set_xticklabels(labels, fontsize=8)
ax.set_ylim(0, 105)
ax.axvline(2.5, ls=":", lw=0.8, color="0.5")
for i, value in enumerate(values):
    ax.text(i, value + 1.5, f"{value:g}", ha="center", va="bottom", fontsize=8)
ax.grid(axis="y", alpha=0.16)
fig.tight_layout(pad=0.7)
out = Path(__file__).resolve().parent / "figures/seq080/comparative_roof_displacement.pdf"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, bbox_inches="tight")
plt.close(fig)
print(out)
