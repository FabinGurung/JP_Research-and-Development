#!/usr/bin/env python3
"""Regenerate SEQ055 figure set from the SEQ054 recorded numeric evidence.
Usage: python generate_seq055_charts.py /path/to/unzipped/NABIN_BISTA_LATEX_SEQ055
Requires matplotlib and numpy; leaves input records untouched.
"""
from pathlib import Path
import json,sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
P=Path(sys.argv[1]).resolve()
A=json.loads((P/"seq054_evidence/response_metrics_240_records.json").read_text())["metrics"]
E=json.loads((P/"seq054_evidence/member_envelopes_144_records.json").read_text())["results"]
O=P/"figures/ch4/seq055";O.mkdir(parents=True,exist_ok=True)
supports=["fixed","hard","medium","soft"]
def mat(kind,factor=1):
 m=np.full((6,4),np.nan)
 for x in A:
  if x["kind"]==kind and x["verified"]=="REPORTED" and x["value"] is not None:
   m[x["block"]-1,supports.index(x["support"])]=x["value"]*factor
 return m
def save(a,name,label,bar=False):
 fig,ax=plt.subplots(figsize=(8.2,4.25))
 if bar:
  for j,s in enumerate(supports):
   ax.bar(np.arange(6)+(j-1.5)*.18,a[:,j],.18,label=s.title())
  ax.set_xticks(np.arange(6),["Block "+str(i) for i in range(1,7)])
  ax.legend(ncol=4,frameon=False,fontsize=8)
 else:
  for b in range(6):ax.plot(range(4),a[b],marker=["o","s","^","D","v","P"][b],label="Block "+str(b+1))
  ax.set_xticks(range(4),[s.title() for s in supports]);ax.legend(ncol=3,frameon=False)
 ax.set_ylabel(label);ax.grid(alpha=.25);fig.tight_layout()
 fig.savefig(O/(name+".pdf"),bbox_inches="tight")
 fig.savefig(O/(name+".png"),dpi=180,bbox_inches="tight")
 plt.close(fig)
period=np.array([[.856,.861,.878,.929],[.583,.594,.628,.698],[.958,.961,.972,1.008],[.723,.727,.743,.788],[.667,.670,.684,.727],[.752,.756,.769,.811]])
modes=np.array([[9,9,9,8],[8,8,7,6],[5,5,5,5],[8,10,8,5],[6,6,6,6],[7,8,7,5]])
save(period,"fundamental_period","Fundamental period (s)")
save(modes,"modal_mass_90","Mode reaching 90% mass, both axes",True)
for field,name,label,mult in [
("displacement_roof_RS-X X-Dir","roof_disp_x","RS-X roof displacement (mm)",1),
("displacement_roof_RS-Y Y-Dir","roof_disp_y","RS-Y roof displacement (mm)",1),
("drift_max_RS-X X-Dir","max_drift_x","RS-X maximum drift (%)",100),
("drift_max_RS-Y Y-Dir","max_drift_y","RS-Y maximum drift (%)",100),
("base_shear_rs_x","base_shear_x","RS-X base shear (kN)",1),
("story_shear_max_RSM_X","story_shear_x","RSM-X maximum storey shear (kN)",1),
("settlement_max_abs_Uz","foundation_settlement","Maximum vertical movement (mm)",1)]:
 save(mat(field,mult),name,label,bar=name in {"base_shear_x","story_shear_x"})
reactions=mat("vertical_reaction_FZ");reactions[2,0]=np.nan;reactions[4,1]=np.nan
save(reactions,"foundation_reaction","Gravity vertical reaction FZ (kN)",True)
for kind,field,name,label in [
("beam","V2","beam_shear_envelope","Beam |V2| (kN)"),
("beam","M3","beam_moment_envelope","Beam |M3| (kN m)"),
("column","P","column_axial_envelope","Column |P| (kN)"),
("column","M3","column_moment_envelope","Column |M3| (kN m)")]:
 v=np.full((6,4),np.nan)
 for r in E:
  if r["kind"]==kind and r["field"]==field:v[r["block"]-1,supports.index(r["support"])]=r["abs"]
 save(v,name,label)
