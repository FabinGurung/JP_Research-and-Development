#!/usr/bin/env python3
"""Rebuild two appendix curves from Nabin Bista's researcher-admitted Tables 4.3 and 4.4."""
from pathlib import Path
import numpy as np
from scipy.interpolate import PchipInterpolator
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

VALUES={
 "B1_disp_seq057_table_derived.png":{
   "RS-X / X":[59.39,62.62,75.37,110.92],
   "RS-Y / Y":[69.63,69.94,70.57,75.59]},
 "B2_drift_seq057_table_derived.png":{
   "RS-X / X":[0.349,0.358,0.383,0.432],
   "RS-Y / Y":[0.279,0.289,0.320,0.390]}
}
def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("out_dir",type=Path)
    args=p.parse_args()
    args.out_dir.mkdir(parents=True,exist_ok=True)
    x=np.arange(4,dtype=float)
    for name,columns in VALUES.items():
        fig,ax=plt.subplots(figsize=(10.5,5))
        fine=np.linspace(0,3,280)
        for label,y in columns.items():
            yy=np.array(y)
            ax.plot(fine,PchipInterpolator(x,yy)(fine),lw=2.4,label=label)
            ax.scatter(x,yy,s=35,zorder=3)
        ax.set_xticks(x,["Fixed","Hard","Medium","Soft"])
        ax.set_xlim(-.08,3.08)
        ax.set_ylim(bottom=0)
        ax.set_xlabel("Foundation support condition")
        ax.set_ylabel("Displacement (mm)" if "disp" in name else "Maximum inter-storey drift (%)")
        ax.set_title("Block 1: Uppermost-storey response-spectrum displacement" if "B1" in name else "Block 2: Maximum response-spectrum inter-storey drift")
        ax.grid(True,axis="y",alpha=.22);ax.legend(loc="upper left")
        fig.tight_layout();fig.savefig(args.out_dir/name,dpi=160);plt.close(fig)
if __name__=="__main__": main()
