#!/usr/bin/env python3
"""Generate nonlinear pushover and fragility figures for the thesis."""
from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import ndtr
ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data"/"part04a_latest_nonlinear"
FIG=ROOT/"figures"/"ch4"/"part04a"; FIG.mkdir(parents=True,exist_ok=True)
push={s:{"X":[],"Y":[]} for s in ["Fixed","Hard","Medium","Soft"]}
with (DATA/"PUSHOVER_CAPACITY__LATEST_SOURCE_DERIVED__SEQ30.csv").open(newline="",encoding="utf-8") as f:
    for r in csv.DictReader(f):
        push[r["soil_condition"]][r["direction"]].append((float(r["roof_displacement_m"]),float(r["base_force_kN"])))
fig,axes=plt.subplots(4,1,figsize=(7.2,10.3),sharex=True)
for ax,soil in zip(axes,["Fixed","Hard","Medium","Soft"]):
    for d,m in [("X","o"),("Y","s")]:
        pts=push[soil][d]; ax.plot([p[0] for p in pts],[p[1] for p in pts],marker=m,markersize=3.2,linewidth=1.2,label=f"Push-{d}")
    ax.set_title(f"{soil} support",fontsize=10); ax.set_ylabel("Base shear (kN)",fontsize=8); ax.grid(True,alpha=.25); ax.legend(fontsize=7,loc="lower right")
axes[-1].set_xlabel("Roof displacement (m)",fontsize=8)
fig.suptitle("Pushover Capacity Curves",fontsize=12,y=.995); fig.tight_layout(rect=(0,0,1,.985))
fig.savefig(FIG/"fig_part04a_pushover_4x1_latest.png",dpi=300,bbox_inches="tight"); fig.savefig(FIG/"fig_part04a_pushover_4x1_latest.pdf",bbox_inches="tight"); plt.close(fig)
frag={s:[] for s in ["Fixed","Hard","Medium","Soft"]}
with (DATA/"FRAGILITY_12EQ__LATEST_SOURCE_DERIVED__SEQ30.csv").open(newline="",encoding="utf-8") as f:
    for r in csv.DictReader(f):
        frag[r["soil_condition"]].append((r["damage_state"],float(r["mean_threshold_PGA_g"]),float(r["final_beta_with_0p4_uncertainty"])))
abbr={"Operational (OP)":"OP","Immediate Occupancy (IO)":"IO","Damage Control (DC)":"DC","Life Safety (LS)":"LS","Collapse Prevention (CP)":"CP"}
pga=np.linspace(.005,1.0,500)
fig,axes=plt.subplots(4,1,figsize=(7.2,10.3),sharex=True,sharey=True)
for ax,soil in zip(axes,["Fixed","Hard","Medium","Soft"]):
    for state,theta,beta in frag[soil]:
        ax.plot(pga,ndtr(np.log(pga/theta)/beta),linewidth=1.2,label=abbr[state])
    ax.axvline(.5,linestyle="--",linewidth=.8); ax.set_title(f"{soil} support",fontsize=10); ax.set_ylabel("Exceedance probability",fontsize=8); ax.grid(True,alpha=.25); ax.legend(fontsize=6,ncol=5,loc="lower right")
axes[-1].set_xlabel("PGA (g)",fontsize=8)
fig.suptitle("Seismic Fragility Curves",fontsize=10.5,y=.995); fig.tight_layout(rect=(0,0,1,.982))
fig.savefig(FIG/"fig_part04a_fragility_4x1_12eq_direction_neutral.png",dpi=300,bbox_inches="tight"); fig.savefig(FIG/"fig_part04a_fragility_4x1_12eq_direction_neutral.pdf",bbox_inches="tight"); plt.close(fig)
