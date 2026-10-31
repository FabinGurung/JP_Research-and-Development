#!/usr/bin/env python3
"""Rebuild the RS-Y maximum storey-shear comparison from the thesis table itself."""
from pathlib import Path
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"24_resultanddiscussion.tex"
text=SOURCE.read_text(encoding="utf-8")
m=re.search(r"(?s)\\begin\{longtable\}\{clrr\}\s*\\caption\{Maximum response-spectrum storey-shear magnitudes.*?\\end\{longtable\}",text)
if not m:
    raise RuntimeError("Storey-shear source table unavailable")
rows={}
for block,support,x,y in re.findall(r"^\s*([1-6])\s*&\s*(Fixed|Hard|Medium|Soft)\s*&\s*([0-9,.]+)\s*&\s*([0-9,.]+)\s*\\\\",m.group(),re.M):
    rows[(int(block),support)]=float(y.replace(",",""))
if len(rows)!=24:
    raise RuntimeError(f"Expected 24 source cases, obtained {len(rows)}")
fig,ax=plt.subplots(figsize=(9,5.3))
for support,style in [("Fixed","o-"),("Hard","s-"),("Medium","^-"),("Soft","D-")]:
    ax.plot(range(1,7),[rows[(b,support)] for b in range(1,7)],style,linewidth=1.8,markersize=5,label=support)
ax.set_xlabel("Hospital structural block")
ax.set_ylabel("Maximum RS-Y storey shear (kN)")
ax.set_xticks(range(1,7))
ax.set_xlim(.8,6.2)
ax.grid(alpha=.25)
ax.legend(title="Foundation support",ncol=2)
fig.tight_layout()
out=ROOT/"figures/ch4/seq055/story_shear_y.png"
out.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(out,dpi=220)
print(out)
